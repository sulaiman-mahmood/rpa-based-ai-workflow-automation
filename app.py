import streamlit as st
import pandas as pd
import joblib
import os
import random
from datetime import datetime

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="AI Approval Automation Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------
# Sidebar Login
# ------------------------
with st.sidebar:
    st.title("AI Portal Login")
    username = st.text_input("Username", key="username_input", placeholder="Enter Username")
    password = st.text_input("Password", type="password", key="password_input", placeholder="Enter Password")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.button("🔐 Login", key="login_button_sidebar"):
        if username == "admin" and password == "nextai123":
            st.session_state["logged_in"] = True
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ------------------------
# Main Page
# ------------------------
st.title("AI Approval Automation Portal")

# --- Initialize session state safely ---
for key, default in {
    "pending_data": None,
    "ai_done": False,
    "processed": [],
    "results_log": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if not st.session_state["logged_in"]:
    st.info("Please log in using the sidebar to continue.")
else:
    st.success("Welcome, Admin. You can now process pending requests.")

    # ------------------------
    # Generate Random Pending Requests
    # ------------------------
    def generate_requests(n=10):
        data = []
        for i in range(n):
            invoice = f"INV-{random.randint(1000, 9999)}"
            amount = random.randint(100, 2000)
            customer_score = random.randint(1, 10)
            urgency = random.randint(1, 5)
            data.append([invoice, amount, customer_score, urgency])
        return pd.DataFrame(data, columns=["InvoiceID", "Amount", "CustomerScore", "Urgency"])

    # ------------------------
    # Setup Folders
    # ------------------------
    os.makedirs("pending", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    if st.session_state["pending_data"] is None:
        st.session_state["pending_data"] = generate_requests(12)

    # ------------------------
    # Step 1: Download Pending Requests
    # ------------------------
    if st.button("⬇️ Download Pending Requests", key="download_btn"):
        df_pending = st.session_state["pending_data"]
        df_pending.to_csv("pending/pending_invoices.csv", index=False)
        st.dataframe(df_pending, use_container_width=True)
        st.success("Pending requests exported successfully.")

    # ------------------------
    # Step 2: Run AI Automation
    # ------------------------
    if st.button("🤖 Run AI Automation", key="run_ai_btn") or st.session_state["ai_done"]:
        try:
            model = joblib.load("approval_model.pkl")
            pending = st.session_state["pending_data"]

            # Predict once
            if not st.session_state["ai_done"]:
                X = pending[["Amount", "CustomerScore", "Urgency"]]
                preds = model.predict(X)
                probs = model.predict_proba(X)[:, 1]
                pending["AI_Confidence"] = (probs * 100).round(1)
                pending["AI_Suggestion"] = ["Approve" if p == 1 else "Reject" for p in preds]
                pending["Final_Decision"] = [
                    "Manual Review" if 40 < c < 60 else s
                    for c, s in zip(pending["AI_Confidence"], pending["AI_Suggestion"])
                ]
                st.session_state["pending_data"] = pending
                st.session_state["ai_done"] = True
                pending.to_excel("results/AI_Results_latest.xlsx", index=False)

            pending = st.session_state["pending_data"]

            st.success("AI automation completed. Ready for review.")
            st.subheader("AI Review Queue")

            st.dataframe(pending, use_container_width=True)
            st.page_link("pages/1_Decision_Mode.py", label="➡️ Enter Decision Mode", icon="🧠")

        except Exception as e:
            st.error(f"Error running AI model: {e}")
