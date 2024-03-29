import streamlit as st
import pandas as pd
import plotly.express as px
import math

## Import and prepare the data----------------
path = r'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.xlsx'

# Function to get the unique values to filter   

###-----------------SIdeBar--------------------------------
st.set_page_config(layout='wide')

data = pd.read_excel(path)

def income_statement_plot():
    st.subheader('Income Statement Analysis')
    
    st.write('#')
    
    average_groth_rate = df.Revenue.pct_change() * 100
    df['COGS_%'] = (df['Cost of Goods Sold'] / df['Revenue']) * 100
    
    # Average ratios info----
    m1, m2, m3, m4 = st.columns((1,1,1,1))
    
    m1.metric(label = 'Average Revenue growth rate', value = str(round(average_groth_rate.mean(), 1)) + ' %')
    m2.metric(label = 'Average Cost of Goods Sold (as % of Revenue)', value = str(round(df['COGS_%'].mean(), 1)) + ' %')
    m3.metric(label = 'Average EBIT', value = str(round(df['EBIT'].mean()))+ ' €')
    m4.metric(label = 'Average Net Profit', value = str(round(df['Net Income'].mean())) + ' €')

    
    st.write('#')
    
    g1, g2 = st.columns((1, 1,))
    
    height = 350
    width = 500
    
    fig1 = px.line(df, x = 'Year', y = 'Revenue', height = height, width = width)
    fig1.update_layout(title_text = 'Revenues', yaxis_title = None)
    g1.plotly_chart(fig1)
    
    
    fig2 = px.line(df, x = 'Year', y = 'COGS_%', height = height, width = width)
    fig2.update_layout(title_text = 'Cost of Goods Sold (as % of Revenue)', yaxis_title = None)
    fig2.update_traces(line_color='#874528')
    g2.plotly_chart(fig2)
    
    st.write('#')
    
    g3, g4 = st.columns((1, 1))
    
    fig3 = px.bar(df, x = 'Year', y = 'EBIT', height = height, width = width)
    fig3.update_layout(title_text = 'Earning before Interest and Taxes', yaxis_title = None)
    fig3.update_traces(marker_color='#675878')
    g3.plotly_chart(fig3)
    
    fig4 = px.bar(df, x = 'Year', y = 'Net Income', height = height, width = width)
    fig4.update_layout(title_text = 'Net Profit', yaxis_title = None)
    fig4.update_traces(marker_color='#7A9E9F')
    g4.plotly_chart(fig4)


def financial_ratios():
    st.write("---")
    st.subheader('Financial Ratio Analysis')
    
    ratios = ['Profitability ratios', 'Efficiency ratios', 'Leverage ratios', 'Liquidity ratios']
    selected_ratios = st.radio('Please select a type', ratios)
    
    
    # ----------------Profitability ratios--------------
    
    st.write("#")
    
    if selected_ratios == 'Profitability ratios':
        gross_margin = df['Gross Profit'] / df.Revenue * 100
        operating_margin = df['EBIT'] / df.Revenue * 100
        net_profit_margin = df['Net Income'] / df.Revenue * 100
        return_on_assets = df['Net Income'] / df['Total Assets'] * 100
        return_on_equity = df['Net Income'] / df["Total Equity"] * 100
        return_on_capital_employed = df['EBIT'] / df['Capital Employed'] * 100
        
        years = df['Year']
        df_ratios_series = {'Year': years, 'Gross margin': gross_margin, 'Operating margin': operating_margin, 'Net Profit margin': net_profit_margin,
                            'Return on Assets': return_on_assets, 'Return on Equity': return_on_equity, 'Return on Capital Employed': return_on_capital_employed}
        df_ratios = pd.concat(df_ratios_series, axis = 1)
    
        # Average ratios info----
        m1, m2, m3 = st.columns((1,1,1))
    
        m1.metric(label = 'Gross Margin (average)', value = str(round(gross_margin.mean(), 1)) + ' %')
        m2.metric(label = 'Operating Margin (average)', value = str(round(operating_margin.mean(), 1)) + ' %')
        m3.metric(label = 'Net Profit Margin (average)', value = str(round(net_profit_margin.mean(), 1)) + ' %')
        
        # Ratios per year plot----
        st.write('#')
    
        g1, g2, g3 = st.columns((1, 1, 1))
    
        height = 350
        width = 400
    
        fig1 = px.line(df_ratios, x = 'Year', y = 'Gross margin', orientation = 'h', height = height, width = width)
        fig1.update_layout(title_text = 'Gross margin per year (%)', yaxis_title = None )
        g1.plotly_chart(fig1)
    
        fig2 = px.line(df_ratios, x = 'Year', y = 'Operating margin', height = height, width = width)
        fig2.update_layout(title_text = 'Operating margin per year (%)', yaxis_title = None )
        fig2.update_traces(line_color='purple')
        g2.plotly_chart(fig2)
    
        fig3 = px.bar(df_ratios, x = 'Year', y = 'Net Profit margin', height = height, width = width)
        fig3.update_layout(title_text = 'Net Profit margin per year (%)', yaxis_title = None )
        fig3.update_traces(marker_color='#964653')
        g3.plotly_chart(fig3)
        
        st.write('---')
        
        m4, m5, m6 = st.columns((1,1,1))
    
        m4.metric(label = 'Return on Assets (average)', value = str(round(return_on_assets.mean(), 1)) + ' %')
        m5.metric(label = 'Return on Equity (average)', value = str(round(return_on_equity.mean(), 1)) + ' %')
        m6.metric(label = 'Return on Capital Employed (average)', value = str(round(return_on_capital_employed.mean(), 1)) + ' %')
        
        st.write('#')
        
        g4, g5, g6 = st.columns((1, 1, 1))
        
        fig4 = px.bar(df_ratios, x = 'Year', y = 'Return on Assets', height = height, width = width)
        fig4.update_layout(title_text = 'Return on Assets (%)', yaxis_title = None )
        fig4.update_traces(marker_color='#947348')
        g4.plotly_chart(fig4)
        
        fig5 = px.line(df_ratios, x = 'Year', y = 'Return on Equity', height = height, width = width)
        fig5.update_layout(title_text = 'Return on Equity (%)', yaxis_title = None )
        g5.plotly_chart(fig5)
    
        fig6 = px.bar(df_ratios, x = 'Year', y = 'Return on Capital Employed', height = height, width = width )
        fig6.update_layout(title_text = 'Return on Capital Employed (%)', yaxis_title = None )
        fig6.update_traces(marker_color='#417962')
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
        inventory_days = df.Inventories.rolling(window = 2).mean() / (df['Cost of Goods Sold']*-1) * days
        receivables_days = df.Receivables.rolling(window = 2).mean() / (df['Revenue']) * days
        payables_days = df.Payables.rolling(window = 2).mean() / (df['Cost of Goods Sold']*-1) * days
        cash_conv_cycle = inventory_days + receivables_days - payables_days
        years = df['Year'].astype(int)
        
        df_ratios_series = {'Year': years, 'Asset Turnover': asset_turnover, 'Days Inventory Outstanding': inventory_days, 'Days Receivables Outstanding': receivables_days,
                            'Days Payables Outstanding': payables_days, 'Cash Conversion Cycle':cash_conv_cycle}
        df_ratios = pd.concat(df_ratios_series, axis = 1)
        df_ratios.set_index('Year', inplace = True)
    
        # Average ratios info----
        m1, m2, m3 = st.columns((1,1,1))
    
        m1.metric(label = 'Asset Turnover (average)', value = str(round(asset_turnover.mean(), 1)) + ' %')
        m3.metric(label = 'Cash Conversion cycle (average)', value = str(round(cash_conv_cycle.mean())) + ' days')
    
        st.write('#')
        
        m4, m5, m6 = st.columns((1, 1, 1))
        
        m4.metric(label = 'Days Payables Outstanding (average)', value = round(payables_days.mean()))
        m5.metric(label = 'Days Inventory Outstanding (average)', value = round(inventory_days.mean()))
        m6.metric(label = 'Days Receivables Outstanding (average)', value = round(receivables_days.mean()))
        
        st.write('---')
        
        st.line_chart(df_ratios.drop(columns = ['Asset Turnover']))
    
    
    ### -------------  Leverage Ratios   ----------------------------------------------------
    elif selected_ratios == 'Leverage ratios':
        debt_to_assets = df['Total Debt'] / df['Total Assets'] * 100
        debt_to_equity = df['Total Debt'] / df["Total Equity"] * 100
        debt_to_capital = (df['Total Debt'] / (df['Total Debt'] + df["Total Equity"])) * 100
        debt_to_ebitda = df['Total Debt'] / df['EBIT'] * 100
        
        
        m1, m2, m3, m4 = st.columns((1, 1, 1, 1))
    
        m1.metric(label = 'Debt to Assets (average)', value = str(round(debt_to_assets.mean(), 1)) + ' %')
        m2.metric(label = 'Debt to Equity (average)', value = str(round(debt_to_equity.mean(), 1)) + ' %')
        m3.metric(label = 'Debt to Capital (average)', value = str(round(debt_to_capital.mean(), 1)) + ' %')
        m4.metric(label = 'Debt to EBITDA (average)', value = str(round(debt_to_ebitda.mean(), 1)) + ' %')
        
        st.write('#')
        
        years = df['Year']
        df_ratios_series = {'Year': years, 'Debt to Assets': debt_to_assets, 'Debt to Equity': debt_to_equity, 'Debt to Capital': debt_to_capital,
                            'Debt to EBITDA': debt_to_ebitda}
        df_ratios = pd.concat(df_ratios_series, axis = 1)
        
        height = 400
        width = 500
        
        g1, g2 = st.columns((1, 1))
    
        fig1 = px.line(df_ratios, x = 'Year', y = 'Debt to Assets', height = height, width = width)
        fig1.update_layout(title_text = 'Debt to Assets (%)', yaxis_title = None )
        g1.plotly_chart(fig1)
        
        fig2 = px.bar(df_ratios, x = 'Year', y = 'Debt to Equity', height = height, width = width)
        fig2.update_layout(title_text = 'Debt to Equity (%)', yaxis_title = None )
        fig2.update_traces(marker_color='#614259')
        g2.plotly_chart(fig2)
    
        g3, g4 = st.columns((1, 1))
        
        fig3 = px.line(df_ratios, x = 'Year', y = 'Debt to Capital', height = height, width = width)
        fig3.update_layout(title_text = 'Debt to Capital (%)', yaxis_title = None )
        fig3.update_traces(line_color='#871693')
        g3.plotly_chart(fig3)
        
        fig4 = px.bar(df_ratios, x = 'Year', y = 'Debt to EBITDA', height = height, width = width)
        fig4.update_layout(title_text = 'Debt to EBITDA (%)', yaxis_title = None )
        fig4.update_traces(marker_color='#618459')
        g4.plotly_chart(fig4)  
    
    ### -------------  Liquidity Ratios   ----------------------------------------------------
    else:
        current_ratio = df['Current Assets'] / df['Current Liabilities'] 
        quick_ratio = (df['Current Assets'] - df['Inventories']) / df["Current Liabilities"]
        cash_ratio = df['Cash'] / df['Current Liabilities']
        
        tab1, tab2, tab3 = st.tabs(["Current Ratio", "Quick Ratio", "Cash Ratio"])       
    
        with tab1:
            st.write('Measures a company’s ability to pay current or short-term liabilities (debts and payables) with its current or short-term assets, such as cash, inventory, and receivables.')
        with tab2:
            st.write('Measures a company’s ability to pay current or short-term liabilities with its most liquid current assets, excluding the Inventory.')
        with tab3:
            st.write('Indicates a company’s capacity to pay off short-term debt obligations with its cash and cash equivalents.')
        
        st.write('#')
        m1, m2, m3 = st.columns((1, 1, 1))
        
        m1.metric(label = 'Current Ratio (average)', value = str(round(current_ratio.mean(), 2)) + 'x')
        m2.metric(label = 'Quick Ratio (average)', value = str(round(quick_ratio.mean(), 2)) + 'x')
        m3.metric(label = 'Cash Ratio (average)', value = str(round(cash_ratio.mean(), 2)) + 'x')
        
        st.write('#')
        
        years = df['Year']
        df_ratios_series = {'Year': years, 'Current Ratio': current_ratio, 'Quick Ratio': quick_ratio, 'Cash Ratio': cash_ratio}
        df_ratios = pd.concat(df_ratios_series, axis = 1)
        height = 380 
        width = 430
        
        g1, g2, g3= st.columns((1, 1, 1))
    
        fig1 = px.line(df_ratios, x = 'Year', y = 'Current Ratio', height = height, width = width)
        fig1.update_layout(title_text = 'Current Ratio', yaxis_title = None )
        fig1.update_traces(line_color='#966571')
        g1.plotly_chart(fig1)
        
        fig2 = px.bar(df_ratios, x = 'Year', y = 'Quick Ratio', height = height, width = width)
        fig2.update_layout(title_text = 'Quick Ratio', yaxis_title = None )
        fig2.update_traces(marker_color='#7A9E9F')
        g2.plotly_chart(fig2)
    
        fig3 = px.line(df_ratios, x = 'Year', y = 'Cash Ratio', height = height, width = width)
        fig3.update_layout(title_text = 'Cash Ratio', yaxis_title = None )
        fig3.update_traces(line_color='#204967')
        g3.plotly_chart(fig3) 
        
        st.write('#')
        
        st.subheader('Current Assets Breakdown')

        current_assets = df[['Year', 'Cash', 'Inventories', 'Receivables']]
        st.bar_chart(current_assets, x = 'Year', y = ['Cash', 'Inventories', 'Receivables'])


    # User Input to see statistical summary of the choosen account ------------------------------------------------
    st.write('---')
    
    st.subheader('In this Section you may choose the Account you would like to be displayed')
    
    col1, col2 = st.columns(2)
    
    with col1:
        option = st.selectbox('Please select an Account', data.columns[3:].unique())
    
    st.write('---')
    
    g1, g2= st.columns((1, 1))    
    
    fig1 = px.bar(df, x = 'Year', y = option)
    fig1.update_layout(title_text = f'{option} per Year', yaxis_title = None)
    fig1.update_traces(marker_color='#195263')
    g1.plotly_chart(fig1)
    
    
    yearly_groth_rate = df[option].pct_change() * 100
    fig2 = px.line(df, x = 'Year', y = yearly_groth_rate)
    fig2.update_layout(title_text = f'Growth rate of {option} per year (%)', yaxis_title = None)
    fig2.update_traces(line_color='#966571')
    g2.plotly_chart(fig2)


    g3, g4= st.columns((1, 1)) 

    fig3 = px.ecdf(df, x = option)
    fig3.update_layout(title_text = f'Empirical Cumulative Distribution Function of {option}', yaxis_title = None)
    g3.plotly_chart(fig3)
        
    fig4 = px.violin(df, x = option, box=True, points='all')
    fig4.update_layout(title_text = f'{option} Distribution', yaxis_title = None)
    fig4.update_traces(line_color='#964653')
    g4.plotly_chart(fig4)



### ------------------ User Input (decide whether to see for a company or for all) -------------------------------



st.sidebar.header('Financial Performance Analysis of the Publishing Market in Greece (2011 - 2021)')
st.sidebar.write('---')
user_input = st.sidebar.radio('What would you like to see: ', ('Market Overview (yearly averages)', 'Specific Company', 'Compare Companies'))
st.sidebar.write('---')

# ------ Display the avregares of all Companies --------------------------------------------------------------------
if user_input == 'Market Overview (yearly averages)':

    df = data.groupby('Year', as_index = False).mean()
    
    st.header('Market Overview')
    
    col1, col2 = st.columns(2)
    
    st.write("Here you can see a quick overview of the financial performance of the major Publishing Companies in Greece, during the last decade.\
             This research is based only on Publishing companies, with a dominant role in market, having a wide product portfolio,\
                 including Fiction, Mystery, Action & Adventure, Romance, Historical, Biographies, Children’s Book etc. \
                     All the information are publicly available and can be found in the Publisher's websites. \
                         This presentation is for educational and informational purposes only and any other use is not permitted.")


    st.write('In this section all the data are being displayed as the yearly average of all the Companies that are included in this research')
    
    st.write('---')
    
    st.subheader('Market Averages per Year')
    st.write('---')
    g1, g2 = st.columns((1,1))
    df_revenue = data.groupby('Company', as_index = False).mean()

    height = 400
    width = 700
    
    fig1 = px.scatter(df_revenue, x = 'Revenue', y = 'Net Income', size = 'Revenue', color = 'Company', height = height, width = width)
    fig1.update_layout(title_text = 'Map of Revenue and Net Profit', xaxis_title = 'Average Revenue', yaxis_title = 'Average Net Profit')
    g1.plotly_chart(fig1)
    
    fig2 = px.box(data, x = 'Net Income', y = 'Company', height = height, width = width)
    fig2.update_layout(title_text = 'Net Profit (distribution)', xaxis_title = 'Net Profit', yaxis_title = 'Company')
    fig2.update_traces(orientation='h')
    g2.plotly_chart(fig2)
    

    
    st.write('---')
    
    income_statement_plot()
    financial_ratios()


    
# ------------ Display only one Company --------------------------------------------------------------------   
elif user_input == 'Specific Company':
    selected_company = st.sidebar.selectbox('Select a Company', data.Company.unique())
    st.header('Company: ' + selected_company)
    st.write('---')
    
    df = data[data['Company'] == selected_company]
    
    income_statement_plot()
    financial_ratios()
    
    st.write('---')

        
# ------Display a comparison of the selected Companies --------------------------------------------------------------------
else:

    selected_companies = st.sidebar.multiselect('Select Companies to compare', data.Company.unique())
    st.header('Comparison of the following Companies: ' )
    for company in selected_companies:
        st.write(company)
        
    df = data[data['Company'].isin(selected_companies)]
    st.write('---')
    st.subheader('Income Statement')
    g1, g2 = st.columns((1, 1,))
        
    height = 400
    width = 500
        
    fig1 = px.line(df, x = 'Year', y = 'Revenue', color = 'Company', height = height, width = width)
    fig1.update_layout(title_text = 'Revenues', yaxis_title = None)
    g1.plotly_chart(fig1)
    
    df['COGS_%'] = (df['Cost of Goods Sold'] / df['Revenue']) * 100
    fig2 = px.line(df, x = 'Year', y = 'COGS_%', color = 'Company', height = height, width = width)
    fig2.update_layout(title_text = 'Cost of Goods Sold (as % of Revenue)', yaxis_title = None)
    g2.plotly_chart(fig2)
        
    g3, g4 = st.columns((1, 1))
        
    fig3 = px.bar(df, x = 'Year', y = 'EBIT', color = 'Company', height = height, width = width)
    fig3.update_layout(title_text = 'Earning before Interest and Taxes', yaxis_title = None)
    g3.plotly_chart(fig3)
        
    fig4 = px.bar(df, x = 'Year', y = 'Net Income', color = 'Company', height = height, width = width)
    fig4.update_layout(title_text = 'Net Profit', yaxis_title = None)
    g4.plotly_chart(fig4)
    
    st.write('---')
    st.header('Financial Ratio Analysis')
    
    ratios = ['Profitability ratios', 'Leverage ratios', 'Liquidity ratios']
    selected_ratios = st.radio('Please select a type', ratios)


    if selected_ratios == 'Profitability ratios':
        df['Gross margin'] = df['Gross Profit'] / df.Revenue * 100
        df['Operating margin'] = df['EBIT'] / df.Revenue * 100
        df['Net Profit margin'] = df['Net Income'] / df.Revenue * 100
        df['Return on Assets'] = df['Net Income'] / df['Total Assets'] * 100
        df['Return on Equity'] = df['Net Income'] / df["Total Equity"] * 100
        df['Return on Capital Employed'] = df['EBIT'] / df['Capital Employed'] * 100
        
     
        # Ratios per year plot----
        st.write('#')
    
        g1, g2, g3 = st.columns((1, 1, 1))
    
        height = 350
        width = 400
    
        fig1 = px.line(df, x = 'Year', y = 'Gross margin', orientation = 'h', color = 'Company', height = height, width = width)
        fig1.update_layout(title_text = 'Gross margin per year (%)', yaxis_title = None )
        g1.plotly_chart(fig1)
    
        fig2 = px.line(df, x = 'Year', y = 'Operating margin', color = 'Company', height = height, width = width)
        fig2.update_layout(title_text = 'Operating margin per year (%)', yaxis_title = None )
        g2.plotly_chart(fig2)
    
        fig3 = px.bar(df, x = 'Year', y = 'Net Profit margin', color = 'Company', height = height, width = width)
        fig3.update_layout(title_text = 'Net Profit margin per year (%)', yaxis_title = None )
        g3.plotly_chart(fig3)
        
        st.write('---')
        
        g4, g5, g6 = st.columns((1, 1, 1))
        
        fig4 = px.bar(df, x = 'Year', y = 'Return on Assets', color = 'Company', height = height, width = width)
        fig4.update_layout(title_text = 'Return on Assets (%)', yaxis_title = None )
        g4.plotly_chart(fig4)
        
        fig5 = px.line(df, x = 'Year', y = 'Return on Equity', color = 'Company', height = height, width = width)
        fig5.update_layout(title_text = 'Return on Equity (%)', yaxis_title = None )
        g5.plotly_chart(fig5)
    
        fig6 = px.bar(df, x = 'Year', y = 'Return on Capital Employed', color = 'Company', height = height, width = width )
        fig6.update_layout(title_text = 'Return on Capital Employed (%)', yaxis_title = None )
        g6.plotly_chart(fig6)

        
    elif selected_ratios == 'Leverage ratios':
        df['Debt to Assets'] = df['Total Debt'] / df['Total Assets'] * 100
        df['Debt to Equity'] = df['Total Debt'] / df["Total Equity"] * 100
        df['Debt to Capital'] = (df['Total Debt'] / (df['Total Debt'] + df["Total Equity"])) * 100
        df['Debt to EBIT'] = df['Total Debt'] / df['EBIT'] * 100
    
        st.write('#')

        g1, g2 = st.columns((1, 1))
        
        height = 400
        width = 650
        
        fig1 = px.line(df, x = 'Year', y = 'Debt to Assets', color = 'Company', height = height, width = width)
        fig1.update_layout(title_text = 'Debt to Assets (%)', yaxis_title = None )
        g1.plotly_chart(fig1)
        
        fig2 = px.bar(df, x = 'Year', y = 'Debt to Equity', color = 'Company', height = height, width = width)
        fig2.update_layout(title_text = 'Debt to Equity (%)', yaxis_title = None )
        g2.plotly_chart(fig2)
    
        g3, g4 = st.columns((1, 1))
    
        fig3 = px.line(df, x = 'Year', y = 'Debt to Capital', color = 'Company', height = height, width = width)
        fig3.update_layout(title_text = 'Debt to Capital (%)', yaxis_title = None )
        g3.plotly_chart(fig3)
        
        fig4 = px.bar(df, x = 'Year', y = 'Debt to EBIT', color = 'Company', height = height, width = width)
        fig4.update_layout(title_text = 'Debt to EBIT (%)', yaxis_title = None )
        g4.plotly_chart(fig4)
    
    else:
     
        df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities'] 
        df['Quick Ratio'] = (df['Current Assets'] - df['Inventories']) / df["Current Liabilities"]
        df['Cash Ratio'] = df['Cash'] / df['Current Liabilities']
        
        tab1, tab2, tab3 = st.tabs(["Current Ratio", "Quick Ratio", "Cash Ratio"])       
    
        with tab1:
            st.write('Measures a company’s ability to pay current or short-term liabilities (debts and payables) with its current or short-term assets, such as cash, inventory, and receivables.')
        with tab2:
            st.write('Measures a company’s ability to pay current or short-term liabilities with its most liquid current assets, excluding the Inventory.')
        with tab3:
            st.write('Indicates a company’s capacity to pay off short-term debt obligations with its cash and cash equivalents.')
        
        st.write('#')

        height = 380 
        width = 430
        
        g1, g2, g3= st.columns((1, 1, 1))
    
        fig1 = px.line(df, x = 'Year', y = 'Current Ratio', color = 'Company', height = height, width = width)
        fig1.update_layout(title_text = 'Current Ratio', yaxis_title = None )
        g1.plotly_chart(fig1)
        
        fig2 = px.bar(df, x = 'Year', y = 'Quick Ratio',color = 'Company', height = height, width = width)
        fig2.update_layout(title_text = 'Quick Ratio', yaxis_title = None )
        g2.plotly_chart(fig2)
    
        fig3 = px.line(df, x = 'Year', y = 'Cash Ratio', color = 'Company', height = height, width = width)
        fig3.update_layout(title_text = 'Cash Ratio', yaxis_title = None )
        g3.plotly_chart(fig3)
