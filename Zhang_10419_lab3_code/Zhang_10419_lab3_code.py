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

st.subheader("write subheader")

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
year_list = ['1990','1997','2004','2011','2019']
# for i in range(30):
#     year = str(1990+i)
#     year_list.append(year)
# Create a continent VS. year polution dataframe
chart_data = pd.DataFrame()
chart_data.index = year_list
continent_list = ['Asia','Europe','South America','Oceania','North America']
for n in range(5):
  total_list = []
  df_tmp = df_1[df_1["Continent"]== continent_list[n]]
  for i in range(5):
    year = year_list[i]
    total = df_tmp[year].sum()
    total_list.append(total)
  chart_data[continent_list[n]] = total_list

# display chart
sns.set()
fig = plt.figure()
sns.heatmap(chart_data,annot=TRUE,cmap="coolwarm")
st.pyplot(fig)
