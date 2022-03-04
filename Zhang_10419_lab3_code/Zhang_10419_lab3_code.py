import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("streamlit quick start")

st.header("Write and magic commands")

st.subheader("write subheader")

st.markdown("# h1")
st.markdown("## h2")
st.markdown("### h3")

st.latex("\sum_{0}^{n}i")

st.header("Display data")

st.subheader("Matplotlib chart")

df = pd.DataFrame({
    'c1':[1,2,3,4],
    'c2':[10,20,30,40]
})

data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")
data
