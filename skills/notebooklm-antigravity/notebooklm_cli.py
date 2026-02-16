#!/usr/bin/env python3
"""
NotebookLM CLI wrapper — callable from Clawdbot agent via bash.
Usage:
  python3 notebooklm_cli.py list
  python3 notebooklm_cli.py query <notebook_id> "<question>"
  python3 notebooklm_cli.py summary <notebook_id>
"""
import sys
import os
import json

# Resolve project root: ANTIGRAVITY_ROOT env > follow server.py symlink > known paths
def _find_project_root():
    # 1. Explicit env var
    if os.environ.get("ANTIGRAVITY_ROOT"):
        return os.environ["ANTIGRAVITY_ROOT"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 2. Follow server.py symlink if it exists
    symlink = os.path.join(script_dir, "server.py")
    if os.path.islink(symlink):
        target = os.path.realpath(symlink)
        # server.py -> <root>/mcp_server/server.py  =>  root = ../..
        return os.path.abspath(os.path.join(os.path.dirname(target), ".."))
    # 3. Check if we're inside the project (bot_skill/ subfolder)
    candidate = os.path.abspath(os.path.join(script_dir, ".."))
    if os.path.isfile(os.path.join(candidate, "mcp_server", "server.py")):
        return candidate
    # 4. Known deployment path
    for p in ["/root/ehealth-notebooklm-antigravity", os.path.expanduser("~/ehealth-notebooklm-antigravity")]:
        if os.path.isdir(p):
            return p
    return script_dir

PROJECT_ROOT = _find_project_root()
sys.path.insert(0, PROJECT_ROOT)

# Load environment from .env if not already set
env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                if key.strip() not in os.environ:
                    os.environ[key.strip()] = value.strip()

LIBRARY_PATH = os.path.join(PROJECT_ROOT, "mcp_server", "library.json")

def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

def load_library():
    """Load the notebook library from library.json"""
    try:
        with open(LIBRARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": True, "message": f"Failed to load library: {e}"}

def cmd_list():
    """List all notebooks from library.json"""
    lib = load_library()
    if "error" in lib:
        return lib
    notebooks = []
    for nb in lib.get("notebooks", []):
        notebooks.append({
            "id": nb.get("id", ""),
            "name": nb.get("name", ""),
            "description": nb.get("description", "")[:200],
            "url": nb.get("url", ""),
            "topics": nb.get("topics", [])[:5]
        })
    return {"success": True, "notebooks": notebooks, "count": len(notebooks)}

def cmd_query(notebook_id, query):
    """Query a notebook using Gemini API"""
    lib = load_library()
    if "error" in lib:
        return lib

    # Find notebook
    notebook = None
    for nb in lib.get("notebooks", []):
        if nb.get("id") == notebook_id:
            notebook = nb
            break
    if not notebook:
        return {"success": False, "error": f"Notebook '{notebook_id}' not found"}

    # Build context from notebook metadata
    context_parts = []
    context_parts.append(f"Notebook: {notebook.get('name', '')}")
    context_parts.append(f"Description: {notebook.get('description', '')}")

    if notebook.get("topics"):
        context_parts.append(f"Topics: {', '.join(notebook['topics'])}")

    if notebook.get("sources"):
        for src in notebook["sources"]:
            if isinstance(src, dict):
                context_parts.append(f"Source: {src.get('title', '')} - {src.get('content', src.get('description', ''))}")
            elif isinstance(src, str):
                context_parts.append(f"Source: {src}")

    if notebook.get("qa_pairs"):
        for qa in notebook["qa_pairs"]:
            if isinstance(qa, dict):
                context_parts.append(f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}")

    context = "\n\n".join(context_parts)

    if not context.strip() or len(context) < 50:
        # Not enough local data — return metadata only
        return {
            "success": True,
            "question": query,
            "answer": f"Нотатник '{notebook.get('name', notebook_id)}' знайдено, але локальний контент обмежений.\n\nОпис: {notebook.get('description', 'N/A')}\n\nURL: {notebook.get('url', 'N/A')}\n\nТеми: {', '.join(notebook.get('topics', []))}",
            "notebook": notebook.get("name", notebook_id),
            "source": "metadata-only"
        }

    # Use Gemini to answer
    try:
        from src.gemini_client import GeminiClient
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "GEMINI_API_KEY not set in environment"}
        client = GeminiClient(api_key=api_key)
        answer = client.analyze_document(context, query)
        return {
            "success": True,
            "question": query,
            "answer": answer,
            "notebook": notebook.get("name", notebook_id),
            "source": "gemini-analysis"
        }
    except Exception as e:
        return {"success": False, "error": f"Gemini query failed: {e}"}

def cmd_summary(notebook_id):
    """Get summary of a notebook"""
    lib = load_library()
    if "error" in lib:
        return lib

    notebook = None
    for nb in lib.get("notebooks", []):
        if nb.get("id") == notebook_id:
            notebook = nb
            break
    if not notebook:
        return {"success": False, "error": f"Notebook '{notebook_id}' not found"}

    return {
        "success": True,
        "notebook_id": notebook_id,
        "name": notebook.get("name", ""),
        "description": notebook.get("description", ""),
        "url": notebook.get("url", ""),
        "topics": notebook.get("topics", []),
        "sources_count": len(notebook.get("sources", []))
    }

def main():
    if len(sys.argv) < 2:
        print_json({"error": True, "message": "Usage: notebooklm_cli.py <list|query|summary> [args...]"})
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        print_json(cmd_list())
    elif command == "query":
        if len(sys.argv) < 4:
            print_json({"error": True, "message": "Usage: notebooklm_cli.py query <notebook_id> \"<question>\""})
            sys.exit(1)
        notebook_id = sys.argv[2]
        query = " ".join(sys.argv[3:])
        print_json(cmd_query(notebook_id, query))
    elif command == "summary":
        if len(sys.argv) < 3:
            print_json({"error": True, "message": "Usage: notebooklm_cli.py summary <notebook_id>"})
            sys.exit(1)
        print_json(cmd_summary(sys.argv[2]))
    else:
        print_json({"error": True, "message": f"Unknown command: {command}. Use: list, query, summary"})
        sys.exit(1)

if __name__ == "__main__":
    main()
