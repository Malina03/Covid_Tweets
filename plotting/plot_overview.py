import os
import pandas as pd
import pickle 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_tweets_per_day(data):
    months = [2,3,4,5,6,7]
    # months = [7]
    for month in months:
        print("plotting month " + str(month))
        dates = []
        tweets = []
        days = data[data['month']==month].day.unique()
        # print(days)
        for day in days: 
            dates.append(datetime.strptime('2020-' + str(month) + '-' + str(day), "%Y-%m-%d").date())
            tweets.append(len(data[(data['month']==month) & (data['day']==day)]['text']))
        plot_monthly_timeline(dates, tweets, month)
    
def plot_monthly_timeline(dates, tweets, month):
    if len(tweets) == 0:
        return
    months = {2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july'}
    important_dates = np.array([datetime.strptime('2020-02-20', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-02-23', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-03-04', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-08', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-09', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-11', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-22', "%Y-%m-%d").date(),
                                datetime.strptime('2020-05-04', "%Y-%m-%d").date(),
                                datetime.strptime('2020-06-15', "%Y-%m-%d").date(), 
                                datetime.strptime('2020-07-02', "%Y-%m-%d").date(),
                                datetime.strptime('2020-07-14', "%Y-%m-%d").date(),
                                datetime.strptime('2020-03-31', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-05', "%Y-%m-%d").date(),
                                datetime.strptime('2020-04-20', "%Y-%m-%d").date()])
    events = np.array(['Third confirmed case', 'Venice Carnival is cancelled', 'Schools and Universities close', 
                        'Lockdown in Northern Italy', 'Nationwide Lockdown', 'Restaurants and Bars close',
                        'Nonessential Factories close', 'Restrictions are relaxed',
                        'Theatres, Sporting Venues, Playgrounds open', 'European Tourists Allowed',
                        'Nightclubs reopen','Peak of the Pandemic announced','Decrease of Daily Deaths', 
                        'Decrease of Active Cases'])
    timeline = pd.DataFrame({'date':important_dates, 'event':events}, columns = {'date', 'event'})
    

    fig, ax = plt.subplots(figsize=(15, 10))
    ylim = max(tweets)
    plt.ylim = (0, ylim)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    ax.scatter(dates, tweets)

    m = str('-0' + str(month) + '-')
    for i in range(len(timeline['date'])): 
        if m in timeline['date'][i].strftime("%Y-%m-%d"):
            plt.vlines(x=timeline['date'][i], ymin=0, ymax=ylim, color = 'r')
            plt.text(timeline['date'][i], ylim/2, timeline['event'][i], rotation=90, verticalalignment='center', fontsize=16)
        
    ax.set_xlabel("Dates", fontsize=18)
    ax.set_ylabel("Number of Tweets", fontsize=18)
    ax.set_title("Timeline of the Tweet Corpus", fontsize=20)
    plt.gcf().autofmt_xdate()
    plt.savefig('results/plots/timelines/timeline_' + months[month] + '.png')    

if __name__ == "__main__":
    save_path = 'data/data_df.pickle'
    # save_path = 'data/dummy_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    plot_tweets_per_day(data)
    
