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



