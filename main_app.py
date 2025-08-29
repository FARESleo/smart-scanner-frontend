# frontend/main_app.py
import streamlit as st
import requests
import pandas as pd
from math import isnan
import os

# --- الرابط الخلفي ---
BACKEND_URL = "https://workspace.chinviyou.repl.co"
# ---------------------

# --- الدوال المساعدة ---
def format_price(price, decimals=None):
    if price is None or isinstance(price, (str, bool)) or isnan(price): 
        return "N/A"
    if decimals is None:
        if price >= 1000: decimals = 2
        elif price >= 10: decimals = 3
        else: decimals = 4
    return f"{price:,.{decimals}f}"

def calculate_pnl_percentages(entry_price, take_profit, stop_loss):
    if entry_price is None or take_profit is None or stop_loss is None or entry_price == 0: 
        return None, None
    profit_pct = ((take_profit - entry_price) / entry_price) * 100
    loss_pct = ((stop_loss - entry_price) / entry_price) * 100
    is_long = take_profit > entry_price
    if not is_long: profit_pct, loss_pct = loss_pct, profit_pct
    return profit_pct, loss_pct

# --- التطبيق ---
def render_main_app():
    if 'analysis_results' not in st.session_state: 
        st.session_state.analysis_results = {}
    if 'selected_instId' not in st.session_state: 
        st.session_state.selected_instId = "BTC-USDT-SWAP"
    if 'bar' not in st.session_state: 
        st.session_state.bar = "1H"

    st.title("🧠 الماسح الذكي")
    st.markdown("---")

    selected_page = st.radio("اذهب إلى", ["📊 التحليل", "🧮 الحاسبة"], horizontal=True)
