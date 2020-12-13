import os
import pandas as pd
import pickle 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def make_emotions_df(data):
    months = [2,3,4,5,6,7]
    # months = [7]
    dates = []
    tweets = []
    positivity = []
    negativity = [] 
    polarity = []
    anger = []	
    anticipation = []
    disgust	= []
    fear = []	
    joy = []	
    sadness	= []
    surprise = [] 
    trust = []
    for month in months:
        print("plotting month " + str(month))
        days = sorted(data[data['month']==month].day.unique())
        # print(days)
        for day in days: 
            dates.append(datetime.strptime('2020-' + str(month) + '-' + str(day), "%Y-%m-%d").date())
            tweets.append(len(data[(data['month']==month) & (data['day']==day)]['text']))
            positivity.append(data[(data['month']==month) & (data['day']==day)]['positivity'].mean())
            negativity.append(data[(data['month']==month) & (data['day']==day)]['negativity'].mean()) 
            polarity.append(data[(data['month']==month) & (data['day']==day)]['polarity'].mean())
            anger.append(data[(data['month']==month) & (data['day']==day)]['anger'].mean())	
            anticipation.append(data[(data['month']==month) & (data['day']==day)]['anticipation'].mean())
            disgust.append(data[(data['month']==month) & (data['day']==day)]['disgust'].mean())
            fear.append(data[(data['month']==month) & (data['day']==day)]['fear'].mean())	
            joy.append(data[(data['month']==month) & (data['day']==day)]['joy'].mean())	
            sadness.append(data[(data['month']==month) & (data['day']==day)]['sadness'].mean())
            surprise.append(data[(data['month']==month) & (data['day']==day)]['surprise'].mean()) 
            trust.append(data[(data['month']==month) & (data['day']==day)]['trust'].mean())
    positivity = positivity + [0.0] * (len(dates) - len(positivity))
    negativity = negativity + [0.0] * (len(dates) - len(negativity))
    polarity = polarity + [0.0] * (len(dates) - len(polarity))
    anger = anger + [0.0] * (len(dates) - len(anger))
    anticipation = anticipation + [0.0] * (len(dates) - len(anticipation))
    disgust = disgust + [0.0] * (len(dates) - len(disgust))
    fear = fear + [0.0] * (len(dates) - len(fear))
    joy = joy + [0.0] * (len(dates) - len(joy))
    sadness = sadness + [0.0] * (len(dates) - len(sadness))
    surprise = surprise + [0.0] * (len(dates) - len(surprise))
    trust = trust + [0.0] * (len(dates) - len(trust))
    emotions = pd.DataFrame({'dates':dates, 'tweets':tweets, 'positivity':positivity, 'negativity':negativity,
                            'polarity':polarity, 'anger':anger, 'anticipation':anticipation, 'disgust':disgust, 
                            'fear':fear, 'joy':joy, 'sadness':sadness, 'surprise':surprise, 'trust':trust}, 
                            columns = ['dates', 'tweets', 'positivity', 'negativity', 'polarity', 'anger', 
                            'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust'])
    return emotions


def plot_timeline(emotions):
    if len(emotions) == 0:
        return
    months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
    important_dates = np.array([datetime.strptime('2020-02-20', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-02-23', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-03-04', "%Y-%m-%d").date(),
                                # datetime.strptime('2020-03-08', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-09', "%Y-%m-%d").date(),
                                # datetime.strptime('2020-03-11', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-22', "%Y-%m-%d").date(),
                                datetime.strptime('2020-05-04', "%Y-%m-%d").date(),
                                datetime.strptime('2020-06-15', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-07-02', "%Y-%m-%d").date(),
                                datetime.strptime('2020-07-14', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-31', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-05', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-20', "%Y-%m-%d").date()])
    events = np.array(['20th Feb: Third confirmed case', '23rd Feb: Venice Carnival is cancelled', '4th March: Schools and Universities close', 
                        '9th March: Nationwide Lockdown', 
                        '22nd March: Nonessential Factories close', '4th May: Restrictions are relaxed',
                        '15th June: Theatres, Sport Venues, Playgrounds open', '2nd July: European Tourists Allowed',
                        '14th July: Nightclubs reopen','31st March: Peak of the Pandemic announced','5th April: Decrease of Daily Deaths', 
                        '20th April: Decrease of Active Cases'])
    timeline = pd.DataFrame({'date':important_dates, 'event':events}, columns = {'date', 'event'})

    plot_pos_neg(emotions, timeline)

def plot_pos_neg(emotions, timeline):   
    fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(emotions['positivity'].max(), emotions['negativity'].max())
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # ax.scatter(dates, tweets)
    ax.plot(emotions['dates'], emotions['positivity'], color = 'g')
    ax.plot(emotions['dates'], emotions['negativity'], color = 'r')

    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.6')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=16, color = '0.6')
        
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Polarity", fontsize=18)
    ax.set_title("Timeline of Polarity", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.savefig('results/plots/timelines/raw_polarity_timeline.png') 

if __name__ == "__main__":
    # save_path_init = 'data/data_df.pickle'
    # save_path_emo = 'data/data_emosen_df.pickle'

    save_path_init = 'data/dummy_df.pickle'
    save_path_emo = 'data/dummy_emosen_df.pickle'

    data = pickle.load(open(save_path_emo, 'rb'))

    emotions = make_emotions_df(data)
    plot_timeline(emotions)