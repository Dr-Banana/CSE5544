import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("Zhang_10419_lab3_code")
# Set Up
university_df = pd.read_csv("https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/qs-world-university-rankings-2017-to-2022-V2.csv")
university_df.set_index('country')
st.dataframe(university_df)

duplicateRows = university_df.duplicated(subset=['country'], keep='first')
st.dataframe(~duplicateRows)
from vega_datasets import data

# def draw_map(mtype='Total'):
    
#     COLOR_THEME = {'Total':"lightgreyred"}
    
#     university_df['num'] = university_df[mtype]

#     source = alt.topo_feature(data.world_110m.url, "countries")

#     world_map = (
#         alt.Chart(source, title=f'Countries by nunummber of {mtype} medals')
#         .mark_geoshape(stroke="black", strokeWidth=0.15)
#         .encode(
#             color=alt.Color(
#                 "num:N", 
#                 scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
#                 legend=None),
#             tooltip=[
#                 alt.Tooltip("country:N", title="country"),
#             ],
#         )
#         .transform_lookup(
#             lookup="id",
#             from_=alt.LookupData(olympic_medal_map, "id", ["Team/NOC", "Medals"]),
#         )
#     ).configure_view(strokeWidth=0).properties(width=700, height=400).project("naturalEarth1")
    
#     return world_map
