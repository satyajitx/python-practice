import json
import os

DATA_FILE = "inventory.json"
LOW_STOCK_LIMIT = 5


# Load products from the JSON file
def load_products():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Error reading inventory file.")
        return []


# Save products to the JSON file
def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)


# Find a product by its ID
def find_product(products, product_id):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


# Add a new product
def add_product(products):
    print("\n--- ADD NEW PRODUCT ---")

    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter price in Rs: "))
        quantity = int(input("Enter quantity: "))

        if price <= 0 or quantity < 0:
            print("Price must be positive and quantity cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Enter a valid price and whole-number quantity.")
        return

    product = {
        "id": max((item["id"] for item in products), default=0) + 1,
        "name": name,
        "price": round(price, 2),
        "quantity": quantity
    }

    products.append(product)
    save_products(products)

    print("Product added successfully!")


# Display all products
def view_products(products):
    print("\n--- INVENTORY ---")

    if not products:
        print("No products found.")
        return

    print("-" * 65)
    print(f"{'ID':<6}{'Product':<22}{'Price (Rs)':<16}{'Quantity':<10}")
    print("-" * 65)

    for product in products:
        print(
            f"{product['id']:<6}"
            f"{product['name'][:21]:<22}"
            f"{product['price']:<16.2f}"
            f"{product['quantity']:<10}"
        )

    print("-" * 65)


# Search for a product
def search_product(products):
    search_name = input("Enter product name to search: ").strip().lower()

    matches = [
        product for product in products
        if search_name in product["name"].lower()
    ]

    if not matches:
        print("No matching products found.")
        return

    print("\n--- SEARCH RESULTS ---")

    for product in matches:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: Rs {product['price']:.2f} | "
            f"Quantity: {product['quantity']}"
        )


# Update stock quantity
def update_stock(products):
    view_products(products)

    if not products:
        return

    try:
        product_id = int(input("Enter product ID: "))
        new_quantity = int(input("Enter new total quantity: "))

        if new_quantity < 0:
            print("Quantity cannot be negative.")
            return

    except ValueError:
        print("Please enter valid whole numbers.")
        return

    product = find_product(products, product_id)

    if product is None:
        print("Product ID not found.")
        return

    product["quantity"] = new_quantity
    save_products(products)

    print("Stock updated successfully!")


# Sell a product
def sell_product(products):
    view_products(products)

    if not products:
        return

    try:
        product_id = int(input("Enter product ID to sell: "))
        quantity_sold = int(input("Enter quantity to sell: "))

        if quantity_sold <= 0:
            print("Quantity sold must be greater than zero.")
            return

    except ValueError:
        print("Please enter valid whole numbers.")
        return

    product = find_product(products, product_id)

    if product is None:
        print("Product ID not found.")
        return

    if quantity_sold > product["quantity"]:
        print("Not enough stock available!")
        return

    product["quantity"] -= quantity_sold

    revenue = product["price"] * quantity_sold

    save_products(products)

    print("\nSale completed successfully!")
    print(f"Product: {product['name']}")
    print(f"Quantity sold: {quantity_sold}")
    print(f"Sale amount: Rs {revenue:.2f}")
    print(f"Remaining stock: {product['quantity']}")


# Calculate total inventory value
def inventory_value(products):
    total = sum(
        product["price"] * product["quantity"]
        for product in products
    )

    print(f"\nTotal inventory value: Rs {total:.2f}")


# Show products with low stock
def low_stock_report(products):
    low_stock = [
        product for product in products
        if product["quantity"] <= LOW_STOCK_LIMIT
    ]

    print("\n--- LOW STOCK REPORT ---")

    if not low_stock:
        print("No products are running low.")
        return

    for product in low_stock:
        print(
            f"{product['name']} | "
            f"Remaining quantity: {product['quantity']}"
        )


# Main application
def main():
    products = load_products()

    while True:
        print("\n====== INVENTORY MANAGEMENT SYSTEM ======")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Update Stock")
        print("5. Sell Product")
        print("6. Calculate Inventory Value")
        print("7. Low Stock Report")
        print("8. Exit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            add_product(products)

        elif choice == "2":
            view_products(products)

        elif choice == "3":
            search_product(products)

        elif choice == "4":
            update_stock(products)

        elif choice == "5":
            sell_product(products)

        elif choice == "6":
            inventory_value(products)

        elif choice == "7":
            low_stock_report(products)

        elif choice == "8":
            print("Thank you for using Inventory Management System!")
            break

        else:
            print("Invalid choice. Select a number from 1 to 8.")


if __name__ == "__main__":
    main()
