#!/bin/bash

#SBATCH --job-name=run_mafft         # Set the name of the job
#SBATCH --account=def-aali           # Specify which account to submit the job under
#SBATCH --mem=4G                     # Request 4GB of CPU memory
#SBATCH --time=00:05:00              # Request 5 mins max to finish the job
#SBATCH --output=mafft_job_%j.out    # Set the output name
#SBATCH --error=mafft_job_%j.err     # Set the error log name

# Load the required modules from the Cedar cluster
# StdEnv/2020 needs to be loaded before mafft can be loaded
module load StdEnv/2020
module load mafft/7.471
# Time command records the total runtime for the function
# mafft is run on the dataset fasta files and the alignment output is in the fasta format
time mafft dataset_A.fasta > mafft_A.fasta_aln
time mafft dataset_B.fasta > mafft_B.fasta_aln
time mafft dataset_C.fasta > mafft_C.fasta_aln
