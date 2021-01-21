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
                                datetime.strptime('2020-03-09', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-22', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-31', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-05', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-20', "%Y-%m-%d").date(),
                                datetime.strptime('2020-05-04', "%Y-%m-%d").date(),
                                datetime.strptime('2020-06-15', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-07-02', "%Y-%m-%d").date(),
                                datetime.strptime('2020-07-14', "%Y-%m-%d").date()])
    events = np.array(['20th Feb: Third confirmed case', '23rd Feb: Venice Carnival is cancelled', '4th March: Schools and Universities close', 
                        '9th March: Nationwide Lockdown', '22nd March: Nonessential Factories close', '31st March: Peak of the Pandemic announced',
                        '5th April: Decrease of Daily Deaths', '20th April: Decrease of Active Cases','4th May: Restrictions are relaxed',
                        '15th June: Theatres, Sport Venues, Playgrounds open', '2nd July: European Tourists Allowed',
                        '14th July: Nightclubs reopen',])
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
    plt.plot(emotions.loc[emotions['anger_emotag'] + emotions['anger_nrc'] !=0]['dates'], emotions.loc[emotions['anger_emotag'] + emotions['anger_nrc'] !=0]['anger_emotag'] + emotions.loc[emotions['anger_emotag'] + emotions['anger_nrc'] !=0]['anger_nrc'], color = 'r', label = "Anger")
    plt.plot(emotions.loc[emotions['anticipation_emotag'] + emotions['anticipation_nrc'] !=0]['dates'], emotions.loc[emotions['anticipation_emotag'] + emotions['anticipation_nrc'] !=0]['anticipation_emotag']+ emotions.loc[emotions['anticipation_emotag'] + emotions['anticipation_nrc'] !=0]['anticipation_nrc'], color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions.loc[emotions['fear_emotag'] + emotions['fear_nrc'] !=0]['dates'], emotions.loc[emotions['fear_emotag'] + emotions['fear_nrc'] !=0]['fear_emotag'] + emotions.loc[emotions['fear_emotag'] + emotions['fear_nrc'] !=0]['fear_nrc'], color = 'tab:olive', label = 'Fear')
    plt.plot(emotions.loc[emotions['disgust_emotag'] + emotions['disgust_nrc'] !=0]['dates'], emotions.loc[emotions['disgust_emotag'] + emotions['disgust_nrc'] !=0]['disgust_emotag'] + emotions.loc[emotions['disgust_emotag'] + emotions['disgust_nrc'] !=0]['disgust_nrc'], color = 'g', label = 'Disgust')
    plt.plot(emotions.loc[emotions['joy_emotag'] + emotions['joy_nrc'] !=0]['dates'], emotions.loc[emotions['joy_emotag'] + emotions['joy_nrc'] !=0]['joy_emotag'] + emotions.loc[emotions['joy_emotag'] + emotions['joy_nrc'] !=0]['joy_nrc'], color = 'tab:pink', label = 'Joy')
    plt.plot(emotions.loc[emotions['sadness_emotag'] + emotions['sadness_nrc'] !=0]['dates'], emotions.loc[emotions['sadness_emotag'] + emotions['sadness_nrc'] !=0]['sadness_emotag'] + emotions.loc[emotions['sadness_emotag'] + emotions['sadness_nrc'] !=0]['sadness_nrc'], color = 'b', label = 'Sadness')
    plt.plot(emotions.loc[emotions['surprise_emotag'] + emotions['surprise_nrc'] !=0]['dates'], emotions.loc[emotions['surprise_emotag'] + emotions['surprise_nrc'] !=0]['surprise_emotag'] + emotions.loc[emotions['surprise_emotag'] + emotions['surprise_nrc'] !=0]['surprise_nrc'], color = 'tab:purple', label ='Surprise')
    plt.plot(emotions.loc[emotions['trust_emotag'] + emotions['trust_nrc'] !=0]['dates'], emotions.loc[emotions['trust_emotag'] + emotions['trust_nrc'] !=0]['trust_emotag'] + emotions.loc[emotions['trust_emotag'] + emotions['trust_nrc'] !=0]['trust_nrc'], color = 'k', label='Trust')

      
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
        plt.text(timeline['date'][i], ylim - ylim/100, letters[i], rotation = 90, verticalalignment='center', fontsize=15, color='0.75')
           
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Emotions", fontsize=18)
    ax.set_title("Timeline of Emotions associated with " + topic, fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend(loc = 'best')
    plt.savefig('results/plots/timelines/topics/emotions_' + topic + '.png') 

def compute_polarity_nrc(emotions):
    return emotions['joy_nrc'] + emotions['trust_nrc'] - emotions['anger_nrc'] - emotions['disgust_nrc']- emotions['fear_nrc'] - emotions['sadness_nrc']

def compute_polarity_emotag(emotions):
    return emotions['joy_emotag'] + emotions['trust_emotag'] - emotions['anger_emotag'] - emotions['disgust_emotag']- emotions['fear_emotag'] - emotions['sadness_emotag']

def plot_topic_popularity(popularity, dates, timeline, topics):
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
    
    for i in topics.keys():
        plt.plot(dates, popularity[i], color=colors[i], label = topics[i])
    
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
        plt.text(timeline['date'][i], ylim - ylim/100, letters[i], rotation = 90, verticalalignment='center', fontsize=15, color='0.75')
       
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Number of Tweets", fontsize=18)
    ax.set_title("Timeline of the Popularity of Topics", fontsize=20)
    plt.gcf().autofmt_dxate()
    plt.legend(loc = 'best')
    plt.savefig('results/plots/timelines/topics/topic_timeline.png')

def plot_topic_polarity(polarity, dates, topics, timeline, lexicon):
    colors =  ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    fig, ax = plt.subplots(figsize=(15, 10))
    

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    plt.hlines(y = 0, xmin = dates[0], xmax = dates[len(dates)-1], color = '0.75')
    ymax = -10
    ymin = 10
    for i in topics.keys():
        plt.plot(dates, polarity[i], color=colors[i], label = topics[i])
        if max(polarity[i]) > ymax :
            ymax = max(polarity[i])
        if min(polarity[i]) < ymin :
            ymin = min(polarity[i])
    plt.ylim = (ymin, ymax)
    
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=ymin, ymax=ymax, color = '0.75')
        plt.text(timeline['date'][i], ymin, timeline['event'][i], rotation=90, verticalalignment='bottom', fontsize=15, color = '0.6')
        plt.text(timeline['date'][i], ymax, letters[i], rotation = 90, verticalalignment='top', fontsize=15, color='0.75')

    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Polarity", fontsize=18)
    ax.set_title("Timeline of the Polarity of Emotions per Topic using " + lexicon,  fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.legend(loc='best')
    plt.savefig('results/plots/timelines/topics/polarity_timeline_' + lexicon +'.png') 

def print_topic_popularity(data, topics):
    print("entered function")
    months = [2,3,4,5,6,7]
    for month in months:
        print(month)
        for topic in topics.values():
            if topic in data[data['month']==month]['topics'].values:
                print(topic + " " + str(len(data[(data['month']==month) & (data['topics']==topic)]['text'])/len(data[data['month']==month]['text'])))


def plot_emotion_dist(data, topic):
    timeline = make_timeline_df()
    months = [2,3,4,5,6,7]
    dates = []
    anger= []	
    anticipation = []
    disgust = []
    fear = []	
    joy = []	
    sadness	= []
    surprise = [] 
    trust = []
    
    for month in months:
        print("loading month " + str(month))
        days = sorted(data[data['month']==month].day.unique())
        # print(days)
        for day in days: 
            dates.append(datetime.strptime('2020-' + str(month) + '-' + str(day), "%Y-%m-%d").date())
            rows = data.loc[(data['month']==month) & (data['day']==day) & (data['topics']==topic)]
            tweets=len(rows['text'])
            anger.append(len(rows[(rows['emotag_anger'] > 0) | (rows['nrc_anger'] > 0)])/tweets)	
            anticipation.append(len(rows[(rows['emotag_anticipation'] > 0) | (rows['nrc_anticipation'] > 0)])/tweets)
            disgust.append(len(rows[(rows['emotag_disgust'] > 0) | (rows['nrc_disgust'] > 0)])/tweets)
            fear.append(len(rows[(rows['emotag_fear'] > 0) | (rows['nrc_fear'] > 0)])/tweets)	
            joy.append(len(rows[(rows['emotag_joy'] > 0) | (rows['nrc_joy'] > 0)])/tweets)	
            sadness.append(len(rows[(rows['emotag_sadness'] > 0) | (rows['nrc_sadness'] > 0)])/tweets)
            surprise.append(len(rows[(rows['emotag_surprise'] > 0) | (rows['nrc_surprise'] > 0)])/tweets) 
            del rows

    emotions = pd.DataFrame({'dates':dates, 'anger':anger, 'anticipation':anticipation,
                            'disgust':disgust, 'fear':fear, 'joy':joy, 'sadness':sadness,
                            'surprise':surprise, 'trust':trust})
    
    colors =  ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    fig, ax = plt.subplots(figsize=(15, 10))
    ylim =  max(emotions['anger'].max(), emotions['anticipation'].max(), emotions['disgust'].max(), 
            emotions['fear'].max(), emotions['joy'].max(), emotions['sadness'].max(), 
            emotions['surprise'].max(), emotions['trust'].max())
    plt.ylim = (0, ylim)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    plt.plot(emotions['dates'], emotions['anger'], color = 'r', label = "Anger")
    plt.plot(emotions['dates'], emortions['anticipation'], color = 'tab:orange', label = 'Anticipation')
    plt.plot(emotions['dates'], emotions['fear'], color = 'tab:olive', label = 'Fear')
    plt.plot(emotions['dates'], emotions['disgust'], color = 'g', label = 'Disgust')
    plt.plot(emotions['dates'], emotions['joy'], label = 'Joy')
    plt.plot(emotions['dates'], emotions['sadness'], color = 'b', label = 'Sadness')
    plt.plot(emotions['dates'], emotions['surprise'], color = 'tab:purple', label ='Surprise')
    plt.plot(emotions['dates'], emotions['trust'], color = 'k', label='Trust')

    
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L']
    for i in range(len(timeline['date'])): 
        plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = '0.75')
        plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=15, color = '0.6')
        plt.text(timeline['date'][i], ylim - ylim/100, letters[i], rotation = 90, verticalalignment='top', fontsize=15, color='0.75')
       
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Percentage of tweets", fontsize=18)
    ax.set_title("Distribution of Emotions for the Covid-19 Cases Topic", fontsize=20)
    plt.gcf().autofmt_dxate()
    plt.legend(loc = 'best')
    plt.savefig('results/plots/timelines/topics/emotion_distribution.png')

if __name__ == "__main__":
    save_path = 'data/data_emo_topics_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    topics = {0:'Covid-19 research', 1:'Covid-19 cases', 2:'Sports', 3:'Politics', 4:'Economy', 5:'Lockdown', 6:'Food', 7:'Arts'}

    # popularity = []
    # nrc = []
    # emotag = []

    # print_topic_popularity(data, topics)
    plot_emotion_dist(data, topics[0])

    # for topic in topics.values():

    #     emotions = make_emotions_df_topic(data, topic)
    #     print("Loaded df")
        # popularity.append(emotions['tweets'])
        # dates = emotions['dates']
        # nrc.append(compute_polarity_nrc(emotions))
        # emotag.append(compute_polarity_emotag(emotions))
       
        # timeline = make_timeline_df()
        # plot_emotions_topic(emotions, timeline, topic)
    
    # plot_topic_popularity(popularity, dates, timeline, topics)
    # plot_topic_polarity(nrc, dates, topics, timeline, 'NRC')
    # plot_topic_polarity(emotag, dates, topics, timeline, 'Emotag')