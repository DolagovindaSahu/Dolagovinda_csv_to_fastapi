import pandas as pd
import math
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.student import Student
from app.models.schemas import StudentFilter

CSV_PATH = "data/students_complete.csv"


def _safe(val):
    try:
        if math.isnan(float(val)):
            return None
    except (TypeError, ValueError):
        pass
    return val if val is not None else None


def seed_from_csv(db: Session) -> dict:
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        sid = str(row.get("student_id", "")).strip()
        if not sid:
            skipped += 1
            continue

        existing = db.query(Student).filter(Student.student_id == sid).first()
        if existing:
            skipped += 1
            continue

        student = Student(
            student_id=sid,
            first_name=_safe(row.get("first_name")),
            last_name=_safe(row.get("last_name")),
            age=int(row["age"]) if pd.notna(row.get("age")) else None,
            major=_safe(row.get("major")),
            gpa=float(row["gpa"]) if pd.notna(row.get("gpa")) else None,
            attendance=float(row["attendance"]) if pd.notna(row.get("attendance")) else None,
            scholarship=int(row["scholarship"]) if pd.notna(row.get("scholarship")) else None,
            city=_safe(row.get("city")),
            status=_safe(row.get("status")),
        )
        db.add(student)
        inserted += 1

    db.commit()
    return {"inserted": inserted, "skipped": skipped, "total_in_csv": len(df)}


def get_students_filtered(db: Session, filters: StudentFilter) -> list[Student]:
    query = db.query(Student)
    conditions = []

    if filters.age_gt is not None:
        conditions.append(Student.age > filters.age_gt)
    if filters.age_lt is not None:
        conditions.append(Student.age < filters.age_lt)
    if filters.major is not None:
        conditions.append(Student.major.ilike(f"%{filters.major}%"))
    if filters.status is not None:
        conditions.append(Student.status.ilike(f"%{filters.status}%"))
    if filters.city is not None:
        conditions.append(Student.city.ilike(f"%{filters.city}%"))
    if filters.gpa_gt is not None:
        conditions.append(Student.gpa > filters.gpa_gt)
    if filters.gpa_lt is not None:
        conditions.append(Student.gpa < filters.gpa_lt)
    if filters.min_scholarship is not None:
        conditions.append(Student.scholarship >= filters.min_scholarship)

    if conditions:
        query = query.filter(and_(*conditions))

    return query.all()


def get_student_by_id_db(db: Session, student_id: str) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()
