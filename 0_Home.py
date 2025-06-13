import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from utility import get_st_theme, global_data_selector
from utility import datamanager as dm
from utility import visualization as viz

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Family Finance Dashboard",
    initial_sidebar_state="collapsed"
)

base_theme = get_st_theme()

# Section 1: Data Functions
# ---------------------------

# ---------------------------
# Section 2: UI Display Functions
# ---------------------------
def display_key_metrics(total_remaining, total_saved):
    st.subheader("📌 Key Metrics Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Remaining Unallocated This Month", total_remaining)
    with col2:
        st.metric("💾 Saved This Month", total_saved)

def display_bank_account_details(total_holding, account_data):
    st.subheader("📊 Detailed Bank Account")
    st.metric("🏦 Total Holding", total_holding)
    st.dataframe(account_data, use_container_width=True, hide_index=True)
    
def display_cashflow_overview(cashflow_data: pd.DataFrame):
    st.subheader("📊 Cashflow Overview")
    cashflow_data.set_index("Cash Flow", inplace=True)
    st.table(cashflow_data)

def display_budgeting_chart(category_df, unallocated):

    def gen_value_remark(category, dif_value, value_string):
        # dif_value = Actual - Plan;
        money = value_string
        color_map = {
            "green": "#2e7d32",
            "red": "#c62828",
            "neutral": "#D4D4D4"
        }
        if category == 'Income':
            if dif_value > 0:
                # dif_value > 0 --> Get more income as planned
                return f"<div style='color:{color_map.get("green")}; font-weight: 500; margin:4px 0;'>You received <b>{money}</b> more income than planned!</div>"
            if dif_value < 0:
                # dif_value < 0 --> Get less income as planned
                return f"<div style='color:{color_map.get("red")}; font-weight: 500; margin:4px 0;'>You received <b>{money}</b> less income than planned!</div>"
            
        if category == 'Expense':
            if dif_value > 0:
                # dif_value > 0 --> Overspending
                return f"<div style='color:{color_map.get("red")}; font-weight: 500; margin:4px 0;'>You overspent <b>{money}</b> more than planned!</div>"
            if dif_value < 0:
                # dif_value < 0 --> Remaining to be allocated
                state = 'remain to be used!' if unallocated != 0 else 'less than planned!'
                return f"<div style='color:{color_map.get("green")}; font-weight: 500; margin:4px 0;'>You have <b>{money}</b> {state}</div>"
            
        if category == 'Savings':
            if dif_value > 0:
                # dif_value > 0 --> Saving more than planned
                return f"<div style='color:{color_map.get("green")}; font-weight: 500; margin:4px 0;'>You saved <b>{money}</b> more than planned!</div>"
            if dif_value < 0:
                # dif_value < 0 --> Saving less than planned
                return f"<div style='color:{color_map.get("red")}; font-weight: 500; margin:4px 0;'>You saved <b>{money}</b> less than planned!</div>"

    st.subheader("📊 Budget Breakdown by Category")
    for _, row in category_df.iterrows():
        if row['Diff'] == 0:
            continue
        st.subheader(f"📦 {row['Budget Category']}")
        
        st.markdown(
            gen_value_remark(row['Cash Flow Type'], row['Diff'], row['Difference']), 
            unsafe_allow_html=True
        )

        chart = viz.create_horizontal_bar_chart(row["Planned"], row["Actual"])
        
        st.markdown(" <style>iframe{ height: 120px } ", unsafe_allow_html=True)
        st_echarts(options=chart, height="100px", renderer="svg", theme=base_theme)
    
    with st.expander("See Details in table"):
        st.dataframe(
            category_df[['Budget Category', 'Planned', 'Actual', 'Difference']], 
            use_container_width=True, 
            hide_index=True
        )


# ---------------------------
# Section 3: Main App Logic
# ---------------------------
def main():
    st.title("💹 Family Finance Dashboard", anchor='am-finance')
    # Filters
    year, month, worksheet = global_data_selector()

    # Load Data
    account_data = dm.load_account_data(worksheet)
    cashflow_data = dm.load_cashflow_data(worksheet)
    category_df = dm.load_category_budget_data(worksheet)

    # Calculations
    overview_metrics = dm.load_overview_metrics(worksheet)
    total_saved = overview_metrics["total_saved"]
    total_remaining = overview_metrics["total_remaining"]
    total_holding = overview_metrics["total_holding"]

    # UI Sections
    Overview_tab, BudgetOverview_tab = st.tabs(["Account Balance", "Budget Overview"])

    with Overview_tab:
        display_key_metrics(total_remaining, total_saved)
        display_cashflow_overview(cashflow_data)
        display_bank_account_details(total_holding, account_data)
        
    with BudgetOverview_tab:
        unallocated_number = float(total_remaining.replace('Rp', '').replace('.', '').replace(',00', ''))
        display_budgeting_chart(category_df, unallocated_number)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    main()
