import os
import pandas as pd

# Define the folder where domain files are stored and output folder
domain_folder = "domain"
output_folder = "domains"

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Function to transform the format of each domain file
def transform_domain_format(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Initialize an empty list to hold the reshaped rows
    reshaped_rows = []

    # Start with an empty list for each UniProt ID block
    current_uniprot_id = None
    current_block = []

    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        if pd.notna(row['uniprot id']):  # If a new UniProt ID is found
            # If we have accumulated data for a previous UniProt ID, process it
            if current_uniprot_id is not None:
                reshaped_rows.append(current_block)

            # Start a new block for the new UniProt ID
            current_uniprot_id = row['uniprot id']
            current_block = [row[['uniprot id', 'begin', 'end', 'amino acid sequence', 'iupred long score', 'iupred short score']].tolist()]
        else:
            # Add the current row to the current block (where the UniProt ID is not present)
            current_block.append([None, None, None] + row[['amino acid sequence', 'iupred long score', 'iupred short score']].tolist())

    # Add the last block to the reshaped_rows
    if current_block:
        reshaped_rows.append(current_block)

    # Create a DataFrame for reshaped data
    reshaped_df = pd.DataFrame()

    # Flatten the reshaped_rows into columns for each UniProt ID
    for i, block in enumerate(reshaped_rows):
        block_df = pd.DataFrame(block, columns=['UniProt ID', 'Begin', 'End', 'Amino Acid Sequence', 'IUPred Long Score', 'IUPred Short Score'])

        # Rename columns to avoid duplication
        block_df.columns = [f'{col} {i+1}' for col in block_df.columns]

        # Concatenate the block to the reshaped_df
        if reshaped_df.empty:
            reshaped_df = block_df
        else:
            reshaped_df = pd.concat([reshaped_df, block_df], axis=1)

    # Write the reshaped DataFrame to an Excel file
    reshaped_df.to_excel(output_file, index=False)

# Step 1: Loop through all domain files in the domain folder
for file_name in os.listdir(domain_folder):
    if file_name.endswith('.xlsx'):
        input_file_path = os.path.join(domain_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)
        
        # Transform and save the file
        transform_domain_format(input_file_path, output_file_path)
        print(f"Transformed {file_name} and saved to {output_file_path}")
