
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "expense-tracker-local-secret"

DATABASE = "expenses.db"


# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE DATABASE
def setup_database():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                transaction_date TEXT NOT NULL
            )
        """)


# HOME DASHBOARD
@app.route("/")
def home():
    with get_db() as conn:

        income = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Income'
        """).fetchone()[0]

        expenses = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
        """).fetchone()[0]

        transactions = conn.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """).fetchall()

    balance = income - expenses

    return render_template(
        "index.html",
        income=income,
        expenses=expenses,
        balance=balance,
        transactions=transactions,
        today=date.today().isoformat()
    )


# ADD TRANSACTION
@app.route("/add", methods=["POST"])
def add_transaction():

    title = request.form.get("title", "").strip()
    amount_text = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()
    transaction_type = request.form.get("transaction_type", "")
    transaction_date = request.form.get("transaction_date", "")

    if not title or not category:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("home"))

    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Please enter a valid positive amount.", "error")
        return redirect(url_for("home"))

    if transaction_type not in ["Income", "Expense"]:
        flash("Please select a valid transaction type.", "error")
        return redirect(url_for("home"))

    try:
        date.fromisoformat(transaction_date)
    except ValueError:
        flash("Please select a valid date.", "error")
        return redirect(url_for("home"))

    with get_db() as conn:
        conn.execute("""
            INSERT INTO transactions
            (title, amount, category, transaction_type, transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            amount,
            category,
            transaction_type,
            transaction_date
        ))

    flash("Transaction added successfully!", "success")
    return redirect(url_for("home"))


# DELETE TRANSACTION
@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):

    with get_db() as conn:
        conn.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

    flash("Transaction deleted successfully!", "success")
    return redirect(url_for("home"))


# START WEBSITE
if __name__ == "__main__":
    setup_database()

    print("\nSmart Expense Tracker is starting...")
    print("Open http://127.0.0.1:5000 in your browser")

    app.run(host="127.0.0.1", port=5000, debug=True)
