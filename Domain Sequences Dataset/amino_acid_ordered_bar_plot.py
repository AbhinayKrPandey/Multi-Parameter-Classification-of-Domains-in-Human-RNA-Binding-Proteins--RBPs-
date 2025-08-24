import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Amino acid codes
amino_acids = list("ACDEFGHIKLMNPQRSTVWY")

def calculate_average_scores(file_path, score_column):
    """Calculate average scores and count for each amino acid."""
    # Read the file
    df = pd.read_excel(file_path)

    # Initialize a dictionary to store sums and counts
    aa_scores = defaultdict(lambda: {'sum': 0, 'count': 0})

    # Loop through sequences and scores
    for sequence, score in zip(df['Amino Acid Sequence'], df[score_column]):
        for aa in sequence:
            if aa in amino_acids:  # Only consider valid amino acids
                aa_scores[aa]['sum'] += score
                aa_scores[aa]['count'] += 1

    # Calculate averages
    aa_averages = {aa: (aa_scores[aa]['sum'] / aa_scores[aa]['count'] if aa_scores[aa]['count'] > 0 else 0) for aa in amino_acids}
    return aa_averages, aa_scores

def generate_plot_and_text(file_short, file_long, short_column, long_column, output_plot, output_text):
    """Generate bar plot and write summary statistics to a text file."""
    # Calculate averages and counts
    short_averages, short_scores = calculate_average_scores(file_short, short_column)
    long_averages, long_scores = calculate_average_scores(file_long, long_column)

    # Prepare data for plotting
    x = range(len(amino_acids))
    short_scores_avg = [short_averages[aa] for aa in amino_acids]
    long_scores_avg = [long_averages[aa] for aa in amino_acids]

    # Plotting
    plt.figure(figsize=(12, 6))
    bar_width = 0.4

    bars_short = plt.bar([i - bar_width / 2 for i in x], short_scores_avg, bar_width, label='Short Scores', color='orange')
    bars_long = plt.bar([i + bar_width / 2 for i in x], long_scores_avg, bar_width, label='Long Scores', color='green')

    # Add labels and title
    plt.xlabel('Amino Acids')
    plt.ylabel('Average IUPred Scores')
    plt.title('Average IUPred Scores for Each Amino Acid')
    plt.xticks(x, amino_acids)
    plt.legend()

    # Add the score values on top of the bars
    for bars, scores in zip([bars_short, bars_long], [short_scores_avg, long_scores_avg]):
        for bar, score in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{score:.2f}', ha='center', va='bottom', fontsize=9)

    # Save the plot as a PNG file
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()

    # Write summary statistics to a text file
    with open(output_text, 'w') as f:
        f.write("Summary Statistics for Amino Acids:\n\n")
        for aa in amino_acids:
            short_count = short_scores[aa]['count']
            short_sum = short_scores[aa]['sum']
            long_count = long_scores[aa]['count']
            long_sum = long_scores[aa]['sum']
            f.write(f"Amino Acid: {aa}\n")
            f.write(f"  Short - Count: {short_count}, Sum: {short_sum:.2f}, Average: {short_averages[aa]:.2f}\n")
            f.write(f"  Long - Count: {long_count}, Sum: {long_sum:.2f}, Average: {long_averages[aa]:.2f}\n\n")

        # Calculate overall sums and averages
        total_short_sum = sum(short_scores[aa]['sum'] for aa in amino_acids)
        total_short_count = sum(short_scores[aa]['count'] for aa in amino_acids)
        total_long_sum = sum(long_scores[aa]['sum'] for aa in amino_acids)
        total_long_count = sum(long_scores[aa]['count'] for aa in amino_acids)

        overall_short_avg = total_short_sum / total_short_count if total_short_count > 0 else 0
        overall_long_avg = total_long_sum / total_long_count if total_long_count > 0 else 0

        f.write("Overall Statistics:\n")
        f.write(f"  Short - Total Count: {total_short_count}, Total Sum: {total_short_sum:.2f}, Overall Average: {overall_short_avg:.2f}\n")
        f.write(f"  Long - Total Count: {total_long_count}, Total Sum: {total_long_sum:.2f}, Overall Average: {overall_long_avg:.2f}\n")

# File paths
file_short = "Ordered_Short_Domain_Sequence.xlsx"
file_long = "Ordered_Long_Domain_Sequence.xlsx"
output_plot = "Average_IUPred_Scores_Ordered.png"
output_text = "Ordered_Summary_Statistics.txt"

# Generate plot and text file
generate_plot_and_text(file_short, file_long, 'IUPred Short Score', 'IUPred Long Score', output_plot, output_text)
