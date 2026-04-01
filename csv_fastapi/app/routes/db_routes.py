from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db, check_db_connection
from app.models.schemas import StudentSchema, StudentFilter
from app.services.db_service import (
    seed_from_csv,
    get_students_filtered,
    get_student_by_id_db,
)

router = APIRouter(tags=["Database"])


# ── Health / connectivity ────────────────────────────────────────────────────

@router.get("/check_db", summary="Verify DB connection")
def check_db():
    result = check_db_connection()
    if result["status"] != "connected":
        raise HTTPException(status_code=503, detail=result)
    return result

# ── Seed ─────────────────────────────────────────────────────────────────────

@router.post("/db/seed", summary="Insert CSV data into DB")
def seed_db(db: Session = Depends(get_db)):
    return seed_from_csv(db)

# ── Query from DB ─────────────────────────────────────────────────────────────

@router.get(
    "/db/students",
    response_model=list[StudentSchema],
    summary="Get students from DB with optional filters",
)
def get_students(
    age_gt: Optional[int] = Query(None, description="Age greater than"),
    age_lt: Optional[int] = Query(None, description="Age less than"),
    major: Optional[str] = Query(None, description="Major contains (case-insensitive)"),
    status: Optional[str] = Query(None, description="Payment status (Paid / Pending)"),
    city: Optional[str] = Query(None, description="City contains (case-insensitive)"),
    gpa_gt: Optional[float] = Query(None, description="GPA greater than"),
    gpa_lt: Optional[float] = Query(None, description="GPA less than"),
    min_scholarship: Optional[int] = Query(None, description="Minimum scholarship amount"),
    db: Session = Depends(get_db),
):
    filters = StudentFilter(
        age_gt=age_gt,
        age_lt=age_lt,
        major=major,
        status=status,
        city=city,
        gpa_gt=gpa_gt,
        gpa_lt=gpa_lt,
        min_scholarship=min_scholarship,
    )
    students = get_students_filtered(db, filters)
    return students

@router.get(
    "/db/students/{student_id}",
    response_model=StudentSchema,
    summary="Get a single student from DB by student_id",
)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student_id = student_id.strip().upper()
    student = get_student_by_id_db(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found in DB")
    return student
