
import json
import streamlit as st
from pathlib import Path
import csv
import os 

st.set_page_config(
    page_title="Survey",
    page_icon="📝"
)

# PAGE TITLE
st.title("Nutrition Tracker 📝")
st.write("Please fill out the protein content of your last meal below")


json_path = Path(__file__).parent.parent / "data.json"


if "data" not in st.session_state:
    with open(json_path, "r") as f:
        st.session_state.data = json.load(f)


meals = st.session_state.data["data_points"][1]


with st.form("survey_form"):
    name = st.text_input("Meal name", key="meal_name")

    protein = st.slider(
        "Grams of protein",
        min_value=0,
        max_value=60,
        value=20,
        key="protein"
    )

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if name.strip():
            # Update both lists
            meals["Types of Meals"].append(name.strip())
            meals["Grams of Protein"].append(int(protein))

      
            with open(json_path, "w") as f:
                json.dump(st.session_state.data, f, indent=4)

            st.success("Your data has been saved to data.json!")
            st.write(f"Meal: {name.strip()}")
            st.write(f"Protein: {protein} g")
        else:
            st.error("Please enter a meal name before submitting.")


## user data for csv file 

st.title("We want to know about your backstory! Please fill in the info :)")
st.write("Tell us about home...")

file = "data.csv"
headers = ["HomeTown", "Miles_from_Campus", "Number_Calls", "October_Temp"]

hometown = st.text_input("What is the name of your hometown?")
miles = st.number_input("Roughly how many miles away is your hometown from campus?", min_value=0.0)
calls = st.select_slider("How often do you call home?", options=["genuinely never", "like once or twice", "3 or 5 times", "after every class"])
temp = st.number_input("What does the average temperature feel like in October at home? (°F)", min_value=-50, max_value=130, value=60, step=1)

submit = st.button("Submit Survey")

if submit:
    if not hometown.strip():
        st.error("enter your hometown pls")
    else:
        new_row = [hometown.strip().title(), str(miles), calls, int(temp)]
        file_exists = os.path.exists(file)

        if file_exists:
            with open(file) as f:
                text = f.read()
            if text and not text.endswith("\n"):
                with open(file, "a") as f:
                    f.write("\n")

        with open(file, mode="a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(new_row)

        st.success("Success! Added your entry.")
