# scripts/preprocess.py

import os
import logging
import pandas as pd
import spacy
from sklearn.utils import resample
from datasets import load_from_disk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    import re
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = text.lower()
    return text

def extract_entities(text, nlp):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def preprocess_dataset():
    try:
        logging.info("Loading dataset from disk...")
        dataset = load_from_disk('data/imdb')
        
        # Convert to DataFrame
        train_df = pd.DataFrame(dataset['train'])
        test_df = pd.DataFrame(dataset['test'])
        
        # Initialize SpaCy
        nlp = spacy.load('en_core_web_sm')
        
        # Clean text
        logging.info("Cleaning text data...")
        train_df['cleaned_text'] = train_df['text'].apply(clean_text)
        test_df['cleaned_text'] = test_df['text'].apply(clean_text)
        
        # Extract entities
        logging.info("Extracting named entities...")
        train_df['entities'] = train_df['cleaned_text'].apply(lambda x: extract_entities(x, nlp))
        test_df['entities'] = test_df['cleaned_text'].apply(lambda x: extract_entities(x, nlp))
        
        # Handle class imbalance by upsampling minority class
        logging.info("Handling class imbalance...")
        df_majority = train_df[train_df.label == 0]
        df_minority = train_df[train_df.label == 1]
        df_minority_upsampled = resample(df_minority,
                                         replace=True,
                                         n_samples=len(df_majority),
                                         random_state=42)
        train_df_upsampled = pd.concat([df_majority, df_minority_upsampled])
        logging.info(f"Training data class distribution after upsampling:\n{train_df_upsampled['label'].value_counts()}")
        
        # Save preprocessed data
        logging.info("Saving preprocessed data to CSV files...")
        os.makedirs('data', exist_ok=True)
        train_df_upsampled.to_csv('data/train.csv', index=False)
        test_df.to_csv('data/test.csv', index=False)
        
        logging.info("Data preprocessing completed successfully.")
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        exit(1)

def main():
    preprocess_dataset()

if __name__ == "__main__":
    main()
