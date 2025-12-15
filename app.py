import pandas as pd
import streamlit as st
from data_handler import SmartFinanceTracker
from llm_service import FinanceInsightService
from visualize import visualize
import calendar
import uuid
# -------------------------
# Load services (cached)
# -------------------------
@st.cache_resource
def load_services():
    return SmartFinanceTracker(), FinanceInsightService()

ft, fi = load_services()

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="💰 FinSight-AI", layout="wide")
st.title("💰 FinSight-AI")

# -------------------------
# Session state defaults
# -------------------------
if "predicted_category" not in st.session_state:
    st.session_state.predicted_category = ""
if "predicted_entry_type" not in st.session_state:
    st.session_state.predicted_entry_type = ""
if "last_description" not in st.session_state:
    st.session_state.last_description = ""

# -------------------------
# Cached data
# -------------------------
@st.cache_data
def get_df():
    return ft.get_data()


@st.cache_data
def get_month_names():
    return list(calendar.month_name)[1:]


df = get_df()

# -------------------------
# Recent Transactions
# -------------------------
def refresh_recent_entries():
    recent = ft.view_recent_entries(n=5)
    st.subheader("Recent Transactions (5 Latest)")
    if recent.empty:
        st.info("No transactions recorded yet.")
    else:
        st.dataframe(recent)
        st.download_button(
            label="📥 Download CSV",
            data=ft.get_data().to_csv(index=False),
            file_name="finance_data.csv",
            mime="text/csv",
            key=f"download-csv-{uuid.uuid4()}"
        )

refresh_recent_entries()
st.divider()

# -------------------------
# Monthly Insights
# -------------------------
st.subheader("📅 Monthly Insights")

year, month = st.columns(2)
with year:
    sel_year = st.selectbox("Year", sorted(df["Date"].dt.year.unique()))
with month:
    month_names = get_month_names()
    sel_month_name = st.selectbox("Month", month_names)
    sel_month = month_names.index(sel_month_name) + 1

if st.button("Generate Insights"):
    with st.spinner("Analyzing spending with AI..."):
        insight = fi.auto_monthly_summary(df, sel_year, sel_month)
    st.markdown("### 🧠 Insights")
    st.info(insight)

st.divider()

# -------------------------
# Add New Transaction
# -------------------------
st.subheader("➕ Add New Transaction")

# Initialize cache for predictions if not present
if "predictions_cache" not in st.session_state:
    st.session_state.predictions_cache = {}

date_col, desc_col, amt_col = st.columns([1, 2, 1])
with date_col:
    date = st.date_input("Date")
with desc_col:
    description = st.text_input("Description")
with amt_col:
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")

# -------------------------
# Dynamic LLM prediction with caching
# -------------------------
if description:
    if description in st.session_state.predictions_cache:
        # Use cached prediction
        category, entry_type = st.session_state.predictions_cache[description]
    else:
        try:
            with st.spinner("Predicting category..."):
                category, entry_type = fi.auto_categorize(description)
                # Cache prediction to avoid repeated API calls
                st.session_state.predictions_cache[description] = (category, entry_type)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            category, entry_type = "", "Expense"

    # Update session state for UI defaults
    st.session_state.predicted_category = category
    st.session_state.predicted_entry_type = entry_type

# -------------------------
# Input widgets for category and type
# -------------------------
category = st.text_input(
    "Category (auto-predicted, editable)",
    value=st.session_state.predicted_category
)
entry_type = st.selectbox(
    "Type (auto-predicted, editable)",
    options=["Expense", "Income"],
    index=0 if st.session_state.predicted_entry_type.lower() == "expense" else 1
)

# -------------------------
# Submit transaction
# -------------------------
if st.button("Add Transaction"):
    if not description or amount <= 0:
        st.error("Please enter a valid description and amount.")
    else:
        ft.add_entry(
            date=date,
            note=description,
            entry_type=entry_type,
            amount=amount,
            category=category
        )
        st.success(f"✅ Added: {description} - {amount} ({category}, {entry_type})")
        # Clear session state for new entry
        st.session_state.predicted_category = ""
        st.session_state.predicted_entry_type = ""
        st.session_state.last_description = ""
        
        # Optional: remove from cache to force re-prediction if user reuses the same note later
        if description in st.session_state.predictions_cache:
            del st.session_state.predictions_cache[description]
        
        refresh_recent_entries()

st.divider()

# -------------------------
# Visualizations
# -------------------------
st.subheader("📊 Transaction Summary & Visualizations")
if not df.empty:
    with st.spinner("Generating visualizations..."):
        visualize(df)
else:
    st.info("No transactions recorded yet.")
