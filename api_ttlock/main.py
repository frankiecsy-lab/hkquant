from fastapi import FastAPI
from api.v1.locks import router as v1_router
from api.v2.locks import router as v2_router
app = FastAPI(
    title="TTLock Test Service",
    description="用於測試 NPM 路徑分流的臨時服務",
    version="1.0.0",
    root_path="/ttlock"  # 配合 NPM 的 /lock/ 路徑
)

app.include_router(v1_router, prefix="/v1", tags=["v1"])
app.include_router(v2_router, prefix="/v2", tags=["v2"])
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Hello from hkquant_api_ttlock container!",
        "path": "/ttlock/"
    }

@app.get("/test")
def test_endpoint():
    return {
        "test": "OK",
        "proxy": "Nginx Proxy Manager is working correctly!"
    }