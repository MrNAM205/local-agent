from pathlib import Path
import re

NOTES_DIR = Path("notes")
NOTES_DIR.mkdir(exist_ok=True)


def _slug_from_text(text: str, max_words: int = 6) -> str:
    words = text.strip().split()
    if not words:
        base = "note"
    else:
        base = "-".join(words[:max_words])
    base = base.lower()
    base = re.sub(r"[^a-z0-9_-]+", "-", base)
    base = re.sub(r"-+", "-", base).strip("-")
    return base or "note"


def _unique_filename(base_slug: str) -> str:
    candidate = NOTES_DIR / f"{base_slug}.txt"
    if not candidate.exists():
        return candidate.name

    counter = 2
    while True:
        candidate = NOTES_DIR / f"{base_slug}_{counter}.txt"
        if not candidate.exists():
            return candidate.name
        counter += 1


def create_note(content: str) -> str:
    base_slug = _slug_from_text(content)
    filename = _unique_filename(base_slug)
    filepath = NOTES_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

    return filename


def list_notes():
    files = sorted(p.name for p in NOTES_DIR.glob("*.txt"))
    return files


def show_note(index: int):
    files = list_notes()
    if index < 1 or index > len(files):
        return None
    filename = files[index - 1]
    filepath = NOTES_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
