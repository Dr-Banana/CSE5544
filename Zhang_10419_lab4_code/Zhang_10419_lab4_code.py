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


from vega_datasets import data

def draw_map(mtype,y):
    
    COLOR_THEME = {'count':"lightgreyred"}
    d['num'] = d[mtype]
    source = alt.topo_feature(data.world_110m.url, "countries")
    
    world_map = (
        alt.Chart(source, title=f'Universities in QS World University Rankings {y} ')
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "num:N", 
                scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
                legend=alt.Legend(title="Number of college", tickCount=6)),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("num:Q", title="Number of College"),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(d, "id", ["country", "num"]),
        )
    ).configure_view(strokeWidth=0).properties(width=700, height=400).project("naturalEarth1")
    
    return world_map

YEAR = st.slider('Select the year', 2017, 2022, 2017)
REGION = st.selectbox('Select continent', options = ['Global','North America','Europe','Asia','Oceania','Latin America','Africa']) 
if(REGION == 'Global'):
    year_university_df = university_df.loc[(university_df['year'] == YEAR)]
else:
    year_university_df = university_df.loc[(university_df['year'] == YEAR) & (university_df['region'] == REGION)]
        
d = pd.DataFrame(university_df.pivot_table(columns=['country'], aggfunc='size'))

d.columns = ['count']
d['id'] = country_codes['Numeric']
d['country'] = d.index

st.write(draw_map('count',YEAR))
