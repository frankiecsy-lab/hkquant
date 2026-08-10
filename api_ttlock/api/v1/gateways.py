import os
import time
import requests
from fastapi import APIRouter, Query
from api.v1.auth import get_access_token  # 引入共用的 Token 函式

router = APIRouter()

TTLOCK_DOMAIN = "cnapi.ttlock.com"
TTLOCK_BASE_URL = f"https://{TTLOCK_DOMAIN}/v3"

@router.get("/list")
def get_gateway_list(
    pageNo: int = Query(1, description="頁碼，預設為第 1 頁"),
    pageSize: int = Query(200, description="每頁筆數，預設為 200 筆")
):
    """查詢帳號底下的藍牙網關列表"""
    access_token = get_access_token()  # 直接調用共用函式
    client_id = os.getenv("TTLOCK_CLIENT_ID")

    url = f"{TTLOCK_BASE_URL}/gateway/list"
    params = {
        "clientId": client_id,
        "accessToken": access_token,
        "pageNo": pageNo,
        "pageSize": pageSize,
        "date": int(time.time() * 1000)
    }

    response = requests.get(url, params=params)
    return response.json()