import pandas as pd

def remove_empty_rows(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Identify columns where empty rows should be removed
    # Assuming 'Complete Domain Sequence' column is key
    key_columns = ['Complete Domain Sequence', 'IUPred Long Score', 'IUPred Short Score']
    
    # Drop rows where all key columns are empty
    cleaned_df = df.dropna(subset=key_columns, how='all')
    
    # Save the cleaned dataframe to a new file
    cleaned_df.to_excel(output_file, index=False)
    print(f"Cleaned file saved as {output_file}")

# Replace these with your actual file paths
input_file = r"C:\Users\91630\Desktop\BTP\complete_domain_sequences.xlsx"
output_file = r"C:\Users\91630\Desktop\BTP/cleaned_complete_domain_sequences.xlsx"

remove_empty_rows(input_file, output_file)
