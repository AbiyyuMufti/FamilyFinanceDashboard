import time
import streamlit as st
from streamlit_theme import st_theme
import datetime
from google.oauth2 import service_account
import gspread


def get_worksheet() -> gspread.Spreadsheet:
    """Initialize and return the worksheet"""
    if "gspread_worksheet" not in st.session_state:
        gsheet_url = st.secrets["gsheet_url"]
        service_account_info = st.secrets["gcp_service_account"]
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=scope
        )

        client = gspread.authorize(credentials)
        st.session_state.gspread_worksheet = client.open_by_url(gsheet_url)

    return st.session_state.gspread_worksheet

def get_st_theme():
    if "base_theme" not in st.session_state:
        theme = st_theme()
        st.session_state.base_theme = theme.get("base", "light")   
    return st.session_state.base_theme

def global_data_selector():
    # Initialize if not exists
    today = datetime.date.today()
    month_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    year_list = [2025]
    worksheet = get_worksheet()
    
    if 'selected_month' not in st.session_state:
        st.session_state.selected_month = month_list[today.month - 1]
        worksheet = update_control_sheet()
    
    st.sidebar.subheader("📅 Filter Options")

    selected_option = st.sidebar.selectbox(
        "Month",
        month_list,
        index=month_list.index(st.session_state.selected_month),
        key='global_selected_month'
    )
    
    if st.session_state.global_selected_month != st.session_state.selected_month:
        st.session_state.selected_month = st.session_state.global_selected_month
        worksheet = update_control_sheet()
        time.sleep(1)
        st.cache_data.clear()
        st.rerun()

    return 2025, st.session_state.selected_month, worksheet

def get_initial_month():
    worksheet = get_worksheet()
    control_sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_overview"])
    return control_sheet.get_values('CurrentMonth')[0][0]

def update_control_sheet():
    worksheet = get_worksheet()
    control_sheet = worksheet.get_worksheet_by_id(st.secrets["sheets_id"]["monthly_overview"])
    control_sheet.update([[st.session_state.selected_month]], 'CurrentMonth')
    return worksheet
