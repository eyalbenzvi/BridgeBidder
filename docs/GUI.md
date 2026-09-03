# The GUI

Two screens over the bidding engine:

- **Deal Explorer** — a board where BEN outscored us, both auctions side by
  side. Click any of our calls to see the rule that produced it, what it shows,
  what it denies, and every candidate it beat with the score each got. Describe
  what looks wrong in your own words; the board is attached automatically.
- **Notes** — the free-text notes captured from those boards, waiting to be
  turned into rule changes. Nothing here edits the rulebook.

## Running it from a phone

The server is Python, so something has to host it — but nothing has to be
installed anywhere by hand. Every option below is driven from a browser.

**Render** (a public URL, free tier). At render.com: **New → Blueprint**, pick
this repository, **Apply**. `render.yaml` describes the rest, and Render hands
back an `https://…onrender.com` address. The free instance sleeps after 15
minutes idle and takes about a minute to wake.

**GitHub Codespaces** (no account beyond GitHub). On the repository page:
**Code → Codespaces → Create**. `.devcontainer/devcontainer.json` installs the
dependencies, starts the server and forwards port 8765 publicly, so the
codespace's own URL opens the app.

**Any Docker host** — Hugging Face Spaces, Fly, Railway, Cloud Run. Point it at
the `Dockerfile`; it listens on `$PORT` (7860 by default, which is what Spaces
expects).

## Running it locally

```bash
pip install -e ".[gui,dd]"
bid-gui                      # http://localhost:8765
```

`PORT`, `HOST` and `BB_GUI_RELOAD=1` (auto-reload, for development) are read
from the environment.

## What runs without BEN

BEN is a neural bidder behind its own interpreter at `/tmp/benenv/bin/python`,
outside this repository. Most machines will not have it, and the GUI does not
require it — `GET /api/env` reports what the current machine can do, and the
front end labels itself accordingly.

| | with BEN | without BEN |
|---|---|---|
| Deal Explorer | plays fresh deals until one loses | replays one of 3,842 boards in `data/pool/` that BEN already won |
| Clicking a bid | full explanation | full explanation — the decision context is a pure function of the auction prefix, and the prefix is read from the record |

The pool boards are real losses, already scored by the real solver. What the
pool cannot do is surface a loss on a deal nobody has played, so with BEN
installed the Explorer prefers the live search.

## Which build am I looking at?

The header carries the commit the server is running. A host that has not
redeployed, and a browser holding a cached module, both look exactly like a
bug that was never fixed — same page, same wrong behaviour, nothing to point
at. Compare that tag against `git log -1 --format=%h` before concluding
anything is broken. Static assets are served `Cache-Control: no-cache`, so
they revalidate on every load and a redeploy takes effect immediately.

## The auction-table click test

`tools/uitest/auction_index.mjs` drives a real browser and clicks every
engine bid on several deals, checking that the seat a call is drawn under
agrees with the index the click sends, and that the inspector opens on the
call that was clicked.

```bash
npm install playwright
PYTHONPATH=src:tools python3 -m uvicorn bridgebidder.gui.app:app --port 8811
node tools/uitest/auction_index.mjs
```

It exists because the bug it covers was invisible to every Python test: the
server was right and the payload was right, and the page still explained the
wrong bid, because nothing compared the index written into the DOM against
the cell it was written on.

## Notes, and what happens to them

The GUI does not edit rules. It used to: a form with an HCP range, four suit
lengths, a priority and a forcing status. That form could express only what its
fields happened to cover — no `evals`, no `shapes`, no `when` conditions, no
"this rule should not exist", no "the real problem is two rules competing" —
and it demanded the answer up front, when what you have at the table is a
question.

Describing the problem and encoding the fix are different jobs, and only the
second needs the DSL. So the Explorer captures the first:

- Click one of our bids and write what is wrong with it. The note carries the
  board, the call, its seat, the rule that fired and what that rule claims to
  show.
- Or write about the board as a whole from the footer, with no bid selected.

Notes land in `data/notes/notes.jsonl`, with the same content laid out to read
straight through in `data/notes/NOTES.md`. Both are tracked, so a note taken on
a phone reaches a session by way of a commit.

Each note is self-contained: the durable board reference (`seed507.jsonl.gz#477`
— the session's deal id is a uuid forgotten on restart), all four hands, both
auctions with the rule behind every one of our calls, and both scores. A note
that cannot say which board it is about stops being actionable within a day.

### Working through them

```bash
python3 tools/notes.py list          # what is open
python3 tools/notes.py show --open   # all of it, hands and auctions included
python3 tools/notes.py done note-0003
```

Reading `data/notes/NOTES.md` is equivalent to `show --open`. The fix goes into
`src/bridgebidder/systems/two_over_one.yaml` by hand.

### Checking a change

```bash
python3 tools/screen_pool.py --json /tmp/before.json      # before the edit
python3 tools/screen_pool.py --json /tmp/after.json --against /tmp/before.json
```

`tools/screen_pool.py` replays `data/pool/*.jsonl.gz` under the working tree,
answering opponent calls from `data/ben_cache.sqlite.gz`, so it runs on a
machine that has never had BEN installed. The statistics are
`roundkit.screen.summarise` — paired total over the whole pool with unchanged
boards as zeros, a bootstrap CI, an eight-board floor, and a CI covering zero
read as REVERT.

One caveat it prints on every run: the pool was played at an older commit, so a
**clean** tree at HEAD already shows about 38 changed boards per 1000. That is
the rulebook having moved since, not your edit. Two readings compared with
`--against` carry the same drift and cancel it; a proper significance test
needs a pool rebuilt at the current commit
(`tools/roundkit/screen.py pool`), which needs a live BEN worker.

`endplay` (the `dd` extra) is not optional here. Without it `get_dd()` falls
back to a HCP-and-shape heuristic and a re-scored board becomes an estimate
wearing the costume of a score; the screen refuses to run rather than produce
one.
