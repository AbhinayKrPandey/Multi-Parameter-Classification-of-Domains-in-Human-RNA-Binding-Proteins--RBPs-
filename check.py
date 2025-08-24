'''import os

# Define the main fasta directory
fasta_dir = 'C:/Users/91630/Desktop/BTP/fasta'

# The PDB ID you're looking for
pdb_id_to_find = '2M2B'  # Replace '1XYZ' with the actual PDB ID you want to search for

# Search for the PDB file in all UniProt subfolders
found_locations = []

for root, dirs, files in os.walk(fasta_dir):
    for file in files:
        if file == f"{pdb_id_to_find}.fasta":  # Match the PDB file by name
            found_locations.append(os.path.join(root, file))

# Display the results
if found_locations:
    print(f"PDB ID {pdb_id_to_find} found in the following locations:")
    for location in found_locations:
        print(location)
else:
    print(f"PDB ID {pdb_id_to_find} was not found in any folder.")
import os

# Define the main fasta directory
fasta_dir = 'C:/Users/91630/Desktop/BTP/fasta'  # Update this path as needed

# Initialize a total count
total_fasta_count = 0

# Dictionary to hold counts for each UniProt subfolder
fasta_counts = {}

# Traverse through the directory
for root, dirs, files in os.walk(fasta_dir):
    fasta_count = 0  # Initialize count for the current subfolder

    for file in files:
        # Check if the file is a FASTA file
        if file.endswith('.fasta'):
            fasta_count += 1  # Increment count for the current subfolder
            total_fasta_count += 1  # Increment total count

    # If there are FASTA files in the subfolder, record the count
    if fasta_count > 0:
        subfolder_name = os.path.basename(root)  # Get the name of the subfolder
        fasta_counts[subfolder_name] = fasta_count  # Store the count in the dictionary

# Print the results
print("FASTA file counts per UniProt subfolder:")
for subfolder, count in fasta_counts.items():
    print(f"{subfolder}: {count} FASTA files")

print(f"\nTotal FASTA files in all subfolders: {total_fasta_count}")'''
'''import os
from Bio import SeqIO
from collections import defaultdict

def check_duplicate_fasta_sequences(main_dir):
    # Dictionary to hold sequence data
    sequence_dict = defaultdict(list)
    
    # Traverse through subfolders (each subfolder is considered as a UniProt ID)
    for subfolder in os.listdir(main_dir):
        subfolder_path = os.path.join(main_dir, subfolder)
        
        # Check if the path is a directory
        if os.path.isdir(subfolder_path):
            # Loop through all files in subfolder
            for file in os.listdir(subfolder_path):
                if file.endswith(".fasta"):
                    file_path = os.path.join(subfolder_path, file)
                    # Read the fasta file
                    for record in SeqIO.parse(file_path, "fasta"):
                        seq_str = str(record.seq)
                        # Store the sequence and PDB file path
                        pdb_id = os.path.splitext(file)[0]  # Extract PDB ID from filename
                        sequence_dict[seq_str].append(pdb_id)

    # Find duplicates and report them
    duplicates = {seq: pdb_ids for seq, pdb_ids in sequence_dict.items() if len(pdb_ids) > 1}
    
    if duplicates:
        print(f"Total number of duplicate sequences found: {len(duplicates)}\n")
        for pdb_ids in duplicates.values():
            print(f"Duplicate found in the following PDB IDs: {set(pdb_ids)}")
            print(f"Occurrence count: {len(pdb_ids)}\n")
    else:
        print("No duplicate sequences found.")
    
# Example usage
main_directory = "fasta"  # Replace this with your actual main directory containing UniProt subfolders
check_duplicate_fasta_sequences(main_directory)'''

'''import os
from Bio import SeqIO
from collections import defaultdict

def check_duplicate_fasta_sequences(main_dir):
    # Dictionary to hold sequence data, indexed by UniProt ID and sequence
    sequence_dict = defaultdict(lambda: defaultdict(list))
    
    # Traverse through subfolders (each subfolder is considered as a UniProt ID)
    for subfolder in os.listdir(main_dir):
        subfolder_path = os.path.join(main_dir, subfolder)
        
        # Check if the path is a directory (each directory is a UniProt ID)
        if os.path.isdir(subfolder_path):
            # Loop through all files in subfolder
            for file in os.listdir(subfolder_path):
                if file.endswith(".fasta"):
                    file_path = os.path.join(subfolder_path, file)
                    # Read the fasta file
                    for record in SeqIO.parse(file_path, "fasta"):
                        seq_str = str(record.seq)
                        # Store the sequence and PDB file path under the UniProt ID
                        pdb_id = os.path.splitext(file)[0]  # Extract PDB ID from filename
                        sequence_dict[seq_str][subfolder].append(pdb_id)

    # Find duplicates and report them
    total_duplicates = 0
    duplicate_report = []

    for seq, uniprot_pdb_dict in sequence_dict.items():
        # For each sequence, check if it exists across multiple UniProt IDs
        if any(len(pdb_ids) > 1 for pdb_ids in uniprot_pdb_dict.values()):
            for uniprot_id, pdb_ids in uniprot_pdb_dict.items():
                if len(pdb_ids) > 1:  # Duplicates within the same UniProt ID folder
                    duplicate_count = len(pdb_ids) - 1  # Calculate duplicates (total - 1)
                    total_duplicates += duplicate_count
                    duplicate_report.append((uniprot_id, pdb_ids, duplicate_count))

    # Print detailed report
    if duplicate_report:
        for uniprot_id, pdb_ids, duplicate_count in duplicate_report:
            print(f"UniProt ID: {uniprot_id}")
            print(f"PDB IDs with duplicates: {pdb_ids}")
            print(f"Number of duplicates in {uniprot_id}: {duplicate_count}")
            print("-" * 40)
        
        print(f"Total number of duplicates across all UniProt IDs: {total_duplicates}")
    else:
        print("No duplicate sequences found.")
    
# Example usage
main_directory = "fasta"  # Replace this with your actual main directory containing UniProt subfolders
check_duplicate_fasta_sequences(main_directory)'''
'''import os

# Path to the main folder containing subfolders
main_folder = 'fasta'

# Path to the file listing subfolder names
subfolder_file = 'unique_uniprot_ids.txt'

# Read the subfolder names from the file
with open(subfolder_file, 'r') as file:
    subfolder_names = file.read().splitlines()

# Initialize variables to count subfolders and files
subfolder_count = 0
total_files = 0

# Iterate through each subfolder listed in the file
for subfolder_name in subfolder_names:
    subfolder_path = os.path.join(main_folder, subfolder_name)

    # Check if the subfolder exists
    if os.path.isdir(subfolder_path):
        subfolder_count += 1
        # Get a list of files in the subfolder
        files = os.listdir(subfolder_path)
        file_count = len([file for file in files if os.path.isfile(os.path.join(subfolder_path, file))])
        total_files += file_count
        print(f"Subfolder: {subfolder_name}, Number of files: {file_count}")

# Final summary
print(f"\nTotal number of subfolders: {subfolder_count}")
print(f"Total number of files in all subfolders: {total_files}")'''
'''import os

# Path to the main folder containing subfolders
main_folder = 'fasta'

# Path to the file listing subfolder names
subfolder_file = 'unique_uniprot_ids.txt'

# Read the subfolder names from the file
with open(subfolder_file, 'r') as file:
    subfolder_names = [line.strip() for line in file if line.strip()]  # Strip whitespace and ignore empty lines

# Initialize variables to count subfolders and files
subfolder_count = 0
total_files = 0

# Iterate through each subfolder listed in the file
for subfolder_name in subfolder_names:
    subfolder_path = os.path.join(main_folder, subfolder_name)

    # Check if the subfolder exists
    if os.path.isdir(subfolder_path):
        subfolder_count += 1
        
        # Get a list of all files in the subfolder (including in subdirectories, if any)
        files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
        file_count = len(files)
        
        total_files += file_count
        print(f"Subfolder: {subfolder_name}, Number of files: {file_count}")
    else:
        print(f"Subfolder does not exist: {subfolder_path}")

# Final summary
print(f"\nTotal number of subfolders: {subfolder_count}")
print(f"Total number of files in all subfolders: {total_files}")'''
import os

'''# Path to the main folder containing subfolders
main_folder = 'Fasta_Sequences_Subfolders'

# Initialize variables to count subfolders and files
subfolder_count = 0
total_files = 0

# Iterate through each subfolder in the main folder
for subfolder_name in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder_name)

    # Check if it's a directory (subfolder)
    if os.path.isdir(subfolder_path):
        subfolder_count += 1
        # Get a list of files in the subfolder
        files = os.listdir(subfolder_path)
        file_count = len([file for file in files if os.path.isfile(os.path.join(subfolder_path, file))])
        total_files += file_count
        print(f"Subfolder: {subfolder_name}, Number of files: {file_count}")

# Final summary
print(f"\nTotal number of subfolders: {subfolder_count}")
print(f"Total number of files in all subfolders: {total_files}")'''
import os

import os

# Folder containing the subfolders
main_folder = 'Fasta_Sequences_Subfolders'

# Initialize variables to keep track of total files
total_files = 0

# Iterate through each subfolder in the main folder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    # Ensure the item is a directory
    if os.path.isdir(subfolder_path):
        # Get the list of files in the current subfolder and filter by .fasta extension
        files_in_subfolder = [f for f in os.listdir(subfolder_path) if f.endswith('.fasta')]
        
        # Count the number of .fasta files in the subfolder
        num_files = len(files_in_subfolder)
        total_files += num_files
        
        # Print the count for the current subfolder
        print(f"Subfolder: {subfolder} - Files: {num_files}")

# Print the total number of .fasta files across all subfolders
print(f"Total number of .fasta files across all subfolders: {total_files}")
'''import os
import hashlib

# Function to calculate file hash (to detect duplicates)
def calculate_file_hash(filepath):
    hasher = hashlib.md5()  # Using MD5 for file content comparison
    with open(filepath, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Folder containing the subfolders
main_folder = 'Fasta_Sequences_Subfolders'

# Dictionary to store file hashes and track duplicates
file_hashes = {}
total_files = 0
duplicate_files = 0

# Iterate through each subfolder in the main folder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    # Ensure the item is a directory
    if os.path.isdir(subfolder_path):
        # Iterate through files in the subfolder
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith('.fasta'):  # Only process .fasta files
                file_path = os.path.join(subfolder_path, file_name)
                
                # Calculate file hash to detect duplicates
                file_hash = calculate_file_hash(file_path)
                
                # Check if the file is a duplicate
                if file_hash in file_hashes:
                    # If duplicate, delete the file
                    os.remove(file_path)
                    duplicate_files += 1
                    print(f"Duplicate file {file_name} deleted from {subfolder}")
                else:
                    # If not a duplicate, add hash to the dictionary
                    file_hashes[file_hash] = file_name
                    total_files += 1

# Print the total counts
print(f"Total unique files: {total_files}")
print(f"Total duplicate files deleted: {duplicate_files}")
'''