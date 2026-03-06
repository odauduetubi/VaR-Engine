import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import os # For file path handling
import sys # For adding src to path

# Fix paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR) # Add current directory to path

# Load data
DATA_PATH = os.path.join(BASE_DIR, 'data', 'log_returns.csv')
log_returns = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)

from src.risk import portfolio_returns, portfolio_stats, historical_var, parametric_var, cvar
from src.monte_carlo import monte_carlo_var, monte_carlo_paths

st.set_page_config(page_title="VaR Engine", layout="wide")
st.title("Portfolio Risk and Monte Carlo VaR Engine")

# Sidebar inputs
st.sidebar.header("Portfolio Configuration")
tickers_input = st.sidebar.text_input("Tickers (comma-separated)", "AAPL,MSFT,JPM,GLD,TLT")
weights_input = st.sidebar.text_input("Weights (comma-separated)", "0.30,0.25,0.20,0.15,0.10")
portfolio_value = st.sidebar.number_input("Portfolio Value ($)", value=1_000_000)
confidence_level = st.sidebar.slider("Confidence Level", 0.90, 0.99, 0.99)
simulations = st.sidebar.slider("Monte Carlo Simulations", 1000, 20000, 10000)

if st.sidebar.button("Run Analysis"):
    tickers = [t.strip() for t in tickers_input.split(',')]
    weights = [float(w) for w in weights_input.split(',')]
    
    with st.spinner("Fetching data..."):
        prices = yf.download(tickers, period='5y', auto_adjust=True)['Close'].dropna()
        log_returns = np.log(prices / prices.shift(1)).dropna()
    
    port_ret = log_returns.dot(weights)
    stats = portfolio_stats(log_returns, weights)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Annual Return", f"{stats['annual_return']:.2%}")
    col2.metric("Annual Volatility", f"{stats['annual_volatility']:.2%}")
    col3.metric("Sharpe Ratio", f"{stats['sharpe_ratio']:.2f}")
    col4.metric("Historical VaR (1-day)",
                f"${historical_var(port_ret, confidence_level) * portfolio_value:,.0f}")
    
    # Monte Carlo
    mc = monte_carlo_var(log_returns, weights, portfolio_value, simulations, confidence_level=confidence_level)
    st.subheader("Monte Carlo Results")
    st.write(f"**MC VaR ({confidence_level:.0%}):** ${mc['VaR']:,.0f}")
    st.write(f"**MC CVaR ({confidence_level:.0%}):** ${mc['CVaR']:,.0f}")