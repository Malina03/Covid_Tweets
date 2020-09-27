from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import re
import string
import os
import pandas as pd

example = '40wita_2020-07-19.csv.bz2'

def read_data(folder):
    data = {}
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            data[f] = pd.read_csv(full_path, delimiter=',')
    return data

def remove_hyperlinks(text):
    return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)

def remove_keywords(text):
    keywords = ['covid', 'covid19', 'covid-19', 'corona virus', 'coronavirus', 'quarantena', 
                'autoisolamento', 'auto-isolamento', 'iorestoacasa', 'stateacasa', 'COVID19Italia',
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
    # print("before stop words " + text)
    stop_words = set(stopwords.words('italian')) 
    # word_tokens = word_tokenize(text)
    # filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = []
    for w in re.split("\W+", text):
        if not w.lower() in stop_words:
            filtered_sentence.append(w)
    return ' '.join(filtered_sentence)

def remove_numbers(text):
    return ''.join(letter for letter in text if not letter.isdigit())

def clean_tweets(data):
    # for folder in data: 
    #     for tweet in data[folder]['text']:
    #         processed = remove_hyperlinks(tweet).lower()

    for tweet in data[example]['text']:
        # print("before " + tweet)
        first = remove_user_ref(tweet)
        second = remove_tags(first)
        third = remove_hyperlinks(second)
        fourth = remove_emoji(third)
        fifth= remove_keywords(fourth)
        sixth = remove_numbers(fifth)
        processed = remove_stopwords(sixth).lower()
        print("after " + processed)


if __name__ == "__main__":
    dummy = 'data/dummy'
    
    data = read_data(dummy)
    clean_tweets(data)





