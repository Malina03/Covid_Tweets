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
    expected_dtypes = {'id': 'int64', 'text': object, 'language': object, 'screen_name': object, 'date': object, 
                        'timestamp': 'int64', 'year': 'int64', 'month': 'int64', 'day': 'int64', 'hour': 'int64', 'lat': 'float64',
                        'lon': 'float64', 'location_json': object, 'location': object, 'source': object, 'urls': object, 
                        'description': object, 'statuses_count': 'int64', 'followers_count': 'int64', 'friends_count': 'int64',
                        'media': object}
    flag = 0
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if f in errors:
            continue
        if os.path.isfile(full_path):
            folder_data = pd.read_csv(full_path, dtype = expected_dtypes, delimiter=',')
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

def clean_tweet(tweet, nlp):
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
        lemma = token.lemma_
        if lemma != ' ' and lemma != '_':
            lemmatized.append(lemma.replace("_", ""))
    return lemmatized

def makde_df_and_raw_file(data):
    doc_path = 'data/SeaNMF'
    nlp = spacy.load("it_core_news_sm")
    all_cleaned = []
    counter = 0
    total  = len(data['text'])

    months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
    # months = {7:'july'}

    for month in months.keys(): 
        fname = 'raw_data_' + months[month] + '.txt' 
        path = os.path.join(doc_path, months[month])
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path ,fname), 'w')  
        for tweet in data['text'][data['month']==month].values:
            if counter % 10000 == 0:
                print("cleaned " + str(counter/total)[0:5] + "% of tweets")
            lemmatized = clean_tweet(tweet, nlp)
            all_cleaned.append(lemmatized)
            if len(lemmatized) > 0 :
                f.write(' '.join(lemmatized) + '\n')
            counter += 1
    data['cleaned_text'] = all_cleaned
    data = data[data['cleaned_text'].map(lambda d: len(d)) > 0]
    f.close()
    return data

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    data_folder = "data/40wita"
    # data_folder = "data/dummy"
    save_path = 'data/data_df.pickle'
    
    data = read_data(data_folder)
    clean_data = makde_df_and_raw_file(data)
    save_data(clean_data,save_path)
