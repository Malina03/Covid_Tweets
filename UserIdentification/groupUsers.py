import pickle
import pandas as pd
import twitter


if __name__ == "__main__":
    # data_folder = "data/40wita"
    # save_path = 'data/data_df.pickle'
    
    data_folder = "data/dummy"
    save_path = 'data/dummy_df.pickle'
    
    data = pickle.load(open(save_path,'rb'))

    api = twitter.Api(consumer_key=[consumer key],
                  consumer_secret=[consumer secret],
                  access_token_key=[access token],
                  access_token_secret=[access token secret])

    print(data.columns)
    
    print(data['screen_name'])