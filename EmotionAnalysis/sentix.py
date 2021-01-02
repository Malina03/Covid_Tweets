import spacy
import pickle
import pandas as pd
import string
import numpy as np
from nltk.corpus import stopwords 
import time

start_time = time.time()

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    
    save_path_init = 'data/data_emosen_df.pickle'
    save_path_emo = 'data/data_emosen_df.pickle'

    # save_path_init = 'data/dummy_df.pickle'
    # save_path_emo = 'data/dummy_emosen_df.pickle'

    data = pickle.load(open(save_path_init, 'rb'))

    sentix = pickle.load(open('EmotionAnalysis/lexicons/sentix_df.pickle', 'rb'))
    size = len(data)

    pos_score = np.zeros(size)
    neg_score = np.zeros(size)
    polarity = np.zeros(size)
    intensity = np.zeros(size)
    
    index = 0

    nlp = spacy.load("it_core_news_sm")

    pos_tags = {'ADJ': 'A', 'ADV': 'R', 'NOUN':'n', 'VERB': 'v'}
    closed_class ={'CONJ', 'CCONJ', 'DET', 'INTJ', 'SCONJ', 'NUM', 'PRON', 'ADP', 'PUNCT', 'SYM', 'SPACE', 'AUX'}
    stop_words = set(stopwords.words('italian')) 

    length = len(data)
    
    for _, row in data.iterrows():

        if index % 100000 == 0:
            print (" {}% of tweets were analysed in {:.2f} seconds".format((index/length),time.time()-start_time))

        for token in nlp(row['text']):

            if not token.text.isalpha():
                continue
        
            lemma = (token.lemma_).lower()
            pos = token.pos_

            if lemma in stop_words or pos in closed_class:
                continue

            if pos in pos_tags.keys():
                # print(lemma)
                rows = sentix.loc[(sentix['Lemma'] == lemma) & (sentix['POS'] == pos_tags[pos])]

                if rows.empty:
                    continue
                
                pos_score[index] += rows['Positive Score'].mean()
                neg_score[index] += rows['Negative Score'].mean()
                polarity[index] += rows['Polarity'].mean()
                intensity[index] += rows['Intensity'].mean()

                del rows
        
        index += 1

    data['sentix_positivity'] = pos_score
    data['sentix_negativity'] = neg_score
    data['sentix_polarity'] = polarity
    data['sentix_intensity'] = intensity
    save_data(data, save_path_emo)

    print(time.time() - start_time, "seconds")