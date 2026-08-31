"""Launch the BridgeBidder GUI server."""
import sys
from pathlib import Path

# Ensure tools/ is on sys.path so compare_ben.Ben is importable.
sys.path.insert(0, str(Path(__file__).parents[3] / "tools"))

import uvicorn


def main():
    uvicorn.run("bridgebidder.gui.app:app", host="0.0.0.0", port=8765, reload=True)


if __name__ == "__main__":
    main()
