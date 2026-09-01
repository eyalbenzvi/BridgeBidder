# Container image for the BridgeBidder GUI.
#
# Works anywhere that builds a Dockerfile from a git repository -- Hugging Face
# Spaces, Fly, Railway, Cloud Run -- which is what makes the app reachable from
# a phone: the host clones and builds, and nothing is ever run locally.
#
# BEN itself is deliberately not in here.  The model lives outside this
# repository and needs its own interpreter, and the GUI does not require it:
# the Deal Explorer replays boards BEN already lost from `data/pool/`, and the
# corpus test answers new positions from the shipped answer cache.  What IS
# installed is `endplay`, the real double-dummy solver, because a re-scored
# board without it is an estimate wearing the costume of a score.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

WORKDIR /app

# Dependencies first, so edits to the source do not re-resolve the wheel set.
COPY pyproject.toml ./
COPY src/bridgebidder/__init__.py src/bridgebidder/__init__.py
RUN pip install --no-cache-dir \
        "pydantic>=2" "PyYAML>=6" \
        "fastapi>=0.110" "uvicorn[standard]>=0.29" "openai>=1.0" \
        "ruamel.yaml>=0.18" \
        "endplay>=0.5"

COPY . .
RUN pip install --no-cache-dir -e . --no-deps

EXPOSE 7860

CMD ["python", "-m", "bridgebidder.gui.run"]
