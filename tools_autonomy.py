import time
from tools_logging import log_event
from tools_context import get_context, set_context


AUTONOMY_STATE = {
    "enabled": False,
    "mode": "suggest"  # suggest | assist | act
}


def enable_autonomy(mode="suggest"):
    AUTONOMY_STATE["enabled"] = True
    AUTONOMY_STATE["mode"] = mode
    log_event("autonomy", f"Autonomy enabled in mode '{mode}'")
    return f"Autonomy enabled ({mode} mode)."


def disable_autonomy():
    AUTONOMY_STATE["enabled"] = False
    log_event("autonomy", "Autonomy disabled")
    return "Autonomy disabled."


def autonomy_status():
    return AUTONOMY_STATE


def autonomy_loop():
    """Runs after every user command."""
    if not AUTONOMY_STATE["enabled"]:
        return None

    mode = AUTONOMY_STATE["mode"]
    last_cmd = get_context("last_command")
    last_output = get_context("last_output")
    last_download = get_context("last_download")
    last_macro = get_context("last_macro")

    suggestions = []

    # --- Suggest opening last download ---
    if last_download and "downloaded" in str(last_download).lower():
        suggestions.append("I can open your last downloaded file.")

    # --- Suggest repeating last command ---
    if last_cmd and "dir" in last_cmd:
        suggestions.append("Want me to sort or filter that directory listing?")

    # --- Suggest running last macro again ---
    if last_macro:
        suggestions.append(f"Want me to run the '{last_macro}' macro again?")

    # --- Suggest next steps based on output ---
    if last_output and "error" in str(last_output).lower():
        suggestions.append("I can help troubleshoot that error.")

    # --- No suggestions ---
    if not suggestions:
        return None

    # --- Suggest Mode ---
    if mode == "suggest":
        return suggestions

    # --- Assist Mode ---
    if mode == "assist":
        # Only perform low-risk actions
        if last_download:
            set_context("autonomy_action", "open_last_download")
            return ["Opening last download automatically."]
        return suggestions

    # --- Act Mode ---
    if mode == "act":
        if last_download:
            set_context("autonomy_action", "open_last_download")
            return ["Acting: opening last download."]
        return suggestions