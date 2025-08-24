'''The PYTHONUTF8=1 environment variable is a way to ensure that Python uses UTF-8 encoding as the default when handling input and output. Normally, Python will use your system's default encoding (like cp1252 on Windows), but this can cause issues when dealing with non-ASCII characters, as in your case.

What PYTHONUTF8=1 Does:
Forces Python to use UTF-8 as the default encoding for standard input, output, and error streams.
Applies to all I/O operations such as print() and file operations.
It prevents issues like the UnicodeEncodeError you're seeing, which is caused by Python trying to print or write characters that your system's default encoding can't handle.
How to Use It:
Set the PYTHONUTF8 environment variable to 1 before running your script. This tells Python to run in UTF-8 mode.

Command to run your script with PYTHONUTF8=1:

Open the Command Prompt on your Windows machine.

Set the environment variable with the command:

bash
Copy code
set PYTHONUTF8=1
Then, run your Python script as usual:

bash
Copy code
python your_script.py
This will make sure that all encoding operations use UTF-8 instead of the default cp1252, preventing the UnicodeEncodeError.

Why Use It:
This solution is helpful when you're running into encoding issues in your script because of non-ASCII characters, and you don't want to modify each script to handle encoding. It provides a quick way to globally enforce UTF-8 for the Python session without editing the script itself.

Would you like to try this, or would you prefer another solution like editing the script itself?'''
import os
import subprocess
import sys

# Ensure the default encoding is set to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Define paths
iupred3_script_path = "C:\\Users\\91630\\Desktop\\BTP\\iupred3\\iupred3\\iupred3.py"  # Update this path
fasta_folders_path = "C:\\Users\\91630\\Desktop\\BTP\\Fasta_Sequences_subfolders"  # Update this path

# Function to process each fasta file using iupred3 and save output
def process_fasta_files(folder_path, fasta_file):
    fasta_file_path = os.path.join(folder_path, fasta_file)
    output_file_path = os.path.join(folder_path, f'{fasta_file}_iupred_scores.txt')

    # Run iupred3.py on the fasta file, force UTF-8 encoding
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        subprocess.run(['python', iupred3_script_path, fasta_file_path, 'long'], stdout=output_file, encoding='utf-8')

# Loop through each subfolder
for subfolder in os.listdir(fasta_folders_path):
    subfolder_path = os.path.join(fasta_folders_path, subfolder)
    
    # Only process directories (subfolders)
    if os.path.isdir(subfolder_path):
        # Loop through each file in the subfolder
        for fasta_file in os.listdir(subfolder_path):
            if fasta_file.endswith('.fasta'):  # Process only fasta files
                process_fasta_files(subfolder_path, fasta_file)

print("Processing complete.")