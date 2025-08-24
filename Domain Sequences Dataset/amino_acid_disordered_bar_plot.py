import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Amino acid codes
amino_acids = list("ACDEFGHIKLMNPQRSTVWY")

# Function to calculate average scores and counts for each amino acid
def calculate_aa_statistics(file_path, score_column):
    # Read the file
    df = pd.read_excel(file_path)

    # Initialize dictionaries to store sums and counts
    aa_scores = defaultdict(lambda: {'sum': 0, 'count': 0})

    # Loop through sequences and scores
    for sequence, score in zip(df['Amino Acid Sequence'], df[score_column]):
        for aa in sequence:
            if aa in amino_acids:  # Only consider valid amino acids
                aa_scores[aa]['sum'] += score
                aa_scores[aa]['count'] += 1

    # Calculate averages
    aa_averages = {aa: (aa_scores[aa]['sum'] / aa_scores[aa]['count'] if aa_scores[aa]['count'] > 0 else 0) for aa in amino_acids}
    return aa_scores, aa_averages

# File paths
short_disordered_file = "Disordered_Short_Domain_Sequence.xlsx"
long_disordered_file = "Disordered_Long_Domain_Sequence.xlsx"

# Calculate statistics for both files
short_disordered_stats, short_disordered_averages = calculate_aa_statistics(short_disordered_file, 'IUPred Short Score')
long_disordered_stats, long_disordered_averages = calculate_aa_statistics(long_disordered_file, 'IUPred Long Score')

# Prepare data for plotting
x = range(len(amino_acids))  # Positions for amino acids
short_scores = [short_disordered_averages[aa] for aa in amino_acids]
long_scores = [long_disordered_averages[aa] for aa in amino_acids]

# Plotting
plt.figure(figsize=(12, 6))
bar_width = 0.4

# Plot bars for short and long scores
bars_short = plt.bar([i - bar_width / 2 for i in x], short_scores, bar_width, label='Short Scores', color='blue')
bars_long = plt.bar([i + bar_width / 2 for i in x], long_scores, bar_width, label='Long Scores', color='green')

# Add labels and title
plt.xlabel('Amino Acids')
plt.ylabel('Average IUPred Scores')
plt.title('Average IUPred Scores for Each Amino Acid (Disordered Sequences)')
plt.xticks(x, amino_acids)
plt.legend()

# Add the score values on top of the bars
for bars, scores in zip([bars_short, bars_long], [short_scores, long_scores]):
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'{score:.2f}', ha='center', va='bottom', fontsize=9)

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('Average_IUPred_Scores_Disordered.png')

# Show plot
plt.show()

# Write statistics to a text file
output_file = "Disordered_Summary_Statistics.txt"
with open(output_file, 'w') as f:
    f.write("Statistics for Disordered Sequences\n")
    f.write("====================================\n")

    # Write short scores statistics
    f.write("\nShort Scores:\n")
    total_count_short = sum(short_disordered_stats[aa]['count'] for aa in amino_acids)
    total_sum_short = sum(short_disordered_stats[aa]['sum'] for aa in amino_acids)
    overall_avg_short = total_sum_short / total_count_short if total_count_short > 0 else 0
    for aa in amino_acids:
        count = short_disordered_stats[aa]['count']
        total = short_disordered_stats[aa]['sum']
        avg = short_disordered_averages[aa]
        f.write(f"{aa}: Count = {count}, Sum = {total:.2f}, Average = {avg:.2f}\n")
    f.write(f"\nTotal Count = {total_count_short}, Total Sum = {total_sum_short:.2f}, Overall Average = {overall_avg_short:.2f}\n")

    # Write long scores statistics
    f.write("\nLong Scores:\n")
    total_count_long = sum(long_disordered_stats[aa]['count'] for aa in amino_acids)
    total_sum_long = sum(long_disordered_stats[aa]['sum'] for aa in amino_acids)
    overall_avg_long = total_sum_long / total_count_long if total_count_long > 0 else 0
    for aa in amino_acids:
        count = long_disordered_stats[aa]['count']
        total = long_disordered_stats[aa]['sum']
        avg = long_disordered_averages[aa]
        f.write(f"{aa}: Count = {count}, Sum = {total:.2f}, Average = {avg:.2f}\n")
    f.write(f"\nTotal Count = {total_count_long}, Total Sum = {total_sum_long:.2f}, Overall Average = {overall_avg_long:.2f}\n")
