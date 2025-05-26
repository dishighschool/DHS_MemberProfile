import os
from flask import Flask, url_for, session, redirect
from flask_login import LoginManager
from models.user import db, User
from config import Config
import secrets
from markupsafe import Markup
from utils.update_avatar import set_auto_update_avatar
from dotenv import load_dotenv

#

def create_app(config_class=Config):
    # Load environment variables from .env file
    load_dotenv()  
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
    
    # Initialize SQLAlchemy database
    db.init_app(app)
    
    # Initialize Flask-Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Set login view to the admin login route
    login_manager.login_view = 'main.admin_login'
    login_manager.login_message = '請先登入以訪問此頁面'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Add nl2br filter to convert newlines to <br> tags
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return s
        return Markup(s.replace('\n', '<br>'))

    with app.app_context():
        # Import blueprints here to avoid circular imports
        from routes.main import main
        from routes.auth import auth_bp
        
        # Register blueprints
        app.register_blueprint(main)
        app.register_blueprint(auth_bp)
        
        # Ensure database tables exist (disabled in production)
        # db.create_all()  # 已部署環境中不應自動創建資料表
          # Add development-only debug routes
        if app.debug:
            @app.route('/debug/session')
            def debug_session():
                return dict(session)
            
    set_auto_update_avatar(app)  # 設定自動更新頭像的排程任務
    return app

# Create a global Flask app instance for use with Gunicorn or development
app = create_app()


if __name__ == '__main__':
    print("Flask 應用已啟動! 訪問: http://0.0.0.0:2005 或 http://<服務器IP>:2005")
    app.run(host='0.0.0.0', debug=False, port=2005)