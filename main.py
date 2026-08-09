from fastapi import FastAPI

app = FastAPI(title="HKQuant API Gateway")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI with Docker is working!"}