import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("Zhang_10419_lab3_code")
# Set Up
university_df = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")
university_df.head()
