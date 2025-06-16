import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import pandas as pd
import polars as pl
from utility import get_st_theme, global_data_selector
from utility import datamanager as dm
from utility import visualization as viz
from streamlit_echarts import st_echarts

# ---------------------------
# Section 1: Data Functions
# ---------------------------
def get_category_dropdown(finance_goal_df: pd.DataFrame):
    return finance_goal_df['Budget Item'].to_list()

# ---------------------------
# Section 2: UI Display Functions
# ---------------------------
def display_finance_goal_selectbox(category: list):
    return st.selectbox(
        "Select a Budget Category", 
        category,
        index=category.index('Tabungan Haji')
    )

def display_finance_goal_metrics(finance_goal_df: pd.DataFrame, selected_category: str):
    def months_difference(date1, date2):
        """Calculates the difference between two dates in months."""
        
        delta = relativedelta(date2, date1)
        return delta.years * 12 + delta.months
    
    st.subheader(f"📌 {selected_category}")
    row = finance_goal_df[finance_goal_df['Budget Item'] == selected_category].iloc[0]
    col1, col2, col3 = st.columns(3)

    target = f'Rp {row['Financial Goal']:,.0f}'
    achieved = f'Rp {row['Currenlty Achieved']:,.0f}'
    remaining = f'Rp {row['Remaining']:,.0f}'

    col1.metric("🎯 Financial Goal", target.replace(',','.') + ',00')
    col2.metric("💰 Saved", achieved.replace(',','.') + ',00')
    col3.metric("🧮 Remaining", remaining.replace(',','.') + ',00')

    due_date = row['Due Date']
    st.write(f"🗓️ **Deadline**: {due_date.date()} ({months_difference(datetime.date.today(), due_date)} months left)")
    st.write(f"📈 **Progress**: {100 * (row['Currenlty Achieved']/row['Financial Goal'])}%")

# ---------------------------
# Section 3: Main App Logic
# ---------------------------

def main():
    st.title("🎯 Financial Goals Progress")

    year, month, worksheet = global_data_selector()
    anual_budget = dm.load_anual_budget()
    category = display_finance_goal_selectbox(get_category_dropdown(anual_budget))
    display_finance_goal_metrics(anual_budget.to_pandas(), category)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    main()