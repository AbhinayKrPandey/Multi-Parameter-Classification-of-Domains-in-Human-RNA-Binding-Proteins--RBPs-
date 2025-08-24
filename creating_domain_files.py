import os
import pandas as pd

# Define paths
base_folder = "Fasta_Sequences_Subfolders"
domain_folder = "domain"
unique_domains_file = "C:\\Users\\91630\\Desktop\\BTP\\domain\\unique_domains.txt"

# Function to read amino acids and scores from IUPred files
def read_iupred_scores(file_path, begin, end):
    amino_acids = []
    scores = []
    with open(file_path, "r") as file:
        lines = file.readlines()[12:]  # Skip header lines
        for line in lines:
            parts = line.strip().split()
            pos = int(parts[0])
            if begin <= pos <= end:
                amino_acids.append(parts[1])   # Amino acid
                scores.append(float(parts[2])) # Score
    return amino_acids, scores

# Step 1: Read the unique domains from the text file
with open(unique_domains_file, "r") as f:
    unique_domains = [line.strip() for line in f.readlines()]

# Function to sanitize domain names (replace slashes and other special characters)
def sanitize_domain_name(domain_name):
    return domain_name.replace("/", "_").replace("\\", "_").replace(":", "_")

# Step 2: Iterate over each domain and create a domain.xlsx file
for domain in unique_domains:
    sanitized_domain = sanitize_domain_name(domain)  # Sanitize the domain name
    domain_filename = os.path.join(domain_folder, f"{sanitized_domain}.xlsx")
    
    # Ensure that the directory exists before saving the file
    os.makedirs(os.path.dirname(domain_filename), exist_ok=True)

    columns = ['uniprot id', 'begin', 'end', 'amino acid sequence', 'iupred long score', 'iupred short score']
    
    # Create an empty DataFrame to store data
    domain_df = pd.DataFrame(columns=columns)

    # Step 3: Go through each subfolder and check for domain in the domain_information.xlsx file
    for uniprot_id in os.listdir(base_folder):
        uniprot_folder = os.path.join(base_folder, uniprot_id)
        if os.path.isdir(uniprot_folder):
            domain_info_file = os.path.join(uniprot_folder, f"{uniprot_id}_domain_information.xlsx")
            
            # Check if domain_information file exists and contains the desired domain
            if os.path.isfile(domain_info_file):
                df = pd.read_excel(domain_info_file)
                
                # Filter the domain information for the current domain
                domain_rows = df[df['description'] == domain]
                if not domain_rows.empty:
                    # Extract begin and end positions for the domain
                    begin_pos = int(domain_rows.iloc[0]['begin position'])
                    end_pos = int(domain_rows.iloc[0]['end position'])
                    
                    # Read the IUPred score files
                    long_score_file = os.path.join(uniprot_folder, f"{uniprot_id}.fasta_iupred_scores_long.txt")
                    short_score_file = os.path.join(uniprot_folder, f"{uniprot_id}.fasta_iupred_scores_short.txt")
                    
                    # Check if both score files exist
                    if os.path.isfile(long_score_file) and os.path.isfile(short_score_file):
                        # Read amino acid sequence and IUPred scores from the long and short score files
                        amino_acids, iupred_long_scores = read_iupred_scores(long_score_file, begin_pos, end_pos)
                        _, iupred_short_scores = read_iupred_scores(short_score_file, begin_pos, end_pos)
                        
                        # Ensure the lengths match between amino acid sequence and scores
                        if len(amino_acids) == len(iupred_long_scores) == len(iupred_short_scores):
                            # Prepare rows to append to the DataFrame
                            rows = []
                            for i in range(len(amino_acids)):
                                row = {
                                    'uniprot id': uniprot_id if i == 0 else "",  # Print only once per block
                                    'begin': begin_pos if i == 0 else "",       # Print only once per block
                                    'end': end_pos if i == 0 else "",           # Print only once per block
                                    'amino acid sequence': amino_acids[i],
                                    'iupred long score': iupred_long_scores[i],
                                    'iupred short score': iupred_short_scores[i]
                                }
                                rows.append(row)
                            
                            # Concatenate new rows to the DataFrame and filter out empty rows
                            temp_df = pd.DataFrame(rows).dropna(how='all')  # Drop rows where all values are NA
                            if not temp_df.empty:  # Only concatenate non-empty rows
                                domain_df = pd.concat([domain_df, temp_df], ignore_index=True)
    
    # Step 4: Write the DataFrame to an Excel file for the domain
    domain_df.to_excel(domain_filename, index=False)
    print(f"Created {domain_filename} with {len(domain_df)} rows of data.")
