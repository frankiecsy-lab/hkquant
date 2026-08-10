import os
import time
import requests
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from api.v1.futu_quoter import FutuQuoter

router = APIRouter()

# 直接建立實例，即使 OpenD 還沒開好，quoter 物件也不會是 None
quoter = FutuQuoter(host=os.getenv('FUTU_HOST', '127.0.0.1'), port=11111)


@router.get("/")
def read_root():
    return {
        "status": "v1",
        "message": "Hello from futu opend container!",
        "path": "/futu/"
    }


@router.get("/market-state")
def get_market_state(
    codes: str = Query(..., description="股票代碼，多個代碼請用逗號隔開，例如: HK.00700,SZ.000001")
):
    """
    獲取市場/股票狀態資訊
    範例 URL: /futu/v1/market-state?codes=HK.00700,SZ.000001
    """
    # 1. 解析股票代碼字串
    code_list = [c.strip() for c in codes.split(",") if c.strip()]
    if not code_list:
        raise HTTPException(status_code=400, detail="請提供有效的股票代碼")

    # 2. 呼叫 Quoter (若未連線，Class 內部會自動嘗試重連)
    data = quoter.get_market_state(code_list)

    if data is None:
        raise HTTPException(status_code=500, detail="獲取市場狀態失敗，請確認代碼或 OpenD 狀態")

    # 3. 將 DataFrame 轉成 List of Dict 供 JSON 回傳
    if hasattr(data, "to_dict"):
        result = data.to_dict(orient="records")
    else:
        result = data

    return {
        "success": True,
        "codes": code_list,
        "data": result
    }