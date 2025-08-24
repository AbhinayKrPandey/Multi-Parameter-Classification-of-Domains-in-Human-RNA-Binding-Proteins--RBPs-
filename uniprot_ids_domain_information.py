import os
import xml.etree.ElementTree as ET
import pandas as pd

# Define the root folder where the UniProt subfolders are stored
root_folder = "Fasta_Sequences_Subfolders"

# Iterate over each UniProt subfolder in the root folder
for subfolder in os.listdir(root_folder):
    subfolder_path = os.path.join(root_folder, subfolder)
    
    # Check if the current path is a directory (subfolder)
    if os.path.isdir(subfolder_path):
        # Path to the XML file for the current UniProt ID
        xml_file_path = os.path.join(subfolder_path, f"{subfolder}_xml.txt")
        
        # Check if the XML file exists in the current subfolder
        if os.path.exists(xml_file_path):
            # Parse the XML file with namespace support
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            # Define the namespace
            ns = {'ns': 'http://uniprot.org/uniprot'}
            
            # Prepare lists to store domain details
            domains = []
            descriptions = []
            begin_positions = []
            end_positions = []
            
            # Iterate through all <feature> elements in the correct namespace
            for feature in root.findall(".//ns:feature", ns):
                feature_type = feature.get('type', 'N/A')  # Get the feature type

                if feature_type == 'domain':
                    description = feature.get('description', 'N/A')  # Get domain description
                    
                    # Extract the <begin> and <end> positions from <location>
                    location = feature.find("ns:location", ns)
                    if location is not None:
                        begin = location.find("ns:begin", ns).get('position', 'N/A') if location.find("ns:begin", ns) is not None else 'N/A'
                        end = location.find("ns:end", ns).get('position', 'N/A') if location.find("ns:end", ns) is not None else 'N/A'
                        
                        # Append details to the lists
                        domains.append('domain')  # Replace with specific identifier if available
                        descriptions.append(description)
                        begin_positions.append(begin)
                        end_positions.append(end)

            if domains:
                # Create a DataFrame from the lists
                df = pd.DataFrame({
                    'domain': domains,
                    'description': descriptions,
                    'begin position': begin_positions,
                    'end position': end_positions
                })

                # Define the output Excel file path
                excel_file_path = os.path.join(subfolder_path, f"{subfolder}_domain_information.xlsx")
                
                # Write the DataFrame to an Excel file
                df.to_excel(excel_file_path, index=False)
                
                # Print a message indicating the file was created
                print(f"{subfolder}_domain_information.xlsx file created.")
            else:
                print(f"No domain information found for {subfolder}.")
                
print("All Excel files have been successfully created.")
