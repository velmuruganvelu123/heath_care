import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Set FastAPI Base URL
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# Function to fetch data from API
def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch {endpoint}")
        return None

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", [
    "Gender Count", "Blood Type Count", "Blood Condition Count", 
    "Gender Condition Count", "Admission Type Count", "Test Result Count"
])

# Main title
st.title("Healthcare Data Visualization")

def display_bar_and_pie_chart(df, category, title):
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df.set_index(category))
    with col2:
        fig = px.pie(df, names=category, values="Count", title=title)
        st.plotly_chart(fig)

# Gender Count
if option == "Gender Count":
    data = fetch_data("gender-count")
    if data and "gender_counts" in data:
        df = pd.DataFrame(list(data["gender_counts"].items()), columns=["Gender", "Count"])
        display_bar_and_pie_chart(df, "Gender", "Gender Distribution")

# Blood Type Count
elif option == "Blood Type Count":
    data = fetch_data("blood-type-count")
    if data and "blood_type_counts" in data:
        df = pd.DataFrame(list(data["blood_type_counts"].items()), columns=["Blood Type", "Count"])
        display_bar_and_pie_chart(df, "Blood Type", "Blood Type Distribution")

# Blood Condition Count
elif option == "Blood Condition Count":
    data = fetch_data("blood-condition-count")
    if data and "blood_condition_counts" in data:
        df = []
        for blood_type, conditions in data["blood_condition_counts"].items():
            for condition, count in conditions.items():
                df.append([blood_type, condition, count])
        df = pd.DataFrame(df, columns=["Blood Type", "Condition", "Count"])
        fig = px.bar(df, x="Blood Type", y="Count", color="Condition", title="Blood Condition Distribution")
        st.plotly_chart(fig)

# Gender Condition Count
elif option == "Gender Condition Count":
    data = fetch_data("gender-condition-count")
    if data and "gender_condition_counts" in data:
        df = []
        for gender, conditions in data["gender_condition_counts"].items():
            for condition, count in conditions.items():
                df.append([gender, condition, count])
        df = pd.DataFrame(df, columns=["Gender", "Condition", "Count"])
        fig = px.bar(df, x="Gender", y="Count", color="Condition", title="Medical Conditions by Gender")
        st.plotly_chart(fig)

# Admission Type Count
elif option == "Admission Type Count":
    data = fetch_data("admission-type-count")
    if data and "admission_type_counts" in data:
        df = pd.DataFrame(list(data["admission_type_counts"].items()), columns=["Admission Type", "Count"])
        display_bar_and_pie_chart(df, "Admission Type", "Admission Type Distribution")

# Test Result Count
elif option == "Test Result Count":
    data = fetch_data("test-result-count")
    if data and "test_result_counts" in data:
        df = pd.DataFrame(list(data["test_result_counts"].items()), columns=["Test Result", "Count"])
        display_bar_and_pie_chart(df, "Test Result", "Test Results Distribution")
