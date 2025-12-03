import streamlit as st
import plotly.express as px

def visualize(data):
    category_totals = data.groupby("Category")["Amount"].sum().reset_index()

    # --- Bar Chart ---
    st.subheader("Expense Breakdown by Category")
    fig_bar = px.bar(
        category_totals,
        x="Category",
        y="Amount",
        text="Amount",
        title="Expenses by Category",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Pie Chart ---
    st.subheader("Category Distribution")
    fig_pie = px.pie(
        category_totals,
        names="Category",
        values="Amount",
        title="Category Distribution",
        hole=0.3,  # donut style
        template="plotly_white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)