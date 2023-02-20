import streamlit as st
import pandas as pd
import plotly.express as px
from pandas import ExcelWriter
from pandas import ExcelFile
st.header("""
test
""")


data = pd.read_excel('publisher.xlsx')
st.dataframe(data)

