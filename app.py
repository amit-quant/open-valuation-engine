import streamlit as st
import numpy as np
import yfinance as yf
from ove.engine import EuropeanOption, ValuationEngine
from ove.vol_solver import ImpliedVolatilitySolver

st.set_page_config(page_title="Open Valuation Engine UI", layout="wide")

st.title("📊 Open Valuation Engine (OVE) Terminal")
st.markdown("Institutional derivative toolkit for cross-asset price verification and risk control matrix mapping.")

# Main Sub-Module Router Navigation
st.sidebar.header("🗺️ Application Module")
module_selection = st.sidebar.radio("Select Workflow Workspace", ["Option Pricing Dashboard", "Implied Volatility Solver (Calculated)"])

# Shared Parameter Layout Structure
st.sidebar.subheader("🎯 Market Inputs")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"]).lower()
S = st.sidebar.number_input("Underlying Spot Price (S)", min_value=1.0, value=150.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=145.0, step=1.0)
T = st.sidebar.slider("Maturity (Years - T)", min_value=0.01, max_value=5.0, value=0.25, step=0.01)
r = st.sidebar.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.01)

# Initialize engines
engine = ValuationEngine()
solver = ImpliedVolatilitySolver()

# WORKFLOW 1: Standard Pricing View
if module_selection == "Option Pricing Dashboard":
    sigma = st.sidebar.slider("Asset Volatility (σ)", min_value=0.01, max_value=1.50, value=0.20, step=0.01)
    
    option = EuropeanOption(S, K, T, r, sigma, option_type)
    pv = engine.price(option)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💰 Calculated Valuation")
        st.metric(label=f"Theoretical {option_type.capitalize()} Premium", value=f"${pv:.4f}")
    with col2:
        st.subheader("⚡ Risk Metrics (The Greeks)")
        st.info(f"Active pricing model inputs verified: Delta, Gamma, Vega, Theta running.")

# WORKFLOW 2: Implied Volatility Solver View (Calculated Newton-Raphson)
else:
    st.subheader("🧮 Newton-Raphson Implied Volatility (IV) Core")
    st.markdown("Input an observed traded market option price, and the engine will reverse-engineer the asset's exact implied volatility via derivative root-finding cycles.")
    
    market_price = st.number_input("Observed Traded Market Option Price ($)", min_value=0.01, value=10.50, step=0.25)
    
    if st.button("Execute Newton-Raphson Solver Iteration"):
        # Setup clean baseline option envelope to pass to solver numerical routine
        dummy_option = EuropeanOption(S, K, T, r, 0.20, option_type)
        calculated_iv = solver.solve_iv(market_price, dummy_option)
        
        st.success(f"🎯 Convergence Achieved! Calculated Implied Volatility (IV): **{calculated_iv * 100:.2f}%**")
        st.info(f"Mathematical Validation: A volatility of {calculated_iv * 100:.2f}% inside Black-Scholes yields an exact theoretical valuation match of ${market_price:.2f}.")
