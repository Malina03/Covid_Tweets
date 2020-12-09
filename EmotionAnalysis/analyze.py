import spacy
from spacymoji import Emoji
import pickle
import pandas as pd

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def getPolarityScore(lemma, lex, pos, score):
    if ((lex['Lemma'] == lemma) & (lex['POS'] == pos)).any():
        if len(lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Polarity'].values) > 1 :
            if score >= 0:
                return lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos) & lex['Polarity'] >= 0]['Polarity'].mean()
            else:
                return lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos) & lex['Polarity'] < 0]['Polarity'].mean()
        else:
            return  float(lex[(lex['Lemma'] == lemma) & (lex['POS'] == pos)]['Polarity'].values)
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
        return float(lex['anger'][lex['emoji'] == lemma].values)
    else:
        return 0

def getAnticipationEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['anticipation'][lex['emoji'] == lemma].values)
    else:
        return 0

def getDisgustEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['disgust'][lex['emoji'] == lemma].values)
    else:
        return 0

def getFearEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['fear'][lex['emoji'] == lemma].values)
    else:
        return 0

def getJoyEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['joy'][lex['emoji'] == lemma].values)
    else:
        return 0

def getSadnessEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['sadness'][lex['emoji'] == lemma].values)
    else:
        return 0

def getSurpriseEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['surprise'][lex['emoji'] == lemma].values)
    else:
        return 0

def getTrustEmo(lemma, lex):
    if lemma in lex['emoji'].values:
        return float(lex['trust'][lex['emoji'] == lemma].values)
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
    emoji = Emoji(nlp)
    nlp.add_pipe(emoji, first=True)

    pos_tags = {'ADJ': 'A', 'ADV': 'R', 'NOUN':'n', 'VERB': 'v'}

    length = len(data)
    
    for _, row in data.iterrows():
        if index % 10 == 0:
            print (" {}% of tweets were analysed".format(index/length))  

        for token in nlp(row['text']):

            lemma = token.lemma_
            pos = token.pos_

            if token._.is_emoji: 

                anger[index] += getAngerEmo(token.text, emotag)
                anticipation[index] += getAnticipationEmo(token.text, emotag)
                disgust[index] += getDisgustEmo(token.text, emotag)
                fear[index] += getFearEmo(token.text, emotag)	
                joy[index] += getJoyEmo(token.text, emotag)	
                sadness[index] += getSadnessEmo(token.text, emotag)
                surprise[index] += getSurpriseEmo(token.text, emotag) 
                trust[index] += getTrustEmo(token.text, emotag)

                pos_score[index] += getJoyEmo(token.text, emotag) + getTrustEmo(token.text, emotag)
                neg_score[index] += getAngerEmo(token.text, emotag) + getDisgustEmo(token.text, emotag) + getFearEmo(token.text, emotag) + getSadnessEmo(token.text, emotag)
                polarity[index] += getJoyEmo(token.text, emotag) + getTrustEmo(token.text, emotag) - getAngerEmo(token.text, emotag) - getDisgustEmo(token.text, emotag) - getFearEmo(token.text, emotag) - getSadnessEmo(token.text, emotag)

                continue

            if pos in pos_tags.keys():

                pos_score[index] += getPosScore(lemma, sentix, pos_tags[pos])
                neg_score[index] += getNegScore(lemma, sentix, pos_tags[pos])
                polarity[index] += getPolarityScore(lemma, sentix, pos_tags[pos], pos_score[index])
                intensity[index] += getIntensityScore(lemma, sentix, pos_tags[pos])

            else:
                # if there are no entries in sentix for that lemma, 
                # then compute the pos/neg/pol based on the emotions found
                
                pos_score[index] += getJoy(token.text, nrc) + getTrust(token.text, nrc)
                neg_score[index] += getAnger(token.text, nrc) + getDisgust(token.text, nrc) + getFear(token.text, nrc) + getSadness(token.text, nrc)
                polarity[index] += getJoy(token.text, nrc) + getTrust(token.text, nrc) - getAnger(token.text, nrc) - getDisgust(token.text, nrc) - getFear(token.text, nrc) - getSadness(token.text, nrc)

            anger[index] += getAnger(token.text, nrc)
            anticipation[index] += getAnticipation(token.text, nrc)
            disgust[index] += getDisgust(token.text, nrc)
            fear[index] += getFear(token.text, nrc)	
            joy[index] += getJoy(token.text, nrc)	
            sadness[index] += getSadness(token.text, nrc)
            surprise[index] += getSurprise(token.text, nrc) 
            trust[index] += getTrust(token.text, nrc)

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