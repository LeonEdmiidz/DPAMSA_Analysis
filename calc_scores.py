# This script is used to calculate the scores for the traditionl methods
# This script relies on config.py and env.py
import sys
import config  # Scores are calculated based off the scoring system specified in config
from env import nucleotides_map  # Get the nucleotides map from env
from Bio import SeqIO  # Using Biopython to parse through the fasta formatted alignments

def calculate_sp_score(alignment):

    score = 0  # Initial SP score
    num_rows = len(alignment)  # Get the number of sequences in the alignment
    seq_ids = list(alignment.keys())  # Extract sequence IDs (keys of the alignment dictionary)
    # Check if the current column index is within the bounds of both sequences
    for col_idx in range(len(alignment[seq_ids[0]])):  # Iterate over columns
        for row_idx1 in range(num_rows):  # Iterate over each sequence
            for row_idx2 in range(row_idx1 + 1, num_rows):  # Iterate over all other sequences to compare pairs
                seq1 = alignment[seq_ids[row_idx1]]  # First sequence in the pair to be compared
                seq2 = alignment[seq_ids[row_idx2]]  # Second sequence in the pair to be compared
                if col_idx < len(seq1) and col_idx < len(seq2):
                    res1 = nucleotides_map.get(seq1[col_idx], 5)  # Get the numerical values of the nucletides from the map
                    res2 = nucleotides_map.get(seq2[col_idx], 5)

                    if res1 == 5 or res2 == 5:            # Gap
                        score += config.GAP_PENALTY         # Apply gap penalty
                    elif res1 == res2:                    # Match
                        score += config.MATCH_REWARD        # Apply the match reward
                    else:                                 # Mismatch
                        score += config.MISMATCH_PENALTY    # Apply the mismatch penalty

    return score  # Return the calculated score
def calculate_cs_score(alignment):

    exact_matches = 0  # Initial CS score
    total_columns = len(alignment[list(alignment.keys())[0]])  # Get the number of columns in the alignment

    for col_idx in range(total_columns):  # Iterate over each column
        first_residue = alignment[list(alignment.keys())[0]][col_idx]  # Get the first nucleotide in the column
        if all(alignment[seq_id][col_idx] == first_residue for seq_id in alignment):  # Check if all nucleotides match
            exact_matches += 1  # Increment the counter if all match

    # Calculate the CS score as the proportion of exact matches to the total number of columns
    return exact_matches / total_columns

if __name__ == "__main__":
    # Included to ensure that the alignment file path is provided as a command-line argument when running the script
    if len(sys.argv) < 2:
        print("Usage: python calculate_sp_score.py <alignment_file>")
        sys.exit(1)  # Exit with an error code if not enough arguments

    alignment_file = sys.argv[1]  # Specify that the argument in the command line is the alignment file
    alignment = {}  # Use a dictionary to store sequences with their IDs
    # Read the FASTA alignment file and store sequences with their IDs in the 'alignment' dictionary
    alignment = {record.id: str(record.seq) for record in SeqIO.parse(alignment_file, "fasta")}

    sp_score = calculate_sp_score(alignment)  # Calculate the SP score
    cs_score = calculate_cs_score(alignment)  # Calculate the CS score

    print(f"SP Score: {sp_score}")  # Print the SP score
    print(f"CS Score: {cs_score:.4f}")  # Print the CS score formatted to 4 decimal places