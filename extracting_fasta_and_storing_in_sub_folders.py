import os
import openpyxl
import subprocess

# Define file paths
input_excel_file = 'C:/Users/91630/Desktop/BTP/RPC_complete.xlsx'  # Path to your Excel file
fasta_dir = 'C:/Users/91630/Desktop/BTP/fasta'  # Folder to store FASTA sequences

# Create the main fasta directory if it doesn't exist
if not os.path.exists(fasta_dir):
    os.makedirs(fasta_dir)

# Initialize sets for unique UniProt and PDB IDs
unique_uniprot_ids = set()
unique_pdb_ids = {}

# Step 1: Open the Excel file using openpyxl
wb = openpyxl.load_workbook(input_excel_file)
ws = wb.active  # Assuming the data is in the first sheet

# Step 2: Iterate over the rows, ignoring header row
for row in ws.iter_rows(min_row=2, values_only=True):
    uniprot_id = row[0]  # Assuming 'IDS' (UniProt IDs) is in the first column
    pdb_ids = row[1]  # Assuming 'RCSB PDB ids' is in the second column
    
    # Skip rows with NA or missing values for PDB IDs or UniProt IDs
    if pdb_ids != 'NA' and uniprot_id:
        uniprot_id = uniprot_id.strip()
        unique_uniprot_ids.add(uniprot_id)

        # Handle PDB IDs separated by semicolons
        for pdb_id in pdb_ids.split(';'):
            pdb_id = pdb_id.strip()
            if pdb_id:
                if uniprot_id not in unique_pdb_ids:
                    unique_pdb_ids[uniprot_id] = []
                unique_pdb_ids[uniprot_id].append(pdb_id)

# Step 3: Create subfolders for each UniProt ID and download FASTA sequences
for uniprot_id in unique_uniprot_ids:
    try:
        # Create a subfolder for each UniProt ID
        uniprot_dir = os.path.join(fasta_dir, uniprot_id)
        if not os.path.exists(uniprot_dir):
            os.makedirs(uniprot_dir)

        # Download UniProt FASTA sequence
        uniprot_fasta_url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
        uniprot_fasta_path = os.path.join(uniprot_dir, f"{uniprot_id}.fasta")
        
        print(f"Downloading UniProt FASTA for {uniprot_id}")
        subprocess.run(['wget', '-O', uniprot_fasta_path, uniprot_fasta_url], check=True)

        # Download FASTA sequences for the corresponding PDB IDs
        if uniprot_id in unique_pdb_ids:
            for pdb_id in unique_pdb_ids[uniprot_id]:
                pdb_fasta_url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
                pdb_fasta_path = os.path.join(uniprot_dir, f"{pdb_id}.fasta")
                
                print(f"Downloading PDB FASTA for {pdb_id} in {uniprot_id} folder")
                subprocess.run(['wget', '-O', pdb_fasta_path, pdb_fasta_url], check=True)
    
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

print(f"FASTA sequences downloaded successfully.")
