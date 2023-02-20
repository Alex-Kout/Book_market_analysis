import streamlit as st
import pandas as pd
import plotly.express as px

st.header("""
test
""")

path = r'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.csv'

data = pd.read_csv(path, sep=";")

st.dataframe(data.head(3))






st.sidebar.header('Please select if you would like to see an overview of all the major companies in the market or just for a specific company: ')
user_input = st.sidebar.radio('', ('Whole Market', 'Specific Company'))
st.sidebar.write('---')

if user_input == 'Whole Market':

    df = data.groupby('Year', as_index = False).mean()
    
    st.header('Market Overview')
    
    col1, col2 = st.columns(2)
    
    st.write("Here you can see a quick overview of the financial performance of the major Publishing Companies in Greece, during the last decade.\
             This research is based only on Publishing companies, with a dominant role in market, having a wide product portfolio,\
                 including Fiction, Mystery, Action & Adventure, Romance, Historical, Biographies, Children’s Book etc. \
                     All the information are publicly available and can be found in the Publisher's websites. \
                         This presentation is for educational and infromational purposes only and any other use is not permitted.")
    
    st.write('---')
