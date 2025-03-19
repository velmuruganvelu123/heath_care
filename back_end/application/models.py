from pydantic import BaseModel
from typing import Dict

class GenderCountResponse(BaseModel):
    gender_counts: Dict[str, int]

class BloodTypeCountResponse(BaseModel):
    blood_type_counts: Dict[str, int]

class AdmissionTypeCountResponse(BaseModel):
    admission_type_counts: Dict[str, int]

class TestResultCountResponse(BaseModel):
    test_result_counts: Dict[str, int]

class Chat(BaseModel):
    prompt: str

