import streamlit as st
import pandas as pd
import polars as pl
from streamlit_echarts import st_echarts
from streamlit_theme import st_theme

from utility import global_data_selector


# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="💹 Family Finance Dashboard",
    # menu_title="Family Finance Dashboard",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }    
)

# st.Page("Family Finance Dashboard")
theme = st_theme()
base_theme = theme.get("base", "light")
# base_theme = theme
print(base_theme)

# Section 1: Data Functions
# ---------------------------
def load_account_data():
    return pd.DataFrame({
        'Account': ['Bank A', 'Bank B', 'Bank C', 'Bank D', 'Bank E', 'Bank F'],
        'Owner': ['You', 'You', 'Spouse', 'Spouse', 'You', 'Spouse'],
        'Balance': [3_200_000, 1_800_000, 2_750_000, 1_250_000, 1_000_000, 2_000_000]
    })


def load_cashflow_data():
    return {
        'Planned': {'Income': 15_000_000, 'Expense': 10_000_000, 'Savings': 5_000_000},
        'Actual': {'Income': 14_800_000, 'Expense': 10_300_000, 'Savings': 4_500_000}
    }


def compute_cashflow_diff(data):
    return {
        key: data['Actual'][key] - data['Planned'][key]
        for key in data['Planned']
    }


def load_category_budget_data():
    df = pd.DataFrame({
        'Category': ['Food', 'Transport', 'Rent', 'Utilities', 'Entertainment'],
        'Planned': [2_000_000, 1_000_000, 4_000_000, 1_500_000, 1_000_000],
        'Actual': [2_200_000, 800_000, 4_000_000, 1_600_000, 900_000],
    })
    df['Difference'] = df['Actual'] - df['Planned']
    return df


# ---------------------------
# Section 2: UI Display Functions
# ---------------------------

def display_key_metrics(total_remaining, total_saved):
    st.subheader("📌 Key Metrics Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Remaining Unallocated This Month", f"Rp {total_remaining:,.0f}")
    with col2:
        st.metric("💾 Saved This Month", f"Rp {total_saved:,.0f}")
    

def display_bank_account_details(total_holding, account_data):
    st.subheader("📊 Detailed Bank Account")
    st.metric("🏦 Total Holding", f"Rp {total_holding:,.0f}")
    # with st.expander(, expanded=False):
    account_data.set_index('Account', inplace=True)
    st.dataframe(account_data, use_container_width=True)
    
        # for _, row in account_data.iterrows():
        #     st.write(f"• {row['Account']} ({row['Owner']}): Rp {row['Balance']:,.0f}")

def display_cashflow_overview(cashflow_data, cashflow_diff):
    st.subheader("📊 Cashflow Overview")
    cashflow_df = pd.DataFrame({
        "Planned": cashflow_data["Planned"],
        "Actual": cashflow_data["Actual"],
        "Difference": cashflow_diff
    })
    st.table(cashflow_df.style.format("Rp {:,.0f}"))

def display_budgeting_chart(category_df):
    def create_horizontal_bar_chart(planned, actual):
        return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "xAxis": {
            "type": "value",
            "show": False,
        },
        "yAxis": {
            "type": "category",
            "data": ["Planned", "Actual"],
            "axisLabel": {
                "margin": 8,
                "fontSize": 10
            },
            "axisLine": {
                "show": False
            },
            "axisTick": {
                "show": False
            }
        },
        "series": [
            {
                "type": "bar",
                "data": [
                    {
                        "value": planned,
                        "itemStyle": {"color": "#5400C6"},
                    },
                    {
                        "value": actual,
                        "itemStyle": {"color": "#FF6B6B"},
                    }
                ],
                # "barWidth": "40%",
                # "barGap": "-100%",
                # "barCategoryGap": "20%",
                "label": {
                    "show": True,
                    "position": "insideLeft",
                    "formatter": "{c}",
                    "fontSize": 10,
                }
            }
        ],
        "grid": {
            "left": "3%",
            "right": "12%",
            "top": "5%",
            "bottom": "0%",
            "containLabel": True
        }
    }
    
    st.subheader("📊 Budget Breakdown by Category")
    for _, row in category_df.iterrows():
        diff = row["Difference"]
        diff_text = f"Rp {abs(diff):,.0f} {'remaining' if diff >= 0 else 'overspent'}"
        st.subheader(f"📦 {row['Category']} — {diff_text}")
        # with st.expander(f"📦 {row['Category']} — {diff_text}"):
        chart = create_horizontal_bar_chart(row["Planned"], row["Actual"])
        st_echarts(options=chart, height="100px", renderer="svg", theme=base_theme)


# ---------------------------
# Section 3: Main App Logic
# ---------------------------
def main():
    st.title("💼 Family Finance Dashboard", anchor='am-finance')

    # Filters
    year, month = global_data_selector()

    # Load Data
    account_data = load_account_data()
    cashflow_data = load_cashflow_data()
    category_df = load_category_budget_data()

    # Calculations
    cashflow_diff = compute_cashflow_diff(cashflow_data)
    total_saved = cashflow_data['Actual']['Savings']
    total_remaining = 4_250_000  # Simulated value
    total_holding = account_data['Balance'].sum()

    # UI Sections
    Overview_tab, BudgetOverview_tab = st.tabs(["Account Balance", "Budget Overview"])
    # Overview_tab.
    with Overview_tab:
        display_key_metrics(total_remaining, total_saved)
        display_cashflow_overview(cashflow_data, cashflow_diff)
        display_bank_account_details(total_holding, account_data)
    with BudgetOverview_tab:
        st.markdown(" <style>iframe{ height: 100px } ", unsafe_allow_html=True)
        display_budgeting_chart(category_df)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    main()
