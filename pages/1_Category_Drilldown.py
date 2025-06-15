import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st
import pandas as pd
import polars as pl
from utility import get_st_theme, global_data_selector
from utility import datamanager as dm
from utility import visualization as viz
from streamlit_echarts import st_echarts

# ---------------------------
# Page Configuration
# ---------------------------
base_theme = get_st_theme()

# ---------------------------
# Section 1: Data Functions
# ---------------------------
def get_category_dropdown(category_df: pd.DataFrame):
    return category_df['Budget Category'].to_list()

def filter_month_transaction_by_category(df: pl.DataFrame, category: str, month: str, year: int):
    month_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    return df.filter(
        pl.col('Budget Category').eq(category),
        pl.col('Transaction Date').ge(datetime.date(year, month_list.index(month) + 1, 1)),
        pl.col('Transaction Date').lt(datetime.date(year, month_list.index(month) + 2, 1))
    )

# ---------------------------
# Section 2: UI Display Functions
# ---------------------------
def display_budget_category_selectbox(category: list):
    return st.selectbox(
        "Select a Budget Category", 
        category,
        index=category.index('Kebutuhan Harian')
    )

def display_category_metrics(category_df: pd.DataFrame, selected_category: str, unallocated: int):
    # Show metrics
    st.markdown(f"### 💼 {selected_category}")
    col1, col2, col3 = st.columns(3)
    row = category_df[category_df['Budget Category'] == selected_category].iloc[0]

    planned = f"Rp {row["Planned"]:,.0f}"
    actual = f"Rp {row["Actual"]:,.0f}"
    col1.metric("Planned", planned.replace(',','.') + ',00')
    col2.metric("Actual", actual.replace(',','.') + ',00')
    col3.metric("Difference", row["Difference"])

    chart = viz.create_horizontal_bar_chart(row["Planned"], row["Actual"])
    st_echarts(options=chart, height="200px", renderer="svg", theme=base_theme)

def display_stacked_chart(filtered_df: pl.DataFrame):
    dxd_activity = filtered_df.pivot(
        on='Budget Item',
        index=['Transaction Date'],
        values='Transasction Amount',
        aggregate_function='sum'
    ).with_columns(
        pl.col('Transaction Date').dt.to_string()
    ).fill_null(0).sort('Transaction Date').to_pandas().set_index('Transaction Date')

    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": list(dxd_activity.columns)},
        "xAxis": {"type": "category", "data": list(dxd_activity.index)},
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": col,
                "type": "bar",
                "stack": "total",
                "emphasis": {"focus": "series"},
                "data": dxd_activity[col].tolist(),
            } for col in dxd_activity.columns
        ]
    }
    print(options)
    st.subheader('💸 Day-to-day Transaction Summary')
    st_echarts(options=options, height="400px", theme=base_theme)

def display_transaction_table(data: pl.DataFrame):
    # with st.expander("# 📋 Transaction Details"):
    df = data.select(
        pl.exclude([''])
    ).to_pandas()
    st.markdown("### 📋 Transaction Details")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, enableRowGroup=True, editable=False)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, height=400)



# ---------------------------
# Section 3: Main App Logic
# ---------------------------
def main():
    st.title("🔍 Category Drilldown")
    
    year, month, worksheet = global_data_selector()
    category_df = dm.load_category_budget_data()
    metrics = dm.load_overview_metrics()
    unallocated_number = float(metrics['total_remaining'].replace('Rp', '').replace('.', '').replace(',00', ''))

    category = display_budget_category_selectbox(get_category_dropdown(category_df))
    display_category_metrics(category_df, category, unallocated_number)

    transaction_data = dm.load_transaction()
    category_transaction_data = filter_month_transaction_by_category(transaction_data, category, month, year)

    display_stacked_chart(category_transaction_data)
    display_transaction_table(category_transaction_data)

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    main()