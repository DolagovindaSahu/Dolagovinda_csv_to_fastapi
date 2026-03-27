import pandas as pd
import math
from typing import Optional
from functools import lru_cache

CSV_PATH = "data/students_complete.csv"


@lru_cache(maxsize=1)
def load_csv() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    # Normalise types
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")
    if "gpa" in df.columns:
        df["gpa"] = pd.to_numeric(df["gpa"], errors="coerce")
    if "attendance" in df.columns:
        df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")
    if "scholarship" in df.columns:
        df["scholarship"] = pd.to_numeric(df["scholarship"], errors="coerce").astype("Int64")
    return df


def _clean(val):
    if val is None:
        return None
    try:
        if math.isnan(float(val)):
            return None
    except (TypeError, ValueError):
        pass
    return val


def df_to_records(df: pd.DataFrame) -> list[dict]:
    records = []
    for row in df.to_dict(orient="records"):
        records.append({k: _clean(v) for k, v in row.items()})
    return records


def get_all_csv() -> list[dict]:
    return df_to_records(load_csv())


def get_by_id_csv(student_id: str) -> Optional[dict]:
    df = load_csv()
    match = df[df["student_id"] == student_id]
    if match.empty:
        return None
    return df_to_records(match)[0]
