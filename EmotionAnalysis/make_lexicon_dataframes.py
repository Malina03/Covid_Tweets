import os
import pickle
import pandas as pd
import gzip
import sys
sys.path.append(os.getcwd())

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

emotag_path = 'EmotionAnalysis/lexicons/EmoTag1200-scores.csv'
sentix_path = 'EmotionAnalysis/lexicons/sentix.gz'
nrc_path = 'EmotionAnalysis/lexicons/NRC-Emotion-Lexicon-IT.csv'

# make sentix df 

lemma = []
pos = []
synset = []
pos_score = []
neg_score = []
polarity = []
intensity = []
data = []
with gzip.open(sentix_path, 'r') as sent:
    for line in sent:
        row = line.decode('utf-8').split('\t')
        lemma.append(row[0])
        pos.append(row[1])
        synset.append(row[2])
        pos_score.append(float(row[3]))
        neg_score.append(float(row[4]))
        polarity.append(float(row[5]))
        intensity.append(float(row[6].strip('\n')))

data = {'Lemma':lemma, "POS":pos, 'Synset ID':synset, 'Positive Score':pos_score, 'Negative Score':neg_score,
                      'Polarity':polarity, 'Intensity':intensity}

sentix = pd.DataFrame(data, columns = ['Lemma', 'POS', 'Synset ID', 'Positive Score', 'Negative Score',
                      'Polarity', 'Intensity'])

save_data(sentix, 'EmotionAnalysis/lexicons/sentix_df.pickle')

# make emotag df
emotag = pd.read_csv(emotag_path, delimiter = ',')
print(emotag)
save_data(emotag, 'EmotionAnalysis/lexicons/emotag_df.pickle')

# make nrc emtion df
nrc = pd.read_csv(nrc_path, delimiter = ',')
print(nrc)
save_data(nrc, 'EmotionAnalysis/lexicons/nrc_df.pickle')