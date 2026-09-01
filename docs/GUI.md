# The GUI

Two screens over the bidding engine:

- **Deal Explorer** — a board where BEN outscored us, both auctions side by
  side. Click any of our calls to see the rule that produced it, what it shows,
  what it denies, and every candidate it beat with the score each got. Edit the
  rule there and the change is staged, not saved; staged changes are submitted
  together as a proposal.
- **Proposals** — replays the board pool under a proposal's changes and reports
  what it did to the paired IMP total, with the verdict rule from
  `roundkit/screen.py`. Accept writes to the YAML; reject discards.

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

Set `GITHUB_TOKEN` in the host's environment to enable AI-assisted rule
extraction. Everything else works without it.

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
| Corpus test | every position answerable | positions answered from `data/ben_cache.sqlite.gz`; anything it does not cover is reported as **unresolved** rather than scored as unchanged |

The pool boards are real losses, already scored by the real solver. What the
pool cannot do is surface a loss on a deal nobody has played, so with BEN
installed the Explorer prefers the live search.

`endplay` (the `dd` extra) is not optional for the corpus test. Without it
`get_dd()` silently falls back to a HCP-and-shape heuristic, and a re-scored
board becomes an estimate wearing the costume of a score; the test refuses to
run rather than produce one.

## Reading a corpus result

The statistics come from `roundkit.screen.summarise` — the same paired total,
bootstrap CI and eight-board verdict floor the command-line screener uses, so
the GUI cannot drift laxer than the tool the project already trusts. Two things
worth knowing about the number it prints:

- **The test runs over the whole selected pool**, with unchanged boards
  entering as zeros. Averaging over changed boards alone would inflate `t` by
  `sqrt(N/k)` — for 15 changed boards out of 12,000, by a factor of 28.
- **A CI that covers zero is a REVERT**, not a "promising". Keeping every
  change that looks positive pays the selection premium rather than the effect.

The **Resolves at 90%** figure says what effect size the run could actually
have detected. A short run that finds nothing has usually not established
that there is nothing to find, and that field is where it says so.

Pool size is a query parameter (`?boards=`, default 2000, rounded to whole
1000-board files) costing roughly a minute per thousand boards on one core.
A smaller pool is not a cheaper version of the same answer — it resolves a
larger effect, and the result says by how much.

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

## Editing a rule: staged, then submitted

Saving a rule edit **stages** a patch in the browser. Nothing appears under
Proposals until you press **Submit Proposal**, because several edits usually
belong in one proposal and each proposal costs a corpus run. The Deal
Explorer's footer carries the staged count, and Proposals says so when
unsubmitted work is waiting — that gap was previously invisible, so a saved
edit looked lost.

The editor speaks in HCP ranges, suit lengths, priority, a shows line and a
forcing status; `rule_patch.ui_changes_to_ops` and `ui_constraint_to_dsl`
translate that into `requires.hcp`, `requires.suits.H`, `establishes.forcing`
and a `not` block. Two guards are worth knowing:

- A suit reset to 0–13 is **removed**, not written back. `S: [0, 13]`
  constrains nothing and would reappear as though the rule had always cared
  about spades.
- An exception that constrains nothing is **refused**. The form always submits
  all four suits whether or not you touched them, and `not: {hcp: [0,37],
  suits: {...}}` matches every hand — an exception like that switches the rule
  off for everyone.

## Accepting a proposal

`rule_patch.apply_and_write` edits the rulebook through `ruamel.yaml` in
round-trip mode and then ports only the changed hunks back onto the original
text. Both steps matter:

- A PyYAML round-trip deletes all 2,230 comment lines and reflows the file
  from 16,683 lines to 32,395. The write refuses outright if `ruamel.yaml` is
  missing, and refuses again if the result would lose more than 10% of the
  comments.
- ruamel still normalises hand-written flow mappings (`{ a: 1 }` becomes
  `{a: 1}`), which alone is a 9,700-line diff around a two-line change. Diffing
  two ruamel dumps isolates the real change, which is then applied to the
  original text — so an accepted proposal lands as about ten lines.

`copy.deepcopy` on a ruamel document drops 244 of those comments, so the write
path patches the loaded document in place rather than a copy.
