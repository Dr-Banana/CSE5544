import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.rcParams['axes.edgecolor']='#FA6E4F'
plt.rcParams['font.family'] = 'monospace'
import seaborn as sns
import geopandas as gpd

import warnings
warnings.filterwarnings("ignore")

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

university_df = pd.read_csv('../input/qs-world-university-rankings-2017-2022/qs-world-university-rankings-2017-to-2022-V2.csv')
