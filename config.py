import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Session 配置 - 使用檔案系統存儲以支援多 worker (Gunicorn)
    # 這是解決生產環境多 worker 下 session 失效問題的關鍵配置
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True  # 簽名 session 數據，防止篡改
    SESSION_KEY_PREFIX = 'dhs_session:'
    PERMANENT_SESSION_LIFETIME = 86400  # 24小時 (單位: 秒)
    
    # Cookie 安全性配置
    # 生產環境使用 HTTPS 時應設置 SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True  # 防止 JavaScript 訪問 cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF 保護
    SESSION_COOKIE_NAME = 'dhs_session'
    
    # Discord OAuth2 配置
    DISCORD_OAUTH_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
    DISCORD_OAUTH_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
    
    # 從 JSON 檔案載入金鑰
    @classmethod
    def load_keys(cls):
        keys_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'keys.json')
        try:
            if os.path.exists(keys_path):
                with open(keys_path, 'r', encoding='utf-8') as f:
                    keys_data = json.load(f)
                    cls.TEAM_KEY = keys_data.get('TEAM_KEY', 'default_team_key')
                    cls.ADMIN_REGISTRATION_CODE = keys_data.get('ADMIN_REGISTRATION_CODE', 'default_admin_code')
            else:
                # 如果 JSON 檔案不存在，使用預設值
                raise BaseException(f"找不到金鑰檔案: {keys_path}")
        except Exception as e:
            raise BaseException(f"載入金鑰時出錯: {str(e)}")

# 載入金鑰
Config.load_keys()