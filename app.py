"""
Streamlit 視覺化應用（CWA 風格增強版）
功能：以專業視覺化方式展示中央氣象局天氣資料
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database import (
    get_latest_weather,
    get_weather_by_batch,
    get_batch_list,
    get_database_stats
)

# ==================== 色彩主題系統 ====================
COLORS = {
    'primary': '#1E88E5',      # 主藍色
    'dark_blue': '#0D47A1',    # 深藍色
    'light_blue': '#90CAF9',   # 淺藍色
    'cold': '#42A5F5',         # 低溫（藍色）
    'moderate': '#FFA726',     # 中溫（橙色）
    'hot': '#EF5350',          # 高溫（紅色）
    'background': '#F5F5F5',   # 背景灰
    'text_dark': '#263238',    # 深色文字
    'text_light': '#FFFFFF',   # 淺色文字
}

# ==================== 地區座標映射 ====================
# 台灣各地區的代表座標（緯度、經度）
LOCATION_COORDINATES = {
    '北部地區': {'lat': 25.0330, 'lon': 121.5654, 'city': '台北'},      # 台北
    '中部地區': {'lat': 24.1477, 'lon': 120.6736, 'city': '台中'},      # 台中
    '南部地區': {'lat': 22.9997, 'lon': 120.2270, 'city': '台南'},      # 台南
    '東北部地區': {'lat': 24.7021, 'lon': 121.7378, 'city': '宜蘭'},    # 宜蘭
    '東部地區': {'lat': 23.9871, 'lon': 121.6015, 'city': '花蓮'},      # 花蓮
    '東南部地區': {'lat': 22.7583, 'lon': 121.1444, 'city': '台東'},    # 台東
}


def get_temp_color(temp):
    """根據溫度返回對應的顏色"""
    if temp is None:
        return COLORS['moderate']
    if temp < 15:
        return COLORS['cold']
    elif temp < 25:
        return COLORS['moderate']
    else:
        return COLORS['hot']


def inject_custom_css():
    """注入自訂 CSS 樣式"""
    st.markdown("""
        <style>
        /* 整體頁面樣式 */
        .main {
            background-color: #FAFAFA;
        }
        
        /* 溫度卡片樣式 */
        .temp-card {
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
        }
        
        .temp-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        
        .temp-card-location {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #263238;
        }
        
        .temp-card-temp {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .temp-card-desc {
            font-size: 14px;
            color: #546E7A;
            margin-top: 8px;
        }
        
        .temp-label {
            font-size: 12px;
            color: #78909C;
            margin-right: 5px;
        }
        
        /* 統計卡片增強 */
        .stat-card {
            background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        
        /* 標題樣式 */
        .cwa-title {
            color: #0D47A1;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .cwa-subtitle {
            color: #546E7A;
            font-size: 16px;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    """渲染頁面標題"""
    st.markdown('<div class="cwa-title">🌤️ 中央氣象局天氣資料</div>', unsafe_allow_html=True)
    st.markdown('<div class="cwa-subtitle">Central Weather Administration - Weather Data Visualization</div>', unsafe_allow_html=True)


def render_enhanced_stats(stats, batches):
    """渲染增強的統計資訊"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 總資料筆數",
            stats['total_records'],
            delta=None,
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "📦 總批次數",
            stats['total_batches'],
            delta=None
        )
    
    with col3:
        st.metric(
            "📅 最早資料",
            stats['earliest_record'][:10] if stats['earliest_record'] else "N/A"
        )
    
    with col4:
        st.metric(
            "🕒 最新資料",
            stats['latest_record'][:10] if stats['latest_record'] else "N/A"
        )


def render_temperature_cards(weather_data):
    """渲染溫度卡片"""
    st.subheader("🌡️ 各地區溫度概況")
    
    # 計算每行顯示的卡片數量（響應式）
    num_cols = 3
    cols = st.columns(num_cols)
    
    for idx, location_data in enumerate(weather_data):
        col_idx = idx % num_cols
        
        with cols[col_idx]:
            location = location_data['location']
            min_temp = location_data['min_temp']
            max_temp = location_data['max_temp']
            description = location_data['description']
            
            # 根據平均溫度決定卡片顏色
            avg_temp = (min_temp + max_temp) / 2 if min_temp and max_temp else 20
            card_color = get_temp_color(avg_temp)
            
            # 使用 HTML 渲染卡片
            st.markdown(f"""
                <div class="temp-card" style="background: linear-gradient(135deg, {card_color}22 0%, {card_color}44 100%); border-left: 4px solid {card_color};">
                    <div class="temp-card-location">{location}</div>
                    <div class="temp-card-temp" style="color: {card_color};">
                        {min_temp}°C - {max_temp}°C
                    </div>
                    <div class="temp-card-desc">
                        <span class="temp-label">天氣：</span>{description}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 添加一些空間
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)


def render_temperature_bar_chart(weather_data):
    """渲染溫度條形圖"""
    st.subheader("📊 溫度對比圖")
    
    # 準備資料
    locations = [d['location'] for d in weather_data]
    min_temps = [d['min_temp'] for d in weather_data]
    max_temps = [d['max_temp'] for d in weather_data]
    
    # 建立 Plotly 圖表
    fig = go.Figure()
    
    # 最低溫度條
    fig.add_trace(go.Bar(
        name='最低溫度',
        x=locations,
        y=min_temps,
        marker_color=COLORS['cold'],
        text=min_temps,
        texttemplate='%{text}°C',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>最低溫度: %{y}°C<extra></extra>'
    ))
    
    # 最高溫度條
    fig.add_trace(go.Bar(
        name='最高溫度',
        x=locations,
        y=max_temps,
        marker_color=COLORS['hot'],
        text=max_temps,
        texttemplate='%{text}°C',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>最高溫度: %{y}°C<extra></extra>'
    ))
    
    # 更新佈局
    fig.update_layout(
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['text_dark']),
        xaxis=dict(
            title='地區',
            showgrid=False,
            showline=True,
            linecolor='lightgray'
        ),
        yaxis=dict(
            title='溫度 (°C)',
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linecolor='lightgray'
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_taiwan_temperature_map_enhanced(batches):
    """渲染增強版台灣溫度分布地圖 (CWA 風格)"""
    st.subheader("🗺️ 台灣溫度分布地圖")
    
    # 動畫控制 (C): 如果有多個批次，顯示動畫控制
    selected_batch_idx = 0
    if len(batches) >= 2:
        st.markdown("**📹 批次動畫控制**")
        col1, col2 = st.columns([4, 1])
        
        with col1:
            selected_batch_idx = st.slider(
                "選擇批次時間軸：",
                min_value=0,
                max_value=len(batches) - 1,
                value=0,
                format="批次 %d",
                help="拖動滑桿查看不同時間的溫度分布"
            )
        
        with col2:
            st.markdown(f"<div style='padding-top:8px;'><b>共 {len(batches)} 個批次</b></div>", unsafe_allow_html=True)
        
        # 顯示選中批次的時間資訊
        batch_id, count, created_at = batches[selected_batch_idx]
        st.info(f"📅 批次時間：{created_at} | 批次 ID: {batch_id} | 資料筆數: {count}")
    else:
        # 只有一個批次
        batch_id =batches[0][0]
        st.info(f"📌 當前批次：{batch_id}")
    
    # 獲取選定批次的資料
    weather_data = get_weather_by_batch(batch_id)
    
    if not weather_data:
        st.warning("無法顯示地圖：沒有可用的天氣資料")
        return
    
    # 準備地圖資料
    map_data = []
    for location_data in weather_data:
        location = location_data['location']
        if location in LOCATION_COORDINATES:
            coords = LOCATION_COORDINATES[location]
            min_temp = location_data['min_temp']
            max_temp = location_data['max_temp']
            avg_temp = (min_temp + max_temp) / 2 if min_temp and max_temp else 20
            
            map_data.append({
                'location': location,
                'city': coords['city'],
                'lat': coords['lat'],
                'lon': coords['lon'],
                'min_temp': min_temp,
                'max_temp': max_temp,
                'avg_temp': avg_temp,
                'description': location_data['description'],
                'color': get_temp_color(avg_temp)
            })
    
    if not map_data:
        st.warning("無法顯示地圖：缺少地理座標資料")
        return
    
    # 建立 Plotly 地圖
    fig = go.Figure()
    
    # 熱力圖效果 (A): 為每個位置添加多層漸變色圈模擬溫度擴散
    for data in map_data:
        # 添加3層光暈效果（由外到內）
        for layer in range(3, 0, -1):
            size = 80 * layer  # 外層更大
            opacity = 0.15 / layer  # 外層更透明
            
            fig.add_trace(go.Scattergeo(
                lon=[data['lon']],
                lat=[data['lat']],
                mode='markers',
                marker=dict(
                    size=size,
                    color=data['color'],
                    opacity=opacity,
                    line=dict(width=0)
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # 添加中心標記點（最清晰）
        marker_size = 20 + (data['avg_temp'] - 15) * 1.5
        marker_size = max(20, min(marker_size, 45))
        
        fig.add_trace(go.Scattergeo(
            lon=[data['lon']],
            lat=[data['lat']],
            text=f"{data['city']}<br>{data['avg_temp']:.1f}°C",
            mode='markers+text',
            name=data['location'],
            marker=dict(
                size=marker_size,
                color=data['color'],
                line=dict(width=3, color='white'),
                opacity=0.9
            ),
            textposition='top center',
            textfont=dict(
                size=13,
                color=COLORS['text_dark'],
                family='Arial Black',
            ),
            hovertemplate=(
                f"<b>{data['location']}</b> ({data['city']})<br>"
                f"🌡️ 溫度範圍: {data['min_temp']}°C - {data['max_temp']}°C<br>"
                f"📊 平均溫度: {data['avg_temp']:.1f}°C<br>"
                f"☁️ 天氣: {data['description']}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
    
    # 改進地圖樣式 (B): 更詳細的台灣地圖設定
    fig.update_geos(
        center=dict(lat=23.7, lon=120.9),  # 調整中心點以更好地框住台灣
        projection_scale=25,                # 增加縮放以顯示更多細節
        showcountries=True,
        countrycolor='#CCCCCC',
        showland=True,
        landcolor='#F0F0F0',              # 淺灰色陸地
        showocean=True,
        oceancolor='#E3F2FD',             # 淺藍色海洋
        coastlinecolor='#78909C',         # 深灰色海岸線
        coastlinewidth=1.5,
        showlakes=True,
        lakecolor='#BBDEFB',
        projection_type='mercator',
        visible=True,
        resolution=50,                     # 提高解析度
        showframe=True,
        framecolor='#BDBDBD',
        framewidth=1
    )
    
    # 更新佈局
    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='#FAFAFA',
        font=dict(family="Arial", size=12),
        geo=dict(
            bgcolor='#FFFFFF',
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 添加溫度圖例和說明
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"<div style='text-align:center; padding:10px; background:linear-gradient(135deg, {COLORS['cold']}22, {COLORS['cold']}44); border-radius:8px;'>"
            f"<span style='color:{COLORS['cold']};font-size:24px; font-weight:bold;'>●</span><br>"
            f"<b>低溫區</b><br>&lt; 15°C"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"<div style='text-align:center; padding:10px; background:linear-gradient(135deg, {COLORS['moderate']}22, {COLORS['moderate']}44); border-radius:8px;'>"
            f"<span style='color:{COLORS['moderate']};font-size:24px; font-weight:bold;'>●</span><br>"
            f"<b>中溫區</b><br>15-25°C"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"<div style='text-align:center; padding:10px; background:linear-gradient(135deg, {COLORS['hot']}22, {COLORS['hot']}44); border-radius:8px;'>"
            f"<span style='color:{COLORS['hot']};font-size:24px; font-weight:bold;'>●</span><br>"
            f"<b>高溫區</b><br>&gt; 25°C"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"<div style='text-align:center; padding:10px; background:#F5F5F5; border-radius:8px;'>"
            f"<span style='font-size:24px;'>🗺️</span><br>"
            f"<b>資料點數</b><br>{len(map_data)} 個地區"
            f"</div>",
            unsafe_allow_html=True
        )


def render_taiwan_temperature_map(weather_data):
    """渲染台灣溫度分布地圖（簡化版，向後兼容）"""
    # 獲取批次列表
    batches = get_batch_list()
    # 調用增強版函數
    render_taiwan_temperature_map_enhanced(batches)


def render_temperature_range_chart(weather_data):
    """渲染溫度範圍圖"""
    st.subheader("🌡️ 溫度範圍分布")
    
    # 準備資料
    locations = [d['location'] for d in weather_data]
    min_temps = [d['min_temp'] for d in weather_data]
    max_temps = [d['max_temp'] for d in weather_data]
    temp_ranges = [max_t - min_t for min_t, max_t in zip(min_temps, max_temps)]
    
    # 建立圖表
    fig = go.Figure()
    
    # 添加範圍條
    for i, location in enumerate(locations):
        avg_temp = (min_temps[i] + max_temps[i]) / 2
        color = get_temp_color(avg_temp)
        
        fig.add_trace(go.Scatter(
            x=[min_temps[i], max_temps[i]],
            y=[location, location],
            mode='lines+markers',
            name=location,
            line=dict(color=color, width=8),
            marker=dict(size=12, color=color),
            hovertemplate=f'<b>{location}</b><br>溫度範圍: {min_temps[i]}°C - {max_temps[i]}°C<br>溫差: {temp_ranges[i]}°C<extra></extra>',
            showlegend=False
        ))
    
    # 更新佈局
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['text_dark']),
        xaxis=dict(
            title='溫度 (°C)',
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linecolor='lightgray'
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            showline=False
        ),
        height=300,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_trend_chart(batches):
    """渲染歷史趨勢圖（如果有多個批次）"""
    if len(batches) < 2:
        return
    
    st.subheader("📈 歷史溫度趨勢")
    
    # 收集所有批次的資料
    all_data = []
    for batch_id, count, created_at in batches[:10]:  # 最多顯示最近 10 個批次
        batch_data = get_weather_by_batch(batch_id)
        for item in batch_data:
            item['batch_time'] = created_at[:16]  # 只取到分鐘
            all_data.append(item)
    
    if not all_data:
        return
    
    df = pd.DataFrame(all_data)
    
    # 獲取所有獨特的地區
    locations = df['location'].unique()
    
    # 讓用戶選擇要顯示的地區
    selected_locations = st.multiselect(
        "選擇要顯示的地區：",
        options=list(locations),
        default=list(locations[:3]) if len(locations) >= 3 else list(locations)
    )
    
    if not selected_locations:
        st.info("請選擇至少一個地區")
        return
    
    # 選擇顯示最低溫或最高溫
    temp_type = st.radio("選擇溫度類型：", ["最低溫度", "最高溫度"], horizontal=True)
    temp_col = 'min_temp' if temp_type == "最低溫度" else 'max_temp'
    
    # 建立趨勢圖
    fig = go.Figure()
    
    for location in selected_locations:
        location_df = df[df['location'] == location].sort_values('batch_time')
        
        fig.add_trace(go.Scatter(
            x=location_df['batch_time'],
            y=location_df[temp_col],
            mode='lines+markers',
            name=location,
            line=dict(width=2),
            marker=dict(size=8),
            hovertemplate=f'<b>{location}</b><br>時間: %{{x}}<br>{temp_type}: %{{y}}°C<extra></extra>'
        ))
    
    # 更新佈局
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['text_dark']),
        xaxis=dict(
            title='批次時間',
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linecolor='lightgray'
        ),
        yaxis=dict(
            title=f'{temp_type} (°C)',
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linecolor='lightgray'
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_enhanced_data_table(weather_data):
    """渲染增強的資料表格"""
    st.subheader("📋 詳細資料表格")
    
    # 轉換為 DataFrame
    df = pd.DataFrame(weather_data)
    
    # 重新排序欄位並重命名
    display_columns = {
        'location': '地區',
        'min_temp': '最低溫度 (°C)',
        'max_temp': '最高溫度 (°C)',
        'description': '天氣描述',
        'batch_id': '批次 ID',
        'fetch_time': '獲取時間'
    }
    
    # 選擇要顯示的欄位
    df_display = df[list(display_columns.keys())].copy()
    df_display.columns = list(display_columns.values())
    
    # 使用可互動的資料表
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            '最低溫度 (°C)': st.column_config.NumberColumn(
                format="%.1f°C",
            ),
            '最高溫度 (°C)': st.column_config.NumberColumn(
                format="%.1f°C",
            ),
        }
    )
    
    return df_display


def main():
    # 設置頁面配置
    st.set_page_config(
        page_title="中央氣象局天氣資料",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 注入自訂 CSS
    inject_custom_css()
    
    # 渲染標題
    render_header()
    
    st.markdown("---")
    
    # 獲取資料庫統計資訊
    stats = get_database_stats()
    batches = get_batch_list()
    
    if not stats or stats['total_records'] == 0:
        st.warning("⚠️ 資料庫中沒有資料")
        st.info("請先執行 `python main.py` 下載並存儲天氣資料")
        return
    
    # 顯示統計資訊
    render_enhanced_stats(stats, batches)
    
    st.markdown("---")
    
    # 批次選擇器
    st.subheader("📂 資料批次選擇")
    
    if not batches:
        st.error("無法獲取批次列表")
        return
    
    # 創建批次選項
    batch_options = ["最新資料"] + [
        f"{batch_id} ({count} 筆) - {created_at}"
        for batch_id, count, created_at in batches
    ]
    
    selected_option = st.selectbox(
        "選擇要查看的資料批次：",
        batch_options,
        index=0
    )
    
    # 根據選擇獲取資料
    if selected_option == "最新資料":
        weather_data = get_latest_weather()
        st.info(f"📌 顯示最新一批資料（批次 ID: {batches[0][0]}）")
    else:
        # 從選項中提取 batch_id
        batch_id = selected_option.split(" (")[0]
        weather_data = get_weather_by_batch(batch_id)
        st.info(f"📌 顯示批次：{batch_id}")
    
    if not weather_data:
        st.warning("該批次沒有資料")
        return
    
    st.markdown("---")
    
    # 溫度卡片視覺化
    render_temperature_cards(weather_data)
    
    st.markdown("---")
    
    # 台灣溫度分布地圖
    render_taiwan_temperature_map(weather_data)
    
    st.markdown("---")
    
    # 溫度圖表
    col1, col2 = st.columns(2)
    
    with col1:
        render_temperature_bar_chart(weather_data)
    
    with col2:
        render_temperature_range_chart(weather_data)
    
    st.markdown("---")
    
    # 歷史趨勢圖（如果有多個批次）
    if len(batches) >= 2:
        render_trend_chart(batches)
        st.markdown("---")
    
    # 資料表格
    df_display = render_enhanced_data_table(weather_data)
    
    # 下載按鈕
    st.markdown("---")
    csv = df_display.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下載為 CSV",
        data=csv,
        file_name=f"weather_data_{batches[0][0]}.csv",
        mime="text/csv"
    )
    
    # 頁尾資訊
    st.markdown("---")
    st.caption("🔗 資料來源：中央氣象局開放資料平台")
    st.caption(f"📊 資料庫檔案：data.db | 最後更新：{stats['latest_record']}")


if __name__ == "__main__":
    main()
