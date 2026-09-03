# Rule notes

Observations captured from the GUI's Deal Explorer: a board where BEN outscored
our engine, and what the reporter thought was wrong with our bidding on it.

**Nothing here edits the rulebook.** These are the input to that work, not the
work. The fixes go into `src/bridgebidder/systems/two_over_one.yaml` by hand.

| file | what it is |
|---|---|
| `notes.jsonl` | the record — one JSON object per line, append-only |
| `NOTES.md` | the same content laid out to read straight through, regenerated on every write |

Do not edit `NOTES.md`; it is overwritten. Edit `notes.jsonl`, or use the CLI.

## Working through them

```bash
python3 tools/notes.py list          # what is open, one line each
python3 tools/notes.py show --open   # everything: hands, both auctions, rules
python3 tools/notes.py done note-0003
```

Each note is self-contained by design: the durable board reference
(`seed507.jsonl.gz#477` — the deal id in the GUI is a uuid forgotten on
restart), all four hands, both auctions with the rule behind every one of our
calls, both scores, and, when the note was written from a specific bid, that
bid's seat, call and rule. So a note can be acted on from this directory alone,
without the GUI running and without the session that wrote it.

## After a change

```bash
python3 tools/screen_pool.py --json /tmp/before.json      # before the edit
python3 tools/screen_pool.py --json /tmp/after.json --against /tmp/before.json
```

The pool was played at an older commit, so a clean tree already shows about 38
changed boards per 1000 — comparing two readings cancels that drift. See
`docs/GUI.md` for the full caveat.
