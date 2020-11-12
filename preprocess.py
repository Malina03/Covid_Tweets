from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import re
import string
import os
import pandas as pd
import pickle 
import spacy
import numpy as np

def read_data(folder):
    errors = ['40wita_2020-05-06.csv.bz2', '40wita_2020-06-21.csv.bz2']
    flag = 0
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if f in errors:
            continue
        if os.path.isfile(full_path):
            folder_data = pd.read_csv(full_path, delimiter=',')
            folder_data = folder_data.drop_duplicates(subset = 'text', keep = 'first')
            folder_data['folder'] = [str(f)] * len(folder_data)
            if flag == 0:
                data = folder_data
                flag = 1
            if flag == 1:
                data = pd.concat([data, folder_data], ignore_index = True, sort = False)
    print("Data was read")
    return data

def remove_hyperlinks(text):
    return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)

def remove_keywords(text):
    keywords = ['covid', 'covid19', 'covid-19', 'corona virus', 'coronavirus', 'quarantena', 
                'autoisolamento', 'auto-isolamento', 'iorestoacasa', 'stateacasa', 'COVID19Italia', 
                'covid19italia', 'nomes', 'milanononsiferma', 'curaitalia', 'inpsdown', 'perchequando', 
                'cercaredi', 'cineinps', 'covid19pandemic', 'andratuttobene',
                'redditodicittadinaza', 'eurobond', 'coronabond', 'restiamoacasa', 'preghiamoinsieme',
                'NoMes', '#milanononsiferma', 'bergamononsiferma', 'l’italianonsiferma',
                'abbraccciauncinese', 'iononsonounvirus', 'iononmifermo', 'aperisera', 'covidunstria',
                'italiazonarossa', 'bergamoisrunning', 'quarantena', 'chiudetetutto', 'apritetutto',
                'CuraItalia', 'ciricordiamotutto', 'oggisciopero', 'chiudiamolefabbriche',
                'iononrinuncioalletradizioni', 'andràtuttobene', 'INPSdown', 'percheQuando', 'cercareDi',
                'ringraziarevoglio', '600euro', 'CineINPS', 'COVID19Pandemic']
    
    filtered = []
    for word in re.split("\W+", text):
        if (word not in keywords and word.lower() not in keywords):
            filtered.append(word)
    return ' '.join(filtered)


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_user_ref(text):
    user_ref = re.compile(r"@\S+")
    return user_ref.sub(r'', text)

def remove_tags(text):
    user_ref = re.compile(r"#\S+")
    return user_ref.sub(r'', text)

def remove_stopwords(text):
    stop_words = set(stopwords.words('italian')) 
    filtered_sentence = []
    for w in re.split("\W+", text):
        if not w.lower() in stop_words:
            filtered_sentence.append(w)
    return ' '.join(filtered_sentence)

def remove_numbers(text):
    return ''.join(letter for letter in text if not letter.isdigit())

def remove_closed_class_words(text):
    closed_class = ["mio", "io", "tuo", "tua", "quello", "quella", "questo",
                    "questa", "tu", "me", "mi", "si", "te", "ti", "suo", "sua",
                    "lo", "la", "che", "lui", "lei", "noi", "le", "nostro",
                    "nostra", "ci", "gli", "loro", "voi", "vi", "vostro", "vostra", 
                    "che", "che cosa", "chi", "dove", "perché", "perche", "come", 
                    "quando", "quale", "ecco", "qui", "qua", "giu", "giù", "li", "lì",
                    "là", "la", "fuori", "sotto", "su", "a", "di", "dentro", "sopra",
                    "da", "con", "lontano", "vicino", "in", "dietro", "per", "davanti", 
                    "fra", "tra", "ancora", "tanto", "tutto", "poco", "altro", "un altro",
                    "un", "uno", "una", "niente", "il", "un po", "anche", "pure", "i", "nessuno",
                    "molto", "lo", "di piu", "di più", "troppo", "del", "della", "dei", "delle",
                    "e", "così", "ma", "quindi", "allora", "se", "voglio", "è", "ho", "sono", 
                    "sei", "posso", "vuoi", "ha", "vuole", "hai", "devo", "devi", "puo", "può", 
                    "deve" ]
    filtered = []
    for word in re.split("\W+", text):
        if (word not in closed_class):
            filtered.append(word)
    return ' '.join(filtered)

def clean_tweets(data):
    nlp = spacy.load("it_core_news_sm")
    all_cleaned = []
    for i in range(len(data['text'])):
        tweet = data['text'][i]
        first = remove_user_ref(tweet)
        second = remove_tags(first)
        third = remove_hyperlinks(second)
        fourth = remove_emoji(third)
        fifth= remove_keywords(fourth)
        sixth = remove_numbers(fifth)
        processed = remove_stopwords(sixth).lower()
        processed = remove_closed_class_words(processed)
        lemmatized = []
        for token in nlp(processed):
            if token.text != ' ':
                lemmatized.append(token.lemma_)
        all_cleaned.append(lemmatized)
    data['cleaned_text'] = all_cleaned
    # remove lines where the tweets are empty after preprocessing
    data = data[data['cleaned_text'].map(lambda d: len(d)) > 0]
    return data

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    data_folder = "data/40wita"
    # data_folder = "data/dummy"
    save_path = 'data/data_df.pickle'
    
    data = read_data(data_folder)
    clean_data = clean_tweets(data)
    save_data(clean_data,save_path)
