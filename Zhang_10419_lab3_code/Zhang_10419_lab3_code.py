import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("Zhang_10419_lab3_code")
st.markdown("# h1")
st.markdown("## h2")
st.markdown("### h3")

st.header("Visualize climate data in heatmaps")

st.subheader("honest/ethical/truthful graph")

data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")

# change ".." to number
data = data.replace('..',0)
for i in range(30):
  year = str(1990+i)
  data[year] = data[year].astype(float)

# Set a new df_1 without OECD-Total and Non-OCED Economies column
df_1 = data.drop(data[data['Country\\year']=="OECD - Total"].index)
df_1.reset_index(inplace=True)
df_1 = df_1.drop(columns=['Non-OECD Economies','index'])
# add corresponding continent
df_1["Continent"] = ["South America","Oceania","Europe","Europe","Europe","South America","Europe","North America","South America","Asia","South America","North America","Europe","Asia","Europe","Europe","Europe","","Europe","Europe","Europe","Europe","Europe","Europe","Asia","Asia","Asia","Europe","Asia","Europe","Asia","Asia","Asia","Europe","Europe","Europe","Europe","Europe","North America","Europe","Europe","Oceania","Europe","","","South America","Europe","Europe","Europe","Europe","Asia","Europe","Europe","Africa","Europe","Europe","Europe","Asia","Europe","Europe","North America"]
# Create a year list
# year_list = ['1990','1997','2004','2011','2019']
year_list = []
for i in range(30):
    year = str(1990+i)
    year_list.append(year)
# Create a continent VS. year polution dataframe
chart_data = pd.DataFrame()
chart_data.index = year_list
continent_list = ['Asia','Europe','South America','Oceania','North America']
options = st.multiselect("select continent", countinent_list, ['Europe'])
for n in range(len(options)):
  total_list = []
  df_tmp = df_1[df_1["Continent"]== options[n]]
  for i in range(30):
    year = year_list[i]
    total = df_tmp[year].sum()
    total_list.append(total)
  
  chart_data[options[n]] = total_list

# display chart
fig, ax = plt.subplots()
sns.set()
ax = sns.heatmap(chart_data,cmap="coolwarm")
ax.set_xlabel("Continent", fontsize = 15)
ax.set_ylabel("Year", fontsize = 15)

st.pyplot(plt)


#prepare the data
countries = data['Country\\year']
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),
                       'std': df_data_country.std(axis=1)})

st.subheader("altair chart")

chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
chart_data

#render using altair
heatmap = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color='emission:Q',
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)


st.subheader("selectbox")
option = st.selectbox("country", ("USA", "China", "Europe Union"))

st.write(option)

st.subheader("multi-select")
option = st.multiselect("country", ("USA", "China", "Europe Union"), ("USA"))

st.write(option)

st.subheader("slider")
x = st.slider("x")
st.write("the square is", x * x)

st.header("Interactive chart")

st.subheader("interactive matplotlib chart")

options = st.multiselect("select countries", countries, ['Australia'])

country_stats.set_index("country", inplace=True)


fig, ax = plt.subplots(figsize=(14, 6), dpi = 50)
ax.bar(options, country_stats.loc[options]['mean'], yerr=country_stats.loc[options]['std'], capsize = 3)
ax.set_axisbelow(True)  #ensure the grid is under the graph elements
ax.margins(x=0.01) #set up the margin of graph
ax.grid(alpha = 0.3) #show the grid line
ax.set_xlabel('country')
ax.set_ylabel('emissions')
ax.set_title('The mean and std of emissions of countries')
xaxis = plt.xticks(rotation=90, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)

st.pyplot(fig)

st.subheader("interactive altair chart")

option = st.selectbox("select one country", countries)

filter_data = chart_data[chart_data['country'] == option]
bar_chart = alt.Chart(filter_data).mark_bar().encode(
    x = 'year:O',
    y = 'emission:Q'
)

st.altair_chart(bar_chart, use_container_width = True)
