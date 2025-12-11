# Specification: CWA-Style Weather Visualization

## Overview
增強 Streamlit 應用的視覺化設計，參考中央氣象局 (CWA) 官方網站的設計風格，提供更直觀、美觀的天氣資料展示。

## Requirements

### REQ-1: 視覺設計主題
**Priority**: HIGH  
**Description**: 採用 CWA 官網的藍白色調設計風格

**Acceptance Criteria**:
- 主色調為藍色系（#1E88E5, #0D47A1）
- 背景使用白色或淺灰色
- 溫度使用漸層色（藍色=低溫，橙紅色=高溫）
- 整體設計簡潔專業

### REQ-2: 溫度卡片視覺化
**Priority**: HIGH  
**Description**: 以卡片形式展示各地區的溫度資訊

**Acceptance Criteria**:
- 每個地區一張卡片
- 顯示：地區名稱、最低溫度、最高溫度、天氣描述
- 根據溫度範圍顯示不同背景顏色
- 響應式佈局（自動調整列數）

### REQ-3: 溫度條形圖
**Priority**: HIGH  
**Description**: 使用 plotly 建立互動式溫度條形圖

**Acceptance Criteria**:
- 顯示所有地區的最低/最高溫度對比
- 使用不同顏色區分最低溫和最高溫
- 支援 hover 顯示詳細資訊
- 圖表配色符合 CWA 風格

### REQ-4: 溫度分布視覺化
**Priority**: MEDIUM  
**Description**: 視覺化溫度範圍和分布情況

**Acceptance Criteria**:
- 以視覺化方式展示溫差
- 使用漸層色表示溫度強度
- 清晰標示各地區名稱

### REQ-5: 歷史趨勢圖
**Priority**: MEDIUM  
**Description**: 當有多個批次資料時，顯示溫度變化趨勢

**Acceptance Criteria**:
- 折線圖顯示不同批次的溫度變化
- 支援選擇特定地區查看
- 可選擇查看最低溫或最高溫趨勢

### REQ-6: 改進資料表格
**Priority**: LOW  
**Description**: 增強現有資料表格的視覺效果

**Acceptance Criteria**:
- 溫度欄位使用條件格式化（背景顏色）
- 保持原有的排序和篩選功能
- 改進表格樣式

### REQ-7: 統計資訊增強
**Priority**: MEDIUM  
**Description**: 改進頁面頂部的統計資訊卡片

**Acceptance Criteria**:
- 添加適當的圖標
- 使用顏色區分不同類型的統計
- 可能顯示與上一批次的變化（delta）

### REQ-8: 響應式設計
**Priority**: MEDIUM  
**Description**: 確保在不同螢幕尺寸下都有良好的顯示效果

**Acceptance Criteria**:
- 自動調整佈局
- 圖表自適應容器寬度
- 卡片響應式排列

## Technical Design

### Color Scheme
```python
COLORS = {
    'primary': '#1E88E5',      # 主藍色
    'dark_blue': '#0D47A1',    # 深藍色
    'light_blue': '#90CAF9',   # 淺藍色
    'cold': '#42A5F5',         # 低溫（藍色）
    'moderate': '#FFA726',     # 中溫（橙色）
    'hot': '#EF5350',          # 高溫（紅色）
    'background': '#F5F5F5',   # 背景灰
}
```

### Temperature Color Mapping
```python
def get_temp_color(temp):
    if temp < 15:
        return COLORS['cold']
    elif temp < 25:
        return COLORS['moderate']
    else:
        return COLORS['hot']
```

### Dependencies
- **plotly**: 互動式圖表庫
- **streamlit**: Web 應用框架（已有）
- **pandas**: 資料處理（已有）

### File Structure
```
app.py                    # 主 Streamlit 應用（需重構）
  ├─ render_header()      # 頁面標題
  ├─ render_stats()       # 統計資訊
  ├─ render_temp_cards()  # 溫度卡片（新）
  ├─ render_bar_chart()   # 條形圖（新）
  ├─ render_trend_chart() # 趨勢圖（新）
  └─ render_data_table()  # 資料表格
```

## Non-Requirements
- 不需要實時資料更新（保持現有的批次更新機制）
- 不需要地圖視覺化（資料不包含地理座標）
- 不需要動畫效果（保持簡潔）
