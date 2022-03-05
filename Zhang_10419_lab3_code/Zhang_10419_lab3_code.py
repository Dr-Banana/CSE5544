import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("Zhang_10419_lab3_code")
# Set Up
data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")

# change ".." to number
data = data.replace('..',0)
for i in range(30):
  year = str(1990+i)
  data[year] = data[year].astype(float)
# Create a year list
year_list = []
for i in range(30):
    year = str(1990+i)
    year_list.append(year)
# Set a new df_1 without OECD-Total and Non-OCED Economies column
df_1 = data.drop(data[data['Country\\year']=="OECD - Total"].index)
df_1.reset_index(inplace=True)
df_1 = df_1.drop(columns=['Non-OECD Economies','index'])
# add corresponding continent
df_1["Continent"] = ["South America","Oceania","Europe","Europe","Europe","South America","Europe","North America","South America","Asia",
                     "South America","North America","Europe","Asia","Europe","Europe","Europe","","Europe","Europe","Europe","Europe",
                     "Europe","Europe","Asia","Asia","Asia","Europe","Asia","Europe","Asia","Asia","Asia","Europe","Europe","Europe",
                     "Europe","Europe","North America","Europe","Europe","Oceania","Europe","","","South America","Europe","Europe",
                     "Europe","Europe","Asia","Europe","Europe","Africa","Europe","Europe","Europe","Asia","Europe","Europe","North America"]
countries = data['Country\\year']
# chart Data create
chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)

st.header("Step 1")
singleSelect = st.selectbox("select one country", countries)
filter_data = chart_data[chart_data['country'] == singleSelect]
boxPlot = alt.Chart(filter_data).mark_boxplot().encode(
    x='country',
    y='emission:Q'
)
st.altair_chart(boxPlot, use_container_width = True)


st.header("Step 2")
st.subheader("Visualize climate data in heatmaps(P1)")

# Create a continent VS. year polution dataframe
chart_data = pd.DataFrame()
continent_list = ['Asia','Europe','South America','Oceania','North America']
# User selection part
options = st.multiselect("Select Continent", continent_list, ['Europe'])
start,end = st.slider("Select Year", 1990, 2019,(1990,1991))
# Data setup 
for n in range(len(options)):
  total_list = []
  df_tmp = df_1[df_1["Continent"]== options[n]]
  for i in range(start-1990,end-1989):
    year = year_list[i]
    total = df_tmp[year].sum()
    total_list.append(total)
  
  chart_data[options[n]] = total_list
year_choose_list = []
for i in range(start-1990,end-1989):
    year = str(1990+i)
    year_choose_list.append(year)
chart_data.index = year_choose_list
# display chart
if(len(options)!=0 and (start-1990)>=0):
  fig, ax = plt.subplots()
  sns.set()
  ax = sns.heatmap(chart_data,cmap="coolwarm")
  ax.set_xlabel("Continent", fontsize = 15)
  ax.set_ylabel("Year", fontsize = 15)
  st.pyplot(plt)
else:
  st.write("Country and Year cannot be null!!!")

#Graph 2:
#prepare the data
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),
                       'std': df_data_country.std(axis=1)})

st.markdown("### Emission of Countries vs. Year Heatmap")
# User Selection
option1 = st.multiselect("select country", countries,['Canada','Austria','India'])
start_1,end_1 = st.slider('Select Year', 1990, 2019,(1990,1990))

# Pick User choose countries
year_choose = []
for i in range(start_1-1990,end_1-1989):
    year = str(1990+i)
    year_choose.append(year)
    
df_output = chart_data[(chart_data['country'].isin(option1))& (chart_data['year'].isin(year_choose))]
df_output.reset_index()

#render using altair
heatmap = alt.Chart(df_output).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color='emission:Q',
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)


# st.subheader("interactive altair chart")

# option = st.selectbox("select one country", countries)

# filter_data = chart_data[chart_data['country'] == option]
# bar_chart = alt.Chart(filter_data).mark_bar().encode(
#     x = 'year:O',
#     y = 'emission:Q'
# )

# st.altair_chart(bar_chart, use_container_width = True)
