import os

# Path to the main folder
main_folder = "C:\\Users\\91630\\Desktop\\BTP\\Fasta_Sequences_Subfolders"

# Loop through each subfolder inside the main folder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    # Check if it's a directory
    if os.path.isdir(subfolder_path):
        print(f"Entering subfolder: {subfolder_path}")  # Debugging line
        
        # Loop through each file in the subfolder
        for filename in os.listdir(subfolder_path):
            print(f"Checking file: {filename}")  # Debugging line
            
            # Check if the filename ends with '.fasta_iupred_scores.txt' but not '_short'
            if filename.endswith(".fasta_iupred_scores.txt") and not filename.endswith("_short.txt"):
                # Generate the new filename by appending '_long' before .txt
                new_filename = filename.replace(".fasta_iupred_scores.txt", ".fasta_iupred_scores_long.txt")
                
                # Full paths for the old and new file
                old_file_path = os.path.join(subfolder_path, filename)
                new_file_path = os.path.join(subfolder_path, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
            else:
                print
