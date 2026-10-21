import json
import os
from datetime import datetime, date

DATA_FILE = "tasks.json"


# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Error reading tasks file.")
        return []


# Save tasks to the JSON file
def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


# Add a new task
def add_task(tasks):
    print("\n--- ADD NEW TASK ---")

    title = input("Enter task name: ").strip()

    if not title:
        print("Task name cannot be empty.")
        return

    description = input("Enter task description: ").strip()

    try:
        deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

        # Validate the date
        datetime.strptime(deadline, "%Y-%m-%d")

    except ValueError:
        print("Invalid date! Use YYYY-MM-DD, for example 2026-12-25.")
        return

    task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": title,
        "description": description,
        "deadline": deadline,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(task)
    save_tasks(tasks)

    print("\nTask added successfully!")


# Display tasks
def view_tasks(tasks, mode="all"):
    print("\n--- TASK LIST ---")

    if mode == "pending":
        selected = [task for task in tasks if not task["completed"]]
    else:
        selected = tasks

    if not selected:
        print("No tasks found.")
        return

    today = date.today()

    for task in selected:
        deadline = date.fromisoformat(task["deadline"])

        if task["completed"]:
            status = "COMPLETED"
        elif deadline < today:
            status = "OVERDUE"
        else:
            status = "PENDING"

        print("-" * 45)
        print(f"ID          : {task['id']}")
        print(f"Title       : {task['title']}")
        print(f"Description : {task['description']}")
        print(f"Deadline    : {task['deadline']}")
        print(f"Status      : {status}")

    print("-" * 45)


# Mark a task as completed
def complete_task(tasks):
    view_tasks(tasks, "pending")

    pending = [task for task in tasks if not task["completed"]]

    if not pending:
        return

    try:
        task_id = int(input("Enter task ID to complete: "))

    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id and not task["completed"]:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed!")
            return

    print("Pending task ID not found.")


# Delete a task
def delete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("Enter task ID to delete: "))

    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted successfully!")
            return

    print("Task ID not found.")


# Display overdue tasks
def show_overdue_tasks(tasks):
    today = date.today()

    overdue = [
        task for task in tasks
        if not task["completed"]
        and date.fromisoformat(task["deadline"]) < today
    ]

    print("\n--- OVERDUE TASKS ---")

    if not overdue:
        print("Great! You have no overdue tasks.")
        return

    for task in overdue:
        print(
            f"ID: {task['id']} | "
            f"Task: {task['title']} | "
            f"Deadline: {task['deadline']}"
        )


# Main program
def main():
    tasks = load_tasks()

    while True:
        print("\n====== STUDENT TASK MANAGER ======")
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. View Overdue Tasks")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks, "pending")

        elif choice == "4":
            complete_task(tasks)

        elif choice == "5":
            delete_task(tasks)

        elif choice == "6":
            show_overdue_tasks(tasks)

        elif choice == "7":
            print("\nThank you for using Student Task Manager!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()