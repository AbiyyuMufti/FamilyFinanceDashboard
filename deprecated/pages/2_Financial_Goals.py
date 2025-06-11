import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_echarts import st_echarts

# Simulated financial goals data
goals_data = [
    {"goal": "Mortgage 2025", "target": 36000000, "saved": 18000000, "deadline": "2025-12-01", "frequency": "Yearly"},
    {"goal": "Emergency Fund", "target": 30000000, "saved": 12000000, "deadline": "2025-06-01", "frequency": "One-time"},
    {"goal": "Hajj Saving", "target": 50000000, "saved": 25000000, "deadline": "2026-08-01", "frequency": "Monthly"},
    {"goal": "New Laptop", "target": 15000000, "saved": 6000000, "deadline": "2025-09-30", "frequency": "One-time"},
]

# Prepare dataframe
df = pd.DataFrame(goals_data)
df["deadline"] = pd.to_datetime(df["deadline"])
df["remaining"] = df["target"] - df["saved"]
df["progress_pct"] = (df["saved"] / df["target"] * 100).round(2)

# Page title
st.title("🎯 Financial Goals Progress")

# Select a goal
goal_list = df["goal"].tolist()
selected_goal = st.selectbox("Select a Goal to View Progress", goal_list)

# Extract selected goal info
goal_row = df[df["goal"] == selected_goal].iloc[0]
days_remaining = (goal_row["deadline"] - datetime.today()).days

# Metrics
st.subheader(f"📌 {selected_goal}")
col1, col2, col3 = st.columns(3)
col1.metric("🎯 Target", f"Rp {goal_row['target']:,}")
col2.metric("💰 Saved", f"Rp {goal_row['saved']:,}")
col3.metric("🧮 Remaining", f"Rp {goal_row['remaining']:,}")

# Deadline & progress
st.write(f"🗓️ **Deadline**: {goal_row['deadline'].date()} ({days_remaining} days left)")
st.write(f"📈 **Progress**: {goal_row['progress_pct']}%")

# --- ECharts: Gauge Progress Chart ---
gauge_option = {
    "series": [
        {
            "type": "gauge",
            "progress": {"show": True, "width": 18},
            "axisLine": {"lineStyle": {"width": 18}},
            "axisTick": {"show": False},
            "splitLine": {"length": 15, "lineStyle": {"width": 2, "color": "#999"}},
            "axisLabel": {"distance": 25, "color": "#999", "fontSize": 14},
            "anchor": {"show": True, "showAbove": True, "size": 20, "itemStyle": {"borderWidth": 10}},
            "title": {"show": True, "offsetCenter": [0, "60%"]},
            "detail": {
                "valueAnimation": True,
                "formatter": "{value}%",
                "fontSize": 24
            },
            "data": [{"value": float(goal_row["progress_pct"]), "name": "Progress"}]
        }
    ]
}
st_echarts(options=gauge_option, height="400px")

# --- Simulate Monthly Savings Data ---
def simulate_monthly_progress(saved_total, months=7):
    base = saved_total / months
    progress = np.cumsum(np.random.normal(loc=base, scale=base * 0.1, size=months)).clip(min=0, max=saved_total)
    dates = pd.date_range(end=datetime.today(), periods=months, freq="M").to_pydatetime()
    return pd.DataFrame({"month": [d.strftime("%b %Y") for d in dates], "saved": progress.astype(int)})

monthly_df = simulate_monthly_progress(goal_row["saved"])

# --- ECharts: Line Chart for Monthly Progress ---
st.subheader("📊 Monthly Savings Progress")

line_option = {
    "tooltip": {"trigger": "axis"},
    "xAxis": {
        "type": "category",
        "data": monthly_df["month"].tolist(),
        "axisLabel": {"rotate": 30}
    },
    "yAxis": {"type": "value", "name": "Saved (Rp)"},
    "series": [{
        "data": monthly_df["saved"].tolist(),
        "type": "line",
        "smooth": True,
        "areaStyle": {},
        "name": "Saved"
    }],
    "color": ["#91cc75"]
}
st_echarts(options=line_option, height="400px")

# --- Expandable Full Table ---
with st.expander("📋 View All Goals"):
    st.dataframe(df[["goal", "target", "saved", "remaining", "progress_pct", "deadline"]])
