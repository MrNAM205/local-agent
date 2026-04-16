from pathlib import Path
from tools_notes import create_note, list_notes, show_note
from tools_commands import run_command
from tools_tasks import add_task, list_tasks, mark_done
from tools_logging import log_event
from tools_downloader import download_file
from tools_desktop import mouse_move, mouse_click, type_text, press_key, open_app
from tools_macros import add_macro, list_macros, delete_macro, run_macro
from tools_nla import parse_natural
from tools_context import set_context, get_context, get_all_context
from tools_autonomy import enable_autonomy, disable_autonomy, autonomy_status, autonomy_loop
from tools_selftrain import self_train

def execute_action(cmd):
    """Central dispatcher for all agent actions to ensure context is updated consistently."""
    if cmd.startswith("run:"):
        raw_cmd = cmd[4:].strip()
        output = run_command(raw_cmd)
        set_context("last_command", raw_cmd)
        set_context("last_output", output)
        return output
    elif cmd.startswith("note:"):
        content = cmd[5:].strip()
        filename = create_note(content)
        set_context("last_note", filename)
        return f"Saved note: {filename}"
    elif cmd.startswith("task:"):
        cat, txt = [x.strip() for x in cmd[5:].split("|", 1)]
        task = add_task(txt, cat)
        set_context("last_task", task)
        return f"Added task: [{cat}] {txt}"
    elif cmd.startswith("download:"):
        url = cmd[9:].strip()
        result = download_file(url)
        set_context("last_download", result)
        return result
    elif cmd.startswith("open:"):
        app = cmd[5:].strip()
        result = open_app(app)
        set_context("last_app", app)
        return result
    elif cmd.startswith("move:"):
        parts = cmd.split()
        x, y = int(parts[1]), int(parts[2])
        result = mouse_move(x, y)
        set_context("last_mouse", [x, y])
        return result
    elif cmd.startswith("click"):
        return mouse_click()
    elif cmd.startswith("type:"):
        return type_text(cmd[5:].strip())
    elif cmd.startswith("key:"):
        return press_key(cmd[4:].strip())
    return f"Unknown action: {cmd}"

def main():
    notes_dir = Path("notes")
    notes_dir.mkdir(exist_ok=True)

    print("Simple Note Agent")
    print("Commands:")
    print("  note: <text>")
    print("  list notes")
    print("  show note <number>")
    print("  run: <command>")
    print("  task: <category> | <task text>")
    print("  tasks")
    print("  tasks all")
    print("  done <number>")
    print("  download: <url>")
    print("  downloads")
    print("  move: <x> <y>")
    print("  click")
    print("  type: <text>")
    print("  key: <key>")
    print("  open: <app>")
    print("  macro: <name> | <step1> ; <step2>")
    print("  macro run: <name>")
    print("  macros")
    print("  do: <natural language>")
    print("  context")
    print("  repeat last")
    print("  open last download")
    print("  show last note")
    print("  move last")
    print("  redo last macro")
    print("  autonomy on | assist | act | off")
    print("  autonomy status")
    print("  train")
    print("  train auto on | off")
    print("  quit")
    print()

    while True:
        try:
            user_input = input("agent> ").strip()
        except (EOFError, KeyboardInterrupt):
            log_event("system", "Agent terminated by user")
            print("\nExiting.")
            break

        if not user_input:
            continue

        # Exit
        if user_input.lower() in ("quit", "exit"):
            log_event("system", "Agent exited normally")
            print("Goodbye.")
            break

        # Create a note
        if user_input.lower().startswith("note:"):
            print(execute_action(user_input))
            log_event("note", f"Note processed: {user_input[5:]}")
            continue

        # List notes
        if user_input.lower() == "list notes":
            notes = list_notes()
            log_event("notes", "Listed notes")
            if not notes:
                print("No notes found.")
            else:
                print("Notes:")
                for idx, name in enumerate(notes, start=1):
                    print(f"  {idx}. {name}")
            continue

        # Show a note
        if user_input.lower().startswith("show note"):
            parts = user_input.split()
            index = int(parts[2])
            content = show_note(index)
            log_event("note", f"Viewed note #{index}")
            print("\n" + "-" * 40)
            print(content)
            print("-" * 40 + "\n")
            continue

        # Run a whitelisted command
        if user_input.lower().startswith("run:"):
            output = execute_action(user_input)
            print("\n" + "-" * 40)
            print(output)
            print("-" * 40 + "\n")
            log_event("command", f"Processed run: {user_input[4:]}")
            continue

        # Add a task
        if user_input.lower().startswith("task:"):
            print(execute_action(user_input))
            continue

        # List tasks
        if user_input.lower() == "tasks":
            tasks = list_tasks(show_done=False)
            log_event("task", "Listed active tasks")
            if not tasks:
                print("No active tasks.")
            else:
                print("Active Tasks:")
                for idx, t in enumerate(tasks, start=1):
                    print(f"  {idx}. [{t['category']}] {t['task']} (created {t['created']})")
            continue

        # List all tasks
        if user_input.lower() == "tasks all":
            tasks = list_tasks(show_done=True)
            log_event("task", "Listed all tasks")
            for idx, t in enumerate(tasks, start=1):
                status = "✓ done" if t["done"] else "• active"
                print(f"  {idx}. [{t['category']}] {t['task']} ({status})")
            continue

        # Mark task done
        if user_input.lower().startswith("done "):
            index = int(user_input.split()[1])
            task = mark_done(index)
            if task:
                set_context("last_task_done", task)
                log_event("task", f"Marked task done: {task['task']}")
                print(f"Marked done: {task['task']}")
            continue

        # Download a file
        if user_input.lower().startswith("download:"):
            print(execute_action(user_input))
            continue

        # List downloads
        if user_input.lower() == "downloads":
            files = sorted(Path("downloads").glob("*"))
            log_event("download", "Listed downloaded files")
            for f in files:
                print(f"  {f.name}")
            continue

        # Desktop control: move mouse
        if user_input.lower().startswith("move:"):
            print(execute_action(user_input))
            continue

        # Desktop control: click
        if user_input.lower() == "click":
            print(execute_action(user_input))
            continue

        # Desktop control: type text
        if user_input.lower().startswith("type:"):
            print(execute_action(user_input))
            continue

        # Desktop control: press key
        if user_input.lower().startswith("key:"):
            print(execute_action(user_input))
            continue

        # Desktop control: open app
        if user_input.lower().startswith("open:"):
            print(execute_action(user_input))
            continue

        # Create a macro
        if user_input.lower().startswith("macro:"):
            raw = user_input[6:].strip()
            if "|" not in raw:
                print("Usage: macro: <name> | <step1> ; <step2> ; ...")
                continue

            name, steps_raw = [x.strip() for x in raw.split("|", 1)]
            steps = [s.strip() for s in steps_raw.split(";") if s.strip()]

            add_macro(name, steps)
            print(f"Macro '{name}' saved with {len(steps)} steps.")
            continue

        # Run a macro
        if user_input.lower().startswith("macro run:"):
            name = user_input[11:].strip()
            steps = run_macro(name)
            if steps is None:
                print(f"No macro named '{name}'.")
                continue

            print(f"Running macro '{name}'...")
            for step in steps:
                print(f" → {step}")
                print(execute_action(step))

            set_context("last_macro", name)
            print(f"Macro '{name}' complete.")
            continue

        # List macros
        if user_input.lower() == "macros":
            macros = list_macros()
            if not macros:
                print("No macros saved.")
            else:
                print("Macros:")
                for name, steps in macros.items():
                    print(f"  {name}: {len(steps)} steps")
            continue

        # Delete a macro
        if user_input.lower().startswith("macro delete:"):
            name = user_input[14:].strip()
            if delete_macro(name):
                print(f"Deleted macro '{name}'.")
            else:
                print(f"No macro named '{name}'.")
            continue

        # Natural language actions
        if user_input.lower().startswith("do:"):
            text = user_input[3:].strip()
            commands = parse_natural(text)

            if not commands:
                print("I couldn't understand that action.")
                continue

            print(f"Interpreting: {text}")
            for cmd in commands:
                print(f" → {cmd}")
                print(execute_action(cmd))
            set_context("last_nla", commands)
            continue

        # Show all context
        if user_input.lower() == "context":
            ctx = get_all_context()
            print("Context State:")
            for k, v in ctx.items():
                print(f"  {k}: {v}")
            continue

        # Repeat last command
        if user_input.lower() == "repeat last":
            last = get_context("last_command")
            if not last:
                print("No last command stored.")
                continue
            print(f"Repeating: {last}")
            print(execute_action(f"run: {last}"))
            continue

        # Open last download
        if user_input.lower() == "open last download":
            last = get_context("last_download")
            if not last or "Downloaded:" not in last:
                print("No valid last download stored.")
                continue
            filename = last.replace("Downloaded: ", "")
            print(execute_action(f"open: downloads/{filename}"))
            continue

        # Show last note
        if user_input.lower() == "show last note":
            last = get_context("last_note")
            if not last:
                print("No last note stored.")
                continue
            try:
                idx = list_notes().index(last) + 1
                print(show_note(idx))
            except ValueError:
                print("Last note no longer exists.")
            continue

        # Move to last mouse position
        if user_input.lower() == "move last":
            pos = get_context("last_mouse")
            if not pos:
                print("No last mouse position stored.")
                continue
            print(execute_action(f"move: {pos[0]} {pos[1]}"))
            continue

        # Redo last macro
        if user_input.lower() == "redo last macro":
            last = get_context("last_macro")
            if not last:
                print("No last macro stored.")
                continue
            steps = run_macro(last)
            print(f"Running macro '{last}' again...")
            for step in steps:
                print(f" → {step}")
                print(execute_action(step))
            continue

        # Autonomy commands
        if user_input.lower() == "autonomy on":
            print(enable_autonomy("suggest"))
            continue
        if user_input.lower() == "autonomy assist":
            print(enable_autonomy("assist"))
            continue
        if user_input.lower() == "autonomy act":
            print(enable_autonomy("act"))
            continue
        if user_input.lower() == "autonomy off":
            print(disable_autonomy())
            continue
        if user_input.lower() == "autonomy status":
            print(autonomy_status())
            continue

        # Self-training commands
        if user_input.lower() == "train":
            improvements = self_train()
            print("Self-training complete.")
            for imp in improvements:
                print("  - " + imp)
            continue
        if user_input.lower() == "train auto on":
            set_context("auto_train", True)
            print("Automatic self-training enabled.")
            continue
        if user_input.lower() == "train auto off":
            set_context("auto_train", False)
            print("Automatic self-training disabled.")
            continue

        # Run autonomy loop and auto-train triggers
        auto = autonomy_loop()
        if auto:
            print("Autonomy suggestions:")
            for s in auto:
                print("  - " + s)

        if get_context("auto_train"):
            self_train()

        # Fallback
            continue

        # Fallback
        log_event("error", f"Unknown command: {user_input}")
        print("Unknown command.")


if __name__ == "__main__":
    main()
