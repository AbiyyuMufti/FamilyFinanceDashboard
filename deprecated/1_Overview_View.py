import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Sample data
df = pd.DataFrame({
    "tags": ["Food", "Transport", "Utilities", "Entertainment", "Healthcare"],
    "planned": [2000, 1500, 1000, 800, 1200],
    "actual": [1800, 1400, 950, 850, 1000],
})
df["remaining"] = df["planned"] - df["actual"]

st.title("📊 Budget Overview")

# Show total metrics
total_planned = df["planned"].sum()
total_actual = df["actual"].sum()
total_remaining = df["remaining"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Planned", f"${total_planned:,.0f}")
col2.metric("Total Actual", f"${total_actual:,.0f}")
col3.metric("Remaining", f"${total_remaining:,.0f}")

# ECharts: Stacked horizontal bar
bar_option = {
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Actual", "Remaining"]},
    "xAxis": {"type": "value"},
    "yAxis": {
        "type": "category",
        "data": df["tags"].tolist()
    },
    "series": [
        {
            "name": "Actual",
            "type": "bar",
            "stack": "total",
            "data": df["actual"].tolist(),
            "itemStyle": {"color": "#4CAF50"}
        },
        {
            "name": "Remaining",
            "type": "bar",
            "stack": "total",
            "data": df["remaining"].tolist(),
            "itemStyle": {"color": "#FFC107"}
        }
    ]
}

st_echarts(options=bar_option, height="400px")

# Show table
st.subheader("📋 Budget Details")
st.dataframe(df, use_container_width=True)
