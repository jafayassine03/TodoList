import json

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

def main():
    tasks = load_tasks()
    while True:
        print("\n1. View Tasks\n2. Add Task\n3. Delete Task\n4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            if not tasks:
                print("No tasks yet.")
            else:
                for i, t in enumerate(tasks, 1):
                    print(f"{i}. {t}")
        elif choice == "2":
            task = input("Task name: ")
            tasks.append(task)
            save_tasks(tasks)
        elif choice == "3":
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t}")
            idx = int(input("Delete task number: ")) - 1
            if 0 <= idx < len(tasks):
                tasks.pop(idx)
                save_tasks(tasks)
                print("Deleted!")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
