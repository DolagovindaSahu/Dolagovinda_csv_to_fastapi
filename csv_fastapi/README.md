# CSV to FastAPI

A FastAPI service that loads student data from a CSV file, persists it to a MySQL database (`csvtofastapi`), and exposes clean, filtered REST endpoints.

---

## Project Structure

```
csv_to_fastapi/
├── app/
│   ├── core/
│   │   └── config.py          # App settings (reads .env)
│   ├── db/
│   │   └── database.py        # SQLAlchemy engine, session, check_db
│   ├── models/
│   │   ├── student.py         # ORM model (students table)
│   │   └── schemas.py         # Pydantic schemas + filter model
│   ├── routes/
│   │   ├── csv_routes.py      # /data endpoints (CSV, in-memory cache)
│   │   └── db_routes.py       # /check_db, /db/* endpoints (MySQL)
│   └── services/
│       ├── csv_service.py     # CSV loading with lru_cache
│       └── db_service.py      # Seed + filtered DB queries
├── data/
│   └── students_complete.csv
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/<your-username>/csv_to_fastapi.git
cd csv_to_fastapi
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

`.env` fields:

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_USER` | `root` | DB username |
| `DB_PASSWORD` | — | DB password |
| `DB_NAME` | `csvtofastapi` | Database name |

### 3. Create the database in MySQL

```sql
CREATE DATABASE csvtofastapi;
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Root

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |

### CSV Endpoints (in-memory, no DB)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/data/` | All records from CSV |
| GET | `/data/{student_id}` | Single record by ID from CSV |

### Database Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/check_db` | Verify MySQL connection |
| POST | `/db/seed` | Insert CSV data into DB (idempotent) |
| GET | `/db/students` | Query students with filters |
| GET | `/db/students/{student_id}` | Fetch one student from DB |

---

## Filtered Queries — `/db/students`

All query params are optional and combinable:

| Param | Type | Example | Description |
|---|---|---|---|
| `age_gt` | int | `?age_gt=20` | Age **greater than** value |
| `age_lt` | int | `?age_lt=25` | Age **less than** value |
| `major` | str | `?major=physics` | Major contains (case-insensitive) |
| `status` | str | `?status=Paid` | Payment status |
| `city` | str | `?city=austin` | City contains (case-insensitive) |
| `gpa_gt` | float | `?gpa_gt=3.5` | GPA greater than |
| `gpa_lt` | float | `?gpa_lt=2.0` | GPA less than |
| `min_scholarship` | int | `?min_scholarship=1000` | Scholarship ≥ value |

### Example Requests

```bash
# All students older than 20
GET /db/students?age_gt=20

# Physics students with GPA > 3.0
GET /db/students?major=physics&gpa_gt=3.0

# Paid students in Austin aged 18–22
GET /db/students?status=Paid&city=austin&age_gt=18&age_lt=22

# Students with scholarship ≥ 1500
GET /db/students?min_scholarship=1500
```

---

## Workflow (first time)

```bash
# 1. Check DB is reachable
curl http://localhost:8000/check_db

# 2. Seed the DB from CSV (run once)
curl -X POST http://localhost:8000/db/seed

# 3. Query with filters
curl "http://localhost:8000/db/students?age_gt=20&status=Paid"
```
