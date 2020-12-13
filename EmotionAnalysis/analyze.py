import spacy
from spacymoji import Emoji
import pickle
import pandas as pd
import string
from nltk.corpus import stopwords 
import math 

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def getPolarityScore(lemma, lex, pos, score):
    if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
        return lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Polarity'].mean()
    else:
        return 0

def getNegScore(lemma, lex, pos):
    if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
        return (lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Negative Score'].values).mean()
    else:
        return 0

def getPosScore(lemma, lex, pos):
    if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
        return (lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Positive Score'].values).mean()
    else:
        return 0

def getIntensityScore(lemma, lex, pos):
    if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
        return (lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Intensity'].values).mean()
    else:
        return 0

def getAnger(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Anger'].mean()
    else:
        return 0

def getAnticipation(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Anticipation'].mean()
    else:
        return 0

def getDisgust(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Disgust'].mean()
    else:
        return 0

def getFear(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Fear'].mean()
    else:
        return 0

def getJoy(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Joy'].mean()
    else:
        return 0

def getSadness(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Sadness'].mean()
    else:
        return 0

def getSurprise(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Surprise'].mean()
    else:
        return 0

def getTrust(lemma, lex):
    if lemma in lex['Italian (it)'].values:
        return lex[lex['Italian (it)'] == lemma]['Trust'].mean()
    else:
        return 0

# Emoticons
def getAngerEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['anger'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getAnticipationEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['anticipation'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getDisgustEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['disgust'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getFearEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['fear'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getJoyEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['joy'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getSadnessEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['sadness'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getSurpriseEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['surprise'][lex['emoji'] == lemma].mean()
    else:
        return 0

def getTrustEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return lex['trust'][lex['emoji'] == lemma].mean()
    else:
        return 0

if __name__ == "__main__":
    
    save_path_init = 'data/data_df.pickle'
    save_path_emo = 'data/data_emosen_df.pickle'

    # save_path_init = 'data/dummy_df.pickle'
    # save_path_emo = 'data/dummy_emosen_df.pickle'

    data = pickle.load(open(save_path_init, 'rb'))

    sentix = pickle.load(open('EmotionAnalysis/lexicons/sentix_df.pickle', 'rb'))
    emotag = pickle.load(open('EmotionAnalysis/lexicons/emotag_df.pickle', 'rb'))
    nrc = pickle.load(open('EmotionAnalysis/lexicons/nrc_df.pickle', 'rb'))
    
    size = len(data)

    pos_score = [0] * size
    neg_score = [0] * size
    polarity = [0] * size
    intensity = [0] * size
    anger = [0] * size	
    anticipation = [0] * size
    disgust	= [0] * size
    fear = [0] * size	
    joy = [0] * size	
    sadness	= [0] * size
    surprise = [0] * size 
    trust = [0] * size

    index = 0

    # print(getPosScore('naturale', sentix))
    # print(getAngerEmo('🌈', emotag))

    nlp = spacy.load("it_core_news_sm")
    emoji = Emoji(nlp, merge_spans=False)
    nlp.add_pipe(emoji, first=True)

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

            if pos in closed_class:
                continue
            
            if token.text in stop_words:
                continue

            if token._.is_emoji: 

                anger[index] += getAngerEmo(token.text, emotag)
                anticipation[index] += getAnticipationEmo(token.text, emotag)
                disgust[index] += getDisgustEmo(token.text, emotag)
                fear[index] += getFearEmo(token.text, emotag)	
                joy[index] += getJoyEmo(token.text, emotag)	
                sadness[index] += getSadnessEmo(token.text, emotag)
                surprise[index] += getSurpriseEmo(token.text, emotag) 
                trust[index] += getTrustEmo(token.text, emotag)

            else:

                anger[index] += getAnger(token.text, nrc)
                anticipation[index] += getAnticipation(token.text, nrc)
                disgust[index] += getDisgust(token.text, nrc)
                fear[index] += getFear(token.text, nrc)	
                joy[index] += getJoy(token.text, nrc)	
                sadness[index] += getSadness(token.text, nrc)
                surprise[index] += getSurprise(token.text, nrc) 
                trust[index] += getTrust(token.text, nrc)


            if pos in pos_tags.keys():

                pos_score[index] += getPosScore(lemma, sentix, pos_tags[pos])
                neg_score[index] += getNegScore(lemma, sentix, pos_tags[pos])
                polarity[index] += getPolarityScore(lemma, sentix, pos_tags[pos], pos_score[index])
                intensity[index] += getIntensityScore(lemma, sentix, pos_tags[pos])

            else:
                
                pos_score[index] += joy[index] + trust[index]
                neg_score[index] += anger[index] + disgust[index] + fear[index] + sadness[index]
                intensity[index] += math.sqrt(pos_score[index]**2 + neg_score[index]**2)
                polarity[index] += 1 - 4 * (math.atan(neg_score[index]/pos_score[index]))
            
        index += 1
    
    data['positivity'] = pos_score
    data['negativity'] = neg_score
    data['polarity'] = polarity
    data['intensity'] = intensity
    data['anger'] = anger
    data['anticipation'] = anticipation
    data['disgust'] = disgust
    data['fear'] = fear
    data['joy'] = joy
    data['sadness'] = sadness
    data['surprise'] = surprise
    data['trust'] = trust        
    save_data(data, save_path_emo)