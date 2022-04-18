import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import numpy as np
import altair as alt
import conda
import os

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib


st.title("Zhang_10419_lab3_code")
# Set Up
university_df = pd.read_csv("https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/qs-world-university-rankings-2017-to-2022-V2.csv")
st.dataframe(university_df)
