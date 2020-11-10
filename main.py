import os
import pickle

if __name__ == "__main__":
    data_folder = "data/40wita"
    save_path = 'data/data_df.pickle'
    
    with open(save_path, 'rb') as save:
        data = pickle.load(save)

    