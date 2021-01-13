import os
import pandas as pd
import pickle 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

if __name__ == "__main__":
    save_path = 'data/data_emo_topics_df.pickle'

    data = pickle.load(open(save_path, 'rb'))
    