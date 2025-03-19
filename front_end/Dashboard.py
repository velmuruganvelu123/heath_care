import streamlit as st
import requests
import plotly.express as px

# Backend API URL
BASE_URL = "http://127.0.0.1:8000"

# Function to fetch data from FastAPI
def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('message', 'Failed to fetch data')}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(page_title="Healthcare Insights", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation 📌")
option = st.sidebar.radio(
    "Select a category:",
    [
        "Gender Distribution",
        "Blood Type Distribution",
        "Blood Type vs Medical Condition",
        "Gender vs Medical Condition",
        "Admission Type Count",
        "Test Result Distribution",
    ],
)

# Full-page display for selected visualization
st.title("Healthcare Data Insights 📊")

# Gender Count Visualization
if option == "Gender Distribution":
    st.subheader("Gender Distribution")
    gender_data = fetch_data("gender-count")

    if gender_data:
        gender_counts = gender_data["gender_counts"]
        gender_df = [{"Gender": k, "Count": v} for k, v in gender_counts.items()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.table(gender_df)
        with col2:
            fig = px.pie(values=list(gender_counts.values()), names=list(gender_counts.keys()), title="Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)

# Blood Type Count Visualization
elif option == "Blood Type Distribution":
    st.subheader("Blood Type Distribution")
    blood_data = fetch_data("blood-type-count")

    if blood_data:
        blood_counts = blood_data["blood_type_counts"]
        blood_df = [{"Blood Type": k, "Count": v} for k, v in blood_counts.items()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.table(blood_df)
        with col2:
            fig = px.bar(x=list(blood_counts.keys()), y=list(blood_counts.values()), title="Blood Type Count", labels={"x": "Blood Type", "y": "Count"})
            st.plotly_chart(fig, use_container_width=True)

# Blood Condition Count
elif option == "Blood Type vs Medical Condition":
    st.subheader("Blood Type vs Medical Condition")
    blood_condition_data = fetch_data("blood-condition-count")

    if blood_condition_data:
        blood_condition_counts = blood_condition_data["blood_condition_counts"]
        blood_condition_list = []

        for blood_type, conditions in blood_condition_counts.items():
            for condition, count in conditions.items():
                blood_condition_list.append({"Blood Type": blood_type, "Condition": condition, "Count": count})

        if blood_condition_list:
            fig = px.sunburst(
                data_frame=blood_condition_list,
                path=["Blood Type", "Condition"],
                values="Count",
                title="Blood Type vs Medical Condition",
            )
            st.plotly_chart(fig, use_container_width=True)

# Gender Condition Count
elif option == "Gender vs Medical Condition":
    st.subheader("Gender vs Medical Condition")
    gender_condition_data = fetch_data("gender-condition-count")

    if gender_condition_data:
        gender_condition_counts = gender_condition_data["gender_condition_counts"]
        gender_condition_list = []

        for gender, conditions in gender_condition_counts.items():
            for condition, count in conditions.items():
                gender_condition_list.append({"Gender": gender, "Condition": condition, "Count": count})

        if gender_condition_list:
            fig = px.bar(
                x=[item["Gender"] for item in gender_condition_list],
                y=[item["Count"] for item in gender_condition_list],
                color=[item["Condition"] for item in gender_condition_list],
                title="Gender vs Medical Condition",
                labels={"x": "Gender", "y": "Count"},
            )
            st.plotly_chart(fig, use_container_width=True)

# Admission Type Count
elif option == "Admission Type Count":
    st.subheader("Admission Type Count")
    admission_data = fetch_data("admission-type-count")

    if admission_data:
        admission_counts = admission_data["admission_type_counts"]
        admission_df = [{"Admission Type": k, "Count": v} for k, v in admission_counts.items()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.table(admission_df)
        with col2:
            fig = px.pie(values=list(admission_counts.values()), names=list(admission_counts.keys()), title="Admission Type Distribution")
            st.plotly_chart(fig, use_container_width=True)

# Test Result Count
elif option == "Test Result Distribution":
    st.subheader("Test Result Distribution")
    test_result_data = fetch_data("test-result-count")

    if test_result_data:
        test_counts = test_result_data["test_result_counts"]
        test_df = [{"Test Result": k, "Count": v} for k, v in test_counts.items()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.table(test_df)
        with col2:
            fig = px.bar(x=list(test_counts.keys()), y=list(test_counts.values()), title="Test Result Count", labels={"x": "Test Result", "y": "Count"})
            st.plotly_chart(fig, use_container_width=True)
