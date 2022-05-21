import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv("dataframe-expat-final.csv",sep=";")


st.set_page_config(page_title="Dashboard Expat",
                   page_icon=":bar_chart:",
                   layout="wide")



# ---side bar---
st.title(":bar_chart: Expat Dashboard")
st.markdown("##")


st.sidebar.header("please filter here:")


country = st.sidebar.multiselect(
    "select the Country:",
    options = df["Country_Name"].unique()
)

region = st.sidebar.multiselect(
    "select the region:",
    options = df["Regional_indicator"].unique()
)

visa = st.sidebar.multiselect(
    "select the visa policy:",
    options = df["required_visa_for_french_citizen"].unique()
)


df_selection = df.query(
    "Country_Name == @country or Regional_indicator == @region or required_visa_for_french_citizen == @visa ")

st.dataframe(df_selection)

st.write("all the columns description :")
st.write("ladder score : Rank of the country based on the Happiness Score")
st.write("The happiness scores and rankings use data from the Gallup World Poll . The columns following the happiness score estimate the extent to which each of six factors – economic production, social support, life expectancy, freedom, absence of corruption, and generosity – contribute to making life evaluations higher in each country than they are in Dystopia, a hypothetical country that has values equal to the world’s lowest national averages for each of the six factors. They have no impact on the total score reported for each country, but they do explain why some countries rank higher than others.")


