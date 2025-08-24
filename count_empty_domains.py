import os
import pandas as pd

# Use raw string for Windows path to avoid escape sequence issues
folder_path = r'C:\Users\91630\Desktop\BTP\domain'

# Define the expected column headers
expected_columns = [
    'UniProt ID', 'Begin Position', 'End Position',
    'Amino Acid', 'IUPred Long Score', 'IUPred Short Score'
]

# Initialize a list to store the names of empty files
empty_files = []

# Check if the folder exists
if not os.path.isdir(folder_path):
    print(f"The folder '{folder_path}' does not exist. Please check the path.")
else:
    print(f"Folder '{folder_path}' exists. Proceeding with file checks...")  # Confirm folder found

    # Print statement to verify folder content
    files_in_folder = os.listdir(folder_path)
    print(f"Files found in the folder: {files_in_folder}")  # List files found in the directory

    # Loop through each file in the folder
    for filename in files_in_folder:
        if filename.endswith('.xlsx'):
            print(f"Processing file: {filename}")  # Debug message
            
            file_path = os.path.join(folder_path, filename)
            
            # Load the Excel file
            try:
                df = pd.read_excel(file_path)
                print(f"Columns in {filename}: {list(df.columns)}")  # Debug column headers
                print(f"Number of rows in {filename}: {df.shape[0]}")  # Debug row count

                # Check if the file has only headers with no data rows
                if list(df.columns) == expected_columns and df.shape[0] == 0:
                    empty_files.append(filename)
            except Exception as e:
                print(f"Could not read '{filename}': {e}")

    # Display the results
    if empty_files:
        print(f"Number of empty files: {len(empty_files)}")
        print("Names of empty files:")
        for file in empty_files:
            print(file)
    else:
        print("No empty files found with only headers.")
