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
    
    COLOR_THEME = {'count':"lighttealblue"}
    d['num'] = d[mtype]
    source = alt.topo_feature(data.world_110m.url, "countries")
    
    world_map = (
        alt.Chart(source, title=f'Universities in QS World University Rankings {y} ')
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "num:N", 
                scale=alt.Scale(scheme=COLOR_THEME[mtype]), 
                legend = None),
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
        
d = pd.DataFrame(year_university_df.pivot_table(columns=['country'], aggfunc='size'))

d.columns = ['count']
d['id'] = country_codes['Numeric']
d['country'] = d.index

st.write(draw_map('count',YEAR))

# ---------------------------------------------

uni_df = year_university_df['university'].value_counts()

fig, ax = plt.subplots(figsize=(10,20), dpi=150)
color_p = sns.dark_palette("#69d", reverse=True, as_cmap=True)
ax = sns.countplot(data=year_university_df, y='country', order=year_university_df.country.value_counts().index, palette = 'ch:start=.2,rot=-.3')
plt.xlabel('Number of universities', fontsize=12, color = '#ff4800')
plt.ylabel('Country', fontsize=12, color = '#ff4800')
plt.title("Distribution of universities across countries", fontsize=14, color = '#ff4800');
st.pyplot(fig)

import plotly.express as px
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)
st.plotly_chart(fig, use_container_width=True)
# research_size = pd.DataFrame(university_df.groupby(['research_output']).apply(lambda df: df['size'].value_counts()))
# st.dataframe(research_size)
