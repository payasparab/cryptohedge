import requests
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from Market_model import crypto_slippage



html_header="""
<head>
<meta charset="utf-8">
<meta name="keywords" content=" Crypto Dashboard, dashboard, management, EVA">
<meta name="description" content="project control dashboard">
</head>
<h1 style="font-size:500%; color:#2F80ED; font-family:Georgia"> CRYPTO DASHBOARD<br>
 <h2 style="font-size: 25%; color:#2F80ED; font-family:Georgia"> Slippage: occurs when an order is executed at a price higher or lower than quoted price</h3> <br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""
st.set_page_config(page_title="CRYPTO DASHBOARD", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
data=pd.read_excel('curva.xlsx')

html_card_header1="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #2F80ED; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#2F80ED; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Currency to Sell</h3>
  </div>
</div>
"""
html_card_footer1="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #2F80ED; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#2F80ED; color:#2F80ED; font-family:Georgia; text-align: center; padding: 0px 0;">Baseline 46%</p>
  </div>
</div>
"""
html_card_header2="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #2F80ED; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#2F80ED; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Order Type</h3>
  </div>
</div>
"""
html_card_footer2="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #FFFFFF; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#FFFFFF; color:#2F80ED; font-family:Georgia; text-align: center; padding: 0px 0;">Baseline 92.700</p>
  </div>
</div>
"""
html_card_header3="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #2F80ED; padding-top: 5px; width: 350px;
   height: 50px;">
    <h3 class="card-title" style="background-color:#2F80ED; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 0px 0;">Amount To Buy Or Sell</h3>
  </div>
</div>
"""
html_card_footer3="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">To Complete Performance Index ≤ 1.00</p>
  </div>
</div>
"""
### Block 1#########################################################################################
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,15,1,15,1,15,1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header1, unsafe_allow_html=True)

        disciplinas = ['BTCUSD', 'AAVE', 'ADA', 'ALGO', 'ANKR', 'ANT', 'ATOM', 'AXS', 'BADGER', 'BAL', 'BAT', 'BCH', 'BNT', 'BTCUSD', 'CHZ', 'COMP', 'CQT', 'CRV', 'CTSI', 'DAI', 'DASH', 'DOGE', 'DOT', 'ENJ', 'EOS', 'ETC', 'ETH', 'EWT', 'FIL', 'FLOW', 'GHST', 'GNO', 'GRT', 'ICX', 'KAR', 'KAVA', 'KEEP', 'KNC', 'KSM', 'LINK', 'LPT', 'LRC', 'LSK', 'LTC', 'MANA', 'MATIC', 'MINA', 'MKR', 'MLN', 'NANO', 'OCEAN', 'OGN', 'OMG', 'OXT', 'PAXG', 'PERP', 'QTUM', 'RARI', 'REN', 'REP', 'REPV2', 'SAND', 'SC', 'SNX', 'SOL', 'SRM', 'STORJ', 'SUSHI', 'TBTC', 'TRX', 'UNI', 'USDC', 'USDT', 'WAVES', 'WBTC', 'XLM', 'XMR', 'XRP', 'XTZ', 'YFI', 'ZEC', 'ZRX']


        selected_disc = st.selectbox('', disciplinas)
        html_br = """
        <br>
        """
        st.markdown(html_br, unsafe_allow_html=True)

    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header2, unsafe_allow_html=True)

        buy_sell = ["buy", "sell"]

        buying_selling = st.selectbox('', buy_sell)
        html_br = """
        <br>
        """
        st.markdown(html_br, unsafe_allow_html=True)

    with col5:
        st.write("")
    with col6:

        st.markdown(html_card_header3, unsafe_allow_html=True)

        number = st.number_input('')

    with col7:
        st.write("")
html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)



html_card_header4="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #2F80ED; padding-top: 5px; width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#2F80ED; color:#FFFFFF; font-family:Georgia; text-align: center; padding: 10px 0;">Slippage</h4>
  </div>
</div>
"""
html_card_footer4="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Baseline 92.7</p>
  </div>
</div>
"""



### Block 2#########################################################################################
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
    with col1:
        st.write("")
    with col4:
        st.markdown(html_card_header4, unsafe_allow_html=True)

        a1 = crypto_slippage(selected_disc, buying_selling, number)
        a1 = "{:.5%}".format(a1)
        #a1 = crypto_slippage("BTCUSD", "buy", 100000)
        #print(a1)
        st.write(a1)

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)

html_card_header6="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">Cost Variance</h4>
  </div>
</div>
"""
html_card_footer6="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Value </p>
  </div>
</div>
"""
html_card_header7="""
<div class="card">
  <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
   height: 50px;">
    <h4 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 10px 0;">Schedule Variance</h4>
  </div>
</div>
"""
html_card_footer7="""
<div class="card">
  <div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
   height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Montly Value</p>
  </div>
</div>
"""


html_subtitlecorr = """
<h2 style="color:#2F80ED; font-family:Georgia;"> Heatmap Showing Correlation Between Different Assets </h2>
"""
st.markdown(html_subtitlecorr, unsafe_allow_html=True)

### Block 3#########################################################################################
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
    with col1:
        st.write("")
    with col2:
        st.markdown(html_card_header6, unsafe_allow_html=True)

        x_axis = st.selectbox("Choose x axis", options=Data_to_select_indexed.index.names)
        y_axis = st.selectbox("Choose y axis", options=Data_to_select_indexed.index.names)

        # Pivot table
        Pivot_data = Data_to_select_indexed.pivot_table(index=x_axis, columns=y_axis, values=data_to_analyse)

        f, ax2 = plt.subplots(figsize=(12, 7))
        # show data
        ax2 = sns.heatmap(Pivot_data, linecolor="white", yticklabels=y_axis, xticklabels=x_axis, cmap="Blues",
                            vmin=0.9, vmax=1.65, linewidth=0.3)
        st.write(ax2)
        st.pyplot()

        st.markdown(html_card_footer6, unsafe_allow_html=True)
    with col3:
        st.write("")
    with col4:
        st.markdown(html_card_header7, unsafe_allow_html=True)
        fig_sv = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=0.95,
            number={"font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 1.5], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "#06282d"},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, 1], 'color': '#FF4136'},
                    {'range': [1, 1.5], 'color': '#3D9970'}]}))
        fig_sv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=250,
                             margin=dict(l=10, r=10, b=15, t=20))
        st.plotly_chart(fig_sv)
        st.markdown(html_card_footer7, unsafe_allow_html=True)
    with col5:
        st.write("")
    with col6:
        def time_series(runs):
            """
            plots a time series to compare pace and heart rate values over time,
            with an adjustable range for the last month, last six months, year-to-date and all time
            """
            ts = runs.copy()
            ts['pace_not_dt'] = ts['pace_in_sec'].apply(pace_plot)
            ts['pace'] = ts['pace_not_dt'].apply(pace_to_dt)
            ts.columns = ['Name', 'Upload ID', 'Distance', 'Moving Time', 'Avg speed', 'Max speed', 'Avg cadence',
                          'Total elevation gain', 'Avg HR', 'Max HR', 'Date', 'Start time', 'Pace in sec',
                          'Pace not dt', 'Pace']

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=ts['Date'], y=ts['Avg HR'], name="Avg HR"),
                secondary_y=True,
            )

            fig.add_trace(
                go.Scatter(x=ts['Date'], y=ts['Max HR'], name="Max HR"),
                secondary_y=True,
            )

            fig.add_trace(
                go.Scatter(x=ts['Date'], y=ts['Pace'], name="Pace"),
                secondary_y=False,
            )

            fig.update_xaxes(
                title_text="Date",
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )

            fig.update_yaxes(title_text="Heart Rate", secondary_y=True)
            fig.update_yaxes(title_text="Pace", secondary_y=False, autorange='reversed')

            fig.update_layout(
                title_text="Pace vs Heart rate trends",
                template='plotly_white',
                yaxis=dict(
                    title='Pace',
                    tickformat='%M:%S'
                )
            )

            return fig

    with col7:
        st.write("")

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)

html_subtitle="""
<h2 style="color:#008080; font-family:Georgia;"> Details by Discipline: </h2>
"""
st.markdown(html_subtitle, unsafe_allow_html=True)

html_table=""" 
<table>
  <tr style="background-color:#eef9ea; color:#008080; font-family:Georgia; font-size: 15px">
    <th style="width:130px">Discipline</th>
    <th style="width:90px">Baseline</th>
    <th style="width:90px">Progress</th>
    <th style="width:90px">Manpower</th>
    <th style="width:90px">Cost Variance</th>
    <th style="width:90px">Schedule Variance</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>civil</th>
    <th>70,00%</th>
    <th>68,50%</th>
    <th>70.000</th>
    <th>0,99</th>
    <th>1,09</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Mechanical</th>
    <th>50,00%</th>
    <th>45,50%</th>
    <th>10.000</th>
    <th>0,95</th>
    <th>0,98</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>Piping</th>
    <th>30,00%</th>
    <th>30,00%</th>
    <th>60.000</th>
    <th>0,99</th>
    <th>1,01</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Electricity</th>
    <th>20,00%</th>
    <th>15,00%</th>
    <th>40.000</th>
    <th>0,90</th>
    <th>0,98</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 14px">
    <th>Intrumentation</th>
    <th>5,00%</th>
    <th>0,00%</th>
    <th>30.000</th>
    <th>-</th>
    <th>-</th>
  </tr>
  <tr style="background-color:#eef9ea; height: 40px; color:#008080; font-size: 14px">
    <th>Commissioning</th>
    <th>0,00%</th>
    <th>0,00%</th>
    <th>15.000</th>
    <th>-</th>
    <th>-</th>
  </tr>
  <tr style="height: 40px; color:#008080; font-size: 15px">
    <th>Total</th>
    <th>35,00%</th>
    <th>46,00%</th>
    <th>225.000</th>
    <th>0,97</th>
    <th>0,91</th>
  </tr>
</table>
"""

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)


html_line="""
<br>
<br>
<br>
<br>
<hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
"""
st.markdown(html_line, unsafe_allow_html=True)



