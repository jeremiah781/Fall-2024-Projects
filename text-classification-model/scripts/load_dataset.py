# scripts/load_dataset.py

from datasets import load_from_disk

# Load the IMDB dataset from the saved disk
dataset = load_from_disk('data/imdb')

# Print the dataset information
print(dataset)
