import os
import pandas as pd
import pickle 
import spacy
from spacymoji import Emoji
import string
from nltk.corpus import stopwords 

def write_step_by_step(tweet, nrc, emotag, nlp, f, closed_class, stop_words):
    f.write("Original text: " + ' '.join(tweet['text']) + '\n')
    f.write("Cleaned text: " + ' '.join(tweet['cleaned_text']) + '\n')
    f.write('Removed as stopword: ')
    for word in tweet['text']:
        if word in stop_words:
            f.write(word + ', ')
    f.write('\n')
    f.write('Removed as closed class: ')
    for word in nlp(tweet['text']):
        lemma = word.lemma_
        if word.pos_ in closed_class:
            f.write(word.text + ', ')
    f.write('\n')
    f.write('Words in NRC: ')
    for word in tweet['text']:
        if word in nrc['Italian (it)']:
            f.write(word + ', ')
    f.write('\n')
    f.write('Emojis in emotag: ')
    for word in nlp(tweet['text']):
        if word._.is_emoji and word in emotag['emoji']:
            f.write(word.text + ', ')
    f.write('\n')

if __name__ == "__main__":
    save_path = 'data/data_emo_topics_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    emotag = pickle.load(open('EmotionAnalysis/lexicons/emotag_df.pickle', 'rb'))
    nrc = pickle.load(open('EmotionAnalysis/lexicons/nrc_df.pickle', 'rb'))

    nlp = spacy.load("it_core_news_sm")
    emoji = Emoji(nlp, merge_spans=False)
    nlp.add_pipe(emoji, first=True)

    closed_class = ['CONJ', 'CCONJ', 'DET', 'INTJ', 'SCONJ', 'NUM', 'PRON', 'ADP', 'PUNCT', 'SYM', 'SPACE', 'AUX']
    stop_words = set(stopwords.words('italian')) 
    
    f = open('results/tweet_examples.txt', 'w')

    i = 0

    for _, tweet in data.iterrows():
        if i == 10:
            break
        if tweet['nrc_joy'] != 0 and tweet['emotag_joy']!= 0:
            f.write("Double joy example: \n")
            write_step_by_step(tweet, nrc, emotag, nlp, f,closed_class, stop_words)
            i += 1
        if tweet['nrc_trust'] != 0 and tweet['emotag_trust']!= 0:
            f.write("Double trust example: \n")
            write_step_by_step(tweet, nrc, emotag, nlp, f,closed_class, stop_words)
            i += 1
        if tweet['nrc_fear'] != 0:
            f.write("Fear example: \n")
            write_step_by_step(tweet, nrc, emotag, nlp, f,closed_class, stop_words)
            i += 1
        if tweet['nrc_fear'] != 0 and tweet['emotag_fear']!=0:
            f.write("Double ear example: \n")
            write_step_by_step(tweet, nrc, emotag, nlp, f,closed_class, stop_words)
            i += 1
        if tweet['nrc_anticipation'] != 0:
            f.write("Anticipation example: \n")
            write_step_by_step(tweet, nrc, emotag, nlp, f,closed_class, stop_words)
            i += 1
    f.close()
            