# utils.py
import streamlit as st
import datetime

def global_data_selector():
    # Initialize if not exists
    today = datetime.date.today()
    month_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    year_list = [2025]

    if 'selected_month' not in st.session_state:
        st.session_state.selected_month = month_list[today.month - 1]
    
    st.sidebar.subheader("📅 Filter Options")

    selected_option = st.sidebar.selectbox(
        "Month",
        month_list,
        index=month_list.index(st.session_state.selected_month),
        key='global_selected_month'
    )
    
    if st.session_state.global_selected_month != st.session_state.selected_month:
        st.session_state.selected_month = st.session_state.global_selected_month
        st.rerun()
    
    return 2025, st.session_state.selected_month