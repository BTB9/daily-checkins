import streamlit as st
import datetime
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

# Set up Google Sheets access using Streamlit secrets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(dict(service_account_info), scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Daily Check-In Log").worksheet("Morning")

# Get current date
today = datetime.datetime.today()
day_name = today.strftime("%A")
date_string = today.strftime("%B %d, %Y")

# Streamlit app setup
st.set_page_config(page_title="Morning Check-In", layout="centered")
st.title("🔴 Morning Check-In Required")
st.subheader("Day begins when discipline starts.")
st.markdown(f"**📅 Today is {day_name}, {date_string}**")

# Input form
with st.form("checkin_form"):
    weight = st.number_input("Weight (lbs):", min_value=0.0, step=0.1)
    whoop = st.number_input("WHOOP Recovery (%):", min_value=0, max_value=100)
    sleep_hours = st.number_input("Sleep Duration (hours):", min_value=0.0, step=0.1)
    grip_left = st.number_input("Grip Strength - Left Hand (lbs):", min_value=0.0, step=0.1)
    grip_two_finger = st.number_input("Grip Strength - Two-Finger (lbs):", min_value=0.0, step=0.1)
    brushed_teeth = st.checkbox("Brushed Teeth")
    mood = st.radio("😌 How do you feel today?", ["😄", "🙂", "😐", "😕", "😫"])
    submitted = st.form_submit_button("Submit Check-In")

# Save to Google Sheets
    if submitted:
        if all([weight > 0, whoop >= 0, sleep_hours > 0, grip_left > 0, grip_two_finger > 0, brushed_teeth]):
            row = [
                str(datetime.datetime.now()),
                day_name,
                date_string,
                weight,
                whoop,
                sleep_hours,
                grip_left,
                grip_two_finger,
                brushed_teeth,
                mood
            ]
            sheet.append_row(row)
            st.success("✅ Check-in saved to Google Sheets.")
        else:
            st.error("⚠️ Please complete all required fields before submitting.")
