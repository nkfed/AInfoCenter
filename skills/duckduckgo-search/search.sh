#!/usr/bin/env bash
# DuckDuckGo Search Wrapper for Linux/WSL
# Auto-detects Python 3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo '{"error": true, "message": "Python not found. Install python3."}' >&2
    exit 1
fi

# Run the search script
"$PYTHON_CMD" "$SCRIPT_DIR/duckduckgo_search.py" "$@"
