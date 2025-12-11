# 中央氣象局爬蟲專案 - 達到目標的 Prompt

## 初始請求

```
目標：
Part 1：中央氣象局（CWA）資料
📌 已提供的連結（上課用）
範例網頁（HTML 版溫度）
https://www.cwa.gov.tw/V8/C/W/OBS_Temp.html

CWA 登入頁
https://opendata.cwa.gov.tw/userLogin

你的 API 金鑰（示範用）
CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F

教學使用的 JSON Dataset（F-A0010-001）
網站資料頁：https://opendata.cwa.gov.tw/dataset/forecast/F-A0010-001
直接下載 JSON 的網址：
https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F&downloadType=WEB&format=JSON

📘 作業要求（Part 1）
1️⃣ 下載中央氣象局 JSON 資料
2️⃣ 解析資料：取出各地區的溫度（或老師要求的欄位）
3️⃣ 設計 SQLite 資料庫（data.db）
4️⃣ 把解析後的資料「存進 SQLite3」
5️⃣ 建立一個本地 Streamlit App
  - 顯示從 SQLite 讀出的資料表格
  - 必須附 screenshot（螢幕截圖）
  - 內容包含：Streamlit 介面、顯示你資料庫裡的天氣資料表

產出達到目標的prompt, 並將所有對話存檔檔名prompt，持續appent
```

##  成功的實施流程

### 階段 1：OpenSpec 規劃（PLANNING 模式）

1. **安裝 OpenSpec**
   ```bash
   npm install -g @fission-ai/openspec@latest
   openspec init
   ```
   - 選擇 AI 工具整合（Amazon Q Developer/Gemini CLI）
   - 創建 OpenSpec 目錄結構

2. **填寫專案配置** (`openspec/project.md`)
   - 專案目的：中興大學課程作業，爬蟲系統實作
   - 技術棧：Python, requests, sqlite3, streamlit, pandas
   - 重要約束：教學用 API 金鑰、保留歷史資料、截圖驗證

3. **創建變更提案** (`01-add-cwa-weather-scraper/`)
   - `proposal.md`：說明為何需要此變更、改變什麼、影響範圍
   - `tasks.md`：詳細的實施檢查清單（6個大項，37個子項）
   - `specs/cwa-weather-scraper/spec.md`：系統需求規範（8個主要需求）

4. **創建實施計劃** (`implementation_plan.md`)
   - 模組設計：fetch_weather.py, database.py, main.py, app.py
   - 資料表設計：包含批次管理和時間戳記
   - 驗證計劃：分4個階段測試

5. **請求審查並獲得批准**
   - 用戶反饋：不要刪除舊資料
   - 調整：改為累積資料模式，使用 batch_id 區分批次
   - 獲得批准：LGTM

### 階段 2：開發實施（EXECUTION 模式）

1. **創建 API 模組** (`fetch_weather.py`)
   ```python
   # 關鍵功能：
   - fetch_weather_data(): API 請求
   - parse_weather_json(): JSON 解析
   # 處理問題：
   - SSL 證書驗證（verify=False）
   - Windows UTF-8 編碼
   ```

2. **創建資料庫模組** (`database.py`)
   ```python
   # 關鍵功能：
   - init_database(): 初始化資料表
   - insert_weather_data(data_list, batch_id): 插入資料
   - get_latest_weather(): 查詢最新批次
   - get_batch_list(): 查詢所有批次
   ```

3. **創建主執行腳本** (`main.py`)
   ```python
   # 整合流程：
   1. 生成批次 ID（YYYYMMDD_HHMMSS）
   2. 下載資料
   3. 解析資料
   4. 初始化資料庫
   5. 存入資料
   6. 顯示執行摘要
   ```

4. **創建 Streamlit 應用** (`app.py`)
   ```python
   # UI 組件：
   - 統計卡片（總筆數、批次數、時間）
   - 批次選擇器（最新/歷史）
   - 資料表格
   - CSV 下載
   ```

### 階段 3：驗證測試（VERIFICATION 模式）

1. **API 測試**
   ```bash
   python fetch_weather.py
   ```
   - ✅ 成功下載並解析 6 個地區資料

2. **完整流程測試**
   ```bash
   python main.py
   ```
   - ✅ 批次 ID: 20251211_222014
   - ✅ 6 筆資料成功存入資料庫

3. **Streamlit 應用**
   ```bash
   streamlit run app.py
   ```
   - ✅ 應用啟動成功
   - ✅ 截圖保存
   - ✅ 所有功能正常

## 關鍵成功因素

### 1. OpenSpec 工作流程
- **規劃先行**：先設計規範再編碼
- **用戶審查**：確保需求理解正確
- **批次管理**：記錄所有變更歷史

### 2. 技術問題解決
- **SSL 證書**：使用 `verify=False` 跳過驗證
- **編碼問題**：設置 UTF-8 輸出包裝器
- **JSON 結構**：分析實際結構並調整解析邏輯

### 3. 資料庫設計
- **歷史保留**：使用 batch_id 而不刪除舊資料
- **時間戳記**：記錄 fetch_time 和 created_at
- **批次查詢**：支持查看不同批次資料

### 4. 用戶體驗
- **友好輸出**：詳細的執行摘要和進度提示
- **互動介面**：Streamlit 批次選擇和統計資訊
- **CSV 下載**：方便資料匯出

## 最終成果

### 檔案結構
```
1210 課堂練習作業 -爬蟲/
├── fetch_weather.py      # API 模組
├── database.py           # 資料庫模組
├── main.py              # 主腳本
├── app.py               # Streamlit 應用
├── requirements.txt     # 依賴套件
├── data.db             # SQLite 資料庫
├── README.md           # 專案文檔
└── openspec/           # OpenSpec 規範
    ├── project.md
    └── changes/01-add-cwa-weather-scraper/
```

### 資料統計
- **地區數量：** 6 個
- **資料筆數：** 6 筆
- **批次數量：** 1 個
- **資料庫大小：** data.db

### 截圖證明
- Streamlit 介面截圖已保存
- 包含所有必要元素（標題、統計、表格）

## 複製成功的步驟

### 快速開始（適用於類似專案）

1. **安裝 OpenSpec**
   ```bash
   npm install -g @fission-ai/openspec@latest
   cd your-project
   openspec init
   ```

2. **填寫專案配置**
   - 編輯 `openspec/project.md`
   - 定義技術棧、約束、依賴

3. **創建變更提案**
   ```
   使用 AI 助手：
   "請使用 OpenSpec 工作流程，為我的 [專案描述] 創建變更提案"
   ```

4. **獲得審查批准**
   - 審查 `implementation_plan.md`
   - 確認所有需求
   - 批准後進入實施

5. **實施與驗證**
   - 按計劃創建各模組
   - 逐步測試驗證
   - 截圖記錄結果

## 對話記錄總結

本專案從 OpenSpec 安裝開始，經歷完整的規劃、實施和驗證階段：

1. **Step 1-23**: OpenSpec 安裝與設置
2. **Step 24-143**: 專案規劃與提案創建
3. **Step 144-167**: 用戶反饋與計劃調整
4. **Step 168-209**: 代碼實施與模組創建
5. **Step 210-223**: 測試驗證與截圖記錄

總共使用的工具調用超過 200 次，成功完成所有作業要求。

---

**專案完成日期：** 2025-12-11
**最終驗證批次：** 20251211_222014
**狀態：** ✅ 所有測試通過，準備交付
