# WORKFLOW 3: Trade Reconciliation View
else:
    st.subheader("🛡️ Middle-Office Trade Reconciliation Engine")
    st.markdown("Automated comparison ledger auditing front-office trade execution data entries directly against back-office clearing logs to spot booking discrepancies.")

    st.markdown("### 📥 Load Operational Data Logs")
    st.markdown("Upload your custom trading logs below. If no files are uploaded, the engine defaults to institutional demo sheets.")
    
    col_upload1, col_upload2 = st.columns(2)
    
    with col_upload1:
        fo_file = st.file_uploader("Upload Front-Office Log (.csv, .xlsx)", type=["csv", "xlsx"])
    with col_upload2:
        bo_file = st.file_uploader("Upload Back-Office Books (.csv, .xlsx)", type=["csv", "xlsx"])

    # Process Front-Office data (User upload OR Demo fallback)
    if fo_file is not None:
        if fo_file.name.endswith('.csv'):
            df_fo = pd.read_csv(fo_file)
        else:
            df_fo = pd.read_excel(fo_file)
        st.success(f"Loaded Front-Office: {fo_file.name}")
    else:
        fo_csv = "trade_id,instrument_fo,volume_fo,price_fo\nT101,AAPL-C150,100,9.85\nT102,TSLA-P220,250,12.40\nT103,NVDA-C500,500,45.10\nT104,MSFT-C400,150,18.25"
        df_fo = pd.read_csv(io.StringIO(fo_csv))
        st.caption("ℹ️ Displaying sample baseline Front-Office logs.")

    # Process Back-Office data (User upload OR Demo fallback)
    if bo_file is not None:
        if bo_file.name.endswith('.csv'):
            df_bo = pd.read_csv(bo_file)
        else:
            df_bo = pd.read_excel(bo_file)
        st.success(f"Loaded Back-Office: {bo_file.name}")
    else:
        bo_csv = "trade_id,instrument_bo,volume_bo,price_bo\nT101,AAPL-C150,100,9.85\nT102,TSLA-P220,180,12.40\nT103,NVDA-C500,500,45.90\nT105,GOOG-P170,300,6.15"
        df_bo = pd.read_csv(io.StringIO(bo_csv))
        st.caption("ℹ️ Displaying sample baseline Back-Office logs.")

    # Display tables side by side
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🏢 Front-Office Systems Log (FO)")
        st.dataframe(df_fo, use_container_width=True, hide_index=True)
    with col2:
        st.write("### 🏛️ Back-Office Clearing Books (BO)")
        st.dataframe(df_bo, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    if st.button("Run System-Wide Reconciliation Audit"):
        required_fo = ["trade_id", "instrument_fo", "volume_fo", "price_fo"]
        required_bo = ["trade_id", "instrument_bo", "volume_bo", "price_bo"]
        
        # Validation gate: ensuring custom uploaded spreadsheets match our exact header columns
        if not all(col in df_fo.columns for col in required_fo) or not all(col in df_bo.columns for col in required_bo):
            st.error(f"❌ Column Header Mismatch! Please verify your uploaded file columns match these exact headers:\n\nFront-Office expected: {required_fo}\n\nBack-Office expected: {required_bo}")
        else:
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
