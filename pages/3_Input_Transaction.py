import datetime
import gspread
import streamlit as st
import pandas as pd
import polars as pl
from utility import get_st_theme, global_data_selector
from utility import datamanager as dm
from datetime import date, datetime
import requests

def input_google_sheet() -> requests.Response:
    url = st.secrets['insert_url']
    payload = {
        "sheetName": "Money Tracker",
        "rowData": [
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            st.session_state.tx_date.strftime("%d/%m/%Y"),
            st.session_state.cashflow_type,
            st.session_state.amount,
            '',
            st.session_state.account,
            st.session_state.category,
            st.session_state.subcategory,
            st.session_state.notes
            ]
    }
    
    st.session_state.insert_response = requests.post(url, json=payload)
    return st.session_state.insert_response


def show_transaction_form():
    st.title("➕ Add Transaction")
    year, month, worksheet = global_data_selector()
    budget_category = dm.load_category_budget_data()['Budget Category'].to_list()
    montly_budget = dm.load_monthly_budget_data()
    
    def get_budget_item(budget_category):
        return montly_budget.filter(pl.col('Budget Category').eq(budget_category))['Budget Item'].to_list()
            
    account_data = pl.from_pandas(dm.load_account_data()).with_columns(
        account_list = pl.col('Owner') + pl.lit(' - ') + pl.col('Account')
    )
    account_list = account_data['account_list'].to_list()

    # --- Form Container ---
    # Date
    st.session_state.tx_date = st.date_input("Transaction Date", value=date.today())

    # Amount
    st.session_state.amount = st.number_input("Amount (Rp)", min_value=0, step=1000, format="%d")

    # Cashflow Type
    st.session_state.cashflow_type = st.radio("Cashflow Type", ['Expense', 'Savings', 'Income'])

    # Category and Subcategory
    if 'transaction_category' not in st.session_state:
        st.session_state.transaction_category = budget_category[budget_category.index('Kebutuhan Harian')]

    
    def on_category_change():
        st.session_state.transaction_category = st.session_state.category_trans
    
    st.session_state.category = st.selectbox(
        "Budget Category", 
        budget_category, 
        index=budget_category.index(st.session_state.transaction_category),
        key='category_trans',
        on_change=on_category_change
    )
    
    st.session_state.subcategory = st.selectbox(
        "Budget Item", 
        get_budget_item(st.session_state.transaction_category)
    )

    # Account/Source
    st.session_state.account = st.radio("Paid From", account_list, index=1)

    # Notes
    st.session_state.notes = st.text_area("Notes (Optional)", height=100)

    # Submit Button
    submitted = st.button(
        "Submit Transaction", 
        on_click=input_google_sheet
    )
    if submitted:
        if st.session_state.insert_response.status_code == 200:
            st.success("✅ Transaction recorded!")
            st.write("### Summary:")
            st.write({
                "Date": st.session_state.tx_date,
                "Amount": f"Rp {st.session_state.amount:,}",
                "Category": st.session_state.category,
                "Subcategory": st.session_state.subcategory,
                "Account": st.session_state.account,
                "Notes": st.session_state.notes
            })
        else:
            st.write(
                st.session_state.insert_response.json
            )
            

# Run the form
def main():
    show_transaction_form()

# ---------------------------
if __name__ == "__main__":
    main()