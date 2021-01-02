import spacy
import pickle
import pandas as pd
import string
from nltk.corpus import stopwords 

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    
    save_path_init = 'data/data_df.pickle'
    save_path_emo = 'data/data_emosen_df.pickle'

    # save_path_init = 'data/dummy_df.pickle'
    # save_path_emo = 'data/dummy_emosen_df.pickle'

    data = pickle.load(open(save_path_init, 'rb'))

    sentix = pickle.load(open('EmotionAnalysis/lexicons/sentix_df.pickle', 'rb'))
    size = len(data)

    pos_score = [0] * size
    neg_score = [0] * size
    polarity = [0] * size
    intensity = [0] * size
    
    index = 0

    nlp = spacy.load("it_core_news_sm")

    pos_tags = {'ADJ': 'A', 'ADV': 'R', 'NOUN':'n', 'VERB': 'v'}
    closed_class = ['CONJ', 'CCONJ', 'DET', 'INTJ', 'SCONJ', 'NUM', 'PRON', 'ADP', 'PUNCT', 'SYM', 'SPACE', 'AUX']
    stop_words = set(stopwords.words('italian')) 

    length = len(data)
    
    for _, row in data.iterrows():

        if index % 100000 == 0:
            print (" {}% of tweets were analysed".format(index/length))

        for token in nlp(row['text']):

            if not token.text.isalpha():
                continue

            lemma = token.lemma_
            pos = token.pos_

            if pos in pos_tags.keys():
                
                if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
                    pos_score[index] += sentix[(sentix['Lemma'] == lemma) & (lex['POS'] == pos_tags[pos])]['Positive Score'].mean()
                    neg_score[index] += sentix[(sentix['Lemma'] == lemma) & (lex['POS'] == pos_tags[pos])]['Negative Score'].mean()
                    polarity[index] += sentix[(sentix['Lemma'] == lemma) & (lex['POS'] == pos_tags[pos])]['Polarity'].mean()
                    intensity[index] += sentix[(sentix['Lemma'] == lemma) & (lex['POS'] == pos_tags[pos])]['Intensity'].mean()
        index += 1

    data['sentix_positivity'] = pos_score
    data['sentix_negativity'] = neg_score
    data['sentix_polarity'] = polarity
    data['sentix_intensity'] = intensity
    save_data(data, save_path_emo)