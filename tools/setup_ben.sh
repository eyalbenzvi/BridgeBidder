#!/usr/bin/env bash
# Install BEN (github.com/lorserker/ben) into an isolated virtualenv.
#
# BEN is the neural bidder this project measures itself against.  It lives in
# its own venv on purpose: it pins numpy<2.1 while this project needs 2.x for
# endplay's double-dummy solver, so the two cannot share an interpreter.  Only
# BEN's ONNX bidder is used (no TensorFlow), driven over a pipe by
# tools/ben_worker.py.
#
# Everything lands in /tmp, which is ephemeral - re-run this after any fresh
# container.  Takes about a minute.
set -euo pipefail

BEN_DIR=${BEN_DIR:-/tmp/ben}
BEN_ENV=${BEN_ENV:-/tmp/benenv}

if [ ! -d "$BEN_DIR" ]; then
  git clone --depth 1 https://github.com/lorserker/ben.git "$BEN_DIR"
fi

if [ ! -x "$BEN_ENV/bin/python" ]; then
  python3 -m venv "$BEN_ENV"
fi
"$BEN_ENV/bin/pip" install -q --upgrade pip
"$BEN_ENV/bin/pip" install -q "numpy<2.1" onnxruntime

test -f "$BEN_DIR/models/onnx/bidder.onnx" || {
  echo "ERROR: $BEN_DIR/models/onnx/bidder.onnx missing (the repo ships it)" >&2
  exit 1
}

echo "BEN ready.  Smoke test (expect 1NT):"
printf '%s\n' '{"hands":{"N":"AQ52.KJ4.QT9.KJ7","E":"K873.A98.J83.QT9","S":"JT96.Q7532.A2.65","W":"4.T6.K7654.A8432"},"dealer":"N","vuln_ns":0,"vuln_ew":0,"auction":[]}' \
  | "$BEN_ENV/bin/python" "$(dirname "$0")/ben_worker.py"
