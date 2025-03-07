import click  # to create command line interface
import json   # to load and save todo list
import os     # to check if file exists

TODO_FILE = "todo.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple todo list manager"""
    pass

@cli.command()
@click.argument("task")
def add(task):
    """Add a new todo task"""
    tasks = load_tasks()
    tasks.append({"task": task, "completed": False})
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")

@cli.command(name="list")  # Rename command to avoid conflict with Python's `list`
def list_tasks():
    """List all todo tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found")
        return
    for index, task in enumerate(tasks, 1):
        status = "✅" if task["completed"] else "❌"
        click.echo(f"{index}. {task['task']} [{status}]")

@cli.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed")
    else:
        click.echo(f"Invalid task number: {task_number}")

@cli.command()
@click.argument("task_number", type=int)  # Added missing argument
def remove(task_number):
    """Remove a task"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Task '{removed_task['task']}' removed")
    else:
        click.echo(f"Invalid task number: {task_number}")

if __name__ == "__main__":
    cli()
