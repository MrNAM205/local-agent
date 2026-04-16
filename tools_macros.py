import json
from pathlib import Path
from tools_logging import log_event

MACRO_FILE = Path("macros.json")


def _load_macros():
    if not MACRO_FILE.exists():
        return {}
    try:
        with open(MACRO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_macros(macros):
    with open(MACRO_FILE, "w", encoding="utf-8") as f:
        json.dump(macros, f, indent=2, ensure_ascii=False)


def add_macro(name: str, steps: list):
    macros = _load_macros()
    macros[name] = steps
    _save_macros(macros)
    log_event("macro", f"Created macro '{name}' with {len(steps)} steps")
    return True


def list_macros():
    return _load_macros()


def delete_macro(name: str):
    macros = _load_macros()
    if name not in macros:
        return False
    del macros[name]
    _save_macros(macros)
    log_event("macro", f"Deleted macro '{name}'")
    return True


def run_macro(name: str):
    macros = _load_macros()
    if name not in macros:
        return None
    steps = macros[name]
    log_event("macro", f"Running macro '{name}' with {len(steps)} steps")
    return steps