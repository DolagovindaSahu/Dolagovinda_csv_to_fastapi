from fastapi import FastAPI
import uvicorn
import pandas as pd

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to CSV TO FASTAPI APPLICATION."}

@app.get("/get-csv-data")
def get_csv_data():

    try:
        df = pd.read_csv("students_complete.csv")

        return {
            "columns": list(df.columns),
            "total_rows": len(df),
            "data": df.fillna("").to_dict(orient="records")
        }

    except FileNotFoundError:
        return {
            "error": "students_complete.csv not found.(it should be in the working directory)"
        }

    except Exception as e:
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app)