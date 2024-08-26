# DPAMSA

## Running DPAMSA
The "run_DPAMSA.sh" bash script is written to be submitted to slurm. DPAMSA runs faster on a GPU node accessed through CUDA, but can also be run on a CPU node when a GPU is not available (automatically configured based on GPU availability). This bash script requests a GPU node through CUDA along with the required amount of time. The "config.py" script is to be editted when altering the parameters for DPAMSA. The code in "main.py" script was altered to accept fasta files containing the sequences to be aligned. Alter the bash script to specify the name of the fasta file that should be treated at the input for DPAMSA.

## Running traditional MSA techniques
The bash scripts for running ClustalW, T-COFFEE, and MAFFT are also designed to be submitted to slurm. Please check the report for information regarding how to download the traditional MSA techniques as well as the version numbers used for this analysis.

## Comparing the results
The "calc_scores.py" script is used to obtain the quality scores for the alignments. The scores can be used to compare the performances of the different MSA techniques.
