import streamlit as st
import datetime
import pandas as pd
import json
from pathlib import Path
from datetime import datetime


# File paths
DATA_FILE = Path("data/morning_checkin_log.csv")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

PLAN_FILE = Path("weekly_plan.json")

# Get today
today = datetime.today()
day_name = today.strftime("%A")
date_string = today.strftime("%B %d, %Y")

st.set_page_config(page_title="Morning Check-In", layout="centered")

st.title("🔴 Morning Check-In Required")
st.subheader("Day begins when discipline starts.")
st.markdown(f"**📅 Today is {day_name}, {date_string}**")

# Display today's plan if it exists
if PLAN_FILE.exists():
    with open(PLAN_FILE, "r") as f:
        weekly_plan = json.load(f)
    today_plan = weekly_plan.get(day_name, {})
    if today_plan:
        st.markdown("### 📋 Today's Plan")
        st.write(f"**Lift:** {today_plan.get('lift', '—')}")
        st.write(f"**Throwing:** {today_plan.get('throw', '—')}")
    else:
        st.info("No plan found for today.")
else:
    st.warning("Weekly plan not yet created. Submit your Sunday check-in.")

# 🔄 Morning check-in form
with st.form("checkin_form"):
    weight = st.number_input("Weight (lbs):", min_value=0.0, step=0.1)
    whoop = st.number_input("WHOOP Recovery (%):", min_value=0, max_value=100)
    sleep_hours = st.number_input("Sleep Duration (hours):", min_value=0.0, step=0.1)
    grip_left = st.number_input("Grip Strength - Left Hand (lbs):", min_value=0.0, step=0.1)
    grip_two_finger = st.number_input("Grip Strength - Two-Finger (lbs):", min_value=0.0, step=0.1)
    brushed_teeth = st.checkbox("Brushed Teeth")
    mood = st.radio("😌 How do you feel today?", ["😄", "🙂", "😐", "😕", "😫"])

    submitted = st.form_submit_button("Submit Check-In")

    if submitted:
        if all([weight > 0, whoop >= 0, sleep_hours > 0, grip_left > 0, grip_two_finger > 0, brushed_teeth]):
            new_data = {
                "Timestamp":datetime.now(),
                "Day": day_name,
                "Date": date_string,
                "Weight": weight,
                "WHOOP_Recovery": whoop,
                "Sleep_Hours": sleep_hours,
                "Grip_Left_Hand": grip_left,
                "Grip_Two_Finger": grip_two_finger,
                "Brushed_Teeth": brushed_teeth,
                "Mood": mood,
            }

            df = pd.DataFrame([new_data])
            if DATA_FILE.exists():
                df.to_csv(DATA_FILE, mode='a', header=False, index=False)
            else:
                df.to_csv(DATA_FILE, index=False)

            st.success("✅ Check-in complete. You're ready to go.")
        else:
            st.error("Please complete all required fields before submitting.")
