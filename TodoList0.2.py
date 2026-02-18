import json
from datetime import datetime

FILE = "tasks.json"


def load_tasks():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\n Your Tasks:")
    print("-" * 50)
    for i, task in enumerate(tasks, 1):
        status = " Done" if task["completed"] else " Pending"
        print(f"{i}. {task['title']}")
        print(f"   Status : {status}")
        print(f"   Due    : {task['due_date']}")
        print(f"   Added  : {task['created_at']}")
        print("-" * 50)


def add_task(tasks):
    title = input("Task title: ").strip()
    due_date = input("Due date (YYYY-MM-DD or leave empty): ").strip()

    task = {
        "title": title,
        "completed": False,
        "due_date": due_date if due_date else "No due date",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(task)
    save_tasks(tasks)
    print(" Task added successfully!")


def delete_task(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"🗑 Deleted: {removed['title']}")
        else:
            print(" Invalid number.")
    except ValueError:
        print(" Please enter a valid number.")


def mark_completed(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to mark as completed: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = True
            save_tasks(tasks)
            print(" Task marked as completed!")
        else:
            print(" Invalid number.")
    except ValueError:
        print(" Please enter a valid number.")


def main():
    tasks = load_tasks()

    while True:
        print("\n====== TO-DO LIST ======")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Mark Task as Completed")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_completed(tasks)
        elif choice == "5":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice.")


if __name__ == "__main__":
    main()
