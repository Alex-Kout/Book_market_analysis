import streamlit as st
import pandas as pd
import plotly.express as px

st.header("""
test
""")

path = r'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FAlex-Kout%2FBook_market_analysis%2Fmain%2Fpublisher.xlsx&wdOrigin=BROWSELINKv'

data = pd.read_csv(path)

