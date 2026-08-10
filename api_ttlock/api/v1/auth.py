import os
import hashlib
import requests
from fastapi import HTTPException

# 官方文件規範的中國區基礎網域與 Token 網址
TTLOCK_DOMAIN = "cnapi.ttlock.com"
TOKEN_URL = f"https://{TTLOCK_DOMAIN}/oauth2/token"

def get_md5_password(password: str) -> str:
    """將密碼轉為 TTLock 要求的 32 位小寫 MD5"""
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def get_access_token() -> str:
    """取得 TTLock Access Token (全域共用)"""
    client_id = os.getenv("TTLOCK_CLIENT_ID")
    client_secret = os.getenv("TTLOCK_CLIENT_SECRET")
    username = os.getenv("TTLOCK_USERNAME")
    password = os.getenv("TTLOCK_PASSWORD")

    if not all([client_id, client_secret, username, password]):
        raise HTTPException(status_code=500, detail="TTLock 環境變數未完整設定")

    pwd_encrypted = password if len(password) == 32 else get_md5_password(password)

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