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
                "num:Q", 
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
    ).configure_view(strokeWidth=0).properties(width=700, height=400).project("naturalEarth1").configure_legend(
    gradientLength=300,
    gradientThickness=25
    ) 
    
    return world_map
  
#  --------------------------------------------------------------------
MODE = st.sidebar.radio('Select view',['Total number of universities in ranking by country','portion of public vs private university by by year'])

#  --------------------------------------------------------------------
if MODE == 'Total number of universities in ranking by country':
    YEAR = st.slider('Select the year', 2017, 2022, 2017)
    REGION = st.selectbox(
     'Select continent', options = ['Global','North America','Europe','Asia','Oceania','Latin America','Africa'])
    if(REGION == 'Global'):
        year_university_df = university_df.loc[(university_df['year'] == YEAR)]
    else:
        year_university_df = university_df.loc[(university_df['year'] == YEAR) & (university_df['region'].isin(REGION))]

    d = pd.DataFrame(year_university_df.pivot_table(columns=['country'], aggfunc='size'))

    d.columns = ['count']
    d['id'] = country_codes['Numeric']
    d['country'] = d.index

    st.write(draw_map('count',YEAR))

else:
    YEAR = st.selectbox('Select a year',
                   options = [2017,2018,2019,2020,2021,2022])
    year_university_df = university_df.loc[university_df['year'] == YEAR]
    type_df = year_university_df['type'].value_counts()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

    pie_bar_colors = ['#FB8E7E','#8EC9BB']
    explode = [0,0.1]
    ax1.pie(year_university_df['type'].value_counts().values, labels = year_university_df['type'].value_counts().index, explode=explode, colors=pie_bar_colors, autopct='%1.1f%%') 
    ax1.axis('equal')

    ax2.bar(year_university_df['type'].value_counts().index, year_university_df['type'].value_counts().values, color=pie_bar_colors) 
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.tick_params(axis='both', which='both', labelsize=10, left=False, bottom=False)
    ax2.get_yaxis().set_visible(False)
    plt.title("University Types", fontsize=15, color = '#ff4800');

    ax2.bar_label(ax2.containers[0])

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.7)
    st.pyplot(fig)
