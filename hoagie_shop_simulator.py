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
"""

# Constants
SALES_TAX_RATE = 0.06

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

    order_total = 0.0

    while True:
        display_hoagie_menu()
        try:
            hoagie_choice = int(input("Please select a hoagie (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if hoagie_choice == 1:
            order_total += 6.00
            print("You selected Italian Hoagie.")
        elif hoagie_choice == 2:
            order_total += 7.50
            print("You selected Cheese Steak Hoagie.")
        elif hoagie_choice == 3:
            order_total += 5.50
            print("You selected Veggie Hoagie.")
        elif hoagie_choice == 4:
            order_total += 6.50
            print("You selected Chicken Hoagie.")
        elif hoagie_choice == 5:
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")
            continue

        # Display toppings menu
        while True:
            display_toppings_menu()
            try:
                topping_choice = int(input("Please select a topping (1-6): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
                continue

            if topping_choice == 1:
                order_total += 0.50
                print("Added Lettuce.")
            elif topping_choice == 2:
                order_total += 0.50
                print("Added Tomato.")
            elif topping_choice == 3:
                order_total += 0.25
                print("Added Onion.")
            elif topping_choice == 4:
                order_total += 0.25
                print("Added Pickles.")
            elif topping_choice == 5:
                order_total += 1.00
                print("Added Extra Cheese.")
            elif topping_choice == 6:
                break
            else:
                print("Invalid choice. Please select a valid option (1-6).")
                continue

            print(f"Current Order Total: {format_currency(order_total)}")

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

if __name__ == "__main__":
    main()
