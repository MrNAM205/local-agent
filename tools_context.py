import json
from pathlib import Path
from tools_logging import log_event

CONTEXT_FILE = Path("context_state.json")


def _load_context():
    if not CONTEXT_FILE.exists():
        return {}
    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_context(ctx):
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(ctx, f, indent=2, ensure_ascii=False)


def set_context(key, value):
    ctx = _load_context()
    ctx[key] = value
    _save_context(ctx)
    log_event("context", f"Updated context '{key}' -> {value}")


def get_context(key):
    ctx = _load_context()
    return ctx.get(key)


def get_all_context():
    return _load_context()