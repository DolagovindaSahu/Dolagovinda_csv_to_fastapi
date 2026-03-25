from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to CSV TO FASTAPI APPLICATION."}

if __name__ == "__main__":
    uvicorn.run(app)