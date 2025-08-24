import os

# Read the unique UniProt IDs from the text file
with open('unique_uniprot_ids.txt', 'r') as file:
    unique_uniprot_ids = {line.strip() for line in file}

# Folder containing the UniProt FASTA sequences
folder_path = 'uniprot_fasta_sequences'

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    # Check if the filename (without extension) is not in the unique UniProt IDs
    file_id = os.path.splitext(filename)[0]  # Extract the filename without extension
    if file_id not in unique_uniprot_ids:
        file_path = os.path.join(folder_path, filename)
        try:
            os.remove(file_path)  # Delete the file
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")

print("File deletion process complete.")
