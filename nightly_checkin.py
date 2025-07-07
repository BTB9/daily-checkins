import streamlit as st
import datetime
import pandas as pd
import json
from pathlib import Path

# File paths
from datetime import datetime


DATA_FILE = Path("data/nightly_checkin_log.csv")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


PLAN_FILE = Path("weekly_plan.json")

st.set_page_config(page_title="Nightly Check-In", layout="centered")

today =datetime.today()
day_name = today.strftime("%A")
date_string = today.strftime("%B %d, %Y")

st.title("🌙 Nightly Check-In")
st.subheader("End the day with clarity and honesty.")
st.markdown(f"**📅 Today is {day_name}, {date_string}**")

weekly_plan = {}

# 🗓️ Weekly plan entry if it's Sunday
if today.weekday() == 6:  # Sunday
    st.markdown("## 🗓️ Plan Your Week")
    st.info("It's Sunday! Let's set your plan for the week.")
    for i in range(7):
        day = (today + datetime.timedelta(days=(i - 6))).strftime("%A")
        with st.expander(f"{day} Plan"):
            lift = st.text_input(f"{day} - Lift Plan", key=f"lift_{day}")
            throw = st.text_input(f"{day} - Throwing Plan", key=f"throw_{day}")
            weekly_plan[day] = {"lift": lift, "throw": throw}

# 🌙 Nightly check-in form
with st.form("nightly_checkin_form"):
    calories = st.number_input("Total Calories Consumed:", min_value=0, step=10)
    protein = st.number_input("Total Protein (g):", min_value=0, step=1)
    hydration = st.select_slider("Hydration Level (estimate):", options=["Low", "Okay", "Good", "Excellent"])
    mindset = st.radio("🧠 How was your mindset today?", ["😄", "🙂", "😐", "😕", "😫"])
    followed_routine = st.checkbox("Followed routine today?")
    brushed_teeth = st.checkbox("Brushed teeth before bed?")
    reflection = st.text_area("✍️ What went well today? (optional)")

    submitted = st.form_submit_button("Submit Nightly Check-In")

    if submitted:
        if calories > 0 and protein > 0:
            new_data = {
                "Timestamp":datetime.now(),
                "Day": day_name,
                "Date": date_string,
                "Calories": calories,
                "Protein": protein,
                "Hydration": hydration,
                "Mindset": mindset,
                "Followed_Routine": followed_routine,
                "Brushed_Teeth": brushed_teeth,
                "Reflection": reflection,
            }

            df = pd.DataFrame([new_data])
            if DATA_FILE.exists():
                df.to_csv(DATA_FILE, mode='a', header=False, index=False)
            else:
                df.to_csv(DATA_FILE, index=False)

            if today.weekday() == 6:  # Save weekly plan on Sunday
                with open(PLAN_FILE, "w") as f:
                    json.dump(weekly_plan, f, indent=2)

            st.success("✅ Nightly check-in saved. Sleep well.")
        else:
            st.error("Please fill in both calories and protein before submitting.")
