# Task Tracker CLI (Tracking task using Command Line Interface)
import argparse
import json
import os
from datetime import datetime

# Define the JSON storage file
DATA_FILE = "cli_data.json"

# Load JSON data
def load():
    # Load existing data or initilize on empty list
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

# Functionality to add
def add(adding_input):
    data = load()

    next_id = len(data) + 1

    entry = {
        "id": next_id,
        "task": adding_input,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }

    # Write into JSON file
    data.append(entry)
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Task added successfully (ID: {next_id})")


# Functionality to list
def list():
    data = load()
    if not data:
        print("No task found")
        return

    print("============ List of tasks ============")
    for index, task in enumerate(data):
        if index > 0:
            print("-" * 80)

        if isinstance(task, dict):
            task_list = ", ".join(str(value) for value in task.values())
            print(task_list)

def list_todo():
    data = load()
    
    target_key = "status"
    target_value = "todo"

    print("============ List of tasks in todo status ============")
    for index, task in enumerate(data):
        if index > 0:
            print("-" * 80)
    
        if isinstance(task, dict) and task.get(target_key) == target_value:
            task_list = ", ".join(str(value) for value in task.values())
            print(task_list)

def list_inprogress():
    data = load()
    
    target_key = "status"
    target_value = "in-progress"

    print("============ List of tasks in in-progress status ============")
    for index, task in enumerate(data):
        if index > 0:
            print("-" * 80)
    
        if isinstance(task, dict) and task.get(target_key) == target_value:
            task_list = ", ".join(str(value) for value in task.values())
            print(task_list)

def list_done():
    data = load()
    
    target_key = "status"
    target_value = "done"

    print("============ List of tasks in done status ============")
    for index, task in enumerate(data):
        if index > 0:
            print("-" * 80)
    
        if isinstance(task, dict) and task.get(target_key) == target_value:
            task_list = ", ".join(str(value) for value in task.values())
            print(task_list)
 

# Functionality to update
def update(id_input, text_input):
    data = load()

    update_task = next((task for task in data if task["id"] == id_input), None)
    if update_task:
        update_task.update(
            {
                "task": text_input,
                "updatedAt": datetime.now().isoformat()
            }
        )
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Task updated successfully (ID: {id_input})")

    else:
        print("Id not found")
        return

# Functionality to delete
def delete(id_input):
    data = load()
    list_task = next((task for task in data if task["id"] == id_input), None)
    if not list_task:
        print("Id not found")
        return

    deleted_task = [task for task in data if task.get("id") != id_input]

    with open(DATA_FILE, "w") as file:
        json.dump(deleted_task, file, indent=4)
    print(f"Task deleted successfully (ID: {id_input})")


# Functionality to marking
def mark_inprogress(id_input):
    data = load()
    
    update_task = next((task for task in data if task["id"] == id_input), None)
    if update_task:
        update_task.update(
            {
                "status": "in-progress"
            }
        )
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Task marked to in-progress (ID: {id_input})")
    
    else:
        print("Id not found")
        return

def mark_done(id_input):
    data = load()
    
    update_task = next((task for task in data if task["id"] == id_input), None)
    if update_task:
        update_task.update(
            {
                "status": "done"
            }
        )
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Task marked to done (ID: {id_input})")
    
    else:
        print("Id not found")
        return


def main(): 
    # Set up CLI argument parsing
    parser = argparse.ArgumentParser(prog="task-cli", description="Begin to manipulate data in task track")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", type=str, help="Input task into JSON file")

    # List command
    list_parser = subparsers.add_parser("list", help="List items in task dictionary")
    list_subparsers = list_parser.add_subparsers(dest="list_format", required=True)

    # List command handles all
    all_parser = list_subparsers.add_parser("all", help="List all items that are in all status")
    all_parser.set_defaults(func=list)

    # List command handles todo
    todo_parser = list_subparsers.add_parser("todo", help="List all items that are in todo status")
    todo_parser.set_defaults(func=list_todo)

    # List command handles in-progress
    inprogress_parser = list_subparsers.add_parser("in-progress", help="List all items that are in in-progress status")
    inprogress_parser.set_defaults(func=list_inprogress)

    # List command handles done
    done_parser = list_subparsers.add_parser("done", help="List all items that are in done status")
    done_parser.set_defaults(func=list_done)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("update_id", type=int, help="Select an id in JSON file")
    update_parser.add_argument("update_text", type=str, help="Update task in JSON file")

    # Delete Command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("delete_id", type=int, help="Select an id in JSON file")

    # Mark In-Progress Command
    markin_parser = subparsers.add_parser("mark-in-progress", help="Mark a task to in-progress status")
    markin_parser.add_argument("markin_id", type=int, help="Select an id in JSON file")

    # Mark Done Command
    markdone_parser = subparsers.add_parser("mark-done", help="Mark a task to done status")
    markdone_parser.add_argument("markdone_id", type=int, help="Select an id in JSON file")

    args = parser.parse_args()

    # Route arguments
    if args.command == "add":
        add(args.text)
    elif args.command == "list":
        args.func()
    elif args.command == "update":
        update(args.update_id, args.update_text)
    elif args.command == "delete":
        delete(args.delete_id)
    elif args.command == "mark-in-progress":
        mark_inprogress(args.markin_id)
    elif args.command == "mark-done":
        mark_done(args.markdone_id)


if __name__ == "__main__":
    main()