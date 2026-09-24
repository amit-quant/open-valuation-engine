import pandas as pd
import numpy as np

class TradeReconciliationEngine:
    def __init__(self):
        pass

    def run_reconciliation(self, front_office_df: pd.DataFrame, back_office_df: pd.DataFrame) -> pd.DataFrame:
        """
        Reconciles Front-Office executions against Back-Office books.
        Flags perfect matches, size mismatches, rate/premium breaks, or missing logs.
        """
        if front_office_df.empty or back_office_df.empty:
            return pd.DataFrame()

        # Merge datasets using unique identifier keys
        merged = pd.merge(
            front_office_df, 
            back_office_df, 
            on="trade_id", 
            how="outer", 
            suffixes=("_fo", "_bo")
        )

        reconciliation_report = []

        for idx, row in merged.iterrows():
            trade_id = row["trade_id"]
            
            # Case 1: Trade missing from Back Office records
            if pd.isna(row["instrument_bo"]):
                status = "⚠️ BREAK: Missing in Back Office"
                details = f"FO booked {row['volume_fo']} lots of {row['instrument_fo']} but no clearing records found."
            
            # Case 2: Trade missing from Front Office systems
            elif pd.isna(row["instrument_fo"]):
                status = "⚠️ BREAK: Missing in Front Office"
                details = f"BO clearing logged {row['volume_bo']} lots of {row['instrument_bo']} but no trading floor records found."
            
            # Case 3: Complete matching records found
            else:
                vol_match = row["volume_fo"] == row["volume_bo"]
                price_match = np.isclose(row["price_fo"], row["price_bo"], atol=1e-4)

                if vol_match and price_match:
                    status = "✅ MATCHED"
                    details = f"Trade cleared cleanly at ${row['price_fo']:.2f} for {row['volume_fo']} contracts."
                elif not vol_match and price_match:
                    status = "❌ BREAK: Volume Mismatch"
                    details = f"FO reports {row['volume_fo']} units vs. BO records showing {row['volume_bo']} units."
                elif vol_match and not price_match:
                    status = "❌ BREAK: Cash Premium Mismatch"
                    details = f"FO price of ${row['price_fo']:.4f} diverges from BO execution value of ${row['price_bo']:.4f}."
                else:
                    status = "❌ BREAK: Dual Field Variance"
                    details = "Discrepancies found in both total contract volume and asset execution pricing lines."

            reconciliation_report.append({
                "Trade ID": trade_id,
                "Instrument": row["instrument_fo"] if not pd.isna(row["instrument_fo"]) else row["instrument_bo"],
                "Reconciliation Status": status,
                "Audit Ledger Details": details
            })

        return pd.DataFrame(reconciliation_report)
