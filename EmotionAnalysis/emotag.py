import spacy
from spacymoji import Emoji
import pickle
import pandas as pd

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    
    save_path_init = 'data/data_emosen_df.pickle'
    save_path_emo = 'data/data_emosen_df.pickle'

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
            print (" {}% of tweets were analysed".format(index/length))

        for token in nlp(row['text']):

            if token._.is_emoji: 

                if token.text in emotag['emoji'].values:

                    anger[index] += emotag['anger'][emotag['emoji'] == token.text].mean()
                    anticipation[index] +=  emotag['anticipation'][emotag['emoji'] == token.text].mean()
                    disgust[index] +=  emotag['disgust'][emotag['emoji'] == token.text].mean()
                    fear[index] += emotag['fear'][emotag['emoji'] == token.text].mean()	
                    joy[index] += emotag['joy'][emotag['emoji'] == token.text].mean()
                    sadness[index] += emotag['sadness'][emotag['emoji'] == token.text].mean()
                    surprise[index] += emotag['surprise'][emotag['emoji'] == token.text].mean()
                    trust[index] += emotag['trust'][emotag['emoji'] == token.text].mean()
            
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