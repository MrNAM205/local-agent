import subprocess
import shlex

# Commands that are NEVER allowed (Hybrid Mode safety)
BLOCKLIST = {
    "del",
    "erase",
    "rm",
    "rmdir",
    "format",
    "shutdown",
    "reboot",
    "poweroff",
    "mv",
    "move",
    "copy",
    "cp",
    "sc",
    "taskkill",
    "reg",
    "diskpart",
}

def run_command(cmd: str):
    cmd = cmd.strip()

    if not cmd:
        return "No command provided."

    # Extract the base command (first word)
    base = cmd.split()[0].lower()

    # Block dangerous commands
    if base in BLOCKLIST:
        return f"Command '{base}' is blocked for safety."

    try:
        # Use shell=True so Windows built-ins like 'dir' work
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if output:
            return output
        if error:
            return error

        return "(no output)"

    except Exception as e:
        return f"Error running command: {e}"
