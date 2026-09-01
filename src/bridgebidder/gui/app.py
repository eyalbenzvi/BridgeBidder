"""FastAPI application for the BridgeBidder GUI.

Provides:
  - WebSocket /ws/deals/generate  — stream deal generation
  - REST /api/deals/{id}/explain/{table}/{n}
  - REST /api/rules/* — system inspection and patching
  - REST /api/proposals/* — proposal CRUD
  - WebSocket /ws/proposals/{id}/test — corpus replay
  - Static file serving for the frontend SPA
"""

from __future__ import annotations

import json
import os
import uuid
import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .services import deal_gen, rule_patch, corpus, corpus_deals, rule_extractor

app = FastAPI(title="BridgeBidder GUI")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

STATIC = Path(__file__).parent / "static"
PROPOSALS_DIR = Path(__file__).parents[3] / "data" / "proposals"
PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# WebSocket: deal generation
# ---------------------------------------------------------------------------


def build_version() -> str:
    """Identify the build serving this page.

    A host that did not redeploy, or a browser holding a cached bundle, is
    indistinguishable from a bug that was never fixed — the page looks the
    same and behaves the old way. Naming the commit in the header turns that
    question into a glance.
    """
    for var in ("RENDER_GIT_COMMIT", "SOURCE_COMMIT", "GIT_COMMIT",
                "VERCEL_GIT_COMMIT_SHA", "HEROKU_SLUG_COMMIT"):
        val = os.environ.get(var)
        if val:
            return val[:7]
    try:
        import subprocess
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=Path(__file__).parents[3], capture_output=True, text=True,
            timeout=5, check=True)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


_BUILD = build_version()


@app.get("/api/env")
async def get_env():
    """What this machine can actually do.

    The front end asks once on load so it can label the deal source and hide
    the corpus test rather than offer a button that fails halfway through a
    twelve-thousand-board run.
    """
    return {
        "build": _BUILD,
        "ben": deal_gen.ben_available(),
        "dd": deal_gen.dd_available(),
        "pool": corpus_deals.available(),
        "pool_losses": corpus_deals.count() if corpus_deals.available() else 0,
        "ai_extract": rule_extractor.available(),
        "deal_source": ("live" if deal_gen.ben_available()
                        else "corpus" if corpus_deals.available() else "none"),
        "corpus_test": corpus.readiness(),
    }


@app.websocket("/ws/deals/generate")
async def ws_generate_deals(
    websocket: WebSocket, seed: int | None = None, source: str = "auto",
):
    """Stream losing deals.

    `source=auto` plays fresh deals against BEN when BEN is installed and
    otherwise replays boards BEN already won from the pool -- same protocol,
    same payload shape, so the front end does not branch.
    """
    await websocket.accept()
    use_live = deal_gen.ben_available() if source == "auto" else (source == "live")
    if use_live and not deal_gen.ben_available():
        await websocket.send_json({
            "type": "error",
            "message": f"BEN is not installed here ({deal_gen.BEN_PYTHON} missing).",
        })
        await websocket.close()
        return
    generator = (deal_gen.DealGenerator(seed=seed) if use_live
                 else corpus_deals.CorpusDealSource(seed=seed))
    try:
        await generator.run(websocket)
    except WebSocketDisconnect:
        generator.stop_event.set()


# ---------------------------------------------------------------------------
# REST: deal explanation
# ---------------------------------------------------------------------------


@app.get("/api/deals/{deal_id}/explain/{table}/{call_n}")
async def explain_call(deal_id: str, table: str, call_n: int):
    """Return the explanation for one of our calls in a generated deal.

    table: "a" or "b"
    call_n: the "n" field from our_calls (position in full auction)
    """
    if table not in ("a", "b"):
        raise HTTPException(status_code=400, detail="table must be 'a' or 'b'")
    try:
        return deal_gen.get_explanation(deal_id, table, call_n)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


# ---------------------------------------------------------------------------
# REST: system inspection
# ---------------------------------------------------------------------------


@app.get("/api/rules/system")
async def get_system_overview():
    """Return a simplified JSON of all contexts and rules."""
    from bridgebidder.system.dsl import load_system
    from bridgebidder.domain.cards import SUITS

    system = load_system()
    contexts_out = []
    for ctx in system.contexts:
        rules_out = []
        for rule in ctx.rules:
            box = rule.requires.box()
            suits_box = {}
            for s in SUITS:
                lo, hi = box.suit(s)
                if (lo, hi) != (0.0, 13.0):
                    suits_box[s] = [int(lo), int(hi)]
            hcp = [int(box.hcp[0]), int(box.hcp[1]) if box.hcp[1] < 40 else 99]
            rules_out.append({
                "id": rule.id,
                "call": str(rule.call),
                "priority": rule.priority,
                "shows": rule.shows,
                "requires_box": {"hcp": hcp, "suits": suits_box},
                "context_id": ctx.id,
            })
        contexts_out.append({
            "id": ctx.id,
            "pattern": str(ctx.pattern),
            "rules": rules_out,
        })
    return {"contexts": contexts_out}


@app.get("/api/rules/context/{ctx_id}")
async def get_context(ctx_id: str):
    """Return full context with all rules and their requires dicts."""
    from bridgebidder.system.dsl import load_system

    system = load_system()
    for ctx in system.contexts:
        if ctx.id == ctx_id:
            rules_out = []
            for rule in ctx.rules:
                rules_out.append({
                    "id": rule.id,
                    "call": str(rule.call),
                    "priority": rule.priority,
                    "shows": rule.shows,
                    "requires": rule.requires.to_dict(),
                    "establishes": {
                        "forcing": rule.establishes.forcing,
                        "game_force": rule.establishes.game_force,
                        "agreed_suit": rule.establishes.agreed_suit,
                    },
                    "alertable": getattr(rule, "alertable", False),
                })
            return {"id": ctx.id, "pattern": str(ctx.pattern), "rules": rules_out}
    raise HTTPException(status_code=404, detail=f"Context {ctx_id!r} not found")


# ---------------------------------------------------------------------------
# REST: patch preview
# ---------------------------------------------------------------------------


@app.post("/api/rules/patch/preview")
async def preview_patch(body: dict):
    """Validate a single patch without writing to disk."""
    patch = body.get("patch")
    if patch is None:
        raise HTTPException(status_code=400, detail="Missing 'patch' field")
    return rule_patch.preview_patch(patch)


# ---------------------------------------------------------------------------
# REST: proposals
# ---------------------------------------------------------------------------


def _list_proposal_files():
    return sorted(PROPOSALS_DIR.glob("prop_*.json"), reverse=True)


@app.get("/api/proposals")
async def list_proposals():
    """List all saved proposals (summary only)."""
    proposals = []
    for path in _list_proposal_files():
        try:
            with open(path) as fh:
                data = json.load(fh)
            proposals.append({
                "id": data.get("id"),
                "name": data.get("name"),
                "note": data.get("note"),
                "status": data.get("status", "pending"),
                "created_at": data.get("created_at"),
                "patches_count": len(data.get("patches", [])),
            })
        except Exception:
            continue
    return {"proposals": proposals}


@app.get("/api/proposals/{prop_id}")
async def get_proposal(prop_id: str):
    """Return full proposal JSON."""
    for path in _list_proposal_files():
        try:
            with open(path) as fh:
                data = json.load(fh)
            if data.get("id") == prop_id:
                return data
        except Exception:
            continue
    raise HTTPException(status_code=404, detail=f"Proposal {prop_id!r} not found")


@app.post("/api/proposals")
async def create_proposal(body: dict):
    """Save a new proposal and return it."""
    name = body.get("name", "Untitled")
    note = body.get("note", "")
    patches = body.get("patches", [])
    deal_ref = body.get("deal_ref")

    now = datetime.datetime.utcnow()
    prop_id = str(uuid.uuid4())
    short_id = prop_id.split("-")[0]
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"prop_{timestamp}_{short_id}.json"

    proposal = {
        "id": prop_id,
        "name": name,
        "note": note,
        "patches": patches,
        "deal_ref": deal_ref,
        "status": "pending",
        "created_at": now.isoformat() + "Z",
    }
    path = PROPOSALS_DIR / filename
    with open(path, "w") as fh:
        json.dump(proposal, fh, indent=2)
    return proposal


def _find_proposal_path(prop_id: str) -> Path:
    for path in _list_proposal_files():
        try:
            with open(path) as fh:
                data = json.load(fh)
            if data.get("id") == prop_id:
                return path
        except Exception:
            continue
    raise HTTPException(status_code=404, detail=f"Proposal {prop_id!r} not found")


def _load_proposal(prop_id: str) -> tuple[Path, dict]:
    path = _find_proposal_path(prop_id)
    with open(path) as fh:
        return path, json.load(fh)


@app.post("/api/proposals/{prop_id}/accept")
async def accept_proposal(prop_id: str):
    """Apply patches to YAML on disk and mark proposal as accepted."""
    path, proposal = _load_proposal(prop_id)
    patches = proposal.get("patches", [])
    try:
        yaml_data = rule_patch.load_system_yaml()
        patched = rule_patch.apply_patches_to_yaml(yaml_data, patches)
        rule_patch.write_system_yaml(patched)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Patch failed: {exc}")

    proposal["status"] = "accepted"
    proposal["accepted_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(path, "w") as fh:
        json.dump(proposal, fh, indent=2)
    return proposal


@app.post("/api/proposals/{prop_id}/reject")
async def reject_proposal(prop_id: str, body: dict | None = None):
    """Mark proposal as rejected with an optional note."""
    path, proposal = _load_proposal(prop_id)
    proposal["status"] = "rejected"
    proposal["rejected_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    if body and body.get("note"):
        proposal["reject_note"] = body["note"]
    with open(path, "w") as fh:
        json.dump(proposal, fh, indent=2)
    return proposal


# ---------------------------------------------------------------------------
# WebSocket: corpus replay
# ---------------------------------------------------------------------------


@app.websocket("/ws/proposals/{prop_id}/test")
async def ws_test_proposal(websocket: WebSocket, prop_id: str, boards: int = 2000):
    """Replay `boards` of the pool under this proposal's patches.

    `boards` is rounded down to whole 1000-board files.  It trades resolution
    for time at roughly a minute a thousand boards on one core; the result
    always reports the effect size the chosen pool can actually resolve.
    """
    await websocket.accept()
    try:
        _, proposal = _load_proposal(prop_id)
    except HTTPException as exc:
        await websocket.send_json({"type": "error", "detail": exc.detail})
        await websocket.close()
        return
    patches = proposal.get("patches", [])
    try:
        await corpus.replay_corpus(websocket, patches, boards=boards)
    except WebSocketDisconnect:
        pass


# ---------------------------------------------------------------------------
# REST: rule extraction via AI
# ---------------------------------------------------------------------------


@app.post("/api/rules/extract")
async def extract_rule(body: dict):
    """Convert natural language to a BidRule dict via GitHub Models."""
    description = body.get("description", "")
    call = body.get("call", "")
    context_pattern = body.get("context_pattern", "")
    if not description or not call:
        raise HTTPException(status_code=400, detail="'description' and 'call' are required")
    return await rule_extractor.extract_rule_from_text(description, call, context_pattern)


# ---------------------------------------------------------------------------
# Static files (SPA frontend) — mounted last so API routes take priority
# ---------------------------------------------------------------------------

class RevalidatingStatic(StaticFiles):
    """Static files that must be revalidated before reuse.

    The front end is unbundled ES modules with stable names, so a browser
    holding `deal-view.js` from a previous deploy keeps running last week's
    code against this week's API — a fixed bug that still reproduces, with no
    way to tell from the page. `no-cache` does not mean "do not store": the
    file is still cached, the browser just asks first, and an unchanged file
    comes back as a 304 with no body. The cost is one conditional request per
    asset; the alternative is silently serving stale JavaScript.
    """

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers["Cache-Control"] = "no-cache"
        return resp


if STATIC.exists():
    app.mount("/", RevalidatingStatic(directory=str(STATIC), html=True),
              name="static")
