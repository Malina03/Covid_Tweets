import spacy
import pickle
import pandas as pd
import string
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

    nrc = pickle.load(open('EmotionAnalysis/lexicons/nrc_df.pickle', 'rb'))
    
    size = len(data)

    pos_score = [0] * size
    neg_score = [0] * size

    anger = [0] * size	
    anticipation = [0] * size
    disgust	= [0] * size
    fear = [0] * size	
    joy = [0] * size	
    sadness	= [0] * size
    surprise = [0] * size 
    trust = [0] * size

    index = 0

    nlp = spacy.load("it_core_news_sm")

    closed_class = ['CONJ', 'CCONJ', 'DET', 'INTJ', 'SCONJ', 'NUM', 'PRON', 'ADP', 'PUNCT', 'SYM', 'SPACE', 'AUX']
    stop_words = set(stopwords.words('italian')) 

    length = len(data)
    
    for _, row in data.iterrows():

        if index % 100000 == 0:
            print (" {}% of tweets were analysed in {:.2f} seconds".format((index/length),time.time()-start_time))


        for token in nlp(row['text']):

            if not token.text.isalpha():
                continue

            pos = token.pos_

            if token.lemma_ in stop_words or pos in closed_class:
                continue

            rows = nrc.loc[nrc['Italian (it)'] == token.text]

            if rows.empty:
                continue

            pos_score += rows['Positive'].mean()
            neg_score += rows['Negative'].mean()
            anger[index] += rows['Anger'].mean()
            anticipation[index] += rows['Anticipation'].mean()
            disgust[index] += rows['Disgust'].mean()
            fear[index] += rows['Fear'].mean()	
            joy[index] += rows['Joy'].mean()
            sadness[index] += rows['Sadness'].mean()
            surprise[index] += rows['Surprise'].mean()
            trust[index] += rows['Trust'].mean()

        index += 1
    
    data['nrc_positivity'] = pos_score
    data['nrc_negativity'] = neg_score
    data['nrc_anger'] = anger
    data['nrc_anticipation'] = anticipation
    data['nrc_disgust'] = disgust
    data['nrc_fear'] = fear
    data['nrc_joy'] = joy
    data['nrc_sadness'] = sadness
    data['nrc_surprise'] = surprise
    data['nrc_trust'] = trust        
    save_data(data, save_path_emo)

    print(time.time() - start_time, "seconds")
