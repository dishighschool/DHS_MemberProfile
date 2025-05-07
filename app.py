import os
from flask import Flask, url_for, session, redirect
from flask_login import LoginManager
from models.user import db, User
from config import Config
import secrets
from markupsafe import Markup

# 設定允許在開發環境中使用 HTTP (僅適用於開發階段)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['FLASK_DEBUG'] = '1'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 確保有一個強密鑰
    if app.config['SECRET_KEY']:
        app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    # 初始化資料庫
    db.init_app(app)
    
    # 初始化登入管理
    login_manager = LoginManager()
    login_manager.init_app(app)
    # 更新登入視圖路徑至新的後台路徑
    login_manager.login_view = 'main.admin_login'
    login_manager.login_message = '請先登入以訪問此頁面'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 添加 nl2br 過濾器以支援換行符顯示
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return s
        return Markup(s.replace('\n', '<br>'))

    with app.app_context():
        # 在這裡導入藍圖以避免循環導入
        from routes.main import main
        from routes.auth import auth_bp
        
        # 註冊藍圖
        app.register_blueprint(main)
        app.register_blueprint(auth_bp)
        
        # 確保資料庫表存在
        db.create_all()
        
        # 為開發階段添加一些調試路由
        if app.debug:
            @app.route('/debug/session')
            def debug_session():
                return dict(session)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print(f"Flask 應用已啟動! 訪問: http://127.0.0.1:5000")
    app.run(debug=True)