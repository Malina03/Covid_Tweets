'''
Visualize Topic
Code Source: Tian Shi
https://github.com/tshi04
'''
import argparse
import os
import sys
sys.path.append(os.getcwd())
from TopicModelling.SeaNMF_utils import *

parser = argparse.ArgumentParser()
parser.add_argument('--corpus_file', default='data/SeaNMF/doc_term_mat.txt', help='term document matrix file')
parser.add_argument('--vocab_file', default='data/SeaNMF/vocab.txt', help='vocab file')
parser.add_argument('--par_file', default='results/SeaNMF/W.txt', help='model results file')
opt = parser.parse_args()

f = open("results/SeaNMF/topics.txt", "w")

docs = read_docs(opt.corpus_file)
vocab = read_vocab(opt.vocab_file)
n_docs = len(docs)
n_terms = len(vocab)
print('n_docs={}, n_terms={}'.format(n_docs, n_terms))
f.write('n_docs={}, n_terms={}'.format(n_docs, n_terms) + '\n')

dt_mat = np.zeros([n_terms, n_terms])
for itm in docs:
    for kk in itm:
        for jj in itm:
            if kk != jj:
                dt_mat[int(kk), int(jj)] += 1.0
print('co-occur done')
        
W = np.loadtxt(opt.par_file, dtype=float)
n_topic = W.shape[1]
print('n_topic={}'.format(n_topic))
f.write('n_topic={}'.format(n_topic) + '\n')

PMI_arr = []
n_topKeyword = 10
for k in range(n_topic):
    topKeywordsIndex = W[:,k].argsort()[::-1][:n_topKeyword]
    PMI_arr.append(calculate_PMI(dt_mat, topKeywordsIndex))
print('Average PMI={}'.format(np.average(np.array(PMI_arr))))
f.write('Average PMI={}'.format(np.average(np.array(PMI_arr))) + '\n')

index = np.argsort(PMI_arr)
  
for k in index:
    print('Topic ' + str(k+1) + ': ', end=' ')
    print(PMI_arr[k], end=' ')
    f.write('Topic ' + str(k+1) + ': ', end=' ')
    f.write(PMI_arr[k], end=' ')
    for w in np.argsort(W[:,k])[::-1][:n_topKeyword]:
        print(vocab[w], end=' ')
        f.write(vocab[w], end=' ')
    print()
    f.write('\n')