import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Decision Mode",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Initialize session safely ---
for key, default in {
    "pending_data": None,
    "ai_done": False,
    "processed": [],
    "results_log": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Safety Check ---
if not st.session_state["ai_done"] or st.session_state["pending_data"] is None:
    st.warning("⚠️ No AI results found! Please run AI Automation first from the main dashboard.")
    st.stop()

# --- Load pending requests ---
pending = st.session_state["pending_data"]

st.title("Decision Mode")

# --- Progress Tracker ---
processed_count = len(st.session_state["processed"])
total_invoices = len(pending)

if processed_count < total_invoices:
    st.info(f"Processing invoice {processed_count + 1} of {total_invoices}")

    # --- Current Invoice ---
    current_idx = processed_count
    row = pending.iloc[current_idx]

    st.subheader(f"Invoice: {row['InvoiceID']}")
    st.write(f"Amount: £{row['Amount']}")
    st.write(f"Customer Score: {row['CustomerScore']}")
    st.write(f"Urgency: {row['Urgency']}")
    st.write(f"AI Confidence: {row['AI_Confidence']}%")
    st.write(f"AI Suggestion: **{row['Final_Decision']}**")

    st.markdown("---")

    # --- Action Buttons ---
    col1, col2, col3 = st.columns(3)
    if col1.button(f"✅ Approve", key=f"approve_{row['InvoiceID']}"):
        st.session_state["processed"].append({"InvoiceID": row["InvoiceID"], "Action": "Approved"})
        st.rerun()

    if col2.button(f"❌ Reject", key=f"reject_{row['InvoiceID']}"):
        st.session_state["processed"].append({"InvoiceID": row["InvoiceID"], "Action": "Rejected"})
        st.rerun()

    if col3.button(f"🕵️ Manual Review", key=f"manual_{row['InvoiceID']}"):
        st.session_state["processed"].append({"InvoiceID": row["InvoiceID"], "Action": "Manual Review"})
        st.rerun()

    # --- ✅ Add fixed invisible HTML IDs for PAD to target ---
    st.markdown(f"""
    <div id="approve_button_{row['InvoiceID']}"></div>
    <div id="reject_button_{row['InvoiceID']}"></div>
    <div id="manual_button_{row['InvoiceID']}"></div>
    """, unsafe_allow_html=True)

else:
    # --- All Done: Summary View ---
    st.success("✅ All invoices processed!")

    df_processed = pd.DataFrame(st.session_state["processed"])
    summary = df_processed["Action"].value_counts().to_dict()

    total = len(df_processed)
    approved = summary.get("Approved", 0)
    rejected = summary.get("Rejected", 0)
    manual = summary.get("Manual Review", 0)

    st.subheader("Summary Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Processed", total)
    col2.metric("Approved", approved)
    col3.metric("Rejected", rejected)
    col4.metric("Manual Review", manual)

    st.bar_chart(df_processed["Action"].value_counts())

    # --- Save results for record ---
    result_df = pd.merge(
        pending,
        df_processed,
        on="InvoiceID",
        how="left"
    )

    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = f"results/final_results_{timestamp}.xlsx"
    result_df.to_excel(result_path, index=False)

    st.info(f"Results saved to: {result_path}")

    if st.button("🔙 Back to Dashboard"):
        st.switch_page("app.py")
