#!/bin/bash

#SBATCH --job-name=run_tcoffee         # Set the name of the job
#SBATCH --account=def-aali             # Specify which account to submit the job under
#SBATCH --mem=4G                       # Request 4GB of CPU memory
#SBATCH --time=00:05:00                # Request 5 mins max to finish the job
#SBATCH --output=tcoffee_job_%j.out    # Set the output name
#SBATCH --error=tcoffee_job_%j.err     # Set the error log name

# MAX_N_PID_4_TCOFFEE must to set to around 5000000 otherwise t-coffee returns an error
# MAX_N_PID_4_TCOFFEE can be adjusted accordingly (May need more for larger datasets)
export MAX_N_PID_4_TCOFFEE=5000000
# Time command records the total runtime for the function
# t-coffee is run on the dataset fasta files and the alignment output is in the fasta format
time ./t_coffee dataset_A.fasta -output=fasta_aln
time ./t_coffee dataset_B.fasta -output=fasta_aln
time ./t_coffee dataset_C.fasta -output=fasta_aln
