import json
import os
import secrets
import string
import getpass
import hashlib
import hmac

DATA_FILE = "passwords.json"
MASTER_FILE = "master.hash"


# Create a hash of the master password
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )


# Set up the master password on first run
def setup_master_password():
    print("\n--- CREATE MASTER PASSWORD ---")

    while True:
        password = getpass.getpass("Create a master password: ")

        if len(password) < 8:
            print("Use at least 8 characters.")
            continue

        confirm = getpass.getpass("Confirm master password: ")

        if password != confirm:
            print("Passwords do not match. Try again.")
            continue

        salt = os.urandom(16)
        password_hash = hash_password(password, salt)

        with open(MASTER_FILE, "w", encoding="utf-8") as file:
            json.dump({
                "salt": salt.hex(),
                "hash": password_hash.hex()
            }, file)

        print("Master password created.")
        return True


# Verify the master password
def authenticate():
    if not os.path.exists(MASTER_FILE):
        return setup_master_password()

    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)

        salt = bytes.fromhex(saved["salt"])
        expected_hash = bytes.fromhex(saved["hash"])

        for attempt in range(3):
            password = getpass.getpass("Enter master password: ")
            actual_hash = hash_password(password, salt)

            if hmac.compare_digest(actual_hash, expected_hash):
                print("Login successful!")
                return True

            print("Incorrect password.")

        print("Too many failed attempts.")
        return False

    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        print("Could not read master password file.")
        return False


# Load account records
def load_accounts():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        print("Could not read account data.")
        return []


# Save account records
def save_accounts(accounts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


# Generate a random password
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    while True:
        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*" for c in password)
        ):
            return password


# Add an account
def add_account(accounts):
    print("\n--- ADD ACCOUNT ---")

    website = input("Website or app name: ").strip()
    username = input("Username or email: ").strip()

    if not website or not username:
        print("Website and username are required.")
        return

    choice = input("Generate a password? (y/n): ").strip().lower()

    if choice == "y":
        password = generate_password()
        print(f"Generated password: {password}")

    else:
        password = getpass.getpass("Enter a test password: ")

        if not password:
            print("Password cannot be empty.")
            return

    account = {
        "id": max((item["id"] for item in accounts), default=0) + 1,
        "website": website,
        "username": username,
        "password": password
    }

    accounts.append(account)
    save_accounts(accounts)

    print("Account saved successfully.")


# View account details
def view_accounts(accounts):
    print("\n--- SAVED ACCOUNTS ---")

    if not accounts:
        print("No accounts saved.")
        return

    for account in accounts:
        print("-" * 35)
        print(f"ID       : {account['id']}")
        print(f"Website  : {account['website']}")
        print(f"Username : {account['username']}")
        print("Password : [HIDDEN]")

    print("-" * 35)


# Search for an account
def search_account(accounts):
    query = input("Enter website or app name: ").strip().lower()

    matches = [
        account for account in accounts
        if query in account["website"].lower()
    ]

    if not matches:
        print("No matching accounts found.")
        return

    for account in matches:
        print(f"ID: {account['id']} | Website: {account['website']}")
        print(f"Username: {account['username']}")


# Reveal a password for a selected account
def reveal_password(accounts):
    try:
        account_id = int(input("Enter account ID: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    for account in accounts:
        if account["id"] == account_id:
            print(f"Website: {account['website']}")
            print(f"Username: {account['username']}")
            print(f"Password: {account['password']}")
            return

    print("Account not found.")


# Delete an account
def delete_account(accounts):
    view_accounts(accounts)

    if not accounts:
        return

    try:
        account_id = int(input("Enter account ID to delete: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    for account in accounts:
        if account["id"] == account_id:
            accounts.remove(account)
            save_accounts(accounts)
            print("Account deleted.")
            return

    print("Account not found.")


# Main application
def main():
    print("\n====== PERSONAL PASSWORD MANAGER ======")

    if not authenticate():
        return

    accounts = load_accounts()

    while True:
        print("\n1. Add Account")
        print("2. View Saved Accounts")
        print("3. Search Account")
        print("4. Reveal Password")
        print("5. Delete Account")
        print("6. Generate Password")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_account(accounts)

        elif choice == "2":
            view_accounts(accounts)

        elif choice == "3":
            search_account(accounts)

        elif choice == "4":
            reveal_password(accounts)

        elif choice == "5":
            delete_account(accounts)

        elif choice == "6":
            try:
                length = int(input("Password length (minimum 12): "))

                if not 12 <= length <= 128:
                    print("Choose a length between 12 and 128.")
                    continue

                print("Generated password:", generate_password(length))

            except ValueError:
                print("Enter a valid whole number.")

        elif choice == "7":
            print("Password Manager closed.")
            break

        else:
            print("Invalid choice. Select 1-7.")


if __name__ == "__main__":
    main()