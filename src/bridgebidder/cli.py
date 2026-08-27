"""CLI: `bid choose input.json` / `bid explain input.json` (or stdin)."""

from __future__ import annotations

import argparse
import json
import sys

from .api import choose_bid, explain_bid


def _read_input(path: str | None) -> dict:
    if path and path != "-":
        with open(path) as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bid",
        description="2/1 Game Forcing bridge bidding engine",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_choose = sub.add_parser("choose", help="choose a call for a hand + auction state")
    p_choose.add_argument("input", nargs="?", default="-", help="JSON input file (default: stdin)")
    p_choose.add_argument("--no-arbitration", action="store_true",
                          help="fast-path only (skip simulation arbitration)")

    p_explain = sub.add_parser("explain", help="explain a candidate call in an auction state")
    p_explain.add_argument("input", nargs="?", default="-", help="JSON input file (default: stdin)")

    args = parser.parse_args(argv)
    try:
        request = _read_input(args.input)
        if args.command == "choose":
            if args.no_arbitration:
                request["use_arbitration"] = False
            result = choose_bid(request)
        else:
            result = explain_bid(request)
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
