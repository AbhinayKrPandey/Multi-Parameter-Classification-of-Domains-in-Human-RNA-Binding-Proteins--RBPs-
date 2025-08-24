import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Amino acid codes
amino_acids = list("ACDEFGHIKLMNPQRSTVWY")

# Function to calculate average scores and statistics for each amino acid
def calculate_average_scores_and_stats(file_path):
    # Read the file
    df = pd.read_excel(file_path)

    # Initialize a dictionary to store sums, counts, and scores
    aa_stats = defaultdict(lambda: {'sum_long': 0, 'sum_short': 0, 'count': 0})

    # Loop through sequences and scores
    for sequence, long_score, short_score in zip(
        df['Complete Domain Sequence'], df['IUPred Long Score'], df['IUPred Short Score']
    ):
        for aa in sequence:
            if aa in amino_acids:  # Only consider valid amino acids
                aa_stats[aa]['sum_long'] += long_score
                aa_stats[aa]['sum_short'] += short_score
                aa_stats[aa]['count'] += 1

    # Calculate averages and totals
    aa_averages_long = {
        aa: (aa_stats[aa]['sum_long'] / aa_stats[aa]['count'] if aa_stats[aa]['count'] > 0 else 0)
        for aa in amino_acids
    }
    aa_averages_short = {
        aa: (aa_stats[aa]['sum_short'] / aa_stats[aa]['count'] if aa_stats[aa]['count'] > 0 else 0)
        for aa in amino_acids
    }
    return aa_averages_long, aa_averages_short, aa_stats

# File path for complete sequence
complete_sequence_file = "complete_domain_sequences.xlsx"

# Calculate averages and stats
averages_long, averages_short, stats = calculate_average_scores_and_stats(complete_sequence_file)

# Prepare data for plotting
x = range(len(amino_acids))  # Positions for amino acids
long_scores = [averages_long[aa] for aa in amino_acids]
short_scores = [averages_short[aa] for aa in amino_acids]

# Plotting
plt.figure(figsize=(12, 6))
bar_width = 0.4

# Plot bars for long and short scores
bars_long = plt.bar([i - bar_width / 2 for i in x], long_scores, bar_width, label='Long Scores', color='purple')
bars_short = plt.bar([i + bar_width / 2 for i in x], short_scores, bar_width, label='Short Scores', color='teal')

# Add labels and title
plt.xlabel('Amino Acids')
plt.ylabel('Average IUPred Scores')
plt.title('Average IUPred Scores for Each Amino Acid (Complete Sequences)')
plt.xticks(x, amino_acids)
plt.legend()

# Add the score values on top of the bars
for bars, scores in zip([bars_long, bars_short], [long_scores, short_scores]):
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f'{score:.2f}', ha='center', va='bottom', fontsize=9)

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('Average_IUPred_Scores_Complete.png')

# Show plot
plt.show()

# Write statistics to a text file
with open("Complete_Summary_Statistics.txt", "w") as f:
    f.write("Amino Acid\tCount\tSum Long\tSum Short\tAverage Long\tAverage Short\n")
    for aa in amino_acids:
        count = stats[aa]['count']
        sum_long = stats[aa]['sum_long']
        sum_short = stats[aa]['sum_short']
        avg_long = averages_long[aa]
        avg_short = averages_short[aa]
        f.write(f"{aa}\t{count}\t{sum_long:.2f}\t{sum_short:.2f}\t{avg_long:.2f}\t{avg_short:.2f}\n")
