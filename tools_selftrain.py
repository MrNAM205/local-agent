import re
from pathlib import Path
from tools_logging import log_event
from tools_context import get_all_context
from tools_macros import add_macro

LOG_FILE = Path("agent.log")


def extract_patterns():
    """Scan logs for repeated patterns."""
    if not LOG_FILE.exists():
        return {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    commands = []
    macros = []
    downloads = []
    opens = []
    moves = []

    for line in lines:
        if "[COMMAND]" in line.upper():
            m = re.search(r"Ran command: (.+)", line)
            if m:
                commands.append(m.group(1).strip())

        if "[MACRO]" in line.upper():
            m = re.search(r"macro '(.+)'", line.lower())
            if m:
                macros.append(m.group(1).strip())

        if "[DOWNLOAD]" in line.upper():
            downloads.append("download")

        if "[DESKTOP]" in line.upper():
            if "opened app" in line.lower():
                opens.append("open")
            if "moved mouse" in line.lower():
                moves.append("move")

    return {
        "commands": commands,
        "macros": macros,
        "downloads": downloads,
        "opens": opens,
        "moves": moves,
    }


def propose_macros(patterns):
    """Find repeated command sequences and propose macros."""
    commands = patterns["commands"]
    if len(commands) < 3:
        return []

    proposals = []
    for i in range(len(commands) - 2):
        seq = commands[i:i+3]
        if commands.count(seq[0]) > 2:
            proposals.append(seq)

    return proposals


def self_train():
    """Main self-training loop."""
    patterns = extract_patterns()
    ctx = get_all_context()

    improvements = []

    macro_proposals = propose_macros(patterns)
    for seq in macro_proposals:
        name = f"auto_{seq[0].replace(' ', '_')}"
        add_macro(name, [f"run: {c}" for c in seq])
        improvements.append(f"Created macro '{name}' from repeated pattern.")

    if patterns["downloads"]:
        improvements.append("Autonomy now suggests opening downloads more aggressively.")

    if improvements:
        log_event("selftrain", f"Self-training improvements: {improvements}")
    return improvements