"""
Program Name: Palindrome Generator
Author: [Jeremiah Ddumba]
Email: [jsd5521@psu.edu]
Purpose: Generate palindromes based on user input criteria including string length specific characters numeric-only options and word-based phrases
Compiler: Python 3.12
"""

import random
import string

# Predefined list of words for generating word-based palindromes
WORD_LIST = [
    "level", "radar", "madam", "refer", "deed", "civic", "kayak", "reviver",
    "racecar", "rotator", "repaper", "stats", "tenet", "wow", "noon", "peep",
    "solos", "malayalam", "redder", "minim", "murdrum", "kayak", "wow",
    "pop", "pip", "pipip"
]

def is_palindrome(s):
    """
    Checks if a given string is a palindrome
    A palindrome reads the same forwards and backwards
    """
    return s == s[::-1]

def generate_palindrome(length=5, include_chars=None, numeric_only=False):
    """
    Generates a random character-based palindrome based on the specified parameters

    Parameters:
        length (int): The total length of the palindrome Must be >= 2
        include_chars (str): Specific characters to include in the palindrome
        numeric_only (bool): If True generate a numeric palindrome

    Returns:
        str: A generated palindrome
    """
    # Validate the length input
    if length < 2:
        raise ValueError("Palindrome length must be at least 2")

    # Decide on the character set
    if numeric_only:
        char_set = string.digits
    else:
        char_set = string.ascii_letters + string.digits

    # If specific characters are provided prioritize them
    if include_chars:
        char_set = ''.join(set(char_set) & set(include_chars))

        # If no valid characters remain after filtering throw an error
        if not char_set:
            raise ValueError("No valid characters left to generate the palindrome")

    # Generate the first half or more for odd lengths
    half_length = (length + 1) // 2
    first_half = ''.join(random.choices(char_set, k=half_length))

    # Mirror the first half to create the second half
    if length % 2 == 0:
        palindrome = first_half + first_half[::-1]
    else:
        palindrome = first_half + first_half[-2::-1]

    return palindrome

def generate_palindromes_batch(count=10, length=5, **kwargs):
    """
    Generates a batch of random character-based palindromes

    Parameters:
        count (int): Number of palindromes to generate
        length (int): Length of each palindrome
        **kwargs: Additional parameters for generate_palindrome

    Returns:
        list: A list of generated palindromes
    """
    return [generate_palindrome(length=length, **kwargs) for _ in range(count)]

def generate_word_palindrome(word_count=3):
    """
    Generates a word-based palindrome with the specified number of words

    Parameters:
        word_count (int): Total number of words in the palindrome Must be >= 1

    Returns:
        str: A generated word-based palindrome
    """
    if word_count < 1:
        raise ValueError("Word count must be at least 1")

    if word_count == 1:
        return random.choice(WORD_LIST)

    # Determine the number of unique words needed
    half_count = word_count // 2
    is_odd = word_count % 2 != 0

    # Select random words for the first half
    first_half = [random.choice(WORD_LIST) for _ in range(half_count)]

    # If odd number of words, add a central word
    if is_odd:
        middle_word = random.choice(WORD_LIST)
    else:
        middle_word = []

    # Mirror the first half to create the second half
    second_half = first_half[::-1]

    # Combine all parts to form the palindrome
    if is_odd:
        palindrome = first_half + [middle_word] + second_half
    else:
        palindrome = first_half + second_half

    return ' '.join(palindrome)

def generate_word_palindromes_batch(count=10, word_count=3):
    """
    Generates a batch of random word-based palindromes

    Parameters:
        count (int): Number of palindromes to generate
        word_count (int): Number of words in each palindrome

    Returns:
        list: A list of generated word-based palindromes
    """
    return [generate_word_palindrome(word_count=word_count) for _ in range(count)]

def get_valid_integer(prompt, min_value=2):
    """
    Prompts the user for an integer input with validation

    Parameters:
        prompt (str): The input prompt message
        min_value (int): The minimum acceptable value

    Returns:
        int: A valid integer input from the user
    """
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer")

def get_yes_no(prompt):
    """
    Prompts the user for a yes/no input

    Parameters:
        prompt (str): The input prompt message

    Returns:
        bool: True if user inputs 'y', False otherwise
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no")

def get_mode_selection():
    """
    Prompts the user to select the palindrome generation mode

    Returns:
        str: The selected mode ('char' or 'word')
    """
    while True:
        mode = input("Select palindrome type - Character-based (c) or Word-based (w): ").strip().lower()
        if mode in ['c', 'character', 'char']:
            return 'char'
        elif mode in ['w', 'word']:
            return 'word'
        else:
            print("Invalid selection. Please enter 'c' for character-based or 'w' for word-based")

def main():
    """
    Main function to interact with the user and generate palindromes based on their input
    """
    print("Welcome to the Advanced Palindrome Generator!")
    print("Create customized palindromes with your own criteria\n")

    # Select mode
    mode = get_mode_selection()

    if mode == 'char':
        # Character-based palindrome options
        length = get_valid_integer("Enter the desired length of the palindrome (min 2): ")
        numeric_only = get_yes_no("Generate numeric-only palindromes? (y/n): ")
        include_chars = input("Enter specific characters to include (leave blank for default): ").strip()

        # Generate a batch of palindromes
        count = get_valid_integer("How many palindromes would you like to generate? ", min_value=1)
        palindromes = generate_palindromes_batch(
            count=count,
            length=length,
            include_chars=include_chars if include_chars else None,
            numeric_only=numeric_only
        )

    else:
        # Word-based palindrome options
        word_count = get_valid_integer("Enter the number of words in the palindrome (min 1): ", min_value=1)

        # Generate a batch of word-based palindromes
        count = get_valid_integer("How many word-based palindromes would you like to generate? ", min_value=1)
        palindromes = generate_word_palindromes_batch(
            count=count,
            word_count=word_count
        )

    # Display the results
    print("\nGenerated Palindromes:")
    for i, palindrome in enumerate(palindromes, 1):
        print(f"{i}: {palindrome}")

if __name__ == "__main__":
    main()
