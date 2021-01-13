import argparse
import os
import sys
import numpy as np
import pickle
sys.path.append(os.getcwd())

save_path_init = 'data/data_emosen_df.pickle'
save_path = 'data/data_emo_topics_df.pickle'
data = pickle.load(open(save_path_init, 'rb'))

months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
topics_february = {0:'Covid-19 testing', 1:'Topic 1', 2:'Politics', 3:'Sports', 4:'Regional restrictions', 5:'Topic 5', 6:'Covid-19 cases', 7:'Food (shortage)', 8:'Covid-19 research', 9:'Economy'}
topics_march = {0:'Lockdown', 1:'English', 2:'Arts', 3:'State of emergency', 4:'Swearing', 5:'Covid-19 cases', 6:'Impact on workers', 7:'Food', 8:'Topic 8', 9:'Economy'}
topics_april = {0:'Covid-19 cases', 1:'Topic 1', 2:'Topic 2', 3:'Lockdown enforcement', 4:'Food', 5:'English', 6:'Arts', 7:'Impact on workers', 8:'Covid-19 research', 9:'Politics'}
topics_may = {0:'Covid-19 cases', 1:'Lockdown (psychological impact)', 2:'Economy', 3:'Topic 3', 4:'Covid-19 research', 5:'English', 6:'Arts', 7:'International', 8:'Politics', 9:'Sports'}
topics_june = {0:'Covid-19 cases', 1:'International', 2:'Topic 2', 3:'Impact on workers', 4:'Politics', 5:'Digitalization', 6:'Economy', 7:'Lockdown', 8:'Sports', 9:'Covid-19 research'}
topics_july = {0:'Covid-19 cases', 1:'Topic 1', 2:'Topic 2', 3:'Economy', 4:'Politics', 5:'Immigration', 6:'Digitalization', 7:'Impact on workers', 8:'Sports', 9:'Covi-19 research'}
topics = 10

all_labels = []

for month in months.values():
    print("Month {}".format(month))
    fname = 'results/SeaNMF/weights/'+ month +'/H_' + str(topics) + '.txt'
    H = np.loadtxt(fname, dtype=float)
    n_topic = H.shape[1]
    if n_topic != topics: 
        print("Not reading the matrix correctly H.shape[1] is n_topic={}".format(n_topic))
        break
    labels = H.argmax(axis=1)
    all_labels.extend(labels.tolist())
    tpcs = np.zeros(10)
    for i in range(0,10):
        tpcs[i] = np.count_nonzero(labels==i)/len(labels)
        print("Topic {} has {} %".format(topics_july[i], tpcs[i]))
    
data['topics'] = all_labels
with open(save_path, 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)