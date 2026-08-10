import os
from futu import *


class FutuQuoter:
    def __init__(self, host=None, port=11111):
        """
        初始化並建立行情連線物件
        優先順序：1. 手動傳入的 host/port -> 2. 環境變數 FUTU_HOST/FUTU_PORT -> 3. 預設值
        """
        self.host = host or os.getenv('FUTU_HOST', '127.0.0.1')
        self.port = int(os.getenv('FUTU_PORT', port))
        self.ctx = None
        self.connect()

    def connect(self):
        """建立連線"""
        if not self.ctx:
            try:
                self.ctx = OpenQuoteContext(host=self.host, port=self.port)
                print(f"成功連線至 FutuOpenD: {self.host}:{self.port}")
            except Exception as e:
                self.ctx = None
                print(f"連線至 FutuOpenD 失敗 ({self.host}:{self.port}): {e}")

    def get_market_state(self, code_list):
        """獲取指定股票/市場的狀態 (若未連線或斷線將自動嘗試重連)"""
        # 防護：若未連線則自動嘗試重連
        if not self.ctx:
            self.connect()

        if not self.ctx:
            print("尚未建立連線且自動重連失敗")
            return None

        ret, data = self.ctx.get_market_state(code_list)
        if ret == RET_OK:
            return data
        else:
            print(f"獲取市場狀態失敗: {data}")
            return None

    def close(self):
        """關閉連線"""
        if self.ctx:
            try:
                self.ctx.close()
            except Exception as e:
                print(f"關閉連線時發生錯誤: {e}")
            finally:
                self.ctx = None
                print("已關閉 FutuOpenD 連線")

    # 支援使用 with 語法管理資源 (Context Manager)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()