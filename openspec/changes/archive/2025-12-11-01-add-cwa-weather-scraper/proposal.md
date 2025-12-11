# Change: 新增中央氣象局天氣資料爬蟲系統

## Why
完成中興大學「人工智慧與資訊安全」課程的爬蟲作業。需要實作一個完整的資料爬取流程：從中央氣象局 API 獲取天氣資料、解析 JSON、存入 SQLite 資料庫，並建立 Streamlit 視覺化介面展示資料。

## What Changes
- 新增 API 資料獲取模組（`fetch_weather.py`）
- 新增 JSON 資料解析功能
- 新增 SQLite 資料庫設計與操作模組（`database.py`）
- 新增 Streamlit 視覺化應用（`app.py`）
- 新增主要執行腳本收集所有功能

**關鍵功能：**
1. 使用 requests 從 CWA API 下載 JSON 資料
2. 解析 JSON 提取地區、溫度、天氣描述
3. 設計並初始化 SQLite 資料庫（data.db）
4. 將解析資料存入資料庫
5. Streamlit UI 讀取並顯示資料表格

## Impact
- 新增的規範：`specs/cwa-weather-scraper/spec.md`
- 新增的檔案：
  - `fetch_weather.py` - API 請求與資料下載
  - `database.py` - 資料庫操作
  - `app.py` - Streamlit 應用
  - `main.py` - 主執行腳本
  - `data.db` - SQLite 資料庫檔案（自動生成）
  - `requirements.txt` - Python 依賴套件
- 輸出檔案：
  - 螢幕截圖（Streamlit 介面）
  - prompt 對話記錄檔案
