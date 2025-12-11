"""
SQLite 資料庫操作模組
功能：初始化資料庫、插入和查詢天氣資料
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime


DATABASE_NAME = "data.db"


def get_connection() -> sqlite3.Connection:
    """獲取資料庫連接"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # 使結果可以像字典一樣訪問
    return conn


def init_database() -> bool:
    """
    初始化資料庫，創建 weather 資料表
    
    Returns:
        bool: 成功返回 True，失敗返回 False
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 創建 weather 資料表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                location TEXT NOT NULL,
                min_temp REAL,
                max_temp REAL,
                description TEXT,
                fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✓ 資料庫初始化成功")
        return True
        
    except sqlite3.Error as e:
        print(f"✗ 資料庫初始化失敗：{e}")
        return False


def insert_weather_data(data_list: List[Dict], batch_id: str) -> int:
    """
    批量插入天氣資料（保留歷史資料，不刪除舊資料）
    
    Args:
        data_list: 天氣資料列表
        batch_id: 批次識別碼
        
    Returns:
        int: 成功插入的資料筆數
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        inserted_count = 0
        
        for weather in data_list:
            cursor.execute("""
                INSERT INTO weather (batch_id, location, min_temp, max_temp, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                batch_id,
                weather.get('location'),
                weather.get('min_temp'),
                weather.get('max_temp'),
                weather.get('description')
            ))
            inserted_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✓ 成功插入 {inserted_count} 筆資料（批次 ID: {batch_id}）")
        return inserted_count
        
    except sqlite3.Error as e:
        print(f"✗ 資料插入失敗：{e}")
        return 0


def get_latest_weather() -> List[Dict]:
    """
    查詢最新一批天氣資料
    
    Returns:
        List[Dict]: 最新批次的天氣資料
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 先找出最新的 batch_id
        cursor.execute("""
            SELECT batch_id
            FROM weather
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return []
        
        latest_batch_id = result['batch_id']
        
        # 查詢該批次的所有資料
        cursor.execute("""
            SELECT id, batch_id, location, min_temp, max_temp, description, 
                   fetch_time, created_at
            FROM weather
            WHERE batch_id = ?
            ORDER BY location
        """, (latest_batch_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # 轉換為字典列表
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"✗ 查詢失敗：{e}")
        return []


def get_all_weather() -> List[Dict]:
    """
    查詢所有歷史天氣資料
    
    Returns:
        List[Dict]: 所有天氣資料
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, batch_id, location, min_temp, max_temp, description,
                   fetch_time, created_at
            FROM weather
            ORDER BY created_at DESC, location
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"✗ 查詢失敗：{e}")
        return []


def get_weather_by_batch(batch_id: str) -> List[Dict]:
    """
    查詢特定批次的天氣資料
    
    Args:
        batch_id: 批次識別碼
        
    Returns:
        List[Dict]: 該批次的天氣資料
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, batch_id, location, min_temp, max_temp, description,
                   fetch_time, created_at
            FROM weather
            WHERE batch_id = ?
            ORDER BY location
        """, (batch_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"✗ 查詢失敗：{e}")
        return []


def get_batch_list() -> List[Tuple[str, int, str]]:
    """
    查詢所有批次列表
    
    Returns:
        List[Tuple]: [(batch_id, count, created_at), ...]
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT batch_id, COUNT(*) as count, MIN(created_at) as created_at
            FROM weather
            GROUP BY batch_id
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [(row['batch_id'], row['count'], row['created_at']) for row in rows]
        
    except sqlite3.Error as e:
        print(f"✗ 查詢失敗：{e}")
        return []


def get_database_stats() -> Dict:
    """
    獲取資料庫統計資訊
    
    Returns:
        Dict: 統計資訊
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 總資料筆數
        cursor.execute("SELECT COUNT(*) as total FROM weather")
        total = cursor.fetchone()['total']
        
        # 批次數量
        cursor.execute("SELECT COUNT(DISTINCT batch_id) as batch_count FROM weather")
        batch_count = cursor.fetchone()['batch_count']
        
        # 最早資料時間
        cursor.execute("SELECT MIN(created_at) as earliest FROM weather")
        earliest = cursor.fetchone()['earliest']
        
        # 最新資料時間
        cursor.execute("SELECT MAX(created_at) as latest FROM weather")
        latest = cursor.fetchone()['latest']
        
        conn.close()
        
        return {
            'total_records': total,
            'total_batches': batch_count,
            'earliest_record': earliest,
            'latest_record': latest
        }
        
    except sqlite3.Error as e:
        print(f"✗ 統計查詢失敗：{e}")
        return {}


# 測試程式碼
if __name__ == "__main__":
    print("=" * 60)
    print("資料庫操作模組測試")
    print("=" * 60)
    
    # 初始化資料庫
    if init_database():
        # 獲取統計資訊
        stats = get_database_stats()
        if stats:
            print(f"\n資料庫統計：")
            print(f"  總資料筆數：{stats['total_records']}")
            print(f"  總批次數：{stats['total_batches']}")
            print(f"  最早資料：{stats['earliest_record']}")
            print(f"  最新資料：{stats['latest_record']}")
        
        # 查詢批次列表
        batches = get_batch_list()
        if batches:
            print(f"\n批次列表：")
            for batch_id, count, created_at in batches:
                print(f"  - {batch_id}: {count} 筆資料 ({created_at})")
    
    print("=" * 60)
