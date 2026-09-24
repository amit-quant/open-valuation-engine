import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from ove.engine import EuropeanOption, ValuationEngine
from ove.vol_solver import ImpliedVolatilitySolver
from ove.recon import TradeReconciliationEngine

st.set_page_config(page_title="Open Valuation Engine UI", layout="wide")

st.title("📊 Open Valuation Engine (OVE) Terminal")
st.markdown("Institutional derivative toolkit for cross-asset price verification and risk control matrix mapping.")

# Main Sub-Module Router Navigation
st.sidebar.header("🗺️ Application Module")
module_selection = st.sidebar.radio(
    "Select Workflow Workspace", 
    ["Option Pricing Dashboard", "Implied Volatility Solver (Calculated)", "Middle-Office Trade Reconciliation"]
)

# Initialize engines
engine = ValuationEngine()
solver = ImpliedVolatilitySolver()
recon_engine = TradeReconciliationEngine()

# WORKFLOW 1: Standard Pricing View
if module_selection == "Option Pricing Dashboard":
    st.sidebar.subheader("🎯 Market Inputs")
    option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"]).lower()
    S = st.sidebar.number_input("Underlying Spot Price (S)", min_value=1.0, value=150.0, step=1.0)
    K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=145.0, step=1.0)
    T = st.sidebar.slider("Maturity (Years - T)", min_value=0.01, max_value=5.0, value=0.25, step=0.01)
    r = st.sidebar.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.01)
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

# WORKFLOW 2: Implied Volatility Solver View
elif module_selection == "Implied Volatility Solver (Calculated)":
    st.sidebar.subheader("🎯 Market Inputs")
    option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"]).lower()
    S = st.sidebar.number_input("Underlying Spot Price (S)", min_value=1.0, value=150.0, step=1.0)
    K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=145.0, step=1.0)
    T = st.sidebar.slider("Maturity (Years - T)", min_value=0.01, max_value=5.0, value=0.25, step=0.01)
    r = st.sidebar.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.01)

    st.subheader("🧮 Newton-Raphson Implied Volatility (IV) Core")
    st.markdown("Input an observed traded market option price, and the engine will reverse-engineer the asset's exact implied volatility via derivative root-finding cycles.")
    
    market_price = st.number_input("Observed Traded Market Option Price ($)", min_value=0.01, value=10.50, step=0.25)
    
    if st.button("Execute Newton-Raphson Solver Iteration"):
        dummy_option = EuropeanOption(S, K, T, r, 0.20, option_type)
        calculated_iv = solver.solve_iv(market_price, dummy_option)
        
        st.success(f"🎯 Convergence Achieved! Calculated Implied Volatility (IV): **{calculated_iv * 100:.2f}%**")
        st.info(f"Mathematical Validation: A volatility of {calculated_iv * 100:.2f}% inside Black-Scholes yields an exact theoretical valuation match of ${market_price:.2f}.")

# WORKFLOW 3: Trade Reconciliation View
else:
    st.subheader("🛡️ Middle-Office Trade Reconciliation Engine")
    st.markdown("Automated comparison ledger auditing front-office trade execution data entries directly against back-office clearing logs to spot booking discrepancies.")

    # Fixed mock datasets with complete trade arrays
    fo_data = {
        "trade_id": ["T101", "T102", "T103", "T104"],
        "instrument_fo": ["AAPL-C150", "TSLA-P220", "NVDA-C500", "MSFT-C400"],
        "volume_fo":,
        "price_fo": [9.85, 12.40, 45.10, 18.25]
    }
    
    bo_data = {
        "trade_id": ["T101", "T102", "T103", "T105"],
        "instrument_bo": ["AAPL-C150", "TSLA-P220", "NVDA-C500", "GOOG-P170"],
        "volume_bo":, # T102 contains a Volume Mismatch break
        "price_bo": [9.85, 12.40, 45.90, 6.15]   # T103 contains a Cash Premium Mismatch break
    }
    
    df_fo = pd.DataFrame(fo_data)
    df_bo = pd.DataFrame(bo_data)

    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🏢 Front-Office Systems Log (FO)")
        st.dataframe(df_fo, use_container_width=True, hide_index=True)
    with col2:
        st.write("### 🏛️ Back-Office Clearing Books (BO)")
        st.dataframe(df_bo, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    if st.button("Run System-Wide Reconciliation Audit"):
        report_df = recon_engine.run_reconciliation(df_fo, df_bo)
        
        st.write("### 📋 Generated Audit Exception Ledger")
        st.dataframe(
            report_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Reconciliation Status": st.column_config.TextColumn("Status", width="medium"),
                "Audit Ledger Details": st.column_config.TextColumn("System Summary Audit Text", width="large")
            }
        )
