import streamlit as st
from ove.engine import EuropeanOption, ValuationEngine

st.set_page_config(page_title="Open Valuation Engine UI", layout="wide")

st.title("📊 Open Valuation Engine (OVE) Dashboard")
st.markdown("An interactive quantitative modeling tool for analytical cross-asset derivatives valuation.")

# Sidebar Configuration Controls
st.sidebar.header("🎯 Option Parameters")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"]).lower()
S = st.sidebar.number_input("Underlying Asset Price (S)", min_value=1.0, value=150.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=145.0, step=1.0)
T = st.sidebar.slider("Time to Maturity (Years - T)", min_value=0.01, max_value=5.0, value=0.25, step=0.01)
r = st.sidebar.slider("Risk-Free Interest Rate (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.01)
sigma = st.sidebar.slider("Volatility (σ)", min_value=0.01, max_value=1.0, value=0.20, step=0.01)

# Computation Core
option = EuropeanOption(S, K, T, r, sigma, option_type)
engine = ValuationEngine()

pv = engine.price(option)
delta_val = engine.delta(option)
gamma_val = engine.gamma(option)
vega_val = engine.vega(option)
theta_val = engine.theta(option)

# Visual Display Modules
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("💰 Calculated Position Value")
    st.metric(label=f"Theoretical {option_type.capitalize()} Price", value=f"\${pv}")

with col2:
    st.subheader("⚡ Risk Metrics (The Greeks)")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g_col1.metric("Delta", delta_val)
    g_col2.metric("Gamma", gamma_val)
    g_col3.metric("Vega (1%)", vega_val)
    g_col4.metric("Theta (Daily)", theta_val)

st.info("💡 Under the hood, this dashboard pulls parameters directly into your `ove/engine.py` modules using analytical Black-Scholes-Merton differential equations.")
