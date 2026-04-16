import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path("tasks.json")


def _load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def _save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(task_text: str, category: str = "general"):
    tasks = _load_tasks()
    new_task = {
        "task": task_text,
        "category": category.lower(),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "done": False,
        "done_at": None
    }
    tasks.append(new_task)
    _save_tasks(tasks)
    return new_task


def list_tasks(show_done=False):
    tasks = _load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t["done"]]
    return tasks


def mark_done(index: int):
    tasks = _load_tasks()
    if index < 1 or index > len(tasks):
        return None

    tasks[index - 1]["done"] = True
    tasks[index - 1]["done_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _save_tasks(tasks)
    return tasks[index - 1]