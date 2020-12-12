import pandas as pd
import pickle


data = pickle.load(open('data/data_df.pickle', 'rb'))

months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
f = open('data/short_overview.txt','w')

for month in months.keys():
    tweets = len(data[data['month']==month]['cleaned_text'])
    max_tweets = 0
    min_tweets = 2000000
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
    
    f.write(f'There are {tweets} for month {months[month]}, collected in {d_number} days, with a daily average of {avg}, a minimum of {min_tweets} and a maximum of {max_tweets}\n')

f.close()