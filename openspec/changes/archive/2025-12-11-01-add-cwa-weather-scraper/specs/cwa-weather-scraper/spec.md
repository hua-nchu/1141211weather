## ADDED Requirements

### Requirement: API 資料獲取
系統 SHALL 能夠從中央氣象局開放資料平台 API 下載 JSON 格式的天氣預報資料。

#### Scenario: 成功下載天氣資料
- **WHEN** 使用正確的 API 金鑰和 Dataset ID 發送請求
- **THEN** 系統成功下載 JSON 資料並返回完整內容

#### Scenario: API 請求失敗處理
- **WHEN** API 請求失敗（網路錯誤、授權失敗等）
- **THEN** 系統記錄錯誤訊息並提示使用者

### Requirement: JSON 資料解析
系統 SHALL 能夠解析從 API 獲取的 JSON 資料，提取各地區的天氣資訊。

#### Scenario: 提取溫度資訊
- **WHEN** 解析下載的 JSON 資料
- **THEN** 系統提取每個地區的最低溫度、最高溫度和天氣描述

#### Scenario: 地區資訊提取
- **WHEN** 解析 JSON 資料
- **THEN** 系統提取所有地區名稱並與對應的天氣資料關聯

### Requirement: SQLite 資料庫設計
系統 SHALL 使用 SQLite3 設計並初始化資料庫，存儲天氣資料。

#### Scenario: 資料庫初始化
- **WHEN** 首次執行程式或資料庫不存在
- **THEN** 系統自動創建 `data.db` 檔案和 `weather` 資料表

#### Scenario: 資料表結構
- **WHEN** 創建 weather 資料表
- **THEN** 資料表包含以下欄位：
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - location (TEXT) - 地區名稱
  - min_temp (REAL) - 最低溫度
  - max_temp (REAL) - 最高溫度
  - description (TEXT) - 天氣描述

### Requirement: 資料存儲
系統 SHALL 將解析後的天氣資料存入 SQLite 資料庫。

#### Scenario: 插入天氣資料
- **WHEN** 解析完成後執行資料存儲
- **THEN** 每筆地區天氣資料正確插入資料庫 weather 表

#### Scenario: 資料完整性驗證
- **WHEN** 資料插入完成
- **THEN** 資料庫中的記錄數量與解析的地區數量一致

### Requirement: Streamlit 視覺化介面
系統 SHALL 提供 Streamlit Web 應用展示資料庫中的天氣資料。

#### Scenario: 啟動 Streamlit 應用
- **WHEN** 執行 `streamlit run app.py`
- **THEN** 本地瀏覽器開啟 Streamlit 介面

#### Scenario: 顯示天氣資料表格
- **WHEN** Streamlit 應用載入
- **THEN** 介面顯示從 data.db 讀取的完整天氣資料表格，包含所有欄位

#### Scenario: UI 元素
- **WHEN** 顯示資料
- **THEN** 介面包含：
  - 應用標題「中央氣象局天氣資料」
  - 資料表格展示
  - 資料來源說明

### Requirement: 完整流程執行
系統 SHALL 提供主執行腳本整合所有功能模組。

#### Scenario: 端到端執行
- **WHEN** 執行主腳本
- **THEN** 系統依序完成：
  1. API 資料下載
  2. JSON 解析
  3. 資料庫初始化
  4. 資料存儲
  5. 確認可啟動 Streamlit 應用

### Requirement: 文檔與交付
系統 SHALL 產出完整的執行文檔和對話記錄。

#### Scenario: 螢幕截圖
- **WHEN** Streamlit 應用成功運行
- **THEN** 提供截圖包含：
  - Streamlit 介面
  - 顯示的天氣資料表格
  - 清晰可見的資料內容

#### Scenario: 對話記錄
- **WHEN** 完成所有實施步驟
- **THEN** 將完整對話記錄持續 append 到 prompt 檔案
