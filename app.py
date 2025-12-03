import streamlit as st
from data_handler import SmartFinanceTracker
from visualize import visualize
from llm_service import auto_categorize

# Initialize tracker
ft = SmartFinanceTracker()

st.set_page_config(page_title="Smart Finance Tracker", layout="wide")
st.title("💰 Smart Finance Tracker")

# Session state for predictions
if "predicted_category" not in st.session_state:
    st.session_state.predicted_category = ""
if "predicted_entry_type" not in st.session_state:
    st.session_state.predicted_entry_type = ""

# Function to refresh the recent table
def refresh_recent_entries():
    recent = ft.view_recent_entries(n=5)
    st.subheader("Recent Transactions (5 Latest)")
    if len(recent) == 0:
        st.info("No transactions recorded yet.")
    else:
        st.dataframe(recent)
        st.download_button(
            label="📥 Download CSV",
            data=ft.get_data().to_csv(index=False),
            file_name="finance_data.csv",
            mime="text/csv"
        )


refresh_recent_entries()
st.divider()

st.subheader("Add New Transaction")

# Input fields outside form to allow dynamic prediction
date = st.date_input("Date")
description = st.text_input("Description")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")

# Trigger prediction dynamically when description changes
if description and description != st.session_state.get("last_description", ""):
    category, entry_type = auto_categorize(description)
    st.session_state.predicted_category = category
    st.session_state.predicted_entry_type = entry_type
    st.session_state.last_description = description

# Use predicted values as default
category = st.text_input(
    "Category (auto-predicted, editable)",
    value=st.session_state.predicted_category
)

entry_type = st.selectbox(
    "Type (auto-predicted, editable)",
    options=["Expense", "Income"],
    index=0 if st.session_state.predicted_entry_type.lower() == "expense" else 1
)

# Submit button
if st.button("Add Transaction"):
    if not description or amount <= 0:
        st.error("Please enter a valid description and amount.")
    else:
        ft.add_entry(date=date, note=description, entry_type=entry_type, amount=amount, category=category)
        st.success(f"✅ Added: {description} - {amount} ({category}, {entry_type})")
        # Clear session state predictions after submit
        st.session_state.predicted_category = ""
        st.session_state.predicted_entry_type = ""
        st.session_state.last_description = ""
        refresh_recent_entries()

st.divider()

# Visualization
data = ft.get_data()
if not data.empty:
    st.subheader("Transaction Summary & Visualizations")
    visualize(data)
else:
    st.info("No transactions recorded yet.")
