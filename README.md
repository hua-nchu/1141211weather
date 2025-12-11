# 中央氣象局天氣資料爬蟲系統

本專案從中央氣象局開放資料平台獲取天氣資料，解析後存入 SQLite 資料庫，並使用 Streamlit 建立視覺化介面。

## 📁 專案結構

```
1210 課堂練習作業 -爬蟲/
│
├── fetch_weather.py      # API 資料獲取模組
├── database.py           # SQLite 資料庫操作
├── main.py              # 主執行腳本
├── app.py               # Streamlit 視覺化應用
├── requirements.txt     # Python 依賴套件
├── data.db             # SQLite 資料庫（自動生成）
├── README.md           # 本文件
└── openspec/           # OpenSpec 規範與變更記錄
```

## 🚀 快速開始

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定 API 金鑰（重要！）

為了安全性，API 金鑰現在使用環境變數管理。

1. **複製環境變數範本檔：**
   ```bash
   copy .env.example .env
   ```

2. **編輯 `.env` 檔案，填入您的 API 金鑰：**
   ```
   CWA_API_KEY=your_actual_api_key_here
   ```

   > **注意**: `.env` 檔案已加入 `.gitignore`，不會被上傳到 Git，保護您的 API 金鑰安全。

3. **（教學用途）** 如果使用課程提供的示範金鑰：
   ```
   CWA_API_KEY=CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F
   ```

### 3. 執行資料爬取

```bash
python main.py
```

這將會：
- 從中央氣象局 API 下載天氣資料
- 解析 JSON 資料提取溫度和天氣描述
- 存入 SQLite 資料庫（保留歷史資料）
- 顯示執行摘要

### 3. 啟動 Streamlit 應用

```bash
streamlit run app.py
```

瀏覽器將自動開啟，顯示天氣資料視覺化介面。

## 🌐 Streamlit Cloud 部署

本應用已部署到 Streamlit Cloud：**https://1141211weather-ptlrev47fzdgquusncukf6.streamlit.app/**

### 部署步驟

1. **Fork 或 Clone 此倉庫到您的 GitHub**

2. **在 Streamlit Cloud 創建應用**:
   - 訪問 https://share.streamlit.io/
   - 連接您的 GitHub 倉庫
   - 選擇此專案

3. **配置 Secrets**:
   - 在 App Settings > Secrets 中添加：
   ```toml
   CWA_API_KEY = "your_api_key_here"
   ```
   參考 `.streamlit/secrets.toml.example` 範本

4. **首次啟動**:
   - 應用會自動初始化資料庫
   - 第一次載入可能需要幾秒鐘
   - 之後訪問將使用已存在的資料

### 注意事項

- ⚠️ 首次訪問時，應用會自動從 CWA API 抓取一批資料
- 📊 Streamlit Cloud 的免費版本有資源限制
- 🔄 資料庫會在每次部署時重置（因為不在 Git 中）

## 📊 功能特色

### API 資料獲取 (`fetch_weather.py`)
- ✅ 使用 requests 從 CWA API 下載 JSON 資料
- ✅ 完整的錯誤處理（網路錯誤、HTTP 錯誤、JSON 解析錯誤）
- ✅ 自動解析 JSON 提取地區、溫度、天氣描述

### 資料庫管理 (`database.py`)
- ✅ SQLite3 資料庫設計
- ✅ **保留所有歷史資料**（不刪除舊資料）
- ✅ 批次管理系統（每次執行使用唯一批次 ID）
- ✅ 多種查詢功能（最新資料、特定批次、所有歷史）

### Streamlit UI (`app.py`) - **CWA 風格增強版** 🎨
- ✅ **CWA 風格設計**：藍白配色主題，專業視覺效果
- ✅ **溫度卡片視覺化**：每個地區顯示為漂亮的卡片，根據溫度變色
- ✅ **互動式圖表**（使用 Plotly）：
  - 溫度條形圖：並排對比最低/最高溫度
  - 溫度範圍圖：視覺化溫度區間分布
  - 歷史趨勢圖：顯示多批次資料的溫度變化（如有多批次）
- ✅ **台灣溫度分布地圖（增強版）** - **新增！🗺️**
  - **多層熱力圖效果**：3 層漸變光暈模擬溫度擴散（類似 CWA 官網）
  - **詳細地形地圖**：改進的台灣輪廓、海岸線、地理細節
  - **批次動畫控制**：時間軸滑桿可查看不同批次的溫度變化
  - **互動式標記**：溫度標記隨溫度變色和調整大小
  - **美化圖例**：4 個漸層背景卡片顯示溫度區間
- ✅ **自訂 CSS 樣式**：卡片懸停效果、漸層背景、響應式佈局
- ✅ 統計資訊卡片（總筆數、批次數、時間範圍）
- ✅ 批次選擇器（查看不同時間的資料）
- ✅ 增強資料表格（溫度格式化）
- ✅ CSV 下載功能

## 📝 資料表結構

```sql
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,           -- 批次識別碼
    location TEXT NOT NULL,            -- 地區名稱
    min_temp REAL,                     -- 最低溫度
    max_temp REAL,                     -- 最高溫度
    description TEXT,                  -- 天氣描述
    fetch_time TIMESTAMP,              -- 資料獲取時間
    created_at TIMESTAMP               -- 記錄創建時間
);
```

## 🔧 模組說明

### `fetch_weather.py`
- `fetch_weather_data()` - 從 API 下載資料
- `parse_weather_json(json_data)` - 解析 JSON 資料

### `database.py`
- `init_database()` - 初始化資料庫
- `insert_weather_data(data_list, batch_id)` - 插入資料
- `get_latest_weather()` - 查詢最新資料
- `get_weather_by_batch(batch_id)` - 查詢特定批次
- `get_batch_list()` - 查詢所有批次

### `main.py`
- 整合所有模組的主執行腳本
- 生成批次 ID 並管理完整流程

### `app.py`
- Streamlit Web 應用（CWA 風格增強版）
- 色彩主題系統與溫度映射
- 11 個視覺化渲染函數（卡片、地圖、圖表、表格）
- **台灣溫度地圖增強版**：
  - 多層熱力圖效果（3 層漸變光暈）
  - 詳細台灣地形地圖
  - 批次動畫控制（時間軸滑桿）
- 提供專業的資料視覺化介面

## 📌 注意事項

1. **資料保留**：每次執行 `main.py` 會新增資料到資料庫，不會刪除舊資料
2. **批次管理**：每批資料使用時間戳記格式的批次 ID（如：20251211_220000）
3. **API 金鑰**：使用課程提供的示範金鑰，僅供教學使用

## 📚 課程資訊

- 課程：中興大學 114 上學期「人工智慧與資訊安全」
- 作業：1210 課堂練習作業 - 爬蟲
- 資料來源：中央氣象局開放資料平台

## 🔗 相關連結

- [中央氣象局開放資料平台](https://opendata.cwa.gov.tw/)
- [Dataset F-A0010-001](https://opendata.cwa.gov.tw/dataset/forecast/F-A0010-001)
