from fastapi import FastAPI
from app.routes.csv_routes import router as csv_router
from app.routes.db_routes import router as db_router
from app.db.database import Base, engine

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CSV to FastAPI",
    description=(
        "FastAPI service that loads student data from a CSV, "
        "stores it in MySQL, and exposes filtered query endpoints."
    )
)

app.include_router(csv_router)
app.include_router(db_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "CSV to FastAPI API"
    }
