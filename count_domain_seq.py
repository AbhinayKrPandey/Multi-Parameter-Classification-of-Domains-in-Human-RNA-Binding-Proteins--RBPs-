import os
import pandas as pd
import re

def count_domain_sequences(domain_folder):
    total_count = 0

    # Loop through all files in the folder
    for filename in os.listdir(domain_folder):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(domain_folder, filename)
            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Find columns matching the pattern 'Amino Acid Sequence 1', 'Amino Acid Sequence 2', etc.
                sequence_columns = [col for col in df.columns if re.match(r'^Amino Acid Sequence \d+$', col)]

                # Count non-empty rows in these columns
                for col in sequence_columns:
                    count = df[col].dropna().shape[0]
                    total_count += count

                print(f"Processed {filename}: Found {len(sequence_columns)} columns, {count} sequences in this file.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"Total count of domain sequences: {total_count}")
    return total_count

# Replace with the path to your 'domains' folder
domain_folder = r"C:\Users\91630\Desktop\BTP\domains"

# Call the function to calculate the count of domain sequences
count_domain_sequences(domain_folder)
