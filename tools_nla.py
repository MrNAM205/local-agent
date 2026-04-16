import re
from tools_logging import log_event

def parse_natural(text: str):
    text = text.lower().strip()
    commands = []

    # --- OPEN APP ---
    if "open" in text:
        match = re.search(r"open ([a-z0-9\.\-_ ]+)", text)
        if match:
            app = match.group(1).strip()
            commands.append(f"open: {app}")

    # --- TYPE TEXT ---
    if "type" in text:
        match = re.search(r"type (.+)", text)
        if match:
            typed = match.group(1).strip()
            commands.append(f"type: {typed}")

    # --- MOVE MOUSE ---
    if "move" in text and "mouse" in text:
        match = re.search(r"move.*?(\d+)[^\d]+(\d+)", text)
        if match:
            x, y = match.group(1), match.group(2)
            commands.append(f"move: {x} {y}")

    # --- CLICK ---
    if "click" in text:
        if "double" in text:
            commands.append("click")
            commands.append("click")
        else:
            commands.append("click")

    # --- RUN COMMAND ---
    if "run" in text:
        match = re.search(r"run ([a-z0-9\.\-_ ]+)", text)
        if match:
            cmd = match.group(1).strip()
            commands.append(f"run: {cmd}")

    # --- DOWNLOAD ---
    if "download" in text:
        match = re.search(r"download (https?://\S+)", text)
        if match:
            url = match.group(1).strip()
            commands.append(f"download: {url}")

    # --- FALLBACK ---
    if not commands:
        log_event("nla", f"No match for natural language: {text}")
        return None

    log_event("nla", f"Parsed natural language into {len(commands)} commands")
    return commands