#!/bin/bash
#SBATCH --time=00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=covid_tweets
#SBATCH --mem=800
#SBATCH --mail-type=BEGIN, END
#SBATCH --mail-user=m.chichirau@student.rug.nl

module load Python/3.6.6-intel-2018b
python TopicModelling/SeaNMF_train.py