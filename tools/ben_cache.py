"""A disk cache for BEN's answers.

BEN is a pure function: the ONNX bidder's output depends only on the request
(hands, dealer, both vulnerabilities, auction prefix) and nothing else - no
sampling, no state carried between calls.  So every answer can be memoised
forever, and re-playing a deal whose auction is unchanged costs nothing.

That is what makes screening possible.  `tools/roundkit/screen.py` re-plays a
candidate system over a cached corpus and re-runs only the boards whose
auction actually changes; on those boards most of the auction prefix is still
shared with the baseline, so the model is consulted only for the genuinely new
positions.  Measured on the 20k pool: a 1000-board re-run that changes 15
boards costs about 2% of a cold run.

Storage is sqlite in WAL mode so several match processes can share one cache
concurrently.  It is content-addressed (sha1 of the canonical request), so it
can never go stale: a different request is a different key.  Deleting the file
only costs time.

    BEN_CACHE=/path/to/ben_cache.sqlite   (default reports/ben_cache.sqlite)
    BEN_CACHE=off                          disables it
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "reports" / "ben_cache.sqlite"


def request_key(req: dict) -> str:
    """Content address of a BEN request: exactly the fields the model reads."""
    canon = json.dumps({
        "hands": {k: req["hands"][k] for k in sorted(req["hands"])},
        "dealer": req["dealer"],
        "vuln_ns": int(req.get("vuln_ns", 0)),
        "vuln_ew": int(req.get("vuln_ew", 0)),
        "auction": list(req["auction"]),
    }, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(canon.encode()).hexdigest()


class BenCache:
    """Content-addressed store of BEN responses.  Safe across processes."""

    def __init__(self, path: str | Path | None = None, flush_every: int = 200):
        p = str(path if path is not None else os.environ.get("BEN_CACHE", DEFAULT))
        self.enabled = p.lower() not in ("off", "none", "0", "")
        self.hits = self.misses = 0
        self._mem: dict[str, dict] = {}     # writes are batched; serve them too
        self._pending: list[tuple[str, str]] = []
        self._flush_every = flush_every
        if not self.enabled:
            self.db = None
            return
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(p, timeout=60.0)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.execute("PRAGMA busy_timeout=60000")
        self.db.execute("CREATE TABLE IF NOT EXISTS ben ("
                        "k TEXT PRIMARY KEY, v TEXT NOT NULL)")
        self.db.commit()

    def get(self, key: str):
        if self.db is None:
            return None
        hit = self._mem.get(key)
        if hit is not None:
            self.hits += 1
            return hit
        row = self.db.execute("SELECT v FROM ben WHERE k=?", (key,)).fetchone()
        if row is None:
            self.misses += 1
            return None
        self.hits += 1
        value = json.loads(row[0])
        self._mem[key] = value
        return value

    def put(self, key: str, value: dict) -> None:
        if self.db is None:
            return
        self._mem[key] = value
        self._pending.append((key, json.dumps(value, separators=(",", ":"))))
        if len(self._pending) >= self._flush_every:
            self.flush()

    def flush(self) -> None:
        if self.db is None or not self._pending:
            return
        for attempt in range(6):
            try:
                self.db.executemany(
                    "INSERT OR IGNORE INTO ben (k, v) VALUES (?, ?)", self._pending)
                self.db.commit()
                break
            except sqlite3.OperationalError:      # another writer holds the lock
                if attempt == 5:
                    raise
                import time
                time.sleep(0.5 * (attempt + 1))
        self._pending.clear()

    def close(self) -> None:
        if self.db is None:
            return
        self.flush()
        self.db.close()
        self.db = None

    def stats(self) -> str:
        n = self.hits + self.misses
        if not self.enabled:
            return "ben cache: off"
        return (f"ben cache: {self.hits}/{n} hits "
                f"({100 * self.hits / n:.1f}%)" if n else "ben cache: unused")
