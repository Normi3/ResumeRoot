#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="$ROOT_DIR/.venv"

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR/vendor/applypilot"
"$VENV_DIR/bin/python" -m pip install --no-deps python-jobspy
"$VENV_DIR/bin/python" -m pip install pydantic tls-client requests markdownify regex
"$VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR"

printf '%s\n' "ResumeRoot is installed. Next: make init && make doctor"
