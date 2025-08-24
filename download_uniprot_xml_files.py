import os
import subprocess

# Base directory containing the subfolders named after UniProt IDs
base_dir = 'Fasta_sequences_Subfolders'

# UniProt REST API URL pattern for fetching XML files
base_url = 'https://rest.uniprot.org/uniprotkb/'

# Get the list of subfolders (each named after a UniProt ID)
subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

# Iterate over each subfolder (UniProt ID)
for subfolder in subfolders:
    # Define the full path to the subfolder
    subfolder_path = os.path.join(base_dir, subfolder)

    # Construct the URL for the XML file using the UniProt ID (subfolder name)
    uniprot_id = subfolder
    xml_url = f'{base_url}{uniprot_id}.xml'

    # Define the output file path with the UniProt ID as the filename (e.g., OS5fg_xml.txt)
    output_file = os.path.join(subfolder_path, f'{uniprot_id}_xml.txt')

    # Use wget to download the XML file directly
    subprocess.run(['wget', '-O', output_file, xml_url])

    # Print message after each download
    print(f"{uniprot_id} XML downloaded.")
 