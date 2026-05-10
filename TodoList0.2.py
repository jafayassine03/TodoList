import json
from datetime import datetime

FILE = "tasks.json"


# =========================
# FILE HANDLING
# =========================

def load_tasks():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# =========================
# HELPERS
# =========================

def sort_tasks(tasks):
    return sorted(
        tasks,
        key=lambda x: (
            x["completed"],
            x["priority"],
            x["due_date"]
        )
    )


def get_status(task):
    return "Done" if task["completed"] else "Pending"


def display_single_task(index, task):
    print(f"{index}. {task['title']}")
    print(f"   Status   : {get_status(task)}")
    print(f"   Priority : {task['priority']}")
    print(f"   Category : {task['category']}")
    print(f"   Due      : {task['due_date']}")
    print(f"   Added    : {task['created_at']}")
    print("-" * 50)


# =========================
# DISPLAY TASKS
# =========================

def display_tasks(tasks):
    tasks = sort_tasks(tasks)

    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nYOUR TASKS")
    print("=" * 50)

    for i, task in enumerate(tasks, start=1):
        display_single_task(i, task)


# =========================
# ADD TASK
# =========================

def add_task(tasks):
    print("\nADD NEW TASK")
    print("-" * 30)

    title = input("Task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    due_date = input("Due date (YYYY-MM-DD or leave empty): ").strip()
    category = input("Category: ").strip()

    try:
        priority = int(
            input("Priority (1=High, 2=Medium, 3=Low): ").strip()
        )

        if priority not in [1, 2, 3]:
            raise ValueError

    except ValueError:
        print("Invalid priority. Defaulting to Medium.")
        priority = 2

    # Validate date
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using no due date.")
            due_date = "9999-12-31"
    else:
        due_date = "9999-12-31"

    task = {
        "title": title,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category if category else "General"
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added successfully!")


# =========================
# DELETE TASK
# =========================

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    display_tasks(tasks)

    try:
        idx = int(input("Enter task number to delete: ")) - 1

        tasks_sorted = sort_tasks(tasks)

        if 0 <= idx < len(tasks_sorted):
            removed_task = tasks_sorted[idx]

            tasks.remove(removed_task)
            save_tasks(tasks)

            print(f"Deleted task: {removed_task['title']}")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# =========================
# MARK COMPLETED
# =========================

def mark_completed(tasks):
    if not tasks:
        print("No tasks available.")
        return

    display_tasks(tasks)

    try:
        idx = int(
            input("Enter task number to mark as completed: ")
        ) - 1

        tasks_sorted = sort_tasks(tasks)

        if 0 <= idx < len(tasks_sorted):

            if tasks_sorted[idx]["completed"]:
                print("Task is already completed.")
                return

            tasks_sorted[idx]["completed"] = True

            save_tasks(tasks)

            print("Task marked as completed!")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# =========================
# EDIT TASK
# =========================

def edit_task(tasks):
    if not tasks:
        print("No tasks available.")
        return

    display_tasks(tasks)

    try:
        idx = int(input("Enter task number to edit: ")) - 1

        tasks_sorted = sort_tasks(tasks)

        if 0 <= idx < len(tasks_sorted):

            task = tasks_sorted[idx]

            print("\nLeave empty to keep current value.")

            new_title = input("New title: ").strip()
            new_due = input("New due date (YYYY-MM-DD): ").strip()
            new_category = input("New category: ").strip()
            new_priority = input(
                "New priority (1=High, 2=Medium, 3=Low): "
            ).strip()

            if new_title:
                task["title"] = new_title

            if new_due:
                try:
                    datetime.strptime(new_due, "%Y-%m-%d")
                    task["due_date"] = new_due
                except ValueError:
                    print("Invalid date format. Keeping old date.")

            if new_category:
                task["category"] = new_category

            if new_priority:
                try:
                    new_priority = int(new_priority)

                    if new_priority in [1, 2, 3]:
                        task["priority"] = new_priority
                    else:
                        print("Invalid priority. Keeping old value.")

                except ValueError:
                    print("Invalid priority input.")

            save_tasks(tasks)

            print("Task updated successfully!")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# =========================
# SEARCH TASKS
# =========================

def search_tasks(tasks):
    keyword = input(
        "Enter keyword or category to search: "
    ).lower().strip()

    found_tasks = []

    for task in tasks:
        if (
            keyword in task["title"].lower()
            or keyword in task["category"].lower()
        ):
            found_tasks.append(task)

    if not found_tasks:
        print("\nNo matching tasks found.")
        return

    print("\nSEARCH RESULTS")
    print("=" * 50)

    for i, task in enumerate(found_tasks, start=1):
        display_single_task(i, task)


# =========================
# TASK STATISTICS
# =========================

def task_stats(tasks):
    total = len(tasks)

    completed = len(
        [task for task in tasks if task["completed"]]
    )

    pending = total - completed

    high = len(
        [task for task in tasks if task["priority"] == 1]
    )

    medium = len(
        [task for task in tasks if task["priority"] == 2]
    )

    low = len(
        [task for task in tasks if task["priority"] == 3]
    )

    overdue = 0
    today = datetime.now().strftime("%Y-%m-%d")

    for task in tasks:
        if (
            not task["completed"]
            and task["due_date"] != "9999-12-31"
            and task["due_date"] < today
        ):
            overdue += 1

    print("\nTASK STATISTICS")
    print("=" * 40)
    print(f"Total Tasks     : {total}")
    print(f"Completed Tasks : {completed}")
    print(f"Pending Tasks   : {pending}")
    print(f"Overdue Tasks   : {overdue}")
    print(f"High Priority   : {high}")
    print(f"Medium Priority : {medium}")
    print(f"Low Priority    : {low}")


# =========================
# CLEAR COMPLETED TASKS
# =========================

def clear_completed(tasks):
    completed_tasks = [task for task in tasks if task["completed"]]

    if not completed_tasks:
        print("No completed tasks to remove.")
        return

    confirm = input(
        "Delete all completed tasks? (y/n): "
    ).lower()

    if confirm == "y":
        tasks[:] = [
            task for task in tasks if not task["completed"]
        ]

        save_tasks(tasks)

        print("Completed tasks removed.")
    else:
        print("Operation cancelled.")


# =========================
# MAIN PROGRAM
# =========================

def main():
    tasks = load_tasks()

    while True:

        print("\n========== TO-DO LIST ==========")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Mark Task as Completed")
        print("5. Edit Task")
        print("6. Search Tasks")
        print("7. Task Statistics")
        print("8. Clear Completed Tasks")
        print("9. Exit")

        choice = input("\nChoose an option: ").strip()

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
            search_tasks(tasks)

        elif choice == "7":
            task_stats(tasks)

        elif choice == "8":
            clear_completed(tasks)

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()