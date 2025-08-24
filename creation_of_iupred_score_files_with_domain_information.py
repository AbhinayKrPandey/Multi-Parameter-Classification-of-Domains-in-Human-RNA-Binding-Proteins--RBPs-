import os
import pandas as pd

# Define the root folder containing UniProt subfolders
root_folder = 'Fasta_Sequences_subfolders'

def annotate_iupred_with_domains(uniprot_id, iupred_file, domain_file, output_file):
    # Load IUPred score data
    with open(iupred_file, 'r') as f:
        iupred_scores = f.readlines()

    # Load domain information with the corrected column names
    domain_info_df = pd.read_excel(domain_file)
    start_col = "begin position"
    end_col = "end position"
    domain_col = "description"

    # Initialize output list
    output_lines = []

    # Read headers from the IUPred score file
    for line in iupred_scores:
        if line.startswith('#'):
            output_lines.append(line)
        else:
            break  # Stop when reaching the data section

    # Add data with domain annotations
    for line in iupred_scores[len(output_lines):]:
        parts = line.strip().split()
        if len(parts) >= 3:
            pos = int(parts[0])  # Position of residue
            res = parts[1]  # Residue
            score = parts[2]  # IUPred score
            domain_label = ''  # Default empty label

            # Check if position falls within any domain range
            for _, row in domain_info_df.iterrows():
                start = int(row[start_col])
                end = int(row[end_col])
                domain_name = row[domain_col]

                if start <= pos <= end:
                    domain_label = f'domain {domain_name}'
                    break  # Only one domain label is added

            # Append the domain information to the line if applicable
            output_lines.append(f"{pos}\t{res}\t{score}\t{domain_label}\n")
        else:
            output_lines.append(line)  # For lines that do not match the format

    # Write the output file
    with open(output_file, 'w') as f:
        f.writelines(output_lines)

def process_all_uniprot_ids():
    # Iterate through each UniProt ID subfolder
    for uniprot_id_folder in os.listdir(root_folder):
        uniprot_folder_path = os.path.join(root_folder, uniprot_id_folder)
        if os.path.isdir(uniprot_folder_path):  # Only proceed if it's a folder
            uniprot_id = uniprot_id_folder

            # Define file paths
            iupred_long_file = os.path.join(uniprot_folder_path, f"{uniprot_id}.fasta_iupred_scores_long.txt")
            iupred_short_file = os.path.join(uniprot_folder_path, f"{uniprot_id}.fasta_iupred_scores_short.txt")
            domain_info_file = os.path.join(uniprot_folder_path, f"{uniprot_id}_domain_information.xlsx")

            # Output file paths
            output_long_file = os.path.join(uniprot_folder_path, f"{uniprot_id}.fasta_iupred_scores_long_with_domain_information.txt")
            output_short_file = os.path.join(uniprot_folder_path, f"{uniprot_id}.fasta_iupred_scores_short_with_domain_information.txt")

            # Process long and short IUPred files
            if os.path.exists(iupred_long_file) and os.path.exists(domain_info_file):
                annotate_iupred_with_domains(uniprot_id, iupred_long_file, domain_info_file, output_long_file)
                print(f"{output_long_file} created")

            if os.path.exists(iupred_short_file) and os.path.exists(domain_info_file):
                annotate_iupred_with_domains(uniprot_id, iupred_short_file, domain_info_file, output_short_file)
                print(f"{output_short_file} created")

# Run the function
process_all_uniprot_ids()
