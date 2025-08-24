import os
import pandas as pd

def combine_domain_data_with_ids(domain_folder, output_file):
    combined_data = []
    gaps_found = []

    # Iterate through all files in the domain folder
    for domain_file in os.listdir(domain_folder):
        if domain_file.startswith('~$') or not domain_file.endswith('.xlsx'):
            continue

        domain_file_path = os.path.join(domain_folder, domain_file)
        domain_df = pd.read_excel(domain_file_path)

        # Identify columns dynamically
        sequence_columns = [col for col in domain_df.columns if "Amino Acid Sequence" in col]
        long_score_columns = [col for col in domain_df.columns if "IUPred Long Score" in col]
        short_score_columns = [col for col in domain_df.columns if "IUPred Short Score" in col]
        uniprot_columns = [col for col in domain_df.columns if "UniProt ID" in col]
        begin_columns = [col for col in domain_df.columns if "Begin" in col]
        end_columns = [col for col in domain_df.columns if "End" in col]

        # Ensure columns are aligned correctly
        for i, (seq_col, long_col, short_col, uni_col, begin_col, end_col) in enumerate(
            zip(sequence_columns, long_score_columns, short_score_columns, uniprot_columns, begin_columns, end_columns)
        ):
            for index, row in domain_df.iterrows():
                sequence = row[seq_col]
                long_score = row[long_col]
                short_score = row[short_col]
                uniprot_id = row[uni_col]
                begin = row[begin_col]
                end = row[end_col]

                if pd.isna(sequence):
                    gaps_found.append((domain_file, index + 2))  # +2 for header row and 0-based indexing
                else:
                    combined_data.append({
                        f"UniProt ID {i+1}": uniprot_id,
                        f"Begin {i+1}": begin,
                        f"End {i+1}": end,
                        f"Amino Acid Sequence {i+1}": sequence,
                        f"IUPred Long Score {i+1}": long_score,
                        f"IUPred Short Score {i+1}": short_score,
                    })

    # Log gaps found
    if gaps_found:
        print("Missing data detected in the following rows:")
        for file_name, row_number in gaps_found:
            print(f"File: {file_name}, Row: {row_number}")
    else:
        print("No gaps found in the dataset.")

    # Combine all data into a DataFrame
    combined_df = pd.DataFrame(combined_data)

    # Save combined data
    combined_df.to_excel(output_file, index=False)
    print(f"Combined dataset saved to {output_file}")
    print(f"Total sequences processed: {len(combined_data)}")

# Define paths
domain_folder = r"C:\Users\91630\Desktop\BTP\domains"  # Replace with actual folder path
output_file = r"C:\Users\91630\Desktop\BTP\combined_domain_data_with_ids.xlsx"  # Replace with output path

# Call the function
combine_domain_data_with_ids(domain_folder, output_file)
