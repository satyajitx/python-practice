import json
import os

FILE_NAME = "contacts.json"


# Load contacts from the JSON file
def load_contacts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read contacts file.")
            return {}
    return {}


# Save contacts to the JSON file
def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save contacts.")
        return False


# Add a new contact
def add_contact(contacts):
    name = input("Enter name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    if name in contacts:
        print("Contact already exists!")
        return

    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        print("Invalid phone number! Enter 7-15 digits.")
        return

    contacts[name] = {
        "phone": phone,
        "email": email
    }

    if save_contacts(contacts):
        print("Contact added successfully!")


# View all contacts
def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("\n========== ALL CONTACTS ==========")

    for name, details in sorted(contacts.items()):
        print(f"\nName: {name}")
        print(f"Phone: {details['phone']}")
        print(f"Email: {details['email']}")
        print("----------------------------------")


# Search for a contact
def search_contact(contacts):
    name = input("Enter name to search: ").strip()

    if name in contacts:
        print("\nContact found!")
        print("Name:", name)
        print("Phone:", contacts[name]["phone"])
        print("Email:", contacts[name]["email"])
    else:
        print("Contact not found.")


# Update an existing contact
def update_contact(contacts):
    name = input("Enter the name to update: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    print("Leave a field blank to keep its current value.")

    phone = input("Enter new phone number: ").strip()
    email = input("Enter new email: ").strip()

    if phone:
        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            print("Invalid phone number!")
            return
        contacts[name]["phone"] = phone

    if email:
        contacts[name]["email"] = email

    if save_contacts(contacts):
        print("Contact updated successfully!")


# Delete a contact
def delete_contact(contacts):
    name = input("Enter the name to delete: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    confirm = input(
        f"Are you sure you want to delete {name}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        del contacts[name]

        if save_contacts(contacts):
            print("Contact deleted successfully!")
    else:
        print("Deletion cancelled.")


# Main program
def main():
    contacts = load_contacts()

    while True:
        print("\n=================================")
        print("    CONTACT BOOK MANAGEMENT")
        print("=================================")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            search_contact(contacts)

        elif choice == "4":
            update_contact(contacts)

        elif choice == "5":
            delete_contact(contacts)

        elif choice == "6":
            print("Thank you for using Contact Book!")
            break

        else:
            print("Invalid choice! Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()