import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts


# Optional: Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
# Theme selector at the top of sidebar

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.session_state.theme = st.selectbox("🎨 Theme", ["Light", "Dark"], index=["Light", "Dark"].index(st.session_state.theme))

# Apply dark/light mode styles (optional basic simulation)
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# st.set_page_config(page_title="Budget Dashboard", layout="wide")
# st.title("💰 Personal Budget Dashboard")

# Sample data
df = pd.DataFrame({
    "tags": ["Food", "Transport", "Utilities", "Entertainment", "Healthcare"],
    "planned": 1000 * np.array([2000, 1500, 1000, 800, 1200]),
    "actual": 1000 * np.array([1800, 1400, 950, 850, 1000]),
})
df["remaining"] = df["planned"] - df["actual"]

st.title("📊 Budget Overview")
st.markdown("Use the sidebar to switch between views.")

# Show total metrics
total_planned = df["planned"].sum()
total_actual = df["actual"].sum()
total_remaining = df["remaining"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Planned", f"Rp {total_planned:,.0f}")
col2.metric("Total Actual", f"Rp {total_actual:,.0f}")
col3.metric("Remaining", f"Rp {total_remaining:,.0f}")

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
