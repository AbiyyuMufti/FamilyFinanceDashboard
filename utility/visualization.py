
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
