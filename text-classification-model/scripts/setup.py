# scripts/setup.py

import os
import logging
from datasets import load_dataset

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_save_dataset():
    try:
        logging.info("Starting dataset download...")
        dataset = load_dataset('imdb')
        dataset.save_to_disk('data/imdb')
        logging.info("IMDB dataset downloaded and saved to 'data/imdb'.")
    except Exception as e:
        logging.error(f"Error downloading dataset: {e}")
        exit(1)

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data/imdb', exist_ok=True)
    
    # Download and save the dataset
    download_and_save_dataset()

if __name__ == "__main__":
    main()
