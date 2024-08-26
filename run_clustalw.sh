#!/bin/bash

#SBATCH --job-name=run_clustalw         # Set the name of the job
#SBATCH --account=def-aali              # Specify which account to submit the job under
#SBATCH --mem=4G                        # Request 4GB of CPU memory
#SBATCH --time=00:05:00                 # Request 5 mins max to finish the job
#SBATCH --output=clustalw_job_%j.out    # Set the output name
#SBATCH --error=clustalw_job_%j.err     # Set the error log name

# Time command records the total runtime for the function
# clustalw is run on dataset fasta files and the alignment output is in the fasta format
time ./clustalw2 dataset_A.fasta -OUTPUT=FASTA
time ./clustalw2 dataset_B.fasta -OUTPUT=FASTA
time ./clustalw2 dataset_C.fasta -OUTPUT=FASTA
