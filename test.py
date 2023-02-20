import streamlit as st
import pandas as pd
import plotly.express as px


path = r'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.xlsx'

# Function to get the unique values to filter   

###-----------------SIdeBar--------------------------------


data = pd.read_excel(path)

st.dataframe(data.head())
