"""
FILE DESCRIPTION: create.py

This script processes nursing home inspection data from CSV files, creates Word2Vec models,
and identifies common words across models. It saves each model with a timestamp-based label
and stores common terms across all models in a JSON file for later reference.

The script is designed to read data from 'data/' and save models in 'models/' within the
BASE_DIR directory.
"""

# imports
import pandas as pd
import nltk
import os
import json
from gensim.models import Word2Vec
from collections import Counter
from home.helper.process import rem_stop_words
import re
import string
# from home.helper.transform import common_terms

# Base directory for data and models
BASE_DIR = "./home/helper/trends/nursing/"
DATA_DIR = BASE_DIR + "data/"
MODELS_DIR = BASE_DIR + "models/"

def common_terms(terms, threshold=0.8):

    # Flatten list of sets and count occurrences of each word
    word_counts = Counter(word for term_set in terms for word in term_set)
    
    # Calculate required minimum count based on threshold
    required_count = threshold * len(terms)
    
    # Filter words that meet the threshold
    common_words = {word for word, count in word_counts.items() if count >= required_count and not any(char in string.punctuation for char in word)}

    # return
    return list(common_words)

def create_common_words():
    """
    Loads all Word2Vec models from the MODELS_DIR, retrieves their vocabularies,
    and finds common terms across all models. Saves this data in a JSON file.
    
    Outputs:
    - Saves 'words.json' containing common terms across models to BASE_DIR.
    """
    # Dynamically get all model files in the MODELS_DIR
    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".model")]
    labels = [os.path.splitext(file)[0] for file in model_files]

    # Load each model and store it in a list
    models = [Word2Vec.load(os.path.join(MODELS_DIR, file)) for file in model_files]

    # Collect all terms from each model
    terms = [model.wv.index_to_key for model in models]
    
    # Creating a dictionary to save common words data
    words_data = {label: terms[idx] for idx, label in enumerate(labels)}
    words_data["common"] = common_terms(terms)

    # Save words data as JSON
    with open(BASE_DIR + 'words.json', 'w') as fp:
        json.dump(words_data, fp, indent=4)

def create_nursing():
    """
    Reads each CSV file in the 'data' directory, processes the data by removing stop words,
    tokenizes it, trains a Word2Vec model, and saves the model in the 'models' directory.
    
    Outputs:
    - Saves each trained Word2Vec model as '<label>.model' in MODELS_DIR.
    - Collects labels of processed files and passes them to create_common_words for common term extraction.
    """
    # Ensure the models directory exists
    os.makedirs(MODELS_DIR, exist_ok=True)

    labels = []
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".csv") and str(file_name) != "full.csv":
            label = file_name.split('.')[0]
            labels.append(label)

            # Read the CSV file
            df = pd.read_csv(os.path.join(DATA_DIR, file_name), encoding="utf-8")

            # Select and preprocess the 'text' column
            cleaned_text = [rem_stop_words(text) for text in df['text'].astype(str)]

            # Tokenize each text entry
            tokenized_text = [nltk.word_tokenize(text) for text in cleaned_text]

            # Create and train Word2Vec model
            model = Word2Vec(sentences=tokenized_text, vector_size=100, window=5, min_count=1, workers=4)
            
            # Save the model
            model.save(os.path.join(MODELS_DIR, f"{label}.model"))
            print(f"Model saved for {label} at {MODELS_DIR}{label}.model")

    # Generate and save common words data
    create_common_words()

