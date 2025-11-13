"""
數據庫遷移腳本：添加 Discord Bot 集成支持

此腳本用於直接在現有數據庫中創建 Discord Bot 相關的表
運行方式：python migrations/add_discord_tables.py
"""

import os
import sys

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.user import db, DiscordConfig, RoleTagMapping

def create_discord_tables():
    """創建 Discord Bot 相關的數據表"""
    app = create_app()
    
    with app.app_context():
        # 檢查表是否已存在
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print("開始創建 Discord Bot 相關數據表...")
        
        # 創建 discord_config 表
        if 'discord_config' not in existing_tables:
            print("創建 discord_config 表...")
            with db.engine.connect() as conn:
                conn.execute(db.text('''
                    CREATE TABLE IF NOT EXISTS discord_config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bot_token VARCHAR(255) NOT NULL,
                        guild_id VARCHAR(128),
                        guild_name VARCHAR(128),
                        is_active BOOLEAN DEFAULT 1,
                        auto_sync_on_register BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                '''))
                conn.commit()
            print("✓ discord_config 表已創建")
        else:
            print("discord_config 表已存在，跳過")
        
        # 創建 role_tag_mapping 表
        if 'role_tag_mapping' not in existing_tables:
            print("創建 role_tag_mapping 表...")
            with db.engine.connect() as conn:
                conn.execute(db.text('''
                    CREATE TABLE IF NOT EXISTS role_tag_mapping (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        discord_config_id INTEGER NOT NULL,
                        role_id VARCHAR(128) NOT NULL,
                        role_name VARCHAR(128) NOT NULL,
                        tag_id INTEGER NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (discord_config_id) REFERENCES discord_config (id),
                        FOREIGN KEY (tag_id) REFERENCES tags (id)
                    )
                '''))
                conn.commit()
            print("✓ role_tag_mapping 表已創建")
        else:
            print("role_tag_mapping 表已存在，跳過")
        
        db.session.commit()
        print("\n數據庫遷移完成！")
        print("Discord Bot 功能已成功集成到系統中。")

if __name__ == '__main__':
    try:
        create_discord_tables()
    except Exception as e:
        print(f"\n❌ 遷移失敗：{str(e)}")
        import traceback
        traceback.print_exc()
