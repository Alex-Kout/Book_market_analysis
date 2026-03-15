import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout='wide',
    page_title='Greek Publishing Market | Financial Analysis',
    initial_sidebar_state='expanded',
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    color: #1a1a2e;
}

.stApp { background-color: #f4f1eb; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f1f3d !important;
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #c8d6e5 !important; }
[data-testid="stSidebar"] .stRadio label {
    color: #a8bdd0 !important;
    font-size: 0.9rem;
    padding: 4px 0;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #7a9bbf !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stSidebar"] hr { border-color: #1e3a5f !important; }

/* Page header */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #0f1f3d;
    border-bottom: 3px solid #c8a96e;
    padding-bottom: 0.4rem;
    margin-bottom: 0.2rem;
    letter-spacing: -0.01em;
}
.page-subtitle {
    font-size: 0.88rem;
    color: #5a6a7e;
    font-weight: 400;
    margin-bottom: 1.5rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #0f1f3d;
    border-left: 4px solid #c8a96e;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e0d9ce;
    border-radius: 6px;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 4px rgba(15,31,61,0.06);
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: #6b7b8d !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.35rem !important;
    color: #0f1f3d !important;
    font-weight: 600 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #d6cfc3;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #7a8a9a;
    background: transparent;
    border: none;
    padding: 0.6rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    color: #0f1f3d !important;
    border-bottom: 2px solid #c8a96e !important;
    background: transparent !important;
}

/* Info boxes */
.stAlert {
    border-radius: 4px;
    border-left: 3px solid #c8a96e !important;
    background: #faf7f2 !important;
    color: #3a4a5a !important;
    font-size: 0.87rem;
}

hr { border-color: #d6cfc3 !important; margin: 1.2rem 0 !important; }

.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-color: #d6cfc3 !important;
    border-radius: 4px !important;
    background: #ffffff !important;
}

/* Company pills */
.company-list { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.company-pill {
    background: #0f1f3d;
    color: #e8dfc8;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 0.3rem 0.9rem;
    border-radius: 2px;
    text-transform: uppercase;
}

/* Description block */
.description-text {
    font-size: 0.88rem;
    color: #4a5a6a;
    line-height: 1.65;
    background: #ffffff;
    border: 1px solid #e0d9ce;
    border-left: 4px solid #0f1f3d;
    padding: 1rem 1.25rem;
    border-radius: 0 4px 4px 0;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = 'https://raw.githubusercontent.com/Alex-Kout/Book_market_analysis/main/publisher.xlsx'
    return pd.read_excel(path)

data = load_data()


# ── Design tokens ─────────────────────────────────────────────────────────────
PALETTE = {
    'navy':      '#0f1f3d',
    'gold':      '#c8a96e',
    'slate':     '#4a6587',
    'teal':      '#2e7d82',
    'rust':      '#9c4a3a',
    'sage':      '#4a7c6e',
    'burgundy':  '#7a3a4a',
    'olive':     '#6a7a3a',
    'steel':     '#5a7a9a',
}

COLOR_SEQ = [
    '#0f1f3d', '#c8a96e', '#2e7d82', '#9c4a3a',
    '#4a6587', '#4a7c6e', '#7a3a4a', '#6a7a3a',
]

CHART_H  = 340
CHART_HS = 300

LAYOUT_BASE = dict(
    margin        = dict(l=12, r=12, t=40, b=12),
    plot_bgcolor  = '#ffffff',
    paper_bgcolor = 'rgba(0,0,0,0)',
    font          = dict(family='Source Sans 3, sans-serif', size=11, color='#3a4a5a'),
    title_font    = dict(family='Source Sans 3, sans-serif', size=12,
                         color='#0f1f3d'),
    xaxis         = dict(showgrid=False, linecolor='#d6cfc3',
                         tickcolor='#d6cfc3', tickfont=dict(size=10), zeroline=False),
    yaxis         = dict(gridcolor='#ede8e0', gridwidth=1, linecolor='#d6cfc3',
                         tickfont=dict(size=10), zeroline=False),
    legend        = dict(orientation='h', yanchor='bottom', y=1.02,
                         xanchor='left', x=0, font=dict(size=10),
                         bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)'),
    hoverlabel    = dict(bgcolor='#0f1f3d', font_color='#e8dfc8',
                         font_family='Source Sans 3', font_size=11),
)

def styled_fig(fig, title, height=CHART_H):
    fig.update_layout(title_text=title, yaxis_title=None, height=height, **LAYOUT_BASE)
    return fig

def chart(fig, title, height=CHART_H):
    styled_fig(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


# ── Number formatting (European: . thousands, , decimal) ─────────────────────
def fmt_num(value, suffix='', decimals=0):
    try:
        v = round(float(value), decimals)
        if decimals == 0:
            s = f"{int(v):,}".replace(',', '.')
        else:
            s = f"{v:,.{decimals}f}"
            s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return s + suffix
    except Exception:
        return str(value)

fmt_pct  = lambda v, d=1: fmt_num(v, ' %', d)
fmt_eur  = lambda v:       fmt_num(v, ' \u20ac')
fmt_x    = lambda v, d=2:  fmt_num(v, 'x', d)
fmt_days = lambda v:       fmt_num(v, ' days')


# ── Helpers ───────────────────────────────────────────────────────────────────
def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label=label, value=value)

def pos_neg_colors(series, pos_col, neg_col):
    return [pos_col if v >= 0 else neg_col for v in series]


# ── Income Statement ──────────────────────────────────────────────────────────
def income_statement_plot():
    section('Income Statement')

    avg_growth   = df.Revenue.pct_change() * 100
    df['COGS_%'] = (df['Cost of Goods Sold'] / df['Revenue']) * 100

    metric_row([
        ('Avg. Revenue Growth',      fmt_pct(avg_growth.mean())),
        ('Avg. COGS (% of Revenue)', fmt_pct(df['COGS_%'].mean())),
        ('Avg. EBIT',                fmt_eur(df['EBIT'].mean())),
        ('Avg. Net Profit',          fmt_eur(df['Net Income'].mean())),
    ])
    st.write('')

    c1, c2 = st.columns(2, gap='large')
    with c1:
        fig = px.area(df, x='Year', y='Revenue',
                      color_discrete_sequence=[PALETTE['navy']])
        fig.update_traces(line_color=PALETTE['navy'], fillcolor='rgba(15,31,61,0.10)')
        chart(fig, 'Revenue')
    with c2:
        fig = px.line(df, x='Year', y='COGS_%',
                      color_discrete_sequence=[PALETTE['rust']])
        fig.update_traces(line_width=2)
        chart(fig, 'Cost of Goods Sold (% of Revenue)')

    st.write('')
    c3, c4 = st.columns(2, gap='large')
    with c3:
        fig = px.bar(df, x='Year', y='EBIT')
        fig.update_traces(marker_color=pos_neg_colors(df['EBIT'], PALETTE['sage'], PALETTE['rust']))
        chart(fig, 'EBIT')
    with c4:
        fig = px.bar(df, x='Year', y='Net Income')
        fig.update_traces(marker_color=pos_neg_colors(df['Net Income'], PALETTE['teal'], PALETTE['rust']))
        chart(fig, 'Net Profit')


# ── Financial Ratios ──────────────────────────────────────────────────────────
def financial_ratios():
    st.write('---')
    section('Financial Ratio Analysis')

    selected = st.radio(
        'Ratio category',
        ['Profitability', 'Efficiency', 'Leverage', 'Liquidity'],
        horizontal=True,
        label_visibility='collapsed',
    )
    st.write('')

    # ── Profitability ─────────────────────────────────────────────────────────
    if selected == 'Profitability':
        gm   = df['Gross Profit'] / df.Revenue * 100
        om   = df['EBIT']         / df.Revenue * 100
        npm  = df['Net Income']   / df.Revenue * 100
        roa  = df['Net Income']   / df['Total Assets']     * 100
        roe  = df['Net Income']   / df['Total Equity']     * 100
        roce = df['EBIT']         / df['Capital Employed'] * 100
        yrs  = df['Year']

        df_r = pd.DataFrame({
            'Year': yrs,
            'Gross Margin': gm, 'Operating Margin': om, 'Net Profit Margin': npm,
            'Return on Assets': roa, 'Return on Equity': roe,
            'Return on Capital Employed': roce,
        })

        metric_row([
            ('Gross Margin (avg)',      fmt_pct(gm.mean())),
            ('Operating Margin (avg)',  fmt_pct(om.mean())),
            ('Net Profit Margin (avg)', fmt_pct(npm.mean())),
        ])
        st.write('')

        c1, c2, c3 = st.columns(3, gap='large')
        for col, col_y, color, title in [
            (c1, 'Gross Margin',      PALETTE['navy'],  'Gross Margin (%)'),
            (c2, 'Operating Margin',  PALETTE['slate'], 'Operating Margin (%)'),
            (c3, 'Net Profit Margin', PALETTE['rust'],  'Net Profit Margin (%)'),
        ]:
            with col:
                fig = px.line(df_r, x='Year', y=col_y, color_discrete_sequence=[color])
                fig.update_traces(line_width=2)
                chart(fig, title, CHART_HS)

        st.write('---')
        metric_row([
            ('Return on Assets (avg)',        fmt_pct(roa.mean())),
            ('Return on Equity (avg)',        fmt_pct(roe.mean())),
            ('Return on Cap. Employed (avg)', fmt_pct(roce.mean())),
        ])
        st.write('')

        c4, c5, c6 = st.columns(3, gap='large')
        for col, col_y, color, title in [
            (c4, 'Return on Assets',           PALETTE['gold'], 'Return on Assets (%)'),
            (c5, 'Return on Equity',           PALETTE['teal'], 'Return on Equity (%)'),
            (c6, 'Return on Capital Employed', PALETTE['sage'], 'Return on Capital Employed (%)'),
        ]:
            with col:
                fig = px.bar(df_r, x='Year', y=col_y)
                fig.update_traces(marker_color=color)
                chart(fig, title, CHART_HS)

    # ── Efficiency ────────────────────────────────────────────────────────────
    elif selected == 'Efficiency':
        tab1, tab2, tab3, tab4 = st.tabs([
            'Cash Conversion Cycle', 'Days Payable Outstanding',
            'Days Receivable Outstanding', 'Days Inventory Outstanding'
        ])
        for tab, desc in zip([tab1, tab2, tab3, tab4], [
            'Number of days to convert inventory investment into cash. Positive values indicate working capital financing is required.',
            'Average number of days the company takes to pay its suppliers.',
            'Average number of days the company takes to collect payment from customers.',
            'Average number of days the company holds inventory before converting it to sales.',
        ]):
            with tab:
                st.info(desc)

        st.write('')
        days  = 365
        inv_d = df.Inventories.rolling(2).mean() / (df['Cost of Goods Sold'] * -1) * days
        rec_d = df.Receivables.rolling(2).mean() / df.Revenue * days
        pay_d = df.Payables.rolling(2).mean()    / (df['Cost of Goods Sold'] * -1) * days
        ccc   = inv_d + rec_d - pay_d
        at    = df.Revenue / df['Total Assets'].rolling(2).mean() * 100
        yrs   = df['Year'].astype(int)

        metric_row([
            ('Asset Turnover (avg)',         fmt_pct(at.mean())),
            ('Cash Conversion Cycle (avg)',  fmt_days(ccc.mean())),
            ('Days Payable Outstanding',     fmt_num(pay_d.mean(), ' days')),
            ('Days Inventory Outstanding',   fmt_num(inv_d.mean(), ' days')),
            ('Days Receivable Outstanding',  fmt_num(rec_d.mean(), ' days')),
        ])
        st.write('')

        df_eff = pd.DataFrame({
            'Year': yrs,
            'Cash Conversion Cycle': ccc,
            'Days Inventory Outstanding': inv_d,
            'Days Receivables Outstanding': rec_d,
            'Days Payables Outstanding': pay_d,
        }).set_index('Year').reset_index()

        fig = px.line(
            df_eff, x='Year',
            y=['Cash Conversion Cycle', 'Days Inventory Outstanding',
               'Days Receivables Outstanding', 'Days Payables Outstanding'],
            color_discrete_sequence=COLOR_SEQ, height=CHART_H,
        )
        fig.update_traces(line_width=2)
        chart(fig, 'Working Capital Efficiency (days)')

    # ── Leverage ──────────────────────────────────────────────────────────────
    elif selected == 'Leverage':
        d2a  = df['Total Debt'] / df['Total Assets'] * 100
        d2e  = df['Total Debt'] / df['Total Equity'] * 100
        d2c  = df['Total Debt'] / (df['Total Debt'] + df['Total Equity']) * 100
        d2eb = df['Total Debt'] / df['EBIT'] * 100
        yrs  = df['Year']

        df_r = pd.DataFrame({
            'Year': yrs,
            'Debt to Assets': d2a, 'Debt to Equity': d2e,
            'Debt to Capital': d2c, 'Debt to EBITDA': d2eb,
        })

        metric_row([
            ('Debt to Assets (avg)',  fmt_pct(d2a.mean())),
            ('Debt to Equity (avg)',  fmt_pct(d2e.mean())),
            ('Debt to Capital (avg)', fmt_pct(d2c.mean())),
            ('Debt to EBITDA (avg)',  fmt_pct(d2eb.mean())),
        ])
        st.write('')

        c1, c2 = st.columns(2, gap='large')
        with c1:
            fig = px.line(df_r, x='Year', y='Debt to Assets',
                          color_discrete_sequence=[PALETTE['navy']])
            fig.update_traces(line_width=2)
            chart(fig, 'Debt to Assets (%)')
        with c2:
            fig = px.bar(df_r, x='Year', y='Debt to Equity')
            fig.update_traces(marker_color=PALETTE['burgundy'])
            chart(fig, 'Debt to Equity (%)')

        c3, c4 = st.columns(2, gap='large')
        with c3:
            fig = px.line(df_r, x='Year', y='Debt to Capital',
                          color_discrete_sequence=[PALETTE['slate']])
            fig.update_traces(line_width=2)
            chart(fig, 'Debt to Capital (%)')
        with c4:
            fig = px.bar(df_r, x='Year', y='Debt to EBITDA')
            fig.update_traces(marker_color=PALETTE['olive'])
            chart(fig, 'Debt to EBITDA (%)')

    # ── Liquidity ─────────────────────────────────────────────────────────────
    else:
        curr  = df['Current Assets'] / df['Current Liabilities']
        quick = (df['Current Assets'] - df['Inventories']) / df['Current Liabilities']
        cash_r= df['Cash'] / df['Current Liabilities']
        yrs   = df['Year']

        tab1, tab2, tab3 = st.tabs(['Current Ratio', 'Quick Ratio', 'Cash Ratio'])
        for tab, desc in zip([tab1, tab2, tab3], [
            'Measures ability to pay short-term liabilities with current assets (cash, inventory, receivables).',
            'Measures ability to pay short-term liabilities with liquid assets — excludes inventory.',
            'Measures capacity to cover short-term debt obligations with cash and cash equivalents only.',
        ]):
            with tab:
                st.info(desc)

        st.write('')
        metric_row([
            ('Current Ratio (avg)', fmt_x(curr.mean())),
            ('Quick Ratio (avg)',   fmt_x(quick.mean())),
            ('Cash Ratio (avg)',    fmt_x(cash_r.mean())),
        ])
        st.write('')

        df_r = pd.DataFrame({
            'Year': yrs, 'Current Ratio': curr,
            'Quick Ratio': quick, 'Cash Ratio': cash_r,
        })
        c1, c2, c3 = st.columns(3, gap='large')
        for col, col_y, color, fn, title in [
            (c1, 'Current Ratio', PALETTE['burgundy'], px.line, 'Current Ratio'),
            (c2, 'Quick Ratio',   PALETTE['teal'],     px.bar,  'Quick Ratio'),
            (c3, 'Cash Ratio',    PALETTE['navy'],     px.line, 'Cash Ratio'),
        ]:
            with col:
                fig = fn(df_r, x='Year', y=col_y, color_discrete_sequence=[color])
                if fn == px.bar:
                    fig.update_traces(marker_color=color)
                else:
                    fig.update_traces(line_width=2)
                chart(fig, title, CHART_HS)

        st.write('')
        section('Current Assets Breakdown')
        ca = df[['Year', 'Cash', 'Inventories', 'Receivables']]
        fig = px.bar(
            ca, x='Year', y=['Cash', 'Inventories', 'Receivables'],
            color_discrete_sequence=[PALETTE['navy'], PALETTE['gold'], PALETTE['teal']],
            barmode='stack', height=CHART_H,
        )
        chart(fig, 'Current Assets Composition')

    # ── Account Explorer ──────────────────────────────────────────────────────
    st.write('---')
    section('Account Explorer')
    st.caption('Select any financial account to inspect its trend and statistical distribution.')

    option = st.selectbox('Account', data.columns[3:].unique(), label_visibility='collapsed')
    st.write('')

    c1, c2 = st.columns(2, gap='large')
    with c1:
        fig = px.bar(df, x='Year', y=option)
        fig.update_traces(marker_color=PALETTE['navy'])
        chart(fig, f'{option} — Annual Values')
    with c2:
        growth = df[option].pct_change() * 100
        fig = px.line(df, x='Year', y=growth, color_discrete_sequence=[PALETTE['rust']])
        fig.update_traces(line_width=2)
        chart(fig, f'{option} — Annual Growth Rate (%)')

    c3, c4 = st.columns(2, gap='large')
    with c3:
        fig = px.ecdf(df, x=option, color_discrete_sequence=[PALETTE['slate']])
        chart(fig, f'{option} — Empirical CDF')
    with c4:
        fig = px.violin(df, x=option, box=True, points='all',
                        color_discrete_sequence=[PALETTE['burgundy']])
        chart(fig, f'{option} — Distribution')


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<h2 style="font-family:Georgia,serif;font-size:1.1rem;line-height:1.5;'
    'color:#e8dfc8 !important;">'
    'Greek Publishing Market<br>'
    '<span style="font-size:0.72rem;font-weight:400;color:#7a9bbf;'
    'letter-spacing:0.1em;text-transform:uppercase;">Financial Analysis 2011 – 2021</span>'
    '</h2>',
    unsafe_allow_html=True,
)
st.sidebar.write('---')

user_input = st.sidebar.radio(
    'View',
    ('Market Overview', 'Specific Company', 'Compare Companies'),
)
st.sidebar.write('---')
st.sidebar.caption(
    'Data sourced from publicly available financial statements. '
    'For educational and informational purposes only.'
)


# ── Market Overview ───────────────────────────────────────────────────────────
if user_input == 'Market Overview':
    df = data.groupby('Year', as_index=False).mean(numeric_only=True)

    st.markdown('<div class="page-title">Market Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Greek Publishing Market &nbsp;&middot;&nbsp; '
        '2011 – 2021 &nbsp;&middot;&nbsp; Yearly Averages</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="description-text">'
        'This dashboard presents the financial performance of major Greek publishing companies '
        'over the last decade. The analysis covers companies with wide product portfolios '
        'including Fiction, Mystery, Romance, Historical, Biographies, and Children\'s Books. '
        'All data are publicly available via publishers\' websites. '
        'Figures represent <strong>yearly averages</strong> across all companies in the dataset.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.write('---')

    df_rev = data.groupby('Company', as_index=False).mean(numeric_only=True)

    c1, c2 = st.columns(2, gap='large')
    with c1:
        fig = px.scatter(
            df_rev, x='Revenue', y='Net Income',
            size='Revenue', color='Company',
            color_discrete_sequence=COLOR_SEQ, height=CHART_H,
        )
        fig.update_layout(
            title_text='Revenue vs. Net Profit by Company',
            height=CHART_H,
            **{k: v for k, v in LAYOUT_BASE.items() if k not in ('xaxis', 'yaxis')},
            xaxis=dict(showgrid=False, linecolor='#d6cfc3', tickfont=dict(size=10),
                       zeroline=False, title='Average Revenue (€)'),
            yaxis=dict(gridcolor='#ede8e0', gridwidth=1, linecolor='#d6cfc3',
                       tickfont=dict(size=10), zeroline=False, title='Average Net Profit (€)'),
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(
            data, x='Net Income', y='Company',
            color='Company', color_discrete_sequence=COLOR_SEQ, height=CHART_H,
        )
        fig.update_traces(orientation='h')
        fig.update_layout(
            title_text='Net Profit Distribution by Company',
            xaxis_title='Net Profit (€)', yaxis_title=None,
            showlegend=False, height=CHART_H,
            **{k: v for k, v in LAYOUT_BASE.items() if k not in ('xaxis', 'yaxis')},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.write('---')
    income_statement_plot()
    financial_ratios()


# ── Specific Company ──────────────────────────────────────────────────────────
elif user_input == 'Specific Company':
    selected_company = st.sidebar.selectbox('Select Company', data.Company.unique())
    df = data[data['Company'] == selected_company].copy()

    st.markdown(f'<div class="page-title">{selected_company}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Company Financial Profile &nbsp;&middot;&nbsp; 2011 – 2021</div>',
        unsafe_allow_html=True,
    )
    st.write('---')
    income_statement_plot()
    financial_ratios()


# ── Compare Companies ─────────────────────────────────────────────────────────
else:
    selected_companies = st.sidebar.multiselect('Select Companies', data.Company.unique())

    st.markdown('<div class="page-title">Company Comparison</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Comparative Financial Analysis &nbsp;&middot;&nbsp; 2011 – 2021</div>',
        unsafe_allow_html=True,
    )

    if not selected_companies:
        st.info('Please select at least two companies from the sidebar to begin the comparison.')
        st.stop()

    pills = ''.join(f'<span class="company-pill">{c}</span>' for c in selected_companies)
    st.markdown(f'<div class="company-list">{pills}</div>', unsafe_allow_html=True)
    st.write('---')

    df = data[data['Company'].isin(selected_companies)].copy()
    df['COGS_%'] = (df['Cost of Goods Sold'] / df['Revenue']) * 100

    section('Income Statement')
    c1, c2 = st.columns(2, gap='large')
    with c1:
        fig = px.line(df, x='Year', y='Revenue', color='Company',
                      color_discrete_sequence=COLOR_SEQ)
        fig.update_traces(line_width=2)
        chart(fig, 'Revenue')
    with c2:
        fig = px.line(df, x='Year', y='COGS_%', color='Company',
                      color_discrete_sequence=COLOR_SEQ)
        fig.update_traces(line_width=2)
        chart(fig, 'Cost of Goods Sold (% of Revenue)')

    c3, c4 = st.columns(2, gap='large')
    with c3:
        fig = px.bar(df, x='Year', y='EBIT', color='Company',
                     color_discrete_sequence=COLOR_SEQ, barmode='group')
        chart(fig, 'EBIT')
    with c4:
        fig = px.bar(df, x='Year', y='Net Income', color='Company',
                     color_discrete_sequence=COLOR_SEQ, barmode='group')
        chart(fig, 'Net Profit')

    st.write('---')
    section('Financial Ratio Analysis')

    sel_r = st.radio(
        'Ratio category',
        ['Profitability', 'Leverage', 'Liquidity'],
        horizontal=True,
        label_visibility='collapsed',
    )
    st.write('')

    if sel_r == 'Profitability':
        df['Gross Margin']               = df['Gross Profit'] / df.Revenue * 100
        df['Operating Margin']           = df['EBIT'] / df.Revenue * 100
        df['Net Profit Margin']          = df['Net Income'] / df.Revenue * 100
        df['Return on Assets']           = df['Net Income'] / df['Total Assets'] * 100
        df['Return on Equity']           = df['Net Income'] / df['Total Equity'] * 100
        df['Return on Capital Employed'] = df['EBIT'] / df['Capital Employed'] * 100

        c1, c2, c3 = st.columns(3, gap='large')
        for col, col_y, title in [
            (c1, 'Gross Margin',     'Gross Margin (%)'),
            (c2, 'Operating Margin', 'Operating Margin (%)'),
            (c3, 'Net Profit Margin','Net Profit Margin (%)'),
        ]:
            with col:
                fig = px.line(df, x='Year', y=col_y, color='Company',
                              color_discrete_sequence=COLOR_SEQ)
                fig.update_traces(line_width=2)
                chart(fig, title, CHART_HS)

        st.write('')
        c4, c5, c6 = st.columns(3, gap='large')
        for col, col_y, title in [
            (c4, 'Return on Assets',           'Return on Assets (%)'),
            (c5, 'Return on Equity',           'Return on Equity (%)'),
            (c6, 'Return on Capital Employed', 'Return on Cap. Employed (%)'),
        ]:
            with col:
                fig = px.bar(df, x='Year', y=col_y, color='Company',
                             color_discrete_sequence=COLOR_SEQ, barmode='group')
                chart(fig, title, CHART_HS)

    elif sel_r == 'Leverage':
        df['Debt to Assets']  = df['Total Debt'] / df['Total Assets'] * 100
        df['Debt to Equity']  = df['Total Debt'] / df['Total Equity'] * 100
        df['Debt to Capital'] = df['Total Debt'] / (df['Total Debt'] + df['Total Equity']) * 100
        df['Debt to EBIT']    = df['Total Debt'] / df['EBIT'] * 100

        c1, c2 = st.columns(2, gap='large')
        with c1:
            fig = px.line(df, x='Year', y='Debt to Assets', color='Company',
                          color_discrete_sequence=COLOR_SEQ)
            fig.update_traces(line_width=2)
            chart(fig, 'Debt to Assets (%)')
        with c2:
            fig = px.bar(df, x='Year', y='Debt to Equity', color='Company',
                         color_discrete_sequence=COLOR_SEQ, barmode='group')
            chart(fig, 'Debt to Equity (%)')

        c3, c4 = st.columns(2, gap='large')
        with c3:
            fig = px.line(df, x='Year', y='Debt to Capital', color='Company',
                          color_discrete_sequence=COLOR_SEQ)
            fig.update_traces(line_width=2)
            chart(fig, 'Debt to Capital (%)')
        with c4:
            fig = px.bar(df, x='Year', y='Debt to EBIT', color='Company',
                         color_discrete_sequence=COLOR_SEQ, barmode='group')
            chart(fig, 'Debt to EBIT (%)')

    else:
        df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities']
        df['Quick Ratio']   = (df['Current Assets'] - df['Inventories']) / df['Current Liabilities']
        df['Cash Ratio']    = df['Cash'] / df['Current Liabilities']

        tab1, tab2, tab3 = st.tabs(['Current Ratio', 'Quick Ratio', 'Cash Ratio'])
        for tab, desc in zip([tab1, tab2, tab3], [
            'Ability to pay short-term liabilities with current assets.',
            'Ability to pay short-term liabilities excluding inventory.',
            'Capacity to cover short-term debt with cash and cash equivalents only.',
        ]):
            with tab:
                st.info(desc)

        st.write('')
        c1, c2, c3 = st.columns(3, gap='large')
        for col, col_y, title in [
            (c1, 'Current Ratio', 'Current Ratio'),
            (c2, 'Quick Ratio',   'Quick Ratio'),
            (c3, 'Cash Ratio',    'Cash Ratio'),
        ]:
            with col:
                fig = px.line(df, x='Year', y=col_y, color='Company',
                              color_discrete_sequence=COLOR_SEQ)
                fig.update_traces(line_width=2)
                chart(fig, title, CHART_HS)