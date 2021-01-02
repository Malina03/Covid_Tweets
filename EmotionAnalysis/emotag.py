import spacy
from spacymoji import Emoji
import pickle
import pandas as pd
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
    emotag = pickle.load(open('EmotionAnalysis/lexicons/emotag_df.pickle', 'rb'))
    
    size = len(data)

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
    emoji = Emoji(nlp, merge_spans=False)
    nlp.add_pipe(emoji, first=True)

    length = len(data)
    
    for _, row in data.iterrows():

        if index % 100000 == 0:
            print (" {}% of tweets were analysed in {:.2f} seconds".format((index/length),time.time()-start_time))

        for token in nlp(row['text']):

            if token._.is_emoji: 

                rows = emotag.loc[emotag['emoji'] == token.text]
                if rows.empty:
                    continue

                anger[index] += rows['anger'].mean()
                anticipation[index] +=  rows['anticipation'].mean()
                disgust[index] +=  rows['disgust'].mean()
                fear[index] += rows['fear'].mean()	
                joy[index] += rows['joy'].mean()
                sadness[index] += rows['sadness'].mean()
                surprise[index] += rows['surprise'].mean()
                trust[index] += rows['trust'].mean()
        
        index += 1
    
    data['emotag_anger'] = anger
    data['emotag_anticipation'] = anticipation
    data['emotag_disgust'] = disgust
    data['emotag_fear'] = fear
    data['emotag_joy'] = joy
    data['emotag_sadness'] = sadness
    data['emotag_surprise'] = surprise
    data['emotag_trust'] = trust        
    save_data(data, save_path_emo)

    print(time.time() - start_time, "seconds")