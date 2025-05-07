from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    discord_id = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(80), nullable=True) # 新增顯示名稱欄位
    email = db.Column(db.String(120), unique=True, nullable=True)
    avatar = db.Column(db.String(256), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # 新增管理員標識欄位
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯到用戶的個人檔案與社交連結
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    social_links = db.relationship('SocialLink', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # 關聯到標籤
    tags = db.relationship('Tag', secondary='user_tags', back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_discord_id(cls, discord_id):
        """根據 Discord ID 查詢使用者"""
        return cls.query.filter_by(discord_id=discord_id).first()
    
    @classmethod
    def create_user(cls, username, discord_id, email=None, avatar=None, is_verified=False, is_admin=False, display_name=None): # 新增 display_name 參數
        """創建新使用者"""
        user = cls(
            username=username,
            discord_id=discord_id,
            display_name=display_name, # 設定 display_name
            email=email,
            avatar=avatar,
            is_verified=is_verified,
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def verify_user(self):
        """驗證使用者帳戶"""
        self.is_verified = True
        db.session.commit()
        return self

    @staticmethod
    def init_db(db):
        """初始化資料庫表格"""
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                discord_id TEXT UNIQUE NOT NULL,
                avatar TEXT,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at DATETIME NOT NULL
            )
        ''')
        db.commit()

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    interests = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 新增: 自訂頁面外觀的欄位
    background_gradient = db.Column(db.String(50), nullable=True)  # 儲存選擇的漸層背景名稱或ID
    main_color = db.Column(db.String(20), nullable=True)  # 儲存主要顏色的色碼
    
    def __repr__(self):
        return f'<UserProfile {self.user_id}>'
    
    @classmethod
    def get_or_create(cls, user_id):
        """獲取用戶檔案，如不存在則創建"""
        profile = cls.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = cls(user_id=user_id)
            db.session.add(profile)
            db.session.commit()
        return profile

class SocialLink(db.Model):
    __tablename__ = 'social_links'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icon_class = db.Column(db.String(50), default='fas fa-globe')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SocialLink {self.title} - {self.user_id}>'

# 新增: 成員團隊留言
class UserTestimonial(db.Model):
    """用戶的團隊留言"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(200), nullable=True)  # 限制為200字
    is_visible = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 用戶關聯
    user = db.relationship('User', backref=db.backref('testimonial', uselist=False, cascade='all, delete-orphan'))
    
    @staticmethod
    def get_visible_testimonials():
        """獲取所有可見的留言，用於前台顯示"""
        # 移除了之前對 approved_by 欄位的檢查
        return db.session.query(UserTestimonial, User).\
               join(User, UserTestimonial.user_id == User.id).\
               filter(UserTestimonial.is_visible == True, 
                      UserTestimonial.message != None, 
                      UserTestimonial.message != '').\
               all()

# 新增: 公開頁面的社群媒體連結
class PublicSocialLink(db.Model):
    __tablename__ = 'public_social_links'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    icon_class = db.Column(db.String(50), default='fas fa-globe')
    display_order = db.Column(db.Integer, default=0)  # 用於排序顯示
    is_active = db.Column(db.Boolean, default=True)  # 是否啟用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PublicSocialLink {self.title}>'
    
    @classmethod
    def get_active_links(cls):
        """獲取所有啟用的社群媒體連結，按排序顯示"""
        return cls.query.filter_by(is_active=True).order_by(cls.display_order).all()

# 新增: 公開頁面的導航連結
class NavLink(db.Model):
    __tablename__ = 'nav_links'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)  # 顯示的名稱
    url = db.Column(db.String(255), nullable=False)   # 連結網址
    icon_class = db.Column(db.String(50), default='fas fa-link')  # 圖標
    display_order = db.Column(db.Integer, default=0)  # 用於排序顯示
    is_active = db.Column(db.Boolean, default=True)   # 是否啟用
    open_in_new_tab = db.Column(db.Boolean, default=False)  # 是否在新分頁打開
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<NavLink {self.title}>'
    
    @classmethod
    def get_active_links(cls):
        """獲取所有啟用的導航連結，按排序顯示"""
        return cls.query.filter_by(is_active=True).order_by(cls.display_order).all()

# 標籤和用戶標籤關聯表
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # 標籤名稱
    display_name = db.Column(db.String(50), nullable=False)  # 顯示名稱(可多語言)
    description = db.Column(db.String(255), nullable=True)  # 標籤描述
    icon_class = db.Column(db.String(50), default='fas fa-tag')  # 圖標
    color = db.Column(db.String(20), default='#7983d4')  # 標籤顏色
    display_order = db.Column(db.Integer, default=0)  # 排序
    is_active = db.Column(db.Boolean, default=True)  # 是否啟用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯到用戶
    users = db.relationship('User', secondary='user_tags', back_populates='tags')
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    @classmethod
    def get_active_tags(cls):
        """獲取所有啟用的標籤，按排序顯示"""
        return cls.query.filter_by(is_active=True).order_by(cls.display_order).all()

# 用戶和標籤的多對多關聯
class UserTag(db.Model):
    __tablename__ = 'user_tags'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)