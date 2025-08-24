import os
import pandas as pd
from openpyxl import Workbook

# Define paths
base_folder = "Fasta_Sequences_Subfolders"
solution_folder = "solution"
empty_domains_file = r"C:\Users\91630\Desktop\BTP\empty_domains.txt"  # Updated path to empty_domains.txt

# Ensure solution folder exists
os.makedirs(solution_folder, exist_ok=True)

# Read empty domains from empty_domains.txt
with open(empty_domains_file, "r") as file:
    empty_domains = set(line.strip() for line in file)

# Process each empty domain
for domain in empty_domains:
    clean_domain = domain.replace('/', '-')  # Make filename safe
    domain_filename = os.path.join(solution_folder, f"{clean_domain}.xlsx")

    # Initialize a workbook for this domain
    wb = Workbook()
    ws = wb.active
    ws.title = clean_domain
    
    # Add header row
    header = ['UniProt ID', 'Begin Position', 'End Position', 'Amino Acid', 'IUPred Long Score', 'IUPred Short Score']
    ws.append(header)
    data_added = False

    # Go through each UniProt ID subfolder to locate data for this domain
    for uniprot_id in os.listdir(base_folder):
        uniprot_folder = os.path.join(base_folder, uniprot_id)
        if os.path.isdir(uniprot_folder):
            # Paths to domain and score files
            domain_info_file = os.path.join(uniprot_folder, f"{uniprot_id}_domain_information.xlsx")
            long_score_file = os.path.join(uniprot_folder, f"{uniprot_id}.fasta_iupred_scores_long.txt")
            short_score_file = os.path.join(uniprot_folder, f"{uniprot_id}.fasta_iupred_scores_short.txt")

            # Check if required files exist
            if not (os.path.isfile(domain_info_file) and os.path.isfile(long_score_file) and os.path.isfile(short_score_file)):
                continue

            # Read domain information
            df = pd.read_excel(domain_info_file)
            domain_rows = df[df['description'] == domain]
            
            # Skip if domain is not in the current file
            if domain_rows.empty:
                continue

            # Load IUPred scores and sequences
            long_scores, short_scores = [], []
            with open(long_score_file, "r") as long_file:
                for line in long_file:
                    parts = line.strip().split()
                    if len(parts) == 3 and parts[2].replace('.', '', 1).isdigit():
                        long_scores.append((parts[1], float(parts[2])))

            with open(short_score_file, "r") as short_file:
                for line in short_file:
                    parts = line.strip().split()
                    if len(parts) == 3 and parts[2].replace('.', '', 1).isdigit():
                        short_scores.append((parts[1], float(parts[2])))

            # Ensure score lists are aligned
            if len(long_scores) != len(short_scores):
                print(f"Score mismatch in {uniprot_id}")
                continue

            # Extract data for each row in the domain information
            for _, row in domain_rows.iterrows():
                begin, end = int(row['begin position']), int(row['end position'])
                domain_sequence = [aa for aa, _ in long_scores[begin-1:end]]
                domain_long_scores = [score for _, score in long_scores[begin-1:end]]
                domain_short_scores = [score for _, score in short_scores[begin-1:end]]
                
                # Only display UniProt ID, begin, and end once per domain
                uniprot_block = True
                for i in range(len(domain_sequence)):
                    if uniprot_block:
                        row_data = [uniprot_id, begin, end, domain_sequence[i], domain_long_scores[i], domain_short_scores[i]]
                        uniprot_block = False
                    else:
                        row_data = ["", "", "", domain_sequence[i], domain_long_scores[i], domain_short_scores[i]]
                    
                    ws.append(row_data)
                    data_added = True

    # Save the file only if data was added for this domain
    if data_added:
        wb.save(domain_filename)
        print(f"{clean_domain}.xlsx file created with content in {solution_folder}.")
    else:
        print(f"No data for domain {clean_domain}, file not created.")
