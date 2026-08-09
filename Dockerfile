# 1. 使用輕量且穩定的官方 Python 映像檔
FROM python:3.11-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 設定環境變數：防止 Python 產生 .pyc 檔，並讓 log 立即輸出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. 裝載系統基礎依賴（如果 Python 套件編譯需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /lib/apt/lists/*

# 5. 先複製 requirements.txt 並安裝套件（利用 Docker 快取機制，加速後續 Build）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製專案所有程式碼到容器內
COPY . .

# 7. 開放 FastAPI 預設 Port
EXPOSE 8000

# 8. 容器啟動指令：使用 uvicorn 運行 main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]