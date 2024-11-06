"""
FILE DESCRIPTION: clean.py

This script contains functions to clean and preprocess the nursing home inspection data.
"""

# sample useage
# python clean.py data/legacy/01_24_modified_data_clip.csv -o data

import pandas as pd
import os
import argparse

def get_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Split a large CSV file by month and year.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument(
        "-o", "--output_folder", type=str, default="output_files",
        help="Folder to save the split files. Defaults to 'output_files'."
    )

    return parser.parse_args()

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY", ""))
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("**** ", ""))
    df["inspection_text"] = df["inspection_text"].str.replace(r'^\d{5}', '', regex=True)
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("<BR/>", ""))
    return df

def split_csv_by_month_year(input_file, output_folder="data"):
    """
    Splits a large CSV file by month and year in the 'inspection_date' column, saving
    each subset as a separate CSV file in the format 'monYY.csv' (e.g., 'jan23.csv').

    Parameters:
    - input_file (str): Path to the large CSV file.
    - output_folder (str): Folder to save the split files. Defaults to "data/".
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read the CSV into a DataFrame
    df = pd.read_csv(input_file)

    # Convert 'inspection_date' to datetime format for easy grouping by month and year
    df['inspection_date'] = pd.to_datetime(df['inspection_date'], format='%m/%d/%Y')

    # clean data
    df = clean(df)

    # Group by year and month, then save each group as a separate CSV
    for (year, month), group in df.groupby([df['inspection_date'].dt.year, df['inspection_date'].dt.month]):
        # Generate the file name in the required format, e.g., "jan23.csv", "feb23.csv", etc.
        file_name = f"{output_folder}/{pd.to_datetime(f'{year}-{month}-01').strftime('%b').lower()}{str(year)[-2:]}.csv"
        
        # Save the group to a CSV file
        group.to_csv(file_name, index=False)
        print(f"Saved {file_name}")

def split_csv_by_time(input_file, output_folder="data", num_files=12):
    """
    Splits a large CSV file into a specified number of files, saving each subset as a separate CSV file.
    Each file will contain approximately equal amounts of text data.
    The files are saved as "17jan-17sep.csv", "18dec-19may.csv", etc., where the names represent the
    start and end months and years of the data in each file.

    Parameters:
    - input_file (str): Path to the large CSV file.
    - output_folder (str): Folder to save the split files. Defaults to "data/".
    - num_files (int): Number of files to split the data into.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read the CSV into a DataFrame
    df = pd.read_csv(input_file)

    # Convert 'inspection_date' to datetime format for sorting
    df['inspection_date'] = pd.to_datetime(df['inspection_date'], format='%m/%d/%Y')

    # Sort by 'inspection_date'
    df = df.sort_values('inspection_date').reset_index(drop=True)

    # Clean data
    df = clean(df)

    # Calculate word counts
    df['word_count'] = df['inspection_text'].str.split().str.len()

    # Calculate cumulative sum of word counts
    df['cum_word_count'] = df['word_count'].cumsum()

    # Calculate total words
    total_words = df['word_count'].sum()

    # Calculate words per file
    words_per_file = total_words // num_files

    # Initialize breakpoints
    break_points = [0]
    for n in range(1, num_files):
        target = words_per_file * n
        # Find the index where cumulative word count >= target
        idx = df[df['cum_word_count'] >= target].index[0]
        break_points.append(idx)
    # Ensure the last breakpoint is the end of the DataFrame
    break_points.append(len(df))

    # Split the DataFrame and save each part
    for i in range(len(break_points) - 1):
        start_idx = break_points[i]
        end_idx = break_points[i + 1]
        df_chunk = df.iloc[start_idx:end_idx]

        # Get start and end dates
        start_date = df_chunk['inspection_date'].iloc[0]
        end_date = df_chunk['inspection_date'].iloc[-1]

        # Format file name
        start_month = start_date.strftime('%b').lower()
        start_year = start_date.strftime('%y')
        end_month = end_date.strftime('%b').lower()
        end_year = end_date.strftime('%y')

        file_name = f"{output_folder}/{start_year}{start_month}-{end_year}{end_month}.csv"

        # Save the chunk to CSV
        df_chunk.drop(columns=['word_count', 'cum_word_count']).to_csv(file_name, index=False)
        print(f"Saved {file_name} with {df_chunk['word_count'].sum()} words")
    
if __name__ == "__main__":
    # Parse arguments
    args = get_args()

    # # Run the split function with parsed arguments
    # split_csv_by_month_year(args.input_file, args.output_folder)

    # Run the split function with parsed arguments
    split_csv_by_time(args.input_file, args.output_folder, num_files=12)
    
