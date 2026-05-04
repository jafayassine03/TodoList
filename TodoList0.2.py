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

def sort_tasks(tasks):
    return sorted(tasks, key=lambda x: (x["completed"], x["priority"], x["due_date"]))

def display_tasks(tasks):
    tasks = sort_tasks(tasks)
    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\n Your Tasks:")
    print("-" * 50)
    for i, task in enumerate(tasks, 1):
        status = "Done" if task["completed"] else "Pending"
        print(f"{i}. {task['title']}")
        print(f"   Status   : {status}")
        print(f"   Priority : {task['priority']}")
        print(f"   Due      : {task['due_date']}")
        print(f"   Added    : {task['created_at']}")
        print("-" * 50)

def add_task(tasks):
    title = input("Task title: ").strip()
    due_date = input("Due date (YYYY-MM-DD or leave empty): ").strip()
    priority = input("Priority (1=High, 2=Medium, 3=Low): ").strip()

    if priority not in ["1", "2", "3"]:
        priority = "2"

    task = {
        "title": title,
        "completed": False,
        "priority": int(priority),
        "due_date": due_date if due_date else "9999-12-31",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(task)
    save_tasks(tasks)
    print(" Task added successfully!")

def delete_task(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        tasks_sorted = sort_tasks(tasks)
        if 0 <= idx < len(tasks_sorted):
            removed = tasks_sorted[idx]
            tasks.remove(removed)
            save_tasks(tasks)
            print(f" Deleted: {removed['title']}")
        else:
            print(" Invalid number.")
    except ValueError:
        print(" Please enter a valid number.")

def mark_completed(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to mark as completed: ")) - 1
        tasks_sorted = sort_tasks(tasks)
        if 0 <= idx < len(tasks_sorted):
            task = tasks_sorted[idx]
            task["completed"] = True
            save_tasks(tasks)
            print(" Task marked as completed!")
        else:
            print(" Invalid number.")
    except ValueError:
        print(" Please enter a valid number.")

def edit_task(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to edit: ")) - 1
        tasks_sorted = sort_tasks(tasks)
        if 0 <= idx < len(tasks_sorted):
            task = tasks_sorted[idx]

            new_title = input("New title (leave empty to keep current): ").strip()
            new_due = input("New due date (leave empty to keep current): ").strip()
            new_priority = input("New priority (1=High, 2=Medium, 3=Low): ").strip()

            if new_title:
                task["title"] = new_title
            if new_due:
                task["due_date"] = new_due
            if new_priority in ["1", "2", "3"]:
                task["priority"] = int(new_priority)

            save_tasks(tasks)
            print(" Task updated!")
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
        print("5. Edit Task")
        print("6. Exit")

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
            edit_task(tasks)
        elif choice == "6":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main()