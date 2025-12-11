"""
中央氣象局天氣資料獲取模組
功能：從 CWA API 下載並解析 JSON 資料
"""

中央氣象局 API 資料獲取模組
功能：從 CWA OpenData API 下載並解析天氣資料
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# API 設置（從環境變數讀取，如無則使用預設教學金鑰）
API_KEY = os.getenv('CWA_API_KEY', 'CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F')
API_BASE_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi"
DATASET_ID = "F-A0010-001"
API_URL = f"{API_BASE_URL}/{DATASET_ID}"


def fetch_weather_data() -> Optional[Dict]:
    """
    從中央氣象局 API 下載天氣資料
    
    Returns:
        Dict: JSON 資料，如果失敗則返回 None
    """
    try:
        # 構建完整的 API URL
        params = {
            'Authorization': API_KEY,
            'downloadType': 'WEB',
            'format': 'JSON'
        }
        
        print("正在從中央氣象局 API 下載資料...")
        print(f"API URL: {API_URL}")
        
        # 發送 GET 請求（跳過 SSL 驗證以避免證書問題）
        response = requests.get(API_URL, params=params, timeout=30, verify=False)
        
        # 抑制 SSL 警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 檢查 HTTP 狀態碼
        response.raise_for_status()
        
        # 解析 JSON
        data = response.json()
        
        print("✓ 資料下載成功！")
        return data
        
    except requests.exceptions.Timeout:
        print("✗ 錯誤：API 請求超時")
        return None
    except requests.exceptions.ConnectionError:
        print("✗ 錯誤：網路連接失敗")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP 錯誤：{e}")
        return None
    except json.JSONDecodeError:
        print("✗ 錯誤：無法解析 JSON 資料")
        return None
    except Exception as e:
        print(f"✗ 未預期的錯誤：{e}")
        return None


def parse_weather_json(json_data: Dict) -> List[Dict]:
    """
    解析 JSON 資料，提取各地區的天氣資訊
    
    Args:
        json_data: 從 API 獲取的 JSON 資料
        
    Returns:
        List[Dict]: 解析後的天氣資料列表
        [
            {
                'location': '地區名稱',
                'min_temp': 最低溫度,
                'max_temp': 最高溫度,
                'description': '天氣描述'
            },
            ...
        ]
    """
    weather_list = []
    
    try:
        print("\n正在解析 JSON 資料...")
        
        # 根據實際 CWA API 結構解析資料
        # 路徑：cwaopendata -> resources -> resource -> data -> agrWeatherForecasts -> weatherForecasts -> location[]
        resources = json_data.get('cwaopendata', {}).get('resources', {})
        resource = resources.get('resource', {})
        data = resource.get('data', {})
        agr_weather = data.get('agrWeatherForecasts', {})
        weather_forecasts = agr_weather.get('weatherForecasts', {})
        locations = weather_forecasts.get('location', [])
        
        print(f"找到 {len(locations)} 個地區的資料")
        
        for location in locations:
            location_name = location.get('locationName', '未知地區')
            
            # 獲取天氣元素
            weather_elements = location.get('weatherElements', {})
            
            # 初始化資料（取每日預報的第一天）
            weather_info = {
                'location': location_name,
                'min_temp': None,
                'max_temp': None,
                'description': None
            }
            
            # 提取最低溫度（MinT）
            min_t = weather_elements.get('MinT', {})
            min_t_daily = min_t.get('daily', [])
            if min_t_daily:
                weather_info['min_temp'] = min_t_daily[0].get('temperature')
            
            # 提取最高溫度（MaxT）
            max_t = weather_elements.get('MaxT', {})
            max_t_daily = max_t.get('daily', [])
            if max_t_daily:
                weather_info['max_temp'] = max_t_daily[0].get('temperature')
            
            # 提取天氣描述（Wx）
            wx = weather_elements.get('Wx', {})
            wx_daily = wx.get('daily', [])
            if wx_daily:
                weather_info['description'] = wx_daily[0].get('weather')
            
            # 轉換溫度為浮點數
            if weather_info['min_temp']:
                try:
                    weather_info['min_temp'] = float(weather_info['min_temp'])
                except ValueError:
                    weather_info['min_temp'] = None
                    
            if weather_info['max_temp']:
                try:
                    weather_info['max_temp'] = float(weather_info['max_temp'])
                except ValueError:
                    weather_info['max_temp'] = None
            
            weather_list.append(weather_info)
        
        print(f"✓ 成功解析 {len(weather_list)} 筆天氣資料")
        
        # 顯示前 3 筆資料作為預覽
        if weather_list:
            print("\n資料預覽（前 3 筆）：")
            for i, weather in enumerate(weather_list[:3], 1):
                print(f"{i}. {weather['location']}: "
                      f"溫度 {weather['min_temp']}°C - {weather['max_temp']}°C, "
                      f"{weather['description']}")
        
        return weather_list
        
    except Exception as e:
        print(f"✗ 解析錯誤：{e}")
        return []


# 測試程式碼（當直接執行此檔案時運行）
if __name__ == "__main__":
    print("=" * 60)
    print("中央氣象局天氣資料獲取測試")
    print("=" * 60)
    
    # 測試下載資料
    data = fetch_weather_data()
    
    if data:
        # 測試解析資料
        weather_list = parse_weather_json(data)
        
        if weather_list:
            print(f"\n總共獲取 {len(weather_list)} 個地區的天氣資料")
        else:
            print("\n無法解析資料")
    else:
        print("\n無法下載資料")
    
    print("=" * 60)
