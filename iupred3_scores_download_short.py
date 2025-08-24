import os
import subprocess

# Define paths
iupred3_script_path = "C:\\Users\\91630\\Desktop\\BTP\\iupred3\\iupred3\\iupred3.py"
fasta_folders_path = "C:\\Users\\91630\\Desktop\\BTP\\Fasta_Sequences_subfolders"

# Function to process each fasta file using iupred3 (short mode) and save output
def process_fasta_files(folder_path, fasta_file):
    fasta_file_path = os.path.join(folder_path, fasta_file)
    output_file_path = os.path.join(folder_path, f'{fasta_file}_iupred_scores_short.txt')

    # Set environment variable to ensure UTF-8 encoding
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Run iupred3.py on the fasta file with 'short' mode, handle encoding errors
    with open(output_file_path, 'w', encoding='utf-8', errors='replace') as output_file:
        subprocess.run(
            ['python', iupred3_script_path, fasta_file_path, 'short'],
            stdout=output_file,
            stderr=subprocess.STDOUT,  # Also capture errors in the output file
            env=env  # Pass the modified environment to subprocess
        )

# Loop through each subfolder
for subfolder in os.listdir(fasta_folders_path):
    subfolder_path = os.path.join(fasta_folders_path, subfolder)
    
    # Only process directories (subfolders)
    if os.path.isdir(subfolder_path):
        # Loop through each file in the subfolder
        for fasta_file in os.listdir(subfolder_path):
            if fasta_file.endswith('.fasta'):  # Process only fasta files
                process_fasta_files(subfolder_path, fasta_file)

print("Processing complete.")

'''
import os

# Define the path to the folder containing subfolders with output files
fasta_folders_path = "C:\\Users\\91630\\Desktop\\BTP\\Fasta_Sequences_subfolders"

# Function to remove iupred output files
def remove_iupred_files(folder_path):
    # Loop through each file in the folder
    for file in os.listdir(folder_path):
        # Identify files with '_iupred_scores_short.txt' in their name
        if file.endswith('_iupred_scores_short.txt'):
            file_path = os.path.join(folder_path, file)
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

# Loop through each subfolder in the main folder
for subfolder in os.listdir(fasta_folders_path):
    subfolder_path = os.path.join(fasta_folders_path, subfolder)
    
    # Only process directories (subfolders)
    if os.path.isdir(subfolder_path):
        # Remove the iupred output files from each subfolder
        remove_iupred_files(subfolder_path)

print("File cleanup complete.")'''

