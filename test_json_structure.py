"""
測試腳本：檢查 JSON 結構
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

# API 配置
API_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"

# 下載資料
params = {
    'Authorization': API_KEY,
    'downloadType': 'WEB',
    'format': 'JSON'
}

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(API_URL, params=params, timeout=30, verify=False)
data = response.json()

# 保存完整 JSON 以便檢視
with open('weather_response.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON 已保存到 weather_response.json")
print("\nJSON 頂層結構：")
print(json.dumps(list(data.keys()), ensure_ascii=False, indent=2))

# 檢查第一層
if 'cwaopendata' in data:
    print("\ncwaopendata 下的結構：")
    print(json.dumps(list(data['cwaopendata'].keys()), ensure_ascii=False, indent=2))
    
    if 'dataset' in data['cwaopendata']:
        dataset = data['cwaopendata']['dataset']
        print("\ndataset 下的結構：")
        print(json.dumps(list(dataset.keys())[:10], ensure_ascii=False, indent=2))
