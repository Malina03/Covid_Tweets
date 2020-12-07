import os
import pickle
import pandas as pd
import gzip
import sys
sys.path.append(os.getcwd())

def save_data(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

