from fastapi import APIRouter, HTTPException
from app.services.csv_service import get_all_csv, get_by_id_csv

router = APIRouter(prefix="/data", tags=["CSV Data"])


@router.get("/", summary="Return all records from CSV")
def get_all():
    return get_all_csv()


@router.get("/{student_id}", summary="Return a single record by student_id from CSV")
def get_by_id(student_id: str):
    record = get_by_id_csv(student_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found in CSV")
    return record
