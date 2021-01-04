import os
import pandas as pd
import pickle 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

def make_emotions_df(data):
    months = [2,3,4,5,6,7]
    # months = [7]
    dates = []
    tweets = []
    # positivity = []
    # negativity = [] 
    # polarity = []
    anger_emotag = []	
    anticipation_emotag = []
    disgust_emotag = []
    fear_emotag = []	
    joy_emotag = []	
    sadness_emotag	= []
    surprise_emotag = [] 
    trust_emotag = []
    anger_nrc = []	
    anticipation_nrc = []
    disgust_nrc = []
    fear_nrc = []	
    joy_nrc = []	
    sadness_nrc	= []
    surprise_nrc = [] 
    trust_nrc = []
    for month in months:
        print("plotting month " + str(month))
        days = sorted(data[data['month']==month].day.unique())
        # print(days)
        for day in days: 
            dates.append(datetime.strptime('2020-' + str(month) + '-' + str(day), "%Y-%m-%d").date())
            tweets.append(len(data[(data['month']==month) & (data['day']==day)]['text']))
            # positivity.append(data[(data['month']==month) & (data['day']==day)]['positivity'].mean())
            # negativity.append(data[(data['month']==month) & (data['day']==day)]['negativity'].mean()) 
            # polarity.append(data[(data['month']==month) & (data['day']==day)]['polarity'].mean())
            anger_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_anger'].mean())	
            anticipation_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_anticipation'].mean())
            disgust_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_disgust'].mean())
            fear_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_fear'].mean())	
            joy_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_joy'].mean())	
            sadness_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_sadness'].mean())
            surprise_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_surprise'].mean()) 
            trust_emotag.append(data[(data['month']==month) & (data['day']==day)]['emotag_trust'].mean())
            anger_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_anger'].mean())	
            anticipation_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_anticipation'].mean())
            disgust_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_disgust'].mean())
            fear_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_fear'].mean())	
            joy_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_joy'].mean())	
            sadness_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_sadness'].mean())
            surprise_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_surprise'].mean()) 
            trust_nrc.append(data[(data['month']==month) & (data['day']==day)]['nrc_trust'].mean())
    # positivity = positivity + [0.0] * (len(dates) - len(positivity))
    # negativity = negativity + [0.0] * (len(dates) - len(negativity))
    # polarity = polarity + [0.0] * (len(dates) - len(polarity))
    anger_emotag = anger_emotag + [0.0] * (len(dates) - len(anger_emotag))
    anticipation_emotag = anticipation_emotag + [0.0] * (len(dates) - len(anticipation_emotag))
    disgust_emotag = disgust_emotag + [0.0] * (len(dates) - len(disgust_emotag))
    fear_emotag = fear_emotag + [0.0] * (len(dates) - len(fear_emotag))
    joy_emotag = joy_emotag + [0.0] * (len(dates) - len(joy_emotag))
    sadness_emotag = sadness_emotag + [0.0] * (len(dates) - len(sadness_emotag))
    surprise_emotag = surprise_emotag + [0.0] * (len(dates) - len(surprise_emotag))
    trust_emotag = trust_emotag + [0.0] * (len(dates) - len(trust_emotag))
    anger_nrc = anger_nrc + [0.0] * (len(dates) - len(anger_nrc))
    anticipation_nrc = anticipation_nrc + [0.0] * (len(dates) - len(anticipation_nrc))
    disgust_nrc = disgust_nrc + [0.0] * (len(dates) - len(disgust_nrc))
    fear_nrc = fear_nrc + [0.0] * (len(dates) - len(fear_nrc))
    joy_nrc = joy_nrc + [0.0] * (len(dates) - len(joy_nrc))
    sadness_nrc = sadness_nrc + [0.0] * (len(dates) - len(sadness_nrc))
    surprise_nrc = surprise_nrc + [0.0] * (len(dates) - len(surprise_nrc))
    trust_nrc = trust_nrc + [0.0] * (len(dates) - len(trust_nrc))
    emotions = pd.DataFrame({'dates':dates, 'tweets':tweets, 'anger_nrc':anger_nrc, 'anticipation_nrc':anticipation_nrc,
                            'disgust_nrc':disgust_nrc, 'fear_nrc':fear_nrc, 'joy_nrc':joy_nrc, 'sadness_nrc':sadness_nrc,
                            'surprise_nrc':surprise_nrc, 'trust_nrc':trust_nrc, 'anger_emotag':anger_emotag, 'anticipation_emotag':anticipation_emotag,
                            'disgust_emotag':disgust_emotag, 'fear_emotag':fear_emotag, 'joy_emotag':joy_emotag, 'sadness_emotag':sadness_emotag,
                            'surprise_emotag':surprise_emotag, 'trust_emotag':trust_emotag}, 
                            columns = ['dates', 'tweets', 'anger_nrc', 'anticipation_nrc', 'disgust_nrc', 'fear_nrc', 'joy_nrc', 
                            'sadness_nrc', 'surprise_nrc', 'trust_nrc', 'anger_emotag', 'anticipation_emotag', 'disgust_emotag', 'fear_emotag', 'joy_emotag', 
                            'sadness_emotag', 'surprise_emotag', 'trust_emotag'])
    return emotions


def make_timeline_df():
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
    return timeline

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

def plot_emotions_nrc(emotions, timeline):
    fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(emotions['anger_nrc'].max(), emotions['anticipation_nrc'].max(), emotions['disgust_nrc'].max(), 
                emotions['fear_nrc'].max(), emotions['joy_nrc'].max(), emotions['sadness_nrc'].max(), 
                emotions['surprise_nrc'].max(), emotions['trust_nrc'].max())
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # ax.scatter(dates, tweets)
    plt.plot(emotions['dates'], emotions['anger_nrc'], color = 'r', label = "Anger")
    plt.plot(emotions['dates'], emotions['anticipation_nrc'], color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions['dates'], emotions['fear_nrc'], color = 'tab:olive', label = 'Fear')
    plt.plot(emotions['dates'], emotions['disgust_nrc'], color = 'g', label = 'Disgust')
    plt.plot(emotions['dates'], emotions['joy_nrc'], color = 'tab:pink', label = 'Joy')
    plt.plot(emotions['dates'], emotions['sadness_nrc'], color = 'b', label = 'Sadness')
    plt.plot(emotions['dates'], emotions['surprise_nrc'], color = 'tab:purple', label ='Surprise')
    plt.plot(emotions['dates'], emotions['trust_nrc'], color = 'k', label='Trust')

    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Emotions", fontsize=18)
    ax.set_title("Timeline of Emotions detected using the NRC Lexicon", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/nrc_emotions_timeline.png') 

def plot_emotions_emotag(emotions, timeline):
    fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(emotions['anger_emotag'].max(), emotions['anticipation_emotag'].max(), emotions['disgust_emotag'].max(), 
                emotions['fear_emotag'].max(), emotions['joy_emotag'].max(), emotions['sadness_emotag'].max(), 
                emotions['surprise_emotag'].max(), emotions['trust_emotag'].max())
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # ax.scatter(dates, tweets)
    plt.plot(emotions['dates'], emotions['anger_emotag'], color = 'r', label = "Anger")
    plt.plot(emotions['dates'], emotions['anticipation_emotag'], color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions['dates'], emotions['fear_emotag'], color = 'tab:olive', label = 'Fear')
    plt.plot(emotions['dates'], emotions['disgust_emotag'], color = 'g', label = 'Disgust')
    plt.plot(emotions['dates'], emotions['joy_emotag'], color = 'tab:pink', label = 'Joy')
    plt.plot(emotions['dates'], emotions['sadness_emotag'], color = 'b', label = 'Sadness')
    plt.plot(emotions['dates'], emotions['surprise_emotag'], color = 'tab:purple', label ='Surprise')
    plt.plot(emotions['dates'], emotions['trust_emotag'], color = 'k', label='Trust')

    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Emotions", fontsize=18)
    ax.set_title("Timeline of Emotions detected using the Emotag Lexicon", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/emotag_emotions_timeline.png') 

plot_emotions_mean(emotions, timeline):
       fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(emotions['anger_emotag'].max(), emotions['anticipation_emotag'].max(), emotions['disgust_emotag'].max(), 
                emotions['fear_emotag'].max(), emotions['joy_emotag'].max(), emotions['sadness_emotag'].max(), 
                emotions['surprise_emotag'].max(), emotions['trust_emotag'].max(), emotions['anger_nrc'].max(), emotions['anticipation_nrc'].max(), emotions['disgust_nrc'].max(), 
                emotions['fear_nrc'].max(), emotions['joy_nrc'].max(), emotions['sadness_nrc'].max(), 
                emotions['surprise_nrc'].max(), emotions['trust_nrc'].max())
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # ax.scatter(dates, tweets)
    plt.plot(emotions['dates'], emotions[['anger_emotag', 'anger_nrc']].mean(axis=1).values, color = 'r', label = "Anger")
    plt.plot(emotions['dates'], emotions[['anticipation_emotag','anticipation_nrc']].mean(axis=1).values, color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions['dates'], emotions[['fear_emotag','fear_nrc']].mean(axis=1).values, color = 'tab:olive', label = 'Fear')
    plt.plot(emotions['dates'], emotions[['disgust_emotag','disgust_nrc']].mean(axis=1).values, color = 'g', label = 'Disgust')
    plt.plot(emotions['dates'], emotions[['joy_emotag', 'joy_nrc']].mean(axis=1).values, color = 'tab:pink', label = 'Joy')
    plt.plot(emotions['dates'], emotions[['sadness_emotag', 'sadness_nrc']].mean(axis=1).values, color = 'b', label = 'Sadness')
    plt.plot(emotions['dates'], emotions[['surprise_emotag', 'surprise_nrc']].mean(axis=1).values, color = 'tab:purple', label ='Surprise')
    plt.plot(emotions['dates'], emotions[['trust_emotag', 'trust_nrc']].mean(axis=1).values, color = 'k', label='Trust')

    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Emotions", fontsize=18)
    ax.set_title("Timeline of Averaged Emotions detected by NRC and Emotag Lexicons", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/mean_emotions_timeline.png') 


if __name__ == "__main__":
    # save_path_init = 'data/data_df.pickle'
    # save_path_emo = 'data/data_emosen_df.pickle'

    save_path_emo = 'data/dummy_emosen_df.pickle'

    data = pickle.load(open(save_path_emo, 'rb'))

    emotions = make_emotions_df(data)
    print("Loaded df")
    timeline = make_timeline_df()
    print("Made timeline df")
    plot_emotions_emotag(emotions,timeline)
    print("Plotted emotag")
    plot_emotions_nrc(emotions, timeline)
    print("Plotted nrc")
    plot_emotions_mean(emotions, timeline)
    print("Plotted mean")