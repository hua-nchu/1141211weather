# Change Proposal: 修復 Streamlit Cloud 部署問題

## Why this change?

**當前問題：**

Streamlit Cloud 部署的應用（https://1141211weather-ptlrev47fzdgquusncukf6.streamlit.app/）顯示「⚠️ 資料庫中沒有資料」錯誤。

**根本原因：**
1. `data.db` 被 `.gitignore` 排除，未上傳到 Git
2. Streamlit Cloud 無法手動執行 `main.py` 抓取資料
3. 應用啟動時沒有自動初始化資料庫的機制

**需要做什麼：**
- 在 `app.py` 啟動時自動檢查資料庫
- 如果資料庫為空，自動抓取一批資料
- 使用 Streamlit Secrets 管理 API 金鑰
- 確保首次訪問時就有資料可顯示

## What changes?

### 解決方案：應用啟動時自動初始化資料

#### 1. 修改 `app.py` 添加自動初始化功能

在應用啟動時：
```python
# 檢查資料庫是否有資料
stats = get_database_stats()
if stats['total_records'] == 0:
    # 自動抓取一批資料
    st.info("首次啟動，正在初始化資料...")
    auto_initialize_database()
```

添加自動初始化函數：
```python
def auto_initialize_database():
    """自動初始化資料庫（用於 Streamlit Cloud）"""
    try:
        from fetch_weather import fetch_weather_data, parse_weather_json
        from datetime import datetime
        
        # 抓取資料
        json_data = fetch_weather_data()
        if json_data:
            weather_list = parse_weather_json(json_data)
            if weather_list:
                # 生成批次 ID
                batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                # 存入資料庫
                insert_weather_data(weather_list, batch_id)
                return True
    except Exception as e:
        st.error(f"自動初始化失敗：{e}")
    return False
```

#### 2. 配置 Streamlit Secrets

在 Streamlit Cloud 設置中添加 secret：
```toml
# .streamlit/secrets.toml (本地測試用)
CWA_API_KEY = "your_api_key_here"
```

修改 `fetch_weather.py` 支援 Streamlit Secrets：
```python
import os
try:
    import streamlit as st
    API_KEY = st.secrets.get("CWA_API_KEY", os.getenv('CWA_API_KEY', 'fallback'))
except:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv('CWA_API_KEY', 'fallback')
```

#### 3. 添加 .streamlit 配置

創建 `.streamlit/secrets.toml.example` 範本：
```toml
# Streamlit Cloud Secrets 設定範本
# 在 Stromlit Cloud 的 App Settings > Secrets 中添加

CWA_API_KEY = "your_cwa_api_key_here"
```

#### 4. 更新文檔

在 README.md 添加 Streamlit Cloud 部署說明：
- 如何設置 Streamlit Secrets
- 首次啟動的預期行為
- 故障排除指南

## Impact

### 正面影響
- ✅ Streamlit Cloud 部署可正常使用
- ✅ 首次訪問自動初始化資料
- ✅ 無需手動執行 main.py
- ✅ 使用 Streamlit Secrets 安全管理 API 金鑰

### 用戶體驗改善
- ✅ 訪問應用即可看到資料
- ✅ 不會看到「沒有資料」錯誤
- ✅ 自動化部署流程

### 技術優勢
- ✅ 支援本地開發（.env）和雲端部署（Secrets）
- ✅ 優雅的降級處理
- ✅ 保持與現有功能的兼容性

## Next Steps

1. 實施自動初始化功能
2. 配置 Streamlit Secrets 支援
3. 本地測試（模擬空資料庫）
4. 提交並推送到 GitHub
5. 在 Streamlit Cloud 配置 Secrets
6. 驗證部署成功

## Alternative Solutions Considered

**選項 A**（採用）：應用啟動時自動初始化
- 優點：完全自動化，用戶體驗最佳
- 缺點：首次啟動稍慢

**選項 B**：提供預填充的資料庫
- 優點：啟動快速
- 缺點：資料會過時，需要定期更新

**選項 C**：提示用戶手動刷新
- 優點：簡單實施
- 缺點：用戶體驗差

選擇選項 A 因為它提供最佳的用戶體驗。
