import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from back_end.application.database import fetch_data
from application.models import GenderCountResponse, BloodTypeCountResponse, AdmissionTypeCountResponse, TestResultCountResponse

router = APIRouter()

"""
API Routes for Healthcare Data Insights

This module provides FastAPI endpoints for querying and analyzing healthcare dataset insights.

Functions:
- get_dataframe(): Fetches the healthcare dataset from the database.
- get_gender_count(): Returns the count of patients by gender.
- get_blood_type_count(): Returns the count of patients by blood type.
- get_blood_condition_count(): Returns the count of medical conditions grouped by blood type.
- get_gender_condition_count(): Returns the count of medical conditions grouped by gender.
- get_admission_type_count(): Returns the count of patients by admission type.
- get_test_result_count(): Returns the count of test results.

Dependencies:
- fetch_data(): Fetches the dataset from the SQLite database.
- FastAPI response models: Defines structured API responses.
"""


def get_dataframe():
    df = fetch_data()
    if df is None or df.empty:
        return None
    return df
# print(df)

@router.get("/gender-count", response_model=GenderCountResponse)
def get_gender_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or "Gender" not in df.columns:
        return JSONResponse(content={"message": "No data found or missing 'Gender' column"}, status_code=404)

    gender_counts = df["Gender"].dropna().str.strip().value_counts().to_dict()
    return {"gender_counts": gender_counts}

@router.get("/blood-type-count", response_model=BloodTypeCountResponse)
def get_blood_type_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or "Blood_Type" not in df.columns:
        return JSONResponse(content={"message": "No data found or missing 'Blood_Type' column"}, status_code=404)

    blood_type_counts = df["Blood_Type"].value_counts().to_dict()
    return {"blood_type_counts": blood_type_counts}

@router.get("/blood-condition-count")
def get_blood_condition_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or not all(col in df.columns for col in ["Blood_Type", "Medical_Condition"]):
        return JSONResponse(content={"message": "No data found or missing columns"}, status_code=404)
    
    blood_condition_counts = df.groupby(["Blood_Type", "Medical_Condition"]).size().reset_index(name="count")
    blood_condition_dict = {bg: {} for bg in df["Blood_Type"].unique()}
    
    for _, row in blood_condition_counts.iterrows():
        blood_condition_dict[row["Blood_Type"]][row["Medical_Condition"]] = row["count"]
    
    return {"blood_condition_counts": blood_condition_dict}

@router.get("/gender-condition-count")
def get_gender_condition_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or not all(col in df.columns for col in ["Gender", "Medical_Condition"]):
        return JSONResponse(content={"message": "No data found or missing columns"}, status_code=404)
    
    gender_condition_counts = df.groupby(["Gender", "Medical_Condition"]).size().reset_index(name="count")
    gender_condition_dict = {g: {} for g in df["Gender"].unique()}
    
    for _, row in gender_condition_counts.iterrows():
        gender_condition_dict[row["Gender"]][row["Medical_Condition"]] = row["count"]
    
    return {"gender_condition_counts": gender_condition_dict}

@router.get("/admission-type-count", response_model=AdmissionTypeCountResponse)
def get_admission_type_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or "Admission_Type" not in df.columns:
        return JSONResponse(content={"message": "No data found or missing 'Admission_Type' column"}, status_code=404)

    admission_counts = df["Admission_Type"].value_counts().to_dict()
    return {"admission_type_counts": admission_counts}

@router.get("/test-result-count", response_model=TestResultCountResponse)
def get_test_result_count(df: pd.DataFrame = Depends(get_dataframe)):
    if df is None or "Test Results" not in df.columns:
        return JSONResponse(content={"message": "No data found"}, status_code=404)  

    test_result_counts = df["Test Results"].value_counts().to_dict()
    return {"test_result_counts": test_result_counts}
