import json
import os
from datetime import datetime

DATA_FILE = "budget_data.json"


def load_data():
    """Load saved transactions and budgets."""
    if not os.path.exists(DATA_FILE):
        return {"transactions": [], "budgets": {}}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid data format")

        if not isinstance(data.get("transactions"), list):
            raise ValueError("Invalid transaction data")

        if not isinstance(data.get("budgets"), dict):
            raise ValueError("Invalid budget data")

        return data

    except (OSError, json.JSONDecodeError, ValueError):
        print("Error reading budget data. Check the data file.")
        return {"transactions": [], "budgets": {}}


def save_data(data):
    """Save transactions and budgets."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_amount(prompt):
    """Get a valid positive monetary amount."""
    try:
        amount = float(input(prompt))

        if not 0 < amount < 1_000_000_000:
            print("Enter an amount greater than zero.")
            return None

        return round(amount, 2)

    except ValueError:
        print("Please enter a valid number.")
        return None


def add_transaction(data, transaction_type):
    """Record income or an expense."""
    print(f"\n--- ADD {transaction_type.upper()} ---")

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description are required.")
        return

    amount = get_amount("Enter amount in Rs: ")

    if amount is None:
        return

    transaction = {
        "id": max(
            (item.get("id", 0) for item in data["transactions"]),
            default=0
        ) + 1,
        "type": transaction_type,
        "category": category.title(),
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    data["transactions"].append(transaction)
    save_data(data)

    print(f"{transaction_type.title()} recorded successfully!")

    if transaction_type == "expense":
        check_budget(data, category.title())


def view_transactions(data):
    """Display all financial transactions."""
    transactions = data["transactions"]

    print("\n--- TRANSACTION HISTORY ---")

    if not transactions:
        print("No transactions recorded yet.")
        return

    for item in transactions:
        print(
            f"ID: {item['id']} | "
            f"Date: {item['date']} | "
            f"Type: {item['type'].title()} | "
            f"Category: {item['category']} | "
            f"Amount: Rs {item['amount']:.2f} | "
            f"Description: {item['description']}"
        )


def calculate_summary(data):
    """Calculate income, expenses, and balance."""
    transactions = data["transactions"]

    income = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "income"
    )

    expenses = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "expense"
    )

    print("\n--- FINANCIAL SUMMARY ---")
    print(f"Total Income:   Rs {income:.2f}")
    print(f"Total Expenses: Rs {expenses:.2f}")
    print(f"Remaining Balance: Rs {income - expenses:.2f}")

    if income > 0:
        savings_rate = ((income - expenses) / income) * 100
        print(f"Balance as percentage of income: {savings_rate:.1f}%")


def set_budget(data):
    """Set a spending limit for a category."""
    category = input("Enter budget category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    amount = get_amount("Enter budget limit in Rs: ")

    if amount is None:
        return

    data["budgets"][category.title()] = amount
    save_data(data)

    print(
        f"Budget set for {category.title()}: "
        f"Rs {amount:.2f}"
    )

    check_budget(data, category.title())


def check_budget(data, category):
    """Compare monthly spending with the category budget."""
    if category not in data["budgets"]:
        return

    current_month = datetime.now().strftime("%Y-%m")

    spent = sum(
        item["amount"]
        for item in data["transactions"]
        if item["type"] == "expense"
        and item["category"].lower() == category.lower()
        and item["date"].startswith(current_month)
    )

    limit = data["budgets"][category]

    print(f"Budget: Rs {limit:.2f}")
    print(f"Spent this month: Rs {spent:.2f}")
    print(f"Budget remaining: Rs {limit - spent:.2f}")

    if spent > limit:
        print("WARNING: You have exceeded your budget!")
    elif spent == limit:
        print("Warning: You have reached your budget limit.")
    elif spent >= limit * 0.8:
        print("Warning: You have used at least 80% of your budget.")


def view_budgets(data):
    """Display all budgets and current monthly spending."""
    print("\n--- BUDGET REPORT ---")

    if not data["budgets"]:
        print("No budgets set yet.")
        return

    for category, limit in data["budgets"].items():
        print(f"\nCategory: {category}")
        check_budget(data, category)


def main():
    data = load_data()

    while True:
        print("\n====== PERSONAL BUDGET PLANNER ======")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Financial Summary")
        print("5. Set Category Budget")
        print("6. View Budget Report")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            add_transaction(data, "income")

        elif choice == "2":
            add_transaction(data, "expense")

        elif choice == "3":
            view_transactions(data)

        elif choice == "4":
            calculate_summary(data)

        elif choice == "5":
            set_budget(data)

        elif choice == "6":
            view_budgets(data)

        elif choice == "7":
            print("Your budget data has been saved.")
            print("Thank you for using Budget Planner!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()