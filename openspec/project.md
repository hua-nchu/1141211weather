# Project Context

## Purpose
中興大學 114 上學期「人工智慧與資訊安全」課程的爬蟲作業。本專案從中央氣象局（CWA）開放資料平台獲取天氣資料，解析後存入 SQLite 資料庫，並使用 Streamlit 建立視覺化介面。

**目標：**
- 學習 API 資料爬取技術
- 掌握 JSON 資料解析
- 實踐資料庫設計與操作
- 建立資料視覺化應用

## Tech Stack
- **Python 3.x** - 主要程式語言
- **requests** - HTTP 請求與 API 調用
- **json** - JSON 資料解析
- **sqlite3** - 資料庫操作（內建模組）
- **Streamlit** - Web 應用框架
- **pandas** - 資料處理（可選）

## Project Conventions

### OpenSpec Change Naming
- **變更 ID 格式**：`<編號>-<動詞>-<描述>`
- **編號規則**：從 01 開始，依序遞增（01, 02, 03...）
- **範例**：
  - `01-add-cwa-weather-scraper`
  - `02-update-database-schema`
  - `03-refactor-api-module`

### Code Style
- 使用 UTF-8 編碼
- 函數和變數使用 snake_case 命名
- 類別使用 PascalCase 命名
- 每個功能模組獨立檔案
- 包含必要的錯誤處理
- 添加中文註解說明關鍵邏輯

### Architecture Patterns
- **模組化設計**：分離資料獲取、資料處理、資料庫操作和 UI 層
- **單一職責**：每個腳本專注單一功能
- **可重用性**：設計可重複執行的資料更新流程

### Testing Strategy
- 手動測試 API 連接
- 驗證資料庫結構正確性
- 測試 Streamlit 應用顯示完整性
- 提供執行截圖作為驗證

### Git Workflow
課程作業，無特定 Git 工作流程要求

## Domain Context
**中央氣象局開放資料平台：**
- API 需要授權金鑰（Authorization Key）
- 資料格式為 JSON
- Dataset F-A0010-001 提供全台各地區天氣預報
- 包含溫度、天氣描述等資訊

**資料欄位（預期）：**
- 地區名稱（location）
- 最低溫度（min_temp）
- 最高溫度（max_temp）
- 天氣描述（description）

## Important Constraints
- 僅供教學使用，使用提供的示範 API 金鑰
- 必須使用 SQLite3（內建模組）
- 必須使用 Streamlit 建立本地應用
- 需要提供螢幕截圖驗證功能
- 需要記錄完整對話 prompt

## External Dependencies
- **中央氣象局開放資料平台 API**
  - 端點：`https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001`
  - 授權金鑰：`CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F`
  - 資料格式：JSON
  - Dataset：F-A0010-001（天氣預報資料）
