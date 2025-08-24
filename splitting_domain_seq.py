import pandas as pd

def split_domain_sequences(input_file):
    # Read the dataset
    df = pd.read_excel(input_file)

    # Ensure column names match exactly
    columns = ['Complete Domain Sequence', 'IUPred Long Score', 'IUPred Short Score']

    # Filter for disordered short domain sequences
    disordered_short = df[df['IUPred Short Score'] > 0.5][['Complete Domain Sequence', 'IUPred Short Score']]
    disordered_short.columns = ['Amino Acid Sequence', 'IUPred Short Score']
    disordered_short.to_excel("Disordered_Short_Domain_Sequence.xlsx", index=False)

    # Filter for disordered long domain sequences
    disordered_long = df[df['IUPred Long Score'] > 0.5][['Complete Domain Sequence', 'IUPred Long Score']]
    disordered_long.columns = ['Amino Acid Sequence', 'IUPred Long Score']
    disordered_long.to_excel("Disordered_Long_Domain_Sequence.xlsx", index=False)

    # Filter for ordered short domain sequences
    ordered_short = df[df['IUPred Short Score'] <= 0.5][['Complete Domain Sequence', 'IUPred Short Score']]
    ordered_short.columns = ['Amino Acid Sequence', 'IUPred Short Score']
    ordered_short.to_excel("Ordered_Short_Domain_Sequence.xlsx", index=False)

    # Filter for ordered long domain sequences
    ordered_long = df[df['IUPred Long Score'] <= 0.5][['Complete Domain Sequence', 'IUPred Long Score']]
    ordered_long.columns = ['Amino Acid Sequence', 'IUPred Long Score']
    ordered_long.to_excel("Ordered_Long_Domain_Sequence.xlsx", index=False)

    print("Files created successfully:")
    print("- Disordered_Short_Domain_Sequence.xlsx")
    print("- Disordered_Long_Domain_Sequence.xlsx")
    print("- Ordered_Short_Domain_Sequence.xlsx")
    print("- Ordered_Long_Domain_Sequence.xlsx")

# Replace with the path to your input file
input_file = "complete_domain_sequences.xlsx"
split_domain_sequences(input_file)
