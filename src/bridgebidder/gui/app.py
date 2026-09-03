"""FastAPI application for the BridgeBidder GUI.

Provides:
  - WebSocket /ws/deals/generate  — stream deal generation
  - REST /api/deals/{id}/explain/{table}/{n}
  - REST /api/rules/* — system inspection (read-only)
  - REST /api/notes/* — free-text notes about the rulebook
  - Static file serving for the frontend SPA
"""

from __future__ import annotations

import asyncio
import json
import os
import uuid
import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .services import deal_gen, corpus_deals, notes

app = FastAPI(title="BridgeBidder GUI")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

STATIC = Path(__file__).parent / "static"


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
        "deal_source": ("live" if deal_gen.ben_available()
                        else "corpus" if corpus_deals.available() else "none"),
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


@app.post("/api/deals/{deal_id}/rehydrate")
async def rehydrate_deal(deal_id: str, body: dict):
    """Rebuild a pool board's decision setups so its bids are clickable again.

    Lets a page survive the server forgetting the board — an eviction, or the
    restart a sleeping free instance performs on every wake.
    """
    source_file = body.get("source_file")
    board = body.get("board")
    if not source_file or board is None:
        raise HTTPException(status_code=400,
                            detail="source_file and board are required")
    ok = await asyncio.get_event_loop().run_in_executor(
        None, corpus_deals.rehydrate, deal_id, source_file, int(board))
    if not ok:
        raise HTTPException(
            status_code=404,
            detail=f"board {board} not found in {source_file}")
    return {"ok": True, "id": deal_id}


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


# ---------------------------------------------------------------------------
# REST: notes
# ---------------------------------------------------------------------------
#
# The GUI no longer edits rules. It records what looked wrong, in the
# reporter's words, against the board it happened on; the fix is made by hand
# in the YAML afterwards. See services/notes.py for why that split.


@app.get("/api/notes")
async def list_notes():
    return {"notes": notes.load_notes()}


@app.post("/api/notes")
async def create_note(body: dict):
    """Record a note. `deal` is the board payload the page is showing."""
    try:
        return notes.add_note(
            text=body.get("text", ""),
            deal=body.get("deal"),
            bid=body.get("bid"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/notes/{note_id}/status")
async def update_note_status(note_id: str, body: dict):
    try:
        return notes.set_status(note_id, body.get("status", "open"))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no note {note_id}")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.delete("/api/notes/{note_id}")
async def remove_note(note_id: str):
    try:
        notes.delete_note(note_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no note {note_id}")
    return {"ok": True}


@app.get("/api/notes/markdown")
async def notes_markdown():
    """The same notes as one readable document (also written to NOTES.md)."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(notes.render_markdown())


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
