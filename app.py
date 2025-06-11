import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Read the secrets
gsheet_url = st.secrets["gsheet_url"]
service_account_info = st.secrets["gcp_service_account"]

# 2. Setup credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# 3. Open the Google Sheet
sheet = client.open_by_url(gsheet_url).get_worksheet_by_id(1486134437)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 4. Streamlit UI
st.title("Secure Google Sheets Dashboard")
st.dataframe(df)
st.write("Summary Stats:")
st.write(df.describe())
