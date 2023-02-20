import streamlit as st
import pandas as pd
import plotly.express as px

st.header("""
test
""")

path = r'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.csv'

data = pd.read_csv(path, sep = ';')
st.dataframe(data)

data.to_excel("test.xlsx", sheet_name="test", index=False)
