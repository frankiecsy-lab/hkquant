from fastapi import FastAPI
from api.v1.quoter import router as v1_quoter_router

app = FastAPI(
    title="Futu OpenD Service",
    description="用於測試 NPM 路徑分流的臨時服務",
    version="1.0.0",
    root_path="/futu"  # 配合 NPM 的 /lock/ 路徑
)
app.include_router(v1_quoter_router, prefix="/v1", tags=["v1 - Quoter"])
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Hello from futu opend container!",
        "path": "/futu/"
    }
