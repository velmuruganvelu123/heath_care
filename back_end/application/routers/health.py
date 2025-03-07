import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import APIRouter
from back_end.application.database import fetch_data
from application.models import GenderCountResponse, BloodTypeCountResponse, AdmissionTypeCountResponse, TestResultCountResponse

router = APIRouter()

@router.get("/gender-count", response_model=GenderCountResponse)
def get_gender_count():
    """Return the total count of Male, Female, and Others"""
    df = fetch_data()
    if df is None or "Gender" not in df.columns:
        return {"message": "No data found or missing 'Gender' column"}

    gender_counts = df["Gender"].dropna().str.strip().value_counts().to_dict()
    return {"gender_counts": gender_counts}

@router.get("/blood-type-count", response_model=BloodTypeCountResponse)
def get_blood_type_count():
    """Return the total count of each blood type"""
    df = fetch_data()
    if df is None or "Blood Type" not in df.columns:
        return {"message": "No data found or missing 'Blood Type' column"}

    blood_type_counts = df["Blood Type"].value_counts().to_dict()
    return {"blood_type_counts": blood_type_counts}

@router.get("/blood-condition-count")
def get_blood_condition_count():
    """Return the count of medical conditions for each blood type"""
    df = fetch_data()
    if df is None or not all(col in df.columns for col in ["Blood Type", "Medical Condition"]):
        return {"message": "No data found or missing columns"}
    
    blood_condition_counts = df.groupby(["Blood Type", "Medical Condition"]).size().reset_index(name="count")
    blood_condition_dict = {}
    for _, row in blood_condition_counts.iterrows():
        blood_group, condition, count = row["Blood Type"], row["Medical Condition"], row["count"]
        if blood_group not in blood_condition_dict:
            blood_condition_dict[blood_group] = {}
        blood_condition_dict[blood_group][condition] = count
    
    return {"blood_condition_counts": blood_condition_dict}

@router.get("/gender-condition-count")
def get_gender_condition_count():
    """Return the count of each medical condition per gender"""
    df = fetch_data()
    if df is None or not all(col in df.columns for col in ["Gender", "Medical Condition"]):
        return {"message": "No data found or missing columns"}
    
    gender_condition_counts = df.groupby(["Gender", "Medical Condition"]).size().reset_index(name="count")
    gender_condition_dict = {}
    for _, row in gender_condition_counts.iterrows():
        gender, condition, count = row["Gender"], row["Medical Condition"], row["count"]
        if gender not in gender_condition_dict:
            gender_condition_dict[gender] = {}
        gender_condition_dict[gender][condition] = count
    
    return {"gender_condition_counts": gender_condition_dict}

@router.get("/admission-type-count", response_model=AdmissionTypeCountResponse)
def get_admission_type_count():
    """Return the total number of each admission type"""
    df = fetch_data()
    if df is None or "Admission Type" not in df.columns:
        return {"message": "No data found or missing 'Admission Type' column"}

    admission_counts = df["Admission Type"].value_counts().to_dict()
    return {"admission_type_counts": admission_counts}

@router.get("/test-result-count", response_model=TestResultCountResponse)
def get_test_result_count():
    """Return the count of each disease found in test results"""
    df = fetch_data()
    if df is None or "Test Results" not in df.columns:
        return {"message": "No data found or missing 'Test Results' column"}

    test_result_counts = df["Test Results"].value_counts().to_dict()
    return {"test_result_counts": test_result_counts}
