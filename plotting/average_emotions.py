import os
import pandas as pd
import pickle 
import numpy as np

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
            row.append(tweets['anger_nrc'].mean() + tweets['anger_emotag'].mean())
            row.append(tweets['anticipation_nrc'].mean() + tweets['anticipation_emotag'].mean())
            row.append(tweets['disgust_nrc'].mean() + tweets['disgust_emotag'].mean())
            row.append(tweets['fear_nrc'].mean() + tweets['fear_emotag'].mean())
            row.append(tweets['joy_nrc'].mean() + tweets['joy_emotag'].mean())
            row.append(tweets['sadness_nrc'].mean() + tweets['sadness_emotag'].mean())
            row.append(tweets['surprise_nrc'].mean() + tweets['surprise_emotag'].mean())
            row.append(tweets['trust_nrc'].mean() + tweets['trust_emotag'].mean())
            row_list.append(row)
        row_list.append([])

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(row_list)
    
    print("Tweets with NRC score:")
    print(len(data.loc[(data['anger_nrc']!=0) || (data['anticipation_nrc']!=0) || (data['disgust_nrc']!=0) ||
             (data['fear_nrc']!=0) || (data['joy_nrc']!=0) || (data['sadness_nrc']!=0) || 
             (data['surprise_nrc']!=0) || (data['trust_nrc']!=0)]))
    print("Tweets with Emotag score:")
    print(len(data.loc[(data['anger_emotag']!=0) || (data['anticipation_emotag']!=0) || (data['disgust_emotag']!=0) ||
             (data['fear_emotag']!=0) || (data['joy_emotag']!=0) || (data['sadness_emotag']!=0) || 
             (data['surprise_emotag']!=0) || (data['trust_emotag']!=0)]))
    print("Tweets woth both scores:")
    print(len(data.loc[((data['anger_nrc']!=0) || (data['anticipation_nrc']!=0) || (data['disgust_nrc']!=0) ||
             (data['fear_nrc']!=0) || (data['joy_nrc']!=0) || (data['sadness_nrc']!=0) || 
             (data['surprise_nrc']!=0) || (data['trust_nrc']!=0)) & ((data['anger_emotag']!=0) || (data['anticipation_emotag']!=0) || (data['disgust_emotag']!=0) ||
             (data['fear_emotag']!=0) || (data['joy_emotag']!=0) || (data['sadness_emotag']!=0) || 
             (data['surprise_emotag']!=0) || (data['trust_emotag']!=0))]))