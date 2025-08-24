
import os
import pandas as pd

# Define the path to the folder containing the domain information files
domain_folder = "domain_information"

# List all files in the domain folder
for filename in os.listdir(domain_folder):
    file_path = os.path.join(domain_folder, filename)
    
    # Check if it's an Excel file
    if file_path.endswith(".xlsx"):
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)

            # Check if the DataFrame only contains the header and no data rows
            if df.shape[0] == 0:  # No rows, only header
                print(f"Deleting empty file: {filename}")
                os.remove(file_path)
            else:
                # Check if the file contains only the header (if no rows with data)
                required_columns = ['domain', 'description', 'begin position', 'end position']
                if all(col in df.columns for col in required_columns) and df.isnull().all().all():
                    print(f"Deleting file with only header: {filename}")
                    os.remove(file_path)
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Empty or header-only files have been deleted.")
