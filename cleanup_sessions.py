#!/usr/bin/env python3
"""
Session 清理腳本
用於定期清理過期的 session 檔案，防止 flask_session 目錄無限增長

使用方法：
1. 手動執行: python cleanup_sessions.py
2. Cron 定期執行: 0 3 * * * cd /path/to/app && python cleanup_sessions.py
"""

import os
import time
from pathlib import Path

# 配置
SESSION_DIR = "flask_session"
MAX_AGE_DAYS = 7  # 保留最近 7 天的 session
MAX_AGE_SECONDS = MAX_AGE_DAYS * 86400

def cleanup_old_sessions():
    """清理舊的 session 檔案"""
    if not os.path.exists(SESSION_DIR):
        print(f"⚠️  Session 目錄不存在: {SESSION_DIR}")
        return
    
    now = time.time()
    deleted_count = 0
    total_size = 0
    
    print(f"🧹 開始清理 {SESSION_DIR} 目錄...")
    print(f"📅 刪除超過 {MAX_AGE_DAYS} 天的檔案")
    
    for file in Path(SESSION_DIR).glob('*'):
        if file.is_file():
            file_age = now - file.stat().st_mtime
            file_size = file.stat().st_size
            
            if file_age > MAX_AGE_SECONDS:
                total_size += file_size
                file.unlink()
                deleted_count += 1
                print(f"  ✓ 刪除: {file.name} (年齡: {file_age / 86400:.1f} 天)")
    
    print(f"\n✅ 清理完成:")
    print(f"   - 刪除檔案數: {deleted_count}")
    print(f"   - 釋放空間: {total_size / 1024:.2f} KB")
    
    # 顯示剩餘檔案
    remaining = len(list(Path(SESSION_DIR).glob('*')))
    print(f"   - 剩餘 session: {remaining}")

if __name__ == '__main__':
    try:
        cleanup_old_sessions()
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        exit(1)
