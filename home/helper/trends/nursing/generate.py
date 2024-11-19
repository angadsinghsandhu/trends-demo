"""
FILE DESCRIPTION: generate.py

This script generates trend data for nursing home inspection reports by computing similarity scores
between a base term and a set of related terms across multiple Word2Vec models. Each model represents
a different time period (e.g., 'jan23') and is dynamically loaded from the 'models/' directory.

The trends are derived based on cosine similarity scores, providing insights into how related terms
vary in relation to the base term across different time periods.

Optimizations:

- Processes models in parallel using multiprocessing to improve speed.
- Utilizes Gensim's built-in `similarity` method for efficient computation.
- Checks for word existence in the vocabulary before attempting similarity computation.
- Manages memory usage by controlling the number of worker processes.

"""

# Imports
import os
from typing import List, Tuple, Dict
from gensim.models import Word2Vec
from multiprocessing import Pool, cpu_count
from scipy.spatial import distance

BASE_DIR = "./home/helper/trends/nursing/"
MODELS_DIR = os.path.join(BASE_DIR, "models/")

# Define a dictionary to map month abbreviations to numbers for sorting
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def process_model(args) -> Tuple[str, Dict[str, float]]:
    """
    Processes a single model file to compute similarity scores between the base term
    and related terms.

    Parameters:
    - args (Tuple): A tuple containing:
        - model_file (str): The filename of the model to process.
        - base_term (str): The base word to calculate similarity against.
        - rel_terms (List[str]): A list of related terms.

    Returns:
    - model_label (str): The label derived from the model filename.
    - scores (Dict[str, float]): A dictionary of similarity scores for each related term.
    """
    model_file, base_term, rel_terms = args
    model_label = os.path.splitext(model_file)[0]
    model_path = os.path.join(MODELS_DIR, model_file)

    # Load the model
    model = Word2Vec.load(model_path)

    scores = {}
    for rel in rel_terms:
        # looping through all models
        vals = []
        try:
            # vals.append(1-distance.cosine(model.wv[base_term], model.wv[rel]))
            cos_dist = distance.cosine(model.wv[base_term], model.wv[rel])
            norm_sim = 1 - (cos_dist / 2)
            scores[rel] = norm_sim
        except Exception as e:
            scores[rel] = -1.0
            print(f"Term '{base_term}' or '{rel}' not found in model. Error: {e}")

    # Delete the model to free memory
    del model

    return model_label, scores

def gen_nursing_trends(base_term: str, rel_terms: List[str]) -> Tuple[List[str], List[List[float]]]:
    """
    Generates trend data by calculating cosine similarity scores between a base term and multiple related terms
    across multiple Word2Vec models. Each model corresponds to a different time period, allowing trend analysis
    over time.

    Parameters:
    - base_term (str): The base word to calculate similarity against.
    - rel_terms (List[str]): A list of related terms for which cosine similarity scores will be calculated
      in relation to the base term.

    Returns:
    - labels (List[str]): List of time period labels derived from the model filenames (e.g., 'jan23').
    - values (List[List[float]]): A 2D list where each inner list contains similarity scores for one related term
      across all models (time periods).

    Notes:
    - If a term is missing in any model, a default similarity score of -1.0 is assigned for that model.
    """
    # Dynamically load model files from the models directory
    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".model")]

    # Prepare arguments for multiprocessing
    args = [(model_file, base_term, rel_terms) for model_file in model_files]

    # Determine the number of worker processes (adjust as needed)
    num_workers = min(cpu_count(), len(model_files))

    # Initialize the multiprocessing pool
    with Pool(processes=num_workers) as pool:
        # Map the processing function to the model files
        results = pool.map(process_model, args)

    # Sort results by labels to maintain consistent ordering

    # # TODO: NEW 
    # results = [row for row in results if row[0][:2].isdigit()]

    results.sort(key=lambda x: (int(x[0][:2]), MONTHS[x[0][2:5].lower()]))

    labels = []
    # Initialize values: a list for each related term
    values_dict = {rel: [] for rel in rel_terms}

    for model_label, scores in results:
        labels.append(f"{model_label[2:5]}{model_label[:2]}-{model_label[8:11]}{model_label[6:8]}")
        for rel in rel_terms:
            values_dict[rel].append(scores[rel])

    # Convert values_dict to a list of lists
    values = [values_dict[rel] for rel in rel_terms]

    return labels, values
