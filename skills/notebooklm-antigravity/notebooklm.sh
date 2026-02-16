#!/usr/bin/env bash
# NotebookLM CLI Wrapper for Clawdbot
# Usage:
#   ./notebooklm.sh list
#   ./notebooklm.sh query <notebook_id> "<question>"
#   ./notebooklm.sh summary <notebook_id>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Resolve project root: follow server.py symlink > known paths
if [ -z "$ANTIGRAVITY_ROOT" ]; then
    if [ -L "$SCRIPT_DIR/server.py" ]; then
        ANTIGRAVITY_ROOT="$(cd "$(dirname "$(readlink -f "$SCRIPT_DIR/server.py")")" && cd .. && pwd)"
    elif [ -f "$SCRIPT_DIR/../mcp_server/server.py" ]; then
        ANTIGRAVITY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    elif [ -d "/root/ehealth-notebooklm-antigravity" ]; then
        ANTIGRAVITY_ROOT="/root/ehealth-notebooklm-antigravity"
    fi
fi
export ANTIGRAVITY_ROOT

# 2. Resolve Python: ANTIGRAVITY_PYTHON env > project venv > system python3
if [ -n "$ANTIGRAVITY_PYTHON" ] && [ -f "$ANTIGRAVITY_PYTHON" ]; then
    PYTHON_CMD="$ANTIGRAVITY_PYTHON"
elif [ -n "$ANTIGRAVITY_ROOT" ] && [ -f "$ANTIGRAVITY_ROOT/venv/bin/python3" ]; then
    PYTHON_CMD="$ANTIGRAVITY_ROOT/venv/bin/python3"
elif [ -n "$ANTIGRAVITY_ROOT" ] && [ -f "$ANTIGRAVITY_ROOT/venv/Scripts/python.exe" ]; then
    PYTHON_CMD="$ANTIGRAVITY_ROOT/venv/Scripts/python.exe"
else
    PYTHON_CMD="python3"
fi

if ! command -v "$PYTHON_CMD" &>/dev/null && [ ! -f "$PYTHON_CMD" ]; then
    echo '{"error": true, "message": "Python not found. Set ANTIGRAVITY_PYTHON or create a venv."}'
    exit 1
fi

"$PYTHON_CMD" "$SCRIPT_DIR/notebooklm_cli.py" "$@"
