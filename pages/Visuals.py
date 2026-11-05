import json
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path


json_path = Path(__file__).parent.parent / "data.json"

with open(json_path, "r") as f:
    myData = json.load(f)


st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
    layout="wide"
)
st.title("Data Visualizations 📈")


sleepData = pd.DataFrame(myData["data_points"][0])
gramsData = pd.DataFrame(myData["data_points"][1])
incomeData = pd.DataFrame(myData["data_points"][2])
paintingData = pd.DataFrame(myData["data_points"][3])

st.title(myData["chart_title"])

st.subheader("Hours of Sleep by Day")
st.bar_chart(
    sleepData,
    x="Day of the Week",
    y="Hours of Sleep"
)

st.subheader("Protein by Meal")
st.line_chart(
    gramsData,
    x="Types of Meals",
    y="Grams of Protein"
)

st.subheader("Income by Person Type")
st.area_chart(
    incomeData,
    x="Person Type",
    y="Income"
)

st.title("Painting hours vs. starting income")

paintingChart = alt.Chart(paintingData).mark_line(point=True).encode(
    x="Number of Hours Painted",
    y="Starting Income after Graduation",
    tooltip=["Number of Hours Painted", "Starting Income after Graduation"],
)

st.altair_chart(paintingChart)

##csvstuff




file = "data.csv"
call_options = ["genuinely never", "like once or twice", "3 or 5 times", "after every class"]
metric_options = ["Number of students", "Average miles from campus"]

st.title("How does distance affect how often students phone home?")

df = pd.read_csv(file)
df["Miles_from_Campus"] = pd.to_numeric(df["Miles_from_Campus"], errors="coerce")
df["October_Temp"] = pd.to_numeric(df["October_Temp"], errors="coerce")
df = df.dropna(subset=["Miles_from_Campus", "October_Temp"])

if df.empty:
    st.warning("sorry no data here, go back to survey on first page")
    st.stop()


if "metric" not in st.session_state:
    st.session_state.metric = metric_options[0]
if "max_miles" not in st.session_state:
    st.session_state.max_miles = 5000

st.slider("Only include hometowns up to this many miles away:", 0, 5000, step=50, key="max_miles")
st.radio("What should the chart show?", metric_options, key="metric", horizontal=True)


filtered = df[df["Miles_from_Campus"] <= st.session_state.max_miles]

if filtered.empty:
    st.warning("No hometowns that close. Move the slider up.")
else:
    if st.session_state.metric == "Number of students":
        st.subheader("Number of students for each call frequency")
        y_label = "Number of students"
        data = filtered["Number_Calls"].value_counts().reindex(call_options, fill_value=0)
    else:
        st.subheader("Average distance from campus for each call frequency")
        y_label = "Average miles from campus"
        data = filtered.groupby("Number_Calls")["Miles_from_Campus"].mean().reindex(call_options, fill_value=0)

    chart_df = data.rename(y_label).to_frame()
    chart_df.index.name = "How often they call home"
    st.bar_chart(chart_df, x_label="How often they call home", y_label=y_label)

    mean = round(filtered["Miles_from_Campus"].mean(), 1)
    median = round(filtered["Miles_from_Campus"].median(), 1)

    if "last_mean" not in st.session_state:
        st.session_state.last_mean = mean
        st.session_state.last_median = median

    col1, col2 = st.columns(2)
    col1.metric("Mean miles from campus", mean, delta=round(mean - st.session_state.last_mean, 1))
    col2.metric("Median miles from campus", median, delta=round(median - st.session_state.last_median, 1))

    st.session_state.last_mean = mean
    st.session_state.last_median = median

#advancedchart 

st.subheader("Hometown vs. October Temperature")

chart = (
    alt.Chart(df)
    .mark_circle(size=300)
    .encode(
        x=alt.X("October_Temp", title="Average October temperature (°F)"),
        y=alt.Y("HomeTown", title="Hometown"),
        color=alt.Color("October_Temp", title="Temp (°F)"),
        tooltip=["HomeTown", "October_Temp"],
    )
    .properties(title="Hometown vs. October Temperature")
)

st.altair_chart(chart, use_container_width=True)