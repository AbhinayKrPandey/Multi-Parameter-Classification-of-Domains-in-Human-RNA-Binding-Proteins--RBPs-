import os

# Paths
input_folder = "uniprot_fasta_sequences"
output_folder = "uniprot_amino_acid_sequences"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each .fasta file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".fasta"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".fasta", ".txt"))

        # Read the .fasta file
        with open(input_path, "r") as infile:
            lines = infile.readlines()

        # Remove the first line (header) and keep the sequence
        sequence = "".join(line.strip() for line in lines[1:] if not line.startswith(">"))

        # Write the sequence to a new .txt file
        with open(output_path, "w") as outfile:
            outfile.write(sequence)

print(f"All amino acid sequences have been saved to the folder '{output_folder}'!")
