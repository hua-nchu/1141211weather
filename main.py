"""
主執行腳本
功能：整合所有模組，完成天氣資料的下載、解析和存儲
"""

from datetime import datetime
from fetch_weather import fetch_weather_data, parse_weather_json
from database import (
    init_database,
    insert_weather_data,
    get_database_stats,
    get_batch_list
)


def generate_batch_id() -> str:
    """
    生成批次 ID
    格式：YYYYMMDD_HHMMSS
    
    Returns:
        str: 批次識別碼
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def main():
    """主執行函數"""
    print("=" * 70)
    print("中央氣象局天氣資料爬蟲系統")
    print("=" * 70)
    
    # 1. 生成批次 ID
    batch_id = generate_batch_id()
    print(f"\n批次 ID: {batch_id}")
    print("-" * 70)
    
    # 2. 初始化資料庫
    print("\n[步驟 1/4] 初始化資料庫...")
    if not init_database():
        print("✗ 資料庫初始化失敗，程式終止")
        return
    
    # 3. 下載資料
    print("\n[步驟 2/4] 下載天氣資料...")
    json_data = fetch_weather_data()
    
    if not json_data:
        print("✗ 資料下載失敗，程式終止")
        return
    
    # 4. 解析資料
    print("\n[步驟 3/4] 解析 JSON 資料...")
    weather_list = parse_weather_json(json_data)
    
    if not weather_list:
        print("✗ 資料解析失敗，程式終止")
        return
    
    # 5. 存入資料庫
    print(f"\n[步驟 4/4] 將資料存入資料庫...")
    inserted_count = insert_weather_data(weather_list, batch_id)
    
    if inserted_count == 0:
        print("✗ 資料存儲失敗")
        return
    
    # 6. 顯示執行摘要
    print("\n" + "=" * 70)
    print("執行摘要")
    print("=" * 70)
    
    stats = get_database_stats()
    batches = get_batch_list()
    
    if stats:
        print(f"\n批次資訊：")
        print(f"  - 批次 ID：{batch_id}")
        print(f"  - 新增資料筆數：{inserted_count}")
        
        print(f"\n資料庫統計：")
        print(f"  - 總資料筆數：{stats['total_records']}")
        print(f"  - 總批次數：{stats['total_batches']}")
        print(f"  - 最早資料時間：{stats['earliest_record']}")
        print(f"  - 最新資料時間：{stats['latest_record']}")
        
        if batches and len(batches) > 1:
            print(f"\n歷史批次：")
            for i, (bid, count, created) in enumerate(batches[:5], 1):
                print(f"  {i}. {bid} ({count} 筆) - {created}")
            if len(batches) > 5:
                print(f"  ... 還有 {len(batches) - 5} 個批次")
    
    print("\n" + "=" * 70)
    print("✓ 資料處理完成！")
    print("\n下一步：")
    print("  執行以下命令啟動 Streamlit 應用查看資料：")
    print("  > streamlit run app.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式被用戶中斷")
    except Exception as e:
        print(f"\n✗ 發生未預期的錯誤：{e}")
        import traceback
        traceback.print_exc()
