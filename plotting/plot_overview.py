import os
import pandas as pd
import pickle 
import numpy as np

def plot_tweets_per_day(data):
    dates = np.zeros(data.date.unique)
    tweet_no = np.zeros(data.date.unique)

if __name__ == "__main__":
    save_path = 'data/data_df.pickle'
    data = pickle.load(open(save_path, 'rb'))
    
