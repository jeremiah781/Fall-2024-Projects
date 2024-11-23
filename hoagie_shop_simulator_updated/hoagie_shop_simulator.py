"""
Program Name: Hoagie Shop Simulator
Author: [Jeremiah Ddumba]
Email: [jsd5521@psu.edu]
Assignment: Lab 8 - Hoagie Shop Simulator
Due Date: October 25, 2024
File Name: hoagie-shop-simulator.py
Program Purpose: Simulate a hoagie shop where customers can place orders, select toppings, and complete their purchase with tax and optional tips
Compiler: Python 3.12
Operating System: [MacOS Sanoma]
References:
- Python Documentation: https://docs.python.org/3/
- SQLite Documentation: https://docs.python.org/3/library/sqlite3.html
"""

import sqlite3
from datetime import datetime

# Constants
SALES_TAX_RATE = 0.06

# Inventory Initialization
inventory = {
    'Italian Hoagie': 20,
    'Cheese Steak Hoagie': 15,
    'Veggie Hoagie': 25,
    'Chicken Hoagie': 18,
    'Lettuce': 50,
    'Tomato': 50,
    'Onion': 40,
    'Pickles': 40,
    'Extra Cheese': 30
}

# Database Setup
def setup_database():
    """
    Sets up the SQLite database and creates necessary tables if they don't exist.
    """
    conn = sqlite3.connect('hoagie_shop.db')
    cursor = conn.cursor()

    # Create Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            subtotal REAL,
            tax REAL,
            tip REAL,
            total REAL,
            timestamp TEXT
        )
    ''')

    # Create Inventory Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            change INTEGER,
            timestamp TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def save_order(cursor, items, subtotal, tax, tip, total):
    """
    Saves the order details to the orders table.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items_str = ', '.join(items)
    cursor.execute('''
        INSERT INTO orders (items, subtotal, tax, tip, total, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (items_str, subtotal, tax, tip, total, timestamp))

def log_inventory_change(cursor, item, change):
    """
    Logs changes to the inventory in the inventory_logs table.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO inventory_logs (item, change, timestamp)
        VALUES (?, ?, ?)
    ''', (item, change, timestamp))

def generate_sales_report(cursor):
    """
    Generates and displays a sales report.
    """
    print("\nGenerating Sales Report...")
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()

    if not orders:
        print("No orders to report.")
        return

    total_sales = 0.0
    item_counts = {}

    for order in orders:
        items = order[1].split(', ')
        subtotal = order[2]
        tax = order[3]
        tip = order[4]
        total = order[5]
        total_sales += total

        for item in items:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

    print(f"Total Orders: {len(orders)}")
    print(f"Total Sales: {format_currency(total_sales)}")
    print("\nMost Popular Items:")
    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
    for item, count in sorted_items[:5]:
        print(f"{item}: {count} sold")

def check_inventory(item, quantity=1):
    """
    Checks if the requested item is available in the inventory.
    """
    return inventory.get(item, 0) >= quantity

def update_inventory(cursor, item, quantity=1):
    """
    Updates the inventory by reducing the quantity of the ordered item.
    Logs the inventory change.
    """
    if check_inventory(item, quantity):
        inventory[item] -= quantity
        log_inventory_change(cursor, item, -quantity)
        return True
    else:
        print(f"Sorry, {item} is out of stock!")
        return False

def display_hoagie_menu():
    """
    Displays the hoagie menu with options 1-4 and an option to exit.
    """
    print("\nHoagie Menu:")
    print("1. Italian Hoagie - $6.00")
    print("2. Cheese Steak Hoagie - $7.50")
    print("3. Veggie Hoagie - $5.50")
    print("4. Chicken Hoagie - $6.50")
    print("5. Exit and Complete Order")

def display_toppings_menu():
    """
    Displays the toppings menu with options 1-5 and their corresponding prices.
    """
    print("\nToppings Menu:")
    print("1. Lettuce - $0.50")
    print("2. Tomato - $0.50")
    print("3. Onion - $0.25")
    print("4. Pickles - $0.25")
    print("5. Extra Cheese - $1.00")
    print("6. No more toppings")

def format_currency(amount):
    """
    Formats a float amount as currency.
    """
    return "${:,.2f}".format(amount)

def main():
    """
    Main function to run the hoagie shop simulator.
    """
    print("Welcome to the Hoagie Shop!")

    # Setup database
    conn, cursor = setup_database()

    order_total = 0.0
    items_ordered = []

    while True:
        display_hoagie_menu()
        try:
            hoagie_choice = int(input("Please select a hoagie (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        hoagie = None
        hoagie_price = 0.0

        if hoagie_choice == 1:
            hoagie = "Italian Hoagie"
            hoagie_price = 6.00
        elif hoagie_choice == 2:
            hoagie = "Cheese Steak Hoagie"
            hoagie_price = 7.50
        elif hoagie_choice == 3:
            hoagie = "Veggie Hoagie"
            hoagie_price = 5.50
        elif hoagie_choice == 4:
            hoagie = "Chicken Hoagie"
            hoagie_price = 6.50
        elif hoagie_choice == 5:
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")
            continue

        # Check inventory for hoagie
        if not update_inventory(cursor, hoagie):
            continue

        order_total += hoagie_price
        items_ordered.append(hoagie)
        print(f"You selected {hoagie}.")

        # Display toppings menu
        while True:
            display_toppings_menu()
            try:
                topping_choice = int(input("Please select a topping (1-6): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
                continue

            topping = None
            topping_price = 0.0

            if topping_choice == 1:
                topping = "Lettuce"
                topping_price = 0.50
            elif topping_choice == 2:
                topping = "Tomato"
                topping_price = 0.50
            elif topping_choice == 3:
                topping = "Onion"
                topping_price = 0.25
            elif topping_choice == 4:
                topping = "Pickles"
                topping_price = 0.25
            elif topping_choice == 5:
                topping = "Extra Cheese"
                topping_price = 1.00
            elif topping_choice == 6:
                break
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

            # Check inventory for topping
            if not update_inventory(cursor, topping):
                continue

            order_total += topping_price
            items_ordered.append(topping)
            print(f"Added {topping}.")
            print(f"Current Order Total: {format_currency(order_total)}")

    if not items_ordered:
        print("No items ordered. Thank you!")
        conn.close()
        return

    # Calculate tax
    tax = order_total * SALES_TAX_RATE
    total_with_tax = order_total + tax
    print("\nOrder Summary:")
    print(f"Subtotal: {format_currency(order_total)}")
    print(f"Sales Tax (6%): {format_currency(tax)}")
    print(f"Total with Tax: {format_currency(total_with_tax)}")

    # Optional tip
    while True:
        try:
            tip_input = input("Enter tip amount (or press Enter to skip): $")
            if tip_input == "":
                tip = 0.0
                break
            else:
                tip = float(tip_input)
                if tip < 0:
                    print("Tip cannot be negative. Please enter a valid amount.")
                    continue
                break
        except ValueError:
            print("Invalid input. Please enter a numerical value for the tip.")

    total_due = total_with_tax + tip
    print(f"Tip: {format_currency(tip)}")
    print(f"Total Amount Due: {format_currency(total_due)}")
    print("Thank you for your order! Have a great day!")

    # Save order to database
    save_order(cursor, items_ordered, order_total, tax, tip, total_due)
    conn.commit()

    # Ask if the user wants to generate a sales report
    while True:
        report_choice = input("\nWould you like to generate a sales report? (y/n): ").strip().lower()
        if report_choice == 'y':
            generate_sales_report(cursor)
            break
        elif report_choice == 'n':
            break
        else:
            print("Please enter 'y' or 'n'.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
