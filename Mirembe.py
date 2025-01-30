# Name: Mirembe Ddumba
# E-mail Address: mnd5365@psu.edu
# Class: CMPSC 101
# Due Date: Friday, January 31, 2025 (1:25 p.m.)
# Brief Project Description:
# This program calculates how many slices a pizza can be divided into
# based on its diameter and the area of each slice.

def calculate_slices(diameter):
    # Define the value of pi as specified in the assignment
    pi = 3.14159

    # Calculate the radius by dividing the diameter by 2
    radius = diameter / 2

    # Calculate the area of the pizza using the formula pi * r^2
    area = pi * (radius ** 2)

    # Define the area of one slice (14.125 square inches per slice)
    slice_area = 14.125

    # The program divides the total pizza area by the slice area
    number_of_slices = area / slice_area

    # Round the result to two decimal places
    number_of_slices = round(number_of_slices, 2)

    return number_of_slices

def main():
    # Test cases to simulate user input
    test_cases = [16.0, 12.0, 8.0, 24.0]

    for diameter in test_cases:
        slices = calculate_slices(diameter)
        print(f"A {diameter:.2f}-inch pizza contains about {slices:.2f} slices.")

if __name__ == "__main__":
    main()
