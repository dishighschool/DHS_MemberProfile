"""
資料庫更新腳本 - 為 user_profiles 表新增缺少的背景漸層和主題色欄位，以及新增留言表
"""

import os
import sqlite3
from flask import Flask
from models.user import db
from config import Config

def add_missing_columns():
    """為 user_profiles 表添加缺少的欄位，並建立留言表"""
    print("開始更新資料庫結構...")
    
    # 獲取資料庫路徑
    app = Flask(__name__)
    app.config.from_object(Config)
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        print(f"錯誤: 找不到資料庫文件: {db_path}")
        return False
    
    # 連接到 SQLite 資料庫
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 檢查 user_profiles 表結構
        print("檢查 user_profiles 表中的欄位...")
        columns_info = cursor.execute('PRAGMA table_info(user_profiles)').fetchall()
        column_names = [column[1] for column in columns_info]
        
        # 檢查缺少的欄位並添加
        columns_to_add = []
        if 'background_gradient' not in column_names:
            columns_to_add.append(('background_gradient', 'TEXT'))
        if 'main_color' not in column_names:
            columns_to_add.append(('main_color', 'TEXT'))
        
        # 檢查 user_testimonials 表是否存在
        print("檢查 user_testimonials 表是否存在...")
        table_exists = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_testimonials'").fetchone()
        
        if not columns_to_add and table_exists:
            print("資料庫結構已經是最新的，無需更新。")
            return True
        
        # 添加缺少的欄位
        for column_name, column_type in columns_to_add:
            print(f"正在添加欄位: {column_name} ({column_type})...")
            cursor.execute(f'ALTER TABLE user_profiles ADD COLUMN {column_name} {column_type}')
        
        # 創建留言表
        if not table_exists:
            print("創建 user_testimonials 表...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_testimonials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    message TEXT,
                    is_visible BOOLEAN DEFAULT 1,
                    approved_by INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (approved_by) REFERENCES users(id)
                )
            ''')
        
        conn.commit()
        print("資料庫更新完成!")
        return True
    
    except sqlite3.Error as e:
        print(f"更新資料庫時發生錯誤: {e}")
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    success = add_missing_columns()
    print("更新" + ("成功" if success else "失敗"))