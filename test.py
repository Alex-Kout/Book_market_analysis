import streamlit as st
import pandas as pd

st.header("""
test
""")

path = 'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.csv'

data = pd.read_csv(path)

st.dataframe(data.head(3))
