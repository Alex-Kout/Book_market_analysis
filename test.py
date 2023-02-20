import streamlit as st
import pandas as pd
import plotly.express as px
from pandas import ExcelWriter
from pandas import ExcelFile

st.header("""
test
""")

path = 'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.xlsx'


data = pd.read_excel(path)
st.dataframe(data)

