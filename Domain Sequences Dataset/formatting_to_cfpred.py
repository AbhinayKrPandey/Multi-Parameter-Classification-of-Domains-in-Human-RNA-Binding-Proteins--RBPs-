import pandas as pd

def format_sequences_to_one_row(file_path, output_path):
    # Load the Excel file
    data = pd.read_excel(file_path)
    
    # Extract the first column (assuming sequences are in the first column)
    sequences = data.iloc[:, 0].dropna().tolist()
    
    # Format sequences into a single row without spaces
    single_row_sequence = "".join(sequences)
    
    # Save the single-row sequence to a text file
    with open(output_path, 'w') as output_file:
        output_file.write(single_row_sequence)

# File paths
disordered_long_file = "Disordered_Long_Domain_Sequence.xlsx"
disordered_short_file = "Disordered_Short_Domain_Sequence.xlsx"

# Output paths
disordered_long_output = "Disordered_Long_Domain_Sequence_One_Row_Formatted.txt"
disordered_short_output = "Disordered_Short_Domain_Sequence_One_Row_Formatted.txt"

# Process each file
format_sequences_to_one_row(disordered_long_file, disordered_long_output)
format_sequences_to_one_row(disordered_short_file, disordered_short_output)

print("Sequences have been formatted and saved into single-row text files without spaces.")
