import json
import os

FILE_NAME = "expenses.json"


def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    category = input("Enter expense category: ")
    amount = float(input("Enter amount (₹): "))
    description = input("Enter description: ")

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    expense = {
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- ALL EXPENSES ---")

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['category']} | "
            f"₹{expense['amount']:.2f} | "
            f"{expense['description']}"
        )


def show_total(expenses):
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses: ₹{total:.2f}")


def search_category(expenses):
    category = input("Enter category to search: ").strip().lower()

    results = [
        expense for expense in expenses
        if expense["category"].lower() == category
    ]

    if not results:
        print("No expenses found in this category.")
        return

    print(f"\nExpenses in {category.title()}:")

    for expense in results:
        print(
            f"₹{expense['amount']:.2f} - "
            f"{expense['description']}"
        )


def main():
    expenses = load_expenses()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expenses")
        print("4. Search by Category")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            search_category(expenses)
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()