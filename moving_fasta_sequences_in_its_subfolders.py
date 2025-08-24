import os
import shutil
import pandas as pd

# Load the Excel file and filter out rows with NA in 'RCSB PDB ids'
excel_file = 'RPC_complete.xlsx'
df = pd.read_excel(excel_file)
filtered_df = df[df['RCSB PDB ids'].notna()]

# Create the main folder 'Fasta_Sequences_Subfolders'
main_folder = 'Fasta_Sequences_Subfolders'
os.makedirs(main_folder, exist_ok=True)

# Folder paths for UniProt and PDB FASTA sequences
uniprot_fasta_folder = 'uniprot_fasta_sequences'
pdb_fasta_folder = 'fasta_sequences_pdb_ids'

# Iterate through each row in the filtered dataframe
for index, row in filtered_df.iterrows():
    uniprot_id = row['IDS']  # Get the UniProt ID
    pdb_ids = row['RCSB PDB ids'].split(';')  # Split PDB IDs by semicolon if there are multiple
    
    # Create a subfolder for the UniProt ID
    subfolder_path = os.path.join(main_folder, uniprot_id)
    os.makedirs(subfolder_path, exist_ok=True)
    
    # Move the UniProt FASTA sequence file to the subfolder
    uniprot_fasta_file = f"{uniprot_id}.fasta"
    uniprot_fasta_source = os.path.join(uniprot_fasta_folder, uniprot_fasta_file)
    if os.path.exists(uniprot_fasta_source):
        shutil.copy(uniprot_fasta_source, subfolder_path)
        print(f"Moved {uniprot_fasta_file} to {subfolder_path}")
    else:
        print(f"UniProt FASTA file {uniprot_fasta_file} not found!")
    
    # Move the corresponding PDB FASTA sequence files to the subfolder
    for pdb_id in pdb_ids:
        pdb_fasta_file = f"{pdb_id}.fasta"
        pdb_fasta_source = os.path.join(pdb_fasta_folder, pdb_fasta_file)
        if os.path.exists(pdb_fasta_source):
            shutil.copy(pdb_fasta_source, subfolder_path)
            print(f"Moved {pdb_fasta_file} to {subfolder_path}")
        else:
            print(f"PDB FASTA file {pdb_fasta_file} not found!")

print("Organizing of FASTA sequences completed.")
