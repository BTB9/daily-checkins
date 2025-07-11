import streamlit as st
from google.oauth2 import service_account
import gspread
import datetime
import pandas as pd

st.title("🌙 Nightly Check-In")

# Get today's date
today = datetime.date.today()
day_of_week = today.strftime("%A")
st.write(f"📅 {today} ({day_of_week})")

# Load Google Sheets credentials
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
client = gspread.authorize(creds)

# Open the correct spreadsheet and worksheet
spreadsheet = client.open("Daily Check-In Log")
worksheet = spreadsheet.worksheet("Night")

# Input questions
calories = st.number_input("🍽️ How many calories did you eat today?", step=1)
protein = st.number_input("🥩 How many grams of protein?", step=1)
creatine = st.checkbox("💊 Did you take your creatine?")
lift = st.checkbox("🏋️ Did you do your lift today?")
throw = st.checkbox(" Did you do your throwing session today?")
notes = st.text_area("📝 Any notes from today?")

if st.button("✅ Submit"):
    data = [
        str(today),
        day_of_week,
        calories,
        protein,
        "Yes" if creatine else "No",
        "Yes" if lift else "No",
        "Yes" if throw else "No",
        notes
    ]
    
    # Insert into the sheet
    worksheet.append_row(data)
    st.success("Submitted successfully!")
