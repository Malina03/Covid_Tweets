import os
import pandas as pd
import pickle 
import numpy as np
import csv

if __name__ == "__main__":
    save_path = 'data/data_emo_topics_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    topics = {0:'Covid-19 research', 1:'Covid-19 cases', 2:'Impact on Workers', 3:'Sports', 4:'Politics', 5:'Economy', 6:'Lockdown', 7:'Food', 8:'Arts'}
    months = {2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July'}

    csv_path = 'results/emotions_topics.csv'

    row_list = []
    header = ['', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust'] 

    for topic in topics.values():
        row_list.append([topic])
        row_list.append(header)
        for month in months.keys():
            row = []
            row.append(months[month])
            tweets = data.loc[(data['month'] == month) & (data['topics']==topic)]
            row.append(tweets['nrc_anger'].mean() + tweets['emotag_anger'].mean())
            row.append(tweets['nrc_anticipation'].mean() + tweets['emotag_anticipation'].mean())
            row.append(tweets['nrc_disgust'].mean() + tweets['emotag_disgust'].mean())
            row.append(tweets['nrc_fear'].mean() + tweets['emotag_fear'].mean())
            row.append(tweets['nrc_joy'].mean() + tweets['emotag_joy'].mean())
            row.append(tweets['nrc_sadness'].mean() + tweets['emotag_sadness'].mean())
            row.append(tweets['nrc_surprise'].mean() + tweets['emotag_surprise'].mean())
            row.append(tweets['nrc_trust'].mean() + tweets['emotag_trust'].mean())
            row_list.append(row)
        row_list.append([])

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(row_list)
    
    print("Tweets with NRC score:")
    print(len(data.loc[(data['nrc_anger']!=0) | (data['nrc_anticipation']!=0) | (data['nrc_disgust']!=0) |
             (data['nrc_fear']!=0) | (data['nrc_joy']!=0) | (data['nrc_sadness']!=0) | 
             (data['nrc_surprise']!=0) | (data['nrc_trust']!=0)]))
    print("Tweets with Emotag score:")
    print(len(data.loc[(data['emotag_anger']!=0) | (data['emotag_anticipation']!=0) | (data['emotag_disgust']!=0) |
             (data['emotag_fear']!=0) | (data['emotag_joy']!=0) | (data['emotag_sadness']!=0) | 
             (data['emotag_surprise']!=0) | (data['emotag_trust']!=0)]))
    print("Tweets woth both scores:")
    print(len(data.loc[((data['nrc_anger']!=0) | (data['nrc_anticipation']!=0) | (data['nrc_disgust']!=0) |
             (data['nrc_fear']!=0) | (data['nrc_joy']!=0) | (data['nrc_sadness']!=0) | 
             (data['nrc_surprise']!=0) | (data['nrc_trust']!=0)) & ((data['emotag_anger']!=0) | (data['emotag_anticipation']!=0) | (data['emotag_disgust']!=0) |
             (data['emotag_fear']!=0) | (data['emotag_joy']!=0) | (data['emotag_sadness']!=0) | 
             (data['emotag_surprise']!=0) | (data['emotag_trust']!=0))]))