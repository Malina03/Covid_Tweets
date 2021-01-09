import argparse
import os
import sys
import numpy as np
import pickle
sys.path.append(os.getcwd())

# months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
months = {2:'july'}
topics = 10
save_path_init = 'data/dummy_df.pickle'
data = pickle.load(open(save_path_init, 'rb'))

for month in months.values():
    fname = 'results/SeaNMF/weights/'+ month +'/H_' + str(topics) + '.txt'
    H = np.loadtxt(fname, dtype=float)
    n_topic = H.shape[1]
    if n_topic != topics: 
        print("Not reading the matrix correctly H.shape[1] is n_topic={}".format(n_topic))
        break
    labels = H.argmax(axis=1)
    print(labels[:10])
    print(data['text'][:10])
