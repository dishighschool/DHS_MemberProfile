import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_decode
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from models.user import User, db
import requests

# 創建認證藍圖，修改 url_prefix 為後台路徑
auth_bp = Blueprint('auth', __name__, url_prefix='/admin-panel/auth')

# Discord OAuth 設定
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
# 更新回調 URI 以符合新的路徑
DISCORD_REDIRECT_URI = "http://127.0.0.1:5000/admin-panel/auth/discord/callback"
DISCORD_API_ENDPOINT = "https://discord.com/api/v10"
DISCORD_AUTH_URL = f"{DISCORD_API_ENDPOINT}/oauth2/authorize"
DISCORD_TOKEN_URL = f"{DISCORD_API_ENDPOINT}/oauth2/token"

@auth_bp.route('/login')
def login():
    """開始 Discord OAuth 流程"""
    # 清除舊的 OAuth 狀態
    session.pop('discord_token', None)
    session.pop('discord_id', None)
    
    # 生成狀態參數以防止 CSRF
    state = os.urandom(16).hex()
    session['oauth_state'] = state
    
    # 重定向到 Discord 授權頁面
    authorize_url = (
        f"{DISCORD_AUTH_URL}"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify email"
        f"&state={state}"
    )
    
    return redirect(authorize_url)

@auth_bp.route('/discord/callback')
def discord_callback():
    """Discord OAuth 回調處理"""
    error = request.args.get('error')
    if error:
        flash(f"Discord 授權錯誤: {error}", "danger")
        return redirect(url_for('main.index'))
    
    # 驗證狀態，防止 CSRF 攻擊
    state = request.args.get('state')
    stored_state = session.pop('oauth_state', None)
    if not state or stored_state != state:
        flash("驗證狀態不匹配，請重新登入", "danger")
        return redirect(url_for('main.index'))
    
    # 獲取授權碼
    code = request.args.get('code')
    if not code:
        flash("沒有收到授權碼", "danger")
        return redirect(url_for('main.index'))
    
    # 用授權碼換取訪問令牌
    try:
        token_data = exchange_code_for_token(code)
        if not token_data or 'access_token' not in token_data:
            flash("無法獲取訪問令牌", "danger")
            return redirect(url_for('main.index'))
        
        # 儲存令牌到會話
        session['discord_token'] = token_data
        
        # 使用令牌獲取用戶信息
        user_info = get_discord_user(token_data['access_token'])
        if not user_info:
            flash("無法獲取 Discord 用戶信息", "danger")
            return redirect(url_for('main.index'))
        
        # 檢查用戶是否已存在
        discord_id = user_info['id']
        user = User.get_by_discord_id(discord_id)
        
        if user:
            # 已存在用戶，檢查是否被停用
            if not user.is_verified:
                flash("您的帳戶已被停用，無法登入。如有疑問請聯繫管理員。", "danger")
                return redirect(url_for('main.index'))
            
            # 用戶存在且未被停用，直接登入
            login_user(user)
            flash(f"歡迎回來，{user.username}！", "success")
            
            # --- MODIFIED Redirect Logic --- 
            # 檢查是否有 'next' 參數，用於重定向到用戶原本想訪問的頁面
            next_page = request.args.get('next')
            # 安全性檢查：確保 next_page 是相對路徑或指向同一個主機
            # (這裡僅做基本檢查，更完善的檢查可能需要 urlparse)
            if next_page and not next_page.startswith(('http://', 'https://', '//')):
                return redirect(next_page)
            else:
                # 否則重定向到儀表板
                return redirect(url_for("main.dashboard"))
        else:
            # 新用戶，儲存 Discord 資訊到 session 並跳轉到驗證頁面
            session["discord_id"] = discord_id
            session["username"] = user_info["username"]
            session["email"] = user_info.get("email")
            avatar = None
            if user_info.get('avatar'):
                avatar = f"https://cdn.discordapp.com/avatars/{discord_id}/{user_info.get('avatar')}.png"
            session["avatar"] = avatar
            return redirect(url_for("main.verify"))
            
    except Exception as e:
        flash(f"處理 Discord 登入時發生錯誤: {str(e)}", "danger")
        print(f"Discord OAuth 錯誤: {type(e).__name__}: {str(e)}")
        return redirect(url_for('main.index'))

@auth_bp.route('/logout')
def logout():
    """登出用戶"""
    logout_user()
    
    # 清除 Discord 相關 session 數據
    session.pop('discord_token', None)
    session.pop('discord_id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('avatar', None)
    
    flash("您已成功登出", "info")
    return redirect(url_for('main.index'))

# 實用函數
def exchange_code_for_token(code):
    """使用授權碼換取訪問令牌"""
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        DISCORD_TOKEN_URL,
        data=data,
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Token 交換失敗: {response.status_code}")
        print(f"響應: {response.text}")
        return None

def get_discord_user(token):
    """使用訪問令牌獲取 Discord 用戶信息"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(
        f"{DISCORD_API_ENDPOINT}/users/@me",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"獲取用戶信息失敗: {response.status_code}")
        print(f"響應: {response.text}")
        return None

# 為舊路徑設置重定向
@auth_bp.route('/auth/login')
def redirect_login():
    """重定向舊的登入路徑"""
    return redirect(url_for("auth.login"))

@auth_bp.route('/auth/logout')
def redirect_logout():
    """重定向舊的登出路徑"""
    return redirect(url_for("auth.logout"))

@auth_bp.route('/auth/discord/callback')
def redirect_callback():
    """重定向舊的回調路徑"""
    return redirect(url_for("auth.discord_callback"))