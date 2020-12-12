import pandas as pd
import pickle
from preprocess import read_data


data = pickle.load(open('data/data_df.pickle', 'rb'))

months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
f = open('data/short_overview.txt','w')

orig_data = read_data('data/40wita')
total_after_clean = 0
total_before_clean = 0
for month in months.keys():
    tweets = len(data[data['month']==month]['cleaned_text'])
    total_after_clean += tweets
    orig_tweets = len(orig_data[orig_data['month']==month]['text'])
    total_before_clean += orig_tweets
    max_tweets = 0
    min_tweets = 2000000
    orig_days = len(sorted(orig_data[orig_data['month']==month].day.unique()))
    days = sorted(data[data['month']==month].day.unique())

    for day in days:
        twts = len(data[(data['month']==month) & (data['day']==day)]['cleaned_text'])
        if twts > max_tweets:
            max_tweets = twts
        if twts < min_tweets:
            min_tweets = twts

    d_number = len(days)

    if d_number != 0:
        avg = float(tweets)/float(d_number)
    else:
        avg = 0

    if min_tweets == 2000000:
        min_tweets = 0
    
    f.write(f'In {months[month]} there were {orig_tweets} tweets before preprocessing, collected in {orig_days} days and 
            afterwerds there were {tweets} tweets left, collected in {d_number} days, with a daily average of {avg}, 
            a minimum of {min_tweets} and a maximum of {max_tweets}\n')
f.write(f'In total there were {total_before_clean} before preprocessring and {total_after_clean} were left afterwards.\n')
f.close()