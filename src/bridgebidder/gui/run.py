"""Launch the BridgeBidder GUI server.

Reads PORT from the environment so the same entry point works locally and on
a PaaS that assigns one (Render, Hugging Face Spaces, Fly, Railway).  Auto-
reload is on only when BB_GUI_RELOAD is set: a reloader in a 512 MB container
doubles the process count and reloads on the answer cache it just wrote.
"""
import os
import sys
from pathlib import Path

# Ensure tools/ is on sys.path so compare_ben.Ben is importable.
sys.path.insert(0, str(Path(__file__).parents[3] / "tools"))

import uvicorn


def main():
    port = int(os.environ.get("PORT", "8765"))
    reload = os.environ.get("BB_GUI_RELOAD", "").lower() in ("1", "true", "yes")
    uvicorn.run(
        "bridgebidder.gui.app:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
