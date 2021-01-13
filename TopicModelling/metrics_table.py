import numpy as np
import os
import sys
import csv
sys.path.append(os.getcwd())

path = 'results/SeaNMF/topics'
csv_path = 'results/SeaNMF/metrics_overview.csv'

row_list = []
header = ['Month', 'Topics #', 'PMI', 'NMPI', 'TD'] 
row_list.append(header)

for folder in os.listdir(path):
    directory = os.path.join(path, folder)
    month = str(folder)
    for f in os.listdir(directory):
        full_path = os.path.join(directory,f)
        with open(full_path, 'r') as file:
            lines=file.readlines()
            n_topics = lines[1].split("=")[1].strip('\n')
            pmi = lines[2].split("=")[1].strip('\n')
            npmi = lines[3].split("=")[1].strip('\n')
            td = lines[4].split("=")[1].strip('\n')
        row = [month, n_topics, pmi, npmi, td]
        row_list.append(row)

with open(csv_path, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(row_list)