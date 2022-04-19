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
long_palette = ["#FA6E4F", "#F2CF59", "#FB8E7E", "#C5D7C0", "#8EC9BB", "#F8CA9D", '#F69EAF', '#8F8CBC', '#7C5396', '#EA6382', '#6BEAF3', '#5A9DE2', '#DDAD64', '#EA876B', '#B98174', '#357866', '#625586', '#647B99']
custom_palette1 = sns.color_palette(long_palette)
research_size = pd.DataFrame(university_df.groupby(['research_output']).apply(lambda df: df['size'].value_counts()))
research_size = research_size.reset_index().rename(columns={'level_1': 'size', 'size': 'count'})
fig, ax = plt.subplots()
ax = sns.catplot(x="research_output", y="count", kind="point", data=research_size, hue='size', palette=custom_palette1);
ax.xlabel('Research Output', fontsize=13, color = '#ff4800')
ax.ylabel('Count', fontsize=13, color = '#ff4800')
ax.title('Research output Vs Size of university', fontsize=15, color = '#ff4800');
st.pyplot(fig)
