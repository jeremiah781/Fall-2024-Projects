# download_dataset.py

from datasets import load_dataset

# Load the IMDB dataset
dataset = load_dataset('imdb')

# Save the dataset to disk
dataset.save_to_disk('data/imdb')

print("Dataset downloaded and saved successfully.")

