import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

from utility import global_data_selector

# Sample data
df = pd.DataFrame({
    "tags": ["Food", "Transport", "Utilities", "Entertainment", "Healthcare"],
    "planned": 1000 * np.array([2000, 1500, 1000, 800, 1200]),
    "actual": 1000 * np.array([1800, 1400, 950, 850, 1000]),
})
df["remaining"] = df["planned"] - df["actual"]


year, month = global_data_selector()
st.title("🔍 Category Drilldown")

# Dropdown selector
category = st.selectbox("Select a Budget Category", df["tags"])

row = df[df["tags"] == category].iloc[0]
# Convert to native types
planned = int(row["planned"])
actual = int(row["actual"])
remaining = int(row["remaining"])

# Show metrics
st.markdown(f"### 💼 {category}")
col1, col2, col3 = st.columns(3)
col1.metric("Planned", f"Rp {planned:,.0f}")
col2.metric("Actual", f"Rp {actual:,.0f}")
col3.metric("Remaining", f"Rp {remaining:,.0f}")

# Grouped bar chart
bar_option = {
    "xAxis": {
        "type": "category",
        "data": ["Budget"]
    },
    "yAxis": {
        "type": "value"
    },
    "series": [
        {
            "name": "Planned",
            "type": "bar",
            "data": [planned],
            "itemStyle": {"color": "#2196F3"}
        },
        {
            "name": "Actual",
            "type": "bar",
            "data": [actual],
            "itemStyle": {"color": "#4CAF50"}
        }
    ],
    "legend": {
        "data": ["Planned", "Actual"]
    }
}

st_echarts(options=bar_option, height="300px")

# Donut chart
donut_option = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Budget",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": "18",
                    "fontWeight": "bold"
                }
            },
            "labelLine": {"show": False},
            "data": [
                {"value": actual, "name": "Actual"},
                {"value": remaining, "name": "Remaining"},
            ]
        }
    ]
}

st_echarts(options=donut_option, height="300px")

with st.expander("📄 View Raw Category Data"):
    st.write(row)
