# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 19:25:12 2023

@author: akout
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image

## Import and prepare the data----------------
path = r'C:\Users\akout\OneDrive\Υπολογιστής\publisher.xlsx'


# Function to get the unique values to filter   

###-----------------SIdeBar--------------------------------
st.set_page_config(layout='wide')

data = pd.read_excel(path)

st.sidebar.header('Select a Company')
selected_company = st.sidebar.selectbox('', data.Company.unique())

df = data[data['Company'] == selected_company]

image = Image.open(r"C:\Users\akout\OneDrive\Υπολογιστής\e.jpg")
st.image(image)

st.header('Εταιρία: ' + selected_company)
st.write('---')

### ----------------------------      Plot Financial Informations      ---------------

st.subheader('Income Statement')
g1, g2, g3 = st.columns((1, 1, 1))

height = 400
width = 500

fig1 = px.line(df, x = 'Year', y = 'Revenue', orientation = 'h', height = height, width = width)
fig1.update_layout(title_text = 'Revenue per year', yaxis_title='Revenue')
g1.plotly_chart(fig1)

fig2 = px.scatter(df, x = 'Year', y = 'Adjusted EBIT', height = height, width = width)
fig2.update_layout(title_text = 'EBIT per year')
g2.plotly_chart(fig2)

fig3 = px.bar(df, x = 'Year', y = 'Net Income', height = height, width = width)
fig3.update_layout(title_text = 'Net Income per year')
g3.plotly_chart(fig3)

st.dataframe(df.head())



### ---------- ---------------------   Financial Ratios Analysis     -------------------
st.write("---")
st.subheader('Financial Ratio Analysis')

ratios = ['Profitability ratios', 'Efficiency ratios', 'Leverage ratios', 'Liquidity ratios']
selected_ratios = st.radio('Choose a type', ratios)




# ----------------Profitability ratios--------------

st.write("#")

if selected_ratios == 'Profitability ratios':
    gross_margin = df['Gross Profit'] / df.Revenue * 100
    operating_margin = df['EBIT'] / df.Revenue * 100
    net_profit_margin = df['Net Income'] / df.Revenue * 100
    return_on_assets = df['Net Income'] / df['Total Assets'] * 100
    return_on_equity = df['Net Income'] / df["Total Shareholders' Equity"] * 100
    return_on_capital_employed = df['EBIT'] / df['Capital Employed'] * 100
    
    
    years = df['Year']
    df_ratios_series = {'Year': years, 'Gross margin': gross_margin, 'Operating margin': operating_margin, 'Net Profit margin': net_profit_margin,
                        'Return on Assets': return_on_assets, 'Return on Equity': return_on_equity, 'Return on Capital Employed': return_on_capital_employed}
    df_ratios = pd.concat(df_ratios_series, axis = 1)

    # Average ratios info----
    m1, m2, m3 = st.columns((1,1,1))

    m1.metric(label = 'Gross Margin (average)', value = str(round(gross_margin.mean(), 1)) + '%')
    m2.metric(label = 'Operating Margin (average)', value = str(round(operating_margin.mean(), 1)) + '%')
    m3.metric(label = 'Net Profit Margin (average)', value = str(round(net_profit_margin.mean(), 1)) + '%')
    
    # Ratios per year plot----
    st.write('#')

    g1, g2, g3 = st.columns((1, 1, 1))

    height = 400
    width = 500

    fig1 = px.line(df_ratios, x = 'Year', y = 'Gross margin', orientation = 'h', height = height, width = width)
    fig1.update_layout(title_text = 'Gross margin per year (%)', yaxis_title = None )
    g1.plotly_chart(fig1)

    fig2 = px.scatter(df_ratios, x = 'Year', y = 'Operating margin', height = height, width = width)
    fig2.update_layout(title_text = 'Operating margin per year (%)', yaxis_title = None )
    g2.plotly_chart(fig2)

    fig3 = px.bar(df_ratios, x = 'Year', y = 'Net Profit margin', height = height, width = width)
    fig3.update_layout(title_text = 'Net Profit margin per year (%)', yaxis_title = None )
    g3.plotly_chart(fig3)
    
    st.write('---')
    
    m4, m5, m6 = st.columns((1,1,1))

    m4.metric(label = 'Return on Assets (average)', value = str(round(return_on_assets.mean(), 1)) + '%')
    m5.metric(label = 'Return on Equity (average)', value = str(round(return_on_equity.mean(), 1)) + '%')
    m6.metric(label = 'Return on Capital Employed (average)', value = str(round(return_on_capital_employed.mean(), 1)) + '%')
    
    g4, g5, g6 = st.columns((1, 1, 1))
    
    fig4 = px.bar(df_ratios, x = 'Year', y = 'Return on Assets', height = height, width = width)
    fig4.update_layout(title_text = 'Return on Assets (%)', yaxis_title = None )
    g4.plotly_chart(fig4)
    
    fig5 = px.scatter(df_ratios, x = 'Year', y = 'Return on Equity', height = height, width = width)
    fig5.update_layout(title_text = 'Return on Equity (%)', yaxis_title = None )
    g5.plotly_chart(fig5)

    fig6 = px.line(df_ratios, x = 'Year', y = 'Return on Capital Employed', height = height, width = width )
    fig6.update_layout(title_text = 'Return on Capital Employed (%)', yaxis_title = None )
    g6.plotly_chart(fig6)


# ----------------Efficiency ratios--------------
elif selected_ratios == 'Efficiency ratios':        

    tab1, tab2, tab3, tab4 = st.tabs(["Cash Conversion Cycle", "Days Payable Outstanding", "Days Receivables Outstanding", 'Days Inventory Outstanding'])       

    with tab1:
        st.write('Are the number of days it takes a company to convert its investments in inventory to cash. If positive the company would need to finance its working capital.')
    with tab2:
        st.write('Are the number of days, on average, it takes a company to pay back its suppliers.')
    with tab3:
        st.write('Are the number of days, on average, it takes a company to collect from its customers.')
    with tab4:
        st.write('Are the number of days, on average, it takes a company to turn its inventory into sales.')        
        
    st.write('---')    
    
    
    asset_turnover = df.Revenue / df['Total Assets'].rolling(window = 2).mean() * 100
    days = 365
    inventory_days = df.Inventories.rolling(window = 2).mean() / (df['Cost of Goods Sold']*-1) * 365
    receivables_days = df.Receivables.rolling(window = 2).mean() / (df['Revenue']) * 365
    payables_days = df.Payables.rolling(window = 2).mean() / (df['Cost of Goods Sold']*-1) * 365
    cash_conv_cycle = inventory_days + receivables_days - payables_days
    years = df['Year'].astype(int)
    
    df_ratios_series = {'Year': years, 'Asset Turnover': asset_turnover, 'Days Inventory Outstanding': inventory_days, 'Days Receivables Outstanding': receivables_days,
                        'Days Payables Outstanding': payables_days, 'Cash Conversion Cycle':cash_conv_cycle}
    df_ratios = pd.concat(df_ratios_series, axis = 1)
    df_ratios.set_index('Year', inplace = True)

    # Average ratios info----
    m1, m2, m3 = st.columns((1,1,1))

    m1.metric(label = 'Asset Turnover (average)', value = str(round(asset_turnover.mean(), 1)) + '%')
    m3.metric(label = 'Cash Conversion cycle (average)', value = round(cash_conv_cycle.mean(), 1))

    
    m4, m5, m6 = st.columns((1, 1, 1))
    
    m4.metric(label = 'Days Payables Outstanding (average)', value = round(payables_days.mean()))
    m5.metric(label = 'Days Inventory Outstanding (average)', value = round(inventory_days.mean()))
    m6.metric(label = 'Days Receivables Outstanding (average)', value = round(receivables_days.mean()))


    
    st.write('---')
    
    st.line_chart(df_ratios.drop(columns = ['Asset Turnover']))



### Current assets break down-------------------
st.write('---')
st.subheader('Current Assets Breakdown')
current_assets = df[['Year', 'Cash', 'Inventories', 'Receivables']]
st.bar_chart(current_assets, x = 'Year', y = ['Cash', 'Inventories', 'Receivables'])
