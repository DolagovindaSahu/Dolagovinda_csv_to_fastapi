from pydantic import BaseModel
from typing import Optional


class StudentSchema(BaseModel):
    student_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    attendance: Optional[float] = None
    scholarship: Optional[int] = None
    city: Optional[str] = None
    status: Optional[str] = None

    model_config = {"from_attributes": True}


class StudentFilter(BaseModel):
    age_gt: Optional[int] = None
    age_lt: Optional[int] = None
    major: Optional[str] = None
    status: Optional[str] = None
    city: Optional[str] = None
    gpa_gt: Optional[float] = None
    gpa_lt: Optional[float] = None
    min_scholarship: Optional[int] = None
