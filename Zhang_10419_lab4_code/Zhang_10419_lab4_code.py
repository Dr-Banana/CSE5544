import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt


# Set Up
# university_df = pd.read_csv("https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/qs-world-university-rankings-2017-to-2022-V2.csv")
#Country codes are needed for building map visualization in Altair
country_codes = pd.read_csv('https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/country_codes.csv' ,sep=',', encoding='latin-1')
country_codes.set_index('English short name', inplace = True)


#Reading file 
university_df = pd.read_csv('https://raw.githubusercontent.com/Dr-Banana/CSE5544/main/Zhang_10419_lab4_code/qs-world-university-rankings-2017-to-2022-V2.csv' ,sep=',', encoding='latin-1')


d = pd.DataFrame(university_df.pivot_table(columns=['country'], aggfunc='size'))
d.columns = ['count']
d['id'] = country_codes['Numeric']
d['country'] = d.index
st.dataframe(d)

from vega_datasets import data

def draw_map(mtype='count'):
    
    COLOR_THEME = {'count':"lightgreyred"}
    d['num'] = d[mtype]
    st.write(1)
    source = alt.topo_feature(data.world_110m.url, "countries")
    st.dataframe(source)
    world_map = (
        alt.Chart(source, title=f'Countries by number of {mtype} universities')
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "num:N", 
                scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
                legend=None),
            tooltip=[
                alt.Tooltip("country:N", title="country"),
                alt.Tooltip("count:Q", title="count"),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(d, "id", ["country", "num"]),
        )
    ).configure_view(strokeWidth=0).properties(width=700, height=400).project("naturalEarth1")
    
    return world_map
st.write(draw_map('count'))

# ------------------------------------------------------------------------------------------------------------------------
# def draw_map(mtype='count'):
    
#     COLOR_THEME = {'count':"lightgreyred"}
    
#     olympic_medal_map['Medals'] = olympic_medal_map[mtype]

#     source = alt.topo_feature(data.world_110m.url, "countries")

#     world_map = (
#         alt.Chart(source, title=f'Countries by number of {mtype} medals')
#         .mark_geoshape(stroke="black", strokeWidth=0.15)
#         .encode(
#             color=alt.Color(
#                 "Medals:N", 
#                 scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
#                 legend=None),
#             tooltip=[
#                 alt.Tooltip("Team/NOC:N", title="Team"),
#                 alt.Tooltip("Medals:Q", title="Medals"),
#             ],
#         )
#         .transform_lookup(
#             lookup="id",
#             from_=alt.LookupData(olympic_medal_map, "id", ["Team/NOC", "Medals"]),
#         )
#     ).configure_view(strokeWidth=0).properties(width=700, height=400).project("naturalEarth1")
    
#     return world_map
