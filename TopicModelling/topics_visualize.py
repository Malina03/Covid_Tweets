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

def visualize_topics(month, topics):
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus_file', default='data/SeaNMF/'+ month + '/doc_term_mat.txt', help='term document matrix file')
    parser.add_argument('--vocab_file', default='data/SeaNMF/'+ month + '/vocab.txt', help='vocab file')
    parser.add_argument('--par_file', default='results/SeaNMF/weights/'+ month + '/W_' + str(topics) + '.txt', help='model results file')
    opt = parser.parse_args()

    topics_path = 'results/SeaNMF/topics/' + month
    if not os.path.exists(topics_path):
        os.makedirs(topics_path)
    f = open(topics_path + '/topics_' + str(topics) + '.txt', "w")
        
    docs = read_docs(opt.corpus_file)
    vocab = read_vocab(opt.vocab_file)
    n_docs = len(docs)
    n_terms = len(vocab)
    # print('n_docs={}, n_terms={}'.format(n_docs, n_terms))
    f.write('n_docs={}, n_terms={}'.format(n_docs, n_terms) + '\n')

    dt_mat = np.zeros([n_terms, n_terms])
    for itm in docs:
        for kk in itm:
            for jj in itm:
                if kk != jj:
                    dt_mat[int(kk), int(jj)] += 1.0
    # print('co-occur done')
            
    W = np.loadtxt(opt.par_file, dtype=float)
    n_topic = W.shape[1]
    # print('n_topic={}'.format(n_topic))
    f.write('n_topic={}'.format(n_topic) + '\n')

    PMI_arr = []
    NPMI_arr = []
    n_topKeyword = 20
    for k in range(n_topic):
        topKeywordsIndex = W[:,k].argsort()[::-1][:n_topKeyword]
        pmi, npmi = calculate_PMI_NPMI(dt_mat, topKeywordsIndex) 
        PMI_arr.append(pmi)
        NPMI_arr.append(npmi)
    
    td = compute_topic_diversity(W[:][::-1][:n_topKeyword], n_topKeyword)
    # print('Average PMI={}'.format(np.average(np.array(PMI_arr))))
    # print('Average NPMI={}'.format(np.average(np.array(NPMI_arr))))
    # print('Topic Diversity={}'.format(td))
    f.write('Average PMI={} \n'.format(np.average(np.array(PMI_arr))))
    f.write('Average NPMI={} \n'.format(np.average(np.array(NPMI_arr))))
    f.write('Topic Diversity={} \n'.format(td))
    index = np.argsort(PMI_arr)
    
    for k in index:
        # print('Topic ' + str(k+1) + ': ', end=' ')
        # print(PMI_arr[k], end=' ')
        f.write('Topic ' + str(k) + ': ')
        f.write('PMI=' + str(PMI_arr[k]) + ' NMPI=' + str(NPMI_arr[k])+ '\n')
        for w in np.argsort(W[:,k])[::-1][:n_topKeyword]:
            # print(vocab[w], end=' ')
            f.write(str(vocab[w]) + ', ')
        # print()
        f.write('\n')
    f.close()


if __name__ == "__main__":
    months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
    n_topics = [10,20,30,50,70,90,110]

    print(months.values())

    for month in months.values():
        print("in the months loop")
        for topics in n_topics:
            print("Creating visualization for " + month + " with {} topics".format(topics))
            visualize_topics(month, topics)