from datetime import datetime
from pathlib import Path

LOG_FILE = Path("agent.log")


def log_event(event_type: str, message: str):
    LOG_FILE.parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"[{timestamp}] [{event_type.upper()}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    return entry