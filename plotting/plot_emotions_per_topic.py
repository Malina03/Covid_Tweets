import os
import pandas as pd
import pickle 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

def make_emotions_df_topic(data, topic):
    months = [2,3,4,5,6,7]
    dates = []
    tweets = []
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
        print("loading month " + str(month))
        days = sorted(data[data['month']==month].day.unique())
        # print(days)
        for day in days: 
            dates.append(datetime.strptime('2020-' + str(month) + '-' + str(day), "%Y-%m-%d").date())
            tweets.append(len(data[(data['month']==month) & (data['day']==day) & (data['topics']==topic)]['text']))
            anger_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_anger'].mean())	
            anticipation_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_anticipation'].mean())
            disgust_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_disgust'].mean())
            fear_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_fear'].mean())	
            joy_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_joy'].mean())	
            sadness_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_sadness'].mean())
            surprise_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_surprise'].mean()) 
            trust_emotag.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['emotag_trust'].mean())
            anger_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_anger'].mean())	
            anticipation_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_anticipation'].mean())
            disgust_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_disgust'].mean())
            fear_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_fear'].mean())	
            joy_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_joy'].mean())	
            sadness_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_sadness'].mean())
            surprise_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_surprise'].mean()) 
            trust_nrc.append(data[(data['month']==month) & (data['day']==day)& (data['topics']==topic)]['nrc_trust'].mean())

    emotions = pd.DataFrame({'dates':dates, 'tweets':tweets, 'anger_nrc':anger_nrc, 'anticipation_nrc':anticipation_nrc,
                            'disgust_nrc':disgust_nrc, 'fear_nrc':fear_nrc, 'joy_nrc':joy_nrc, 'sadness_nrc':sadness_nrc,
                            'surprise_nrc':surprise_nrc, 'trust_nrc':trust_nrc, 'anger_emotag':anger_emotag, 'anticipation_emotag':anticipation_emotag,
                            'disgust_emotag':disgust_emotag, 'fear_emotag':fear_emotag, 'joy_emotag':joy_emotag, 'sadness_emotag':sadness_emotag,
                            'surprise_emotag':surprise_emotag, 'trust_emotag':trust_emotag})
    
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

def plot_emotions_topic(emotions, timeline, topic):
    fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(emotions['anger_emotag'].max(), emotions['anticipation_emotag'].max(), emotions['disgust_emotag'].max(), 
                emotions['fear_emotag'].max(), emotions['joy_emotag'].max(), emotions['sadness_emotag'].max(), 
                emotions['surprise_emotag'].max(), emotions['trust_emotag'].max()) + max(emotions['anger_nrc'].max(), 
                emotions['anticipation_nrc'].max(), emotions['disgust_nrc'].max(), emotions['fear_nrc'].max(), emotions['joy_nrc'].max(),
                emotions['sadness_nrc'].max(), emotions['surprise_nrc'].max(), emotions['trust_nrc'].max())
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # ax.scatter(dates, tweets)
    plt.plot(emotions['dates'], emotions['anger_emotag'] + emotions['anger_nrc'], color = 'r', label = "Anger")
    plt.plot(emotions['dates'], emotions['anticipation_emotag']+ emotions['anticipation_nrc'], color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions['dates'], emotions['fear_emotag'] + emotions['fear_nrc'], color = 'tab:olive', label = 'Fear')
    plt.plot(emotions['dates'], emotions['disgust_emotag'] + emotions['disgust_nrc'], color = 'g', label = 'Disgust')
    plt.plot(emotions['dates'], emotions['joy_emotag'] + emotions['joy_nrc'], color = 'tab:pink', label = 'Joy')
    plt.plot(emotions['dates'], emotions['sadness_emotag'] + emotions['sadness_nrc'], color = 'b', label = 'Sadness')
    plt.plot(emotions['dates'], emotions['surprise_emotag'] + emotions['surprise_nrc'], color = 'tab:purple', label ='Surprise')
    plt.plot(emotions['dates'], emotions['trust_emotag'] + emotions['trust_nrc'], color = 'k', label='Trust')

    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Emotions", fontsize=18)
    ax.set_title("Timeline of Emotions associated with " + topic, fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/topics/emotions_' + topic + '.png') 

def compute_polarity_nrc(emotions):
    return emotions['joy_nrc'] + emotions['trust_nrc'] - emotions['anger_nrc'] - emotions['disgust_nrc']- emotions['fear_nrc'] - emotions['sadness_nrc']

def compute_polarity_emotag(emotions):
    return emotions['joy_emotag'] + emotions['trust_emotag'] - emotions['anger_emotag'] - emotions['disgust_emotag']- emotions['fear_emotag'] - emotions['sadness_emotag']

def plot_topic_popularity(popularity, dates, topics):
    colors =  ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    fig, ax = plt.subplots(figsize=(15, 10))
    max_pop = 0
    for i in popularity:
        if i.max() > max_pop:
            max_pop = i.max()
    ylim = max_pop
    plt.ylim = (0, ylim)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    for i in topics:
        plt.plot(dates, popularity[i], color=colors[i], label = topics[i])
    
    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Number of Tweets", fontsize=18)
    ax.set_title("Timeline of the Popularity of Topics", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/topics/topic_timeline.png')

def plot_topic_polarity(polarity, dates, topics, lexicon):
    colors =  ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    fig, ax = plt.subplots(figsize=(15, 10))
    plt.ylim = (-1, 1)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    plt.axhlines(y = 0, color = '0.75')
    for i in topics:
        plt.plot(dates, polarity[i], color=colors[i], label = topics[i])
    
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Polarity", fontsize=18)
    ax.set_title("Timeline of the Polarity of Emotions per Topic using " + lexicon,  fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('results/plots/timelines/topics/polarity_timeline_' + lexicon +'.png') 

if __name__ == "__main__":
    save_path = 'data/data_emo_topics_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    topics = {0:'Covid-19 research', 1:'Covid-19 cases', 2:'Impact on Workers', 3:'Sports', 4:'Politics', 5:'Economy', 6:'Lockdown', 7:'Food', 8:'Arts'}

    popularity = []
    nrc = []
    emotag = []

    for topic in topics.values():

        emotions = make_emotions_df_topic(data, topic)
        print("Loaded df")
        popularity.append(emotions['tweets'])
        dates = emotions['dates']
        nrc.append(compute_polarity_nrc(emotions))
        emotag.append(compute_polarity_emotag(emotions))
       
        timeline = make_timeline_df()
        plot_emotions_topic(emotions, timeline, topic)
    
    plot_topic_popularity(popularity, dates, topics)
    plot_topic_polarity(nrc, dates, topics, 'NRC')
    plot_topic_polarity(emotag, dates, topics, 'Emotag')