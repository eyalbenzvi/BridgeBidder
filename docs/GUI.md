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
