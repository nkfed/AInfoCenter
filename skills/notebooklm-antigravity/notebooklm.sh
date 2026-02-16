#!/usr/bin/env bash
# NotebookLM CLI Wrapper for Clawdbot
# Usage:
#   ./notebooklm.sh list
#   ./notebooklm.sh query <notebook_id> "<question>"
#   ./notebooklm.sh summary <notebook_id>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve Python: ANTIGRAVITY_PYTHON env > project venv > system python3
if [ -n "$ANTIGRAVITY_PYTHON" ] && [ -f "$ANTIGRAVITY_PYTHON" ]; then
    PYTHON_CMD="$ANTIGRAVITY_PYTHON"
elif [ -f "$SCRIPT_DIR/../../venv/bin/python3" ]; then
    PYTHON_CMD="$SCRIPT_DIR/../../venv/bin/python3"
elif [ -f "$SCRIPT_DIR/../../venv/Scripts/python.exe" ]; then
    # Windows venv
    PYTHON_CMD="$SCRIPT_DIR/../../venv/Scripts/python.exe"
else
    PYTHON_CMD="python3"
fi

if ! command -v "$PYTHON_CMD" &>/dev/null && [ ! -f "$PYTHON_CMD" ]; then
    echo '{"error": true, "message": "Python not found. Set ANTIGRAVITY_PYTHON or create a venv."}'
    exit 1
fi

export ANTIGRAVITY_ROOT="${ANTIGRAVITY_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
"$PYTHON_CMD" "$SCRIPT_DIR/notebooklm_cli.py" "$@"
