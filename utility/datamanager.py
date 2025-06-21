import polars as pl
import pandas as pd
import streamlit as st
from utility import get_worksheet
from utility.utils import currency_to_number

@st.cache_data(show_spinner="Loading monthly budget data...")
def load_account_data() -> pd.DataFrame:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["accounts_state"])
    account_data = pl.DataFrame(sheet.get_all_records()).select(
        pl.col("Alias").str.split(' - ').list.get(1).alias('Account'),
        pl.col("Alias").str.split(' - ').list.get(0).alias('Owner'),
        pl.col('Account Balance')
    ).to_pandas()
    return account_data

def load_cashflow_data():
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_overview"])
    cash_flow_raw = sheet.get_values(st.secrets["table_definition"]["cash_flow"])
    return pd.DataFrame(cash_flow_raw[1:], columns=cash_flow_raw[0])    

@st.cache_data(show_spinner="Loading monthly budget data...")
def load_category_budget_data() -> pd.DataFrame:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_overview"])
    category_overview_raw = sheet.get_values(st.secrets["table_definition"]["category_overview"])
    category_data = pl.from_pandas(pd.DataFrame(category_overview_raw[1:], columns=category_overview_raw[0]))
    
    if 'category_summary' not in st.session_state:
        st.session_state.category_summary = category_data.with_columns(
            currency_to_number('Planned').abs(),
            currency_to_number('Actual').abs(),
            (currency_to_number('Actual').abs() - currency_to_number('Planned').abs()).alias('Diff')
        ).to_pandas()

    return st.session_state.category_summary

@st.cache_data(show_spinner="Loading monthly budget data...")
def load_monthly_budget_data() -> pl.DataFrame:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_planning"])
    monthly_budget = pl.DataFrame(sheet.get_all_records())

    return monthly_budget

def load_overview_metrics() -> dict:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_overview"])
    if 'overall_metrics' not in st.session_state:
        st.session_state.overall_metrics = {
        'total_saved': sheet.get_values('Total_This_Month_Saving')[0][0],
        'total_remaining': sheet.get_values('Unallocated')[0][0],
        'total_holding': sheet.get_values('Total_Holding')[0][0],
    }
    return st.session_state.overall_metrics

@st.cache_data(show_spinner="Loading transaction data...")
def load_transaction() -> pl.DataFrame:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(
        st.secrets["sheets_id"]["money_tracker"]
    )
    return pl.DataFrame(sheet.get_all_records()).with_columns(
        currency_to_number('Transasction Amount'),
        currency_to_number('Cashflow'),
        pl.col('Transaction Date').str.to_date('%d/%m/%Y')
    )

def load_anual_budget() -> pl.DataFrame:
    worksheet = get_worksheet()
    sheet = worksheet.get_worksheet_by_id(
        st.secrets["sheets_id"]["anual_planning"]
    )
    return pl.DataFrame(sheet.get_all_records()).with_columns(
        pl.col('Funds Achieved').eq('TRUE'),
        currency_to_number('Financial Goal'),
        currency_to_number('Currenlty Achieved'),
        currency_to_number('Remaining'),
        pl.col('Due Date').str.to_date("%d/%m/%Y")
    ).filter(
        pl.col('Funds Achieved').eq(False)
    )

    