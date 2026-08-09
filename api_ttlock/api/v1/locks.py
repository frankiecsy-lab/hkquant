import os
import time
import hashlib
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# 官方文件規範的中國區基礎網域與 Token 網址
TTLOCK_DOMAIN = "cnapi.ttlock.com"
TTLOCK_BASE_URL = f"https://{TTLOCK_DOMAIN}/v3"
TOKEN_URL = f"https://{TTLOCK_DOMAIN}/oauth2/token"

def get_md5_password(password: str) -> str:
    """將密碼轉為 TTLock 要求的 32 位小寫 MD5"""
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def get_access_token() -> str:
    """取得 TTLock Access Token (依官方 OAuth2 規範)"""
    client_id = os.getenv("TTLOCK_CLIENT_ID")
    client_secret = os.getenv("TTLOCK_CLIENT_SECRET")
    username = os.getenv("TTLOCK_USERNAME")
    password = os.getenv("TTLOCK_PASSWORD")

    if not all([client_id, client_secret, username, password]):
        raise HTTPException(status_code=500, detail="TTLock 環境變數未完整設定")

    # 確保密碼是 32 位小寫 MD5
    pwd_encrypted = password if len(password) == 32 else get_md5_password(password)

    # 官方文件要求的 ContentType: application/x-www-form-urlencoded 格式參數
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
        "username": username,
        "password": pwd_encrypted,
        "grant_type": "password"
    }

    response = requests.post(TOKEN_URL, data=payload)
    data = response.json()

    if "access_token" not in data:
        raise HTTPException(status_code=400, detail=f"TTLock 授權失敗: {data}")

    return data["access_token"]


@router.get("/list")
def get_lock_list():
    """查詢帳號底下的門鎖列表"""
    access_token = get_access_token()
    client_id = os.getenv("TTLOCK_CLIENT_ID")

    url = f"{TTLOCK_BASE_URL}/lock/list"
    params = {
        "clientId": client_id,
        "accessToken": access_token,
        "pageNo": 1,
        "pageSize": 200,
        "date": int(time.time() * 1000)
    }

    response = requests.get(url, params=params)
    return response.json()


class UnlockRequest(BaseModel):
    lock_id: int


@router.post("/unlock")
def unlock_door(body: UnlockRequest):
    """遠端開鎖指令"""
    access_token = get_access_token()
    client_id = os.getenv("TTLOCK_CLIENT_ID")

    url = f"{TTLOCK_BASE_URL}/lock/unlock"
    payload = {
        "clientId": client_id,
        "accessToken": access_token,
        "lockId": body.lock_id,
        "date": int(time.time() * 1000)
    }

    response = requests.post(url, data=payload)
    return response.json()