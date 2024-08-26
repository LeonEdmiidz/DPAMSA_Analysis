#!/bin/bash

#SBATCH --job-name=run_dpamsa         # Set the name of the job
#SBATCH --account=def-aali            # Specify which account to submit the job under
#SBATCH --gres=gpu:1                  # Request 1 GPU node
#SBATCH --mem=32G                     # Request 32GB of CPU memory (only got 12.8)
#SBATCH --time=24:00:00               # Request 24 hours max to finish the job
#SBATCH --output=dpamsa_job_%j.out    # Set the output name
#SBATCH --error=dpamsa_job_%j.err     # Set the error log name

# Load in the required modules to access and interact with the GPU node
module load StdEnv/2020
module load gcc/8.4.0
module load cuda/10.2
# Load python module to run the python scripts
module load python
# Utilize a virtual environment if necessary (commented out for now)
# Was needed for the Cedar cluster as it did not have all the required modules
# source py_env1000/bin/activate  # Sets the virtual environment as the source
# Run the gpu_test.py script to get all the info regarding the accessed GPU node
python gpu_test.py
# Run the DPAMSA script on dataset_A.fasta
python main.py dataset_A.fasta
