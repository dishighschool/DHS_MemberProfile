import os
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User, UserProfile, SocialLink, PublicSocialLink, NavLink, Tag, UserTag, UserTestimonial, db
from functools import wraps
from datetime import datetime, timedelta
import secrets
from sqlalchemy import or_

main = Blueprint('main', __name__)

# Decorator to check for admin privileges
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# === 前台路由區域 ===

@main.route('/')
def index():
    """公開首頁 - 顯示所有活躍成員列表及其資料"""
    # 查詢所有活躍成員並加載其個人資料
    users = User.query.filter_by(is_verified=True).all()
    
    # 獲取活躍的社群媒體連結和導航連結
    public_social_links = PublicSocialLink.get_active_links()
    nav_links = NavLink.get_active_links()
    
    # 獲取所有活躍的標籤，用於前端篩選
    active_tags = Tag.get_active_tags()
    
    # 獲取可見的用戶留言，用於輪播展示
    testimonials = UserTestimonial.get_visible_testimonials()
    
    # 為每個用戶加載個人資料並確保每個用戶都有可用資料
    active_users = []
    for user in users:
        profile = UserProfile.query.filter_by(user_id=user.id).first()
        # 如果用戶沒有個人資料，創建一個空的資料
        if not profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()
        user.profile = profile
        active_users.append(user)
    
    return render_template('public_home.html', 
                          title='成員列表', 
                          users=active_users,
                          tags=active_tags,
                          testimonials=testimonials,
                          public_social_links=public_social_links, 
                          nav_links=nav_links,
                          now=datetime.now())

@main.route('/user/<username>')
def public_profile(username):
    """使用者公開檔案頁面"""
    # Query without first_or_404 to handle both cases
    user = User.query.filter_by(username=username).first()
    
    # Check if user exists and is verified (not deactivated)
    if not user or not user.is_verified:
        return render_template('public_error.html', 
                               error_title="找不到該成員", 
                               error_message=f"無法找到成員 {username} 的個人頁面，該頁面可能不存在或已被停用。",
                               now=datetime.now())
    
    # User exists and is verified, proceed to show profile
    profile = UserProfile.query.filter_by(user_id=user.id).first()
    social_links = SocialLink.query.filter_by(user_id=user.id).all()
    
    # 獲取活躍的社群媒體連結和導航連結
    public_social_links = PublicSocialLink.get_active_links()
    nav_links = NavLink.get_active_links()
    
    return render_template('public_profile.html', 
                          title=f'{user.display_name or user.username} 的個人頁面', # Use display_name
                          user=user, 
                          profile=profile, 
                          social_links=social_links,
                          public_social_links=public_social_links,
                          nav_links=nav_links,
                          now=datetime.now())

# === 後台路由區域 ===

@main.route('/admin-panel')
@login_required
def admin_home():
    """後台首頁"""
    # 獲取用戶統計
    total_users = User.query.filter(User.is_admin == False).count()
    verified_users = User.query.filter(User.is_admin == False, User.is_verified == True).count()
    unverified_users = total_users - verified_users
    
    # 獲取最近加入的用戶（最多5個）
    recent_users = User.query.filter(User.is_admin == False).order_by(User.created_at.desc()).limit(5).all()
    
    # 獲取標籤統計
    tags = Tag.query.all()
    tag_stats = []
    for tag in tags:
        user_count = db.session.query(UserTag).filter(UserTag.tag_id == tag.id).count()
        tag_stats.append({
            'name': tag.display_name,
            'count': user_count,
            'color': tag.color,
            'icon': tag.icon_class
        })
    
    # 獲取系統最近留言
    recent_testimonials = db.session.query(UserTestimonial, User).\
        join(User, UserTestimonial.user_id == User.id).\
        filter(UserTestimonial.message != None, UserTestimonial.message != '').\
        order_by(UserTestimonial.updated_at.desc()).limit(3).all()
    
    # 獲取管理員列表
    admins = User.query.filter_by(is_admin=True).all()
    admin_count = len(admins)
    
    return render_template('home.html', 
                          title='個人介紹頁面管理', 
                          now=datetime.now(),
                          total_users=total_users,
                          verified_users=verified_users,
                          unverified_users=unverified_users,
                          recent_users=recent_users,
                          tag_stats=tag_stats,
                          recent_testimonials=recent_testimonials,
                          admins=admins,
                          admin_count=admin_count,
                          is_admin=True)

@main.route('/admin-panel/login')
def admin_login():
    """管理後台登入頁面 - 重定向到 Discord 認證"""
    return redirect(url_for("auth.login"))

@main.route('/admin-panel/verify', methods=['GET', 'POST'])
def verify():
    """團隊金鑰驗證頁面"""
    if current_user.is_authenticated and current_user.is_verified:
        return redirect(url_for("main.dashboard"))
    
    # 確認是否有 Discord 賊
    if not session.get("discord_id"):
        return redirect(url_for("auth.login"))
    
    if request.method == 'POST':
        submitted_key = request.form.get('team_key') # Renamed variable for clarity
        is_admin_signup = False

        if submitted_key == current_app.config['ADMIN_REGISTRATION_CODE']:
            is_admin_signup = True
        elif submitted_key != current_app.config['TEAM_KEY']:
            flash("團隊金鑰或管理員代碼不正確，請重試", "danger")
            return render_template('verify.html', title='團隊驗證', username=session.get("username"), avatar=session.get("avatar"), now=datetime.now()) # Pass avatar

        # 金鑰正確 (either team or admin)
        user = User.create_user(
            username=session["username"],
            discord_id=session["discord_id"],
            email=session.get("email"),
            avatar=session.get("avatar"),
            is_verified=True,
            is_admin=is_admin_signup # Set admin status based on key
        )
        login_user(user)
        
        # 清除 session 中的暫存資訊
        for key in ["discord_id", "username", "email", "avatar"]:
            session.pop(key, None)
            
        flash("驗證成功！歡迎加入 DisHighSchool！", "success")
        if is_admin_signup:
             flash("您已成功註冊為管理員。", "info")
        return redirect(url_for("main.welcome"))
    
    # Pass avatar to GET request as well
    return render_template('verify.html', title='團隊驗證', username=session.get("username"), avatar=session.get("avatar"), now=datetime.now())

# 歡迎頁面
@main.route('/admin-panel/welcome')
@login_required
def welcome():
    """新用戶歡迎頁面"""
    if not current_user.is_verified:
        return redirect(url_for("main.verify"))
    
    return render_template('welcome.html', title='歡迎加入', user=current_user, now=datetime.now())

# 使用者儀表板
@main.route('/admin-panel/dashboard', methods=['GET'])
@login_required
def dashboard():
    """用戶儀表板 - 顯示個人資料和社交連結"""
    # Check if user is verified (active)
    if not current_user.is_verified:
        flash("您的帳戶已被停用，無法存取此頁面。", "warning")
        logout_user() # Log out the deactivated user
        return redirect(url_for("main.index"))
    
    # GET Request: 獲取用戶的社交媒體連結並渲染頁面
    profile = UserProfile.get_or_create(current_user.id)
    social_links = SocialLink.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', 
                          title='個人介面',
                          user=current_user, 
                          profile=profile, 
                          social_links=social_links,
                          now=datetime.now())

# 使用者留言設定頁面
@main.route('/admin-panel/user-testimonial', methods=['GET', 'POST'])
@login_required
def user_testimonial():
    """使用者留言設定頁面 - 讓使用者可以設定自己的團隊留言"""
    # 確認用戶已驗證
    if not current_user.is_verified:
        flash("您的帳戶已被停用，無法存取此頁面。", "warning")
        logout_user() # 登出已停用的用戶
        return redirect(url_for("main.index"))
    
    # 獲取用戶現有的留言
    testimonial = UserTestimonial.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        is_visible = 'is_visible' in request.form
        
        if not testimonial:
            testimonial = UserTestimonial(user_id=current_user.id)
            db.session.add(testimonial)
        
        testimonial.message = message
        testimonial.is_visible = is_visible
        
        try:
            db.session.commit()
            flash('您的團隊留言已更新，將顯示在公開頁面。', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'儲存留言時發生錯誤: {str(e)}', 'danger')
    
    # 如果是 GET 請求或儲存失敗，渲染留言編輯頁面
    return render_template('user_testimonial.html',
                          title='設定團隊留言',
                          user=current_user,
                          testimonial=testimonial,
                          now=datetime.now())

# === API區域 - 保持在後台路由下 ===
# 統一的資料儲存 API
@main.route('/admin-panel/api/save-profile', methods=['POST'])
@login_required
def save_profile():
    """統一的資料儲存 API - 處理所有用戶資料更新"""
    # Check if user is verified (active)
    if not current_user.is_verified:
        return jsonify({'success': False, 'message': '您的帳戶已被停用，無法儲存變更。'}), 403

    try:
        data = request.form

        # --- Start Transaction ---
        # 0. 更新用戶顯示名稱
        display_name = data.get('displayName', '').strip()
        current_user.display_name = display_name if display_name else None

        # 1. 更新個人資料
        profile = UserProfile.get_or_create(current_user.id)
        profile.title = data.get('profileTitle', '').strip()
        profile.bio = data.get('profileBio', '').strip()
        profile.interests = data.get('profile_interests', '').strip()
        
        # 新增: 更新頁面自定義外觀設定
        profile.background_gradient = data.get('background_gradient', '').strip()
        profile.main_color = data.get('main_color', '').strip()

        # 2. 更新社交媒體連結
        SocialLink.query.filter_by(user_id=current_user.id).delete()
        titles = data.getlist('social_titles[]')
        urls = data.getlist('social_urls[]')
        icons = data.getlist('social_icons[]')

        for i in range(min(len(titles), len(urls))):
            title = titles[i].strip() if i < len(titles) else ''
            url = urls[i].strip() if i < len(urls) else ''
            icon = icons[i] if i < len(icons) and icons[i] else 'fas fa-globe'

            if title and url:
                link = SocialLink(
                    user_id=current_user.id,
                    title=title,
                    url=url,
                    icon_class=icon
                )
                db.session.add(link)
        
        # 3. 新增：更新用戶留言
        testimonial_message = data.get('testimonial_message', '').strip()
        testimonial_visible = 'testimonial_visible' in data
        
        testimonial = UserTestimonial.query.filter_by(user_id=current_user.id).first()
        if not testimonial:
            testimonial = UserTestimonial(user_id=current_user.id)
            db.session.add(testimonial)
        
        testimonial.message = testimonial_message
        testimonial.is_visible = testimonial_visible
        
        # Commit all changes
        db.session.commit()
        # --- End Transaction ---
        
        return jsonify({
            'success': True, 
            'message': '個人資料已成功更新'
        })
        
    except Exception as e:
        db.session.rollback() # Rollback in case of error
        print(f"Error saving profile data: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'更新失敗: {str(e)}'
        }), 500

# 獲取個人資料資料 API
@main.route('/admin-panel/api/get-profile-data', methods=['GET'])
@login_required
def get_profile_data():
    # 獲取當前登入的用戶資料
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    social_links = SocialLink.query.filter_by(user_id=current_user.id).order_by(SocialLink.id).all()
    testimonial = UserTestimonial.query.filter_by(user_id=current_user.id).first()
    
    # 轉換為字典格式
    profile_data = {}
    if profile:
        profile_data = {
            'title': profile.title,
            'bio': profile.bio,
            'interests': profile.interests,
            'background_gradient': profile.background_gradient,
            'main_color': profile.main_color
        }
    
    # 轉換社交連結
    social_links_data = []
    for link in social_links:
        social_links_data.append({
            'title': link.title,
            'url': link.url,
            'icon_class': link.icon_class
        })
    
    # 添加留言數據
    testimonial_data = {}
    if testimonial:
        testimonial_data = {
            'message': testimonial.message,
            'is_visible': testimonial.is_visible
        }
    
    return jsonify({
        'success': True,
        'user': {
            'username': current_user.username,
            'display_name': current_user.display_name
        },
        'profile': profile_data,
        'social_links': social_links_data,
        'testimonial': testimonial_data
    })

# 個人檔案預覽
@main.route('/admin-panel/preview/profile')
@login_required
def profile_preview():
    """個人檔案預覽頁面 - 用於 iframe 內嵌顯示"""
    # Check if user is verified (active)
    if not current_user.is_verified:
        # Render a simple message within the iframe
        return "<p>您的帳戶已被停用，無法預覽。</p>", 403
    
    # 獲取用戶檔案資料
    profile = UserProfile.get_or_create(current_user.id)
    social_links = SocialLink.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile_preview.html', 
                          user=current_user, 
                          profile=profile, 
                          social_links=social_links,
                          is_preview=True,
                          now=datetime.now())

# 後台登出
@main.route('/admin-panel/logout')
@login_required
def admin_logout():
    """登出"""
    return redirect(url_for("auth.logout"))

# 錯誤頁面
@main.route('/error')
def error():
    return render_template('error.html', now=datetime.now())

# === 管理員區域 ===

@main.route('/admin-panel/admin/manage-admins', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_manage_admins():
    """管理員管理頁面，顯示所有管理員和管理功能"""
    # 處理 POST 請求 - 新增管理員
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('請輸入用戶名稱或電子郵件', 'danger')
            return redirect(url_for('main.admin_manage_admins'))
        
        # 查找用戶 (根據用戶名或電子郵件)
        user = User.query.filter(
            or_(
                User.username == username,
                User.email == username
            )
        ).first()
        
        if not user:
            flash(f'找不到用戶: {username}', 'danger')
            return redirect(url_for('main.admin_manage_admins'))
        
        # 確認用戶尚未是管理員
        if user.is_admin:
            flash(f'用戶 {user.display_name or user.username} 已經是管理員', 'info')
            return redirect(url_for('main.admin_manage_admins'))
        
        # 將用戶設為管理員
        user.is_admin = True
        try:
            db.session.commit()
            flash(f'已成功將 {user.display_name or user.username} 設為管理員', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'設置管理員失敗: {str(e)}', 'danger')
        
        return redirect(url_for('main.admin_manage_admins'))
    
    # GET 請求處理邏輯
    search_query = request.args.get('search', '').strip()
    
    # 基本查詢: 查找所有管理員
    query = User.query.filter(User.is_admin == True)
    
    # 如果有搜索條件，應用過濾
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                User.username.ilike(search_term),
                User.display_name.ilike(search_term),
                User.email.ilike(search_term)
            )
        )
    
    # 獲取管理員列表
    admins = query.order_by(User.created_at.desc()).all()
    
    # 獲取統計信息
    total_admins = User.query.filter_by(is_admin=True).count()
    active_admins = total_admins  # 由於沒有 last_login 欄位，所以暫時設為所有管理員數量
    
    # 計算最近30天新增的管理員
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_admins = User.query.filter_by(is_admin=True).filter(User.created_at >= thirty_days_ago).count()
    
    # 獲取總用戶數（非管理員）
    total_users = User.query.filter_by(is_admin=False).count()
    
    return render_template('admin_manage_admins.html',
                           title='管理員設定',
                           admins=admins,
                           total_admins=total_admins,
                           active_admins=active_admins,
                           new_admins=new_admins,
                           total_users=total_users,
                           search_query=search_query,
                           now=datetime.now())

@main.route('/admin-panel/admin/edit-admin/<int:admin_id>')
@login_required
@admin_required
def admin_edit_admin(admin_id):
    """管理員編輯其他管理員頁面"""
    admin = User.query.filter_by(id=admin_id, is_admin=True).first_or_404()
    
    return render_template('admin_edit_admin.html',
                          title=f'編輯管理員 - {admin.username}',
                          admin=admin,
                          now=datetime.now())

@main.route('/admin-panel/admin/remove-admin-role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_remove_admin_role(user_id):
    """移除管理員權限"""
    if current_user.id == user_id:
        flash("您不能移除自己的管理員權限！", "danger")
        return redirect(url_for('main.admin_manage_admins'))
    
    user = User.query.get_or_404(user_id)
    username = user.username
    
    if not user.is_admin:
        flash(f"用戶 {username} 不是管理員", "warning")
        return redirect(url_for('main.admin_manage_admins'))
    
    user.is_admin = False
    db.session.commit()
    
    flash(f"已成功移除 {username} 的管理員權限", "success")
    return redirect(url_for('main.admin_manage_admins'))

@main.route('/admin-panel/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """管理員儀表板頁面"""
    # 獲取用戶統計
    total_users = User.query.filter(User.is_admin == False).count()
    verified_users = User.query.filter(User.is_admin == False, User.is_verified == True).count()
    unverified_users = total_users - verified_users
    
    # 獲取最近加入的用戶（最多5個）
    recent_users = User.query.filter(User.is_admin == False).order_by(User.created_at.desc()).limit(5).all()
    
    # 獲取標籤統計
    tags = Tag.query.all()
    tag_stats = []
    for tag in tags:
        user_count = db.session.query(UserTag).filter(UserTag.tag_id == tag.id).count()
        tag_stats.append({
            'name': tag.display_name,
            'count': user_count,
            'color': tag.color,
            'icon': tag.icon_class
        })
    
    # 獲取系統最近留言
    recent_testimonials = db.session.query(UserTestimonial, User).\
        join(User, UserTestimonial.user_id == User.id).\
        filter(UserTestimonial.message != None, UserTestimonial.message != '').\
        order_by(UserTestimonial.updated_at.desc()).limit(3).all()
    
    # 獲取管理員列表
    admins = User.query.filter_by(is_admin=True).all()
    admin_count = len(admins)
    
    return render_template('admin_dashboard.html', 
                          title='管理員儀表板',
                          total_users=total_users,
                          verified_users=verified_users,
                          unverified_users=unverified_users,
                          recent_users=recent_users,
                          tag_stats=tag_stats, 
                          recent_testimonials=recent_testimonials,
                          admins=admins,
                          admin_count=admin_count,
                          now=datetime.now())

@main.route('/admin-panel/admin/update-admin/<int:admin_id>', methods=['POST'])
@login_required
@admin_required
def admin_update_admin(admin_id):
    """更新管理員資訊"""
    admin_to_edit = User.query.filter_by(id=admin_id, is_admin=True).first_or_404()
    
    # 確保管理員不能移除自己的管理員權限
    if admin_to_edit.id == current_user.id:
        if not 'is_admin' in request.form:
            flash("您不能移除自己的管理員權限！", "danger")
            return redirect(url_for('main.admin_edit_admin', admin_id=admin_id))
    
    # 更新管理員資訊
    admin_to_edit.display_name = request.form.get('display_name', '').strip() or None
    admin_to_edit.email = request.form.get('email', '').strip() or None
    
    # 檢查是否更新密碼
    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    
    if new_password:
        if new_password == confirm_password:
            admin_to_edit.password = new_password  # 密碼哈希在模型中處理
            flash("密碼已成功更新", "success")
        else:
            flash("新密碼與確認密碼不符，密碼未更新", "danger")
            return redirect(url_for('main.admin_edit_admin', admin_id=admin_id))
    
    # 如果不是編輯自己，可以更改管理員權限
    if admin_to_edit.id != current_user.id:
        is_admin = 'is_admin' in request.form
        admin_to_edit.is_admin = is_admin
        
        # 如果取消管理員權限，重定向到用戶管理
        if not is_admin:
            db.session.commit()
            flash(f"已移除 {admin_to_edit.username} 的管理員權限", "success")
            return redirect(url_for('main.admin_manage_admins'))
    
    # 儲存變更
    try:
        db.session.commit()
        flash("管理員資訊已更新", "success")
        return redirect(url_for('main.admin_manage_admins'))
    except Exception as e:
        db.session.rollback()
        flash(f"更新失敗: {str(e)}", "danger")
        return redirect(url_for('main.admin_edit_admin', admin_id=admin_id))

# === 管理員公開頁面設定區域 ===
@main.route('/admin-panel/admin/public-settings')
@login_required
@admin_required
def admin_public_settings():
    """管理員公開頁面設定入口"""
    return render_template('admin_public_settings.html', title='公開頁面設定', now=datetime.now())

@main.route('/admin-panel/admin/manage-social-links', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_manage_social_links():
    """管理公開首頁的社群媒體連結"""
    social_links = PublicSocialLink.query.order_by(PublicSocialLink.display_order).all()
    
    if request.method == 'POST':
        # 如果是刪除操作
        if 'delete' in request.form:
            link_id = request.form.get('delete')
            link_to_delete = PublicSocialLink.query.get_or_404(link_id)
            db.session.delete(link_to_delete)
            db.session.commit()
            flash('社群媒體連結已刪除', 'success')
            return redirect(url_for('main.admin_manage_social_links'))
        
        # 如果是新增或更新操作
        link_id = request.form.get('link_id')
        title = request.form.get('title')
        url = request.form.get('url')
        icon_class = request.form.get('icon_class')
        is_active = 'is_active' in request.form
        display_order = request.form.get('display_order', 0)
        
        # 驗證輸入
        if not title and not url:
            flash('標題和網址不能為空', 'danger')
            return redirect(url_for('main.admin_manage_social_links'))
        
        if link_id:  # 更新現有連結
            link = PublicSocialLink.query.get_or_404(link_id)
            link.title = title
            link.url = url
            link.icon_class = icon_class
            link.is_active = is_active
            link.display_order = display_order
            flash('社群媒體連結已更新', 'success')
        else:  # 新增連結
            link = PublicSocialLink(
                title=title,
                url=url,
                icon_class=icon_class,
                is_active=is_active,
                display_order=display_order
            )
            db.session.add(link)
            flash('社群媒體連結已新增', 'success')
        
        db.session.commit()
        return redirect(url_for('main.admin_manage_social_links'))
        
    return render_template('admin_social_links.html', 
                          title='管理社群媒體連結',
                          social_links=social_links,
                          now=datetime.now())

@main.route('/admin-panel/admin/manage-nav-links', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_manage_nav_links():
    """管理公開頁面的導航連結"""
    nav_links = NavLink.query.order_by(NavLink.display_order).all()
    
    if request.method == 'POST':
        # 如果是刪除操作
        if 'delete' in request.form:
            link_id = request.form.get('delete')
            link_to_delete = NavLink.query.get_or_404(link_id)
            db.session.delete(link_to_delete)
            db.session.commit()
            flash('導航連結已刪除', 'success')
            return redirect(url_for('main.admin_manage_nav_links'))
        
        # 如果是新增或更新操作
        link_id = request.form.get('link_id')
        title = request.form.get('title')
        url = request.form.get('url')
        icon_class = request.form.get('icon_class')
        is_active = 'is_active' in request.form
        open_in_new_tab = 'open_in_new_tab' in request.form
        display_order = request.form.get('display_order', 0)
        
        # 驗證輸入 - 修復中文「或」為英文 or
        if not title or not url:
            flash('標題和網址不能為空', 'danger')
            return redirect(url_for('main.admin_manage_nav_links'))
        
        if link_id:  # 更新現有連結
            link = NavLink.query.get_or_404(link_id)
            link.title = title
            link.url = url
            link.icon_class = icon_class
            link.is_active = is_active
            link.open_in_new_tab = open_in_new_tab
            link.display_order = display_order
            flash('導航連結已更新', 'success')
        else:  # 新增連結
            link = NavLink(
                title=title,
                url=url,
                icon_class=icon_class,
                is_active=is_active,
                open_in_new_tab=open_in_new_tab,
                display_order=display_order
            )
            db.session.add(link)
            flash('導航連結已新增', 'success')
        
        db.session.commit()
        return redirect(url_for('main.admin_manage_nav_links'))
        
    return render_template('admin_nav_links.html', 
                          title='管理導航連結',
                          nav_links=nav_links,
                          now=datetime.now())

# === 註冊金鑰管理 ===
@main.route('/admin-panel/admin/manage-keys')
@login_required
@admin_required
def admin_manage_keys():
    """管理註冊金鑰和管理員代碼"""
    # 從設定中獲取當前金鑰和代碼
    team_key = current_app.config['TEAM_KEY']
    admin_key = current_app.config['ADMIN_REGISTRATION_CODE']
    
    return render_template('admin_api_keys.html', 
                          title='管理註冊金鑰',
                          team_key=team_key,
                          admin_key=admin_key,
                          now=datetime.now())

@main.route('/admin-panel/admin/refresh-keys', methods=['POST'])
@login_required
@admin_required
def admin_refresh_keys():
    """重新生成註冊金鑰或管理員代碼"""
    key_type = request.form.get('key_type')
    
    if key_type == 'team_key':
        # 生成新的團隊註冊金鑰
        new_key = secrets.token_urlsafe(16)  # 生成長度為 16 的隨機字串
        current_app.config['TEAM_KEY'] = new_key
        
        # 更新 JSON 金鑰文件
        try:
            update_keys_json('TEAM_KEY', new_key)
            flash('團隊成員註冊金鑰已成功重新生成', 'success')
        except Exception as e:
            flash(f'金鑰生成成功，但無法更新金鑰檔案: {str(e)}', 'warning')
            
    elif key_type == 'admin_key':
        # 生成新的管理員註冊代碼
        new_key = secrets.token_urlsafe(20)  # 管理員代碼長度為 20
        current_app.config['ADMIN_REGISTRATION_CODE'] = new_key
        
        # 更新 JSON 金鑰文件
        try:
            update_keys_json('ADMIN_REGISTRATION_CODE', new_key)
            flash('管理員註冊代碼已成功重新生成', 'success')
        except Exception as e:
            flash(f'代碼生成成功，但無法更新金鑰檔案: {str(e)}', 'warning')
    
    else:
        flash('未知的金鑰類型', 'danger')
        
    return redirect(url_for('main.admin_manage_keys'))

def update_keys_json(key, value):
    """更新 JSON 金鑰文件中的值"""
    import json
    keys_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'keys.json')
    
    try:
        # 讀取現有 JSON 文件
        with open(keys_path, 'r', encoding='utf-8') as file:
            keys_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或格式不正確，創建新的字典
        keys_data = {}
    
    # 更新金鑰值
    keys_data[key] = value
    # 更新上次修改時間
    keys_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 寫回文件
    with open(keys_path, 'w', encoding='utf-8') as file:
        json.dump(keys_data, file, indent=4)

# === 重定向路由 - 保持舊路徑相容性 ===
# 重定向舊的路徑到新路徑，以保持相容性
@main.route('/dashboard')
def redirect_dashboard():
    """重定向舊的儀表板路徑"""
    return redirect(url_for('main.dashboard'))

@main.route('/admin')
def redirect_admin():
    """重定向舊的管理員路徑"""
    return redirect(url_for('main.admin_dashboard'))

@main.route('/logout')
def redirect_logout():
    """重定向舊的登出路徑"""
    return redirect(url_for('main.admin_logout'))

@main.route('/preview/profile')
def redirect_preview():
    """重定向舊的預覽路徑"""
    return redirect(url_for('main.profile_preview'))

@main.route('/profile/<username>')
def redirect_profile(username):
    """重定向舊的個人檔案路徑"""
    return redirect(url_for('main.public_profile', username=username))

@main.route('/login')
def redirect_login():
    """重定向舊的登入路徑到後台首頁"""
    return redirect(url_for('main.admin_home'))

# === 標籤管理區域 ===
@main.route('/admin-panel/admin/manage-tags', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_manage_tags():
    """管理標籤分類"""
    tag = None
    # 檢查是否是編輯模式（通過URL參數獲取tag_id）
    edit_tag_id = request.args.get('tag_id')
    if edit_tag_id:
        tag = Tag.query.get_or_404(edit_tag_id)
    
    tags = Tag.query.order_by(Tag.display_order).all()
    
    if request.method == 'POST':
        tag_id = request.form.get('tag_id')
        name = request.form.get('name')
        display_name = request.form.get('display_name')
        description = request.form.get('description', '')
        icon_class = request.form.get('icon_class', 'fas fa-tag')
        color = request.form.get('color', '#7983d4')
        display_order = request.form.get('display_order', 0, type=int)
        is_active = 'is_active' in request.form
        
        # 驗證輸入
        if not name or not display_name:
            flash('標籤名稱和顯示名稱不能為空', 'danger')
            return redirect(url_for('main.admin_manage_tags'))
        
        # 檢查標籤名稱是否已存在 (排除當前編輯的標籤)
        existing_tag = Tag.query.filter(Tag.name == name).first()
        if existing_tag and (not tag_id or int(tag_id) != existing_tag.id):
            flash(f'標籤名稱 "{name}" 已被使用，請使用其他名稱', 'danger')
            return redirect(url_for('main.admin_manage_tags'))
        
        if tag_id:  # 更新現有標籤
            tag = Tag.query.get_or_404(tag_id)
            tag.name = name
            tag.display_name = display_name
            tag.description = description
            tag.icon_class = icon_class
            tag.color = color
            tag.display_order = display_order
            tag.is_active = is_active
            flash('標籤已更新成功', 'success')
        else:  # 新增標籤
            tag = Tag(
                name=name,
                display_name=display_name,
                description=description,
                icon_class=icon_class,
                color=color,
                display_order=display_order,
                is_active=is_active
            )
            db.session.add(tag)
            flash('標籤已新增成功', 'success')
        
        db.session.commit()
        return redirect(url_for('main.admin_manage_tags'))
        
    return render_template('admin_manage_tags.html', 
                          title='管理標籤分類',
                          tags=tags,
                          tag=tag,
                          now=datetime.now())

@main.route('/admin-panel/admin/toggle-tag/<int:tag_id>', methods=['POST'])
@login_required
@admin_required
def admin_toggle_tag(tag_id):
    """切換標籤的啟用/停用狀態"""
    tag = Tag.query.get_or_404(tag_id)
    tag.is_active = not tag.is_active
    db.session.commit()
    
    status = "啟用" if tag.is_active else "停用"
    flash(f'標籤 "{tag.display_name}" 已設為{status}', 'success')
    return redirect(url_for('main.admin_manage_tags'))

@main.route('/admin-panel/admin/delete-tag/<int:tag_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_tag(tag_id):
    """刪除標籤"""
    tag = Tag.query.get_or_404(tag_id)
    
    # 刪除所有使用此標籤的關聯
    UserTag.query.filter_by(tag_id=tag.id).delete()
    
    # 刪除標籤
    display_name = tag.display_name  # 保存名稱用於提示消息
    db.session.delete(tag)
    db.session.commit()
    
    flash(f'標籤 "{display_name}" 已成功刪除', 'success')
    return redirect(url_for('main.admin_manage_tags'))

# === 成員管理 ===
@main.route('/admin-panel/admin/manage-users')
@login_required
@admin_required
def admin_manage_users():
    """獨立的成員管理頁面"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    tag_id = request.args.get('tag_id', None, type=int)
    per_page = 15
    
    # 基本查詢 - 排除管理員
    query = User.query.filter(User.is_admin == False)
    
    # 根據搜尋條件過濾
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                User.username.ilike(search_term),
                User.display_name.ilike(search_term),
                User.discord_id.ilike(search_term)
            )
        )
    
    # 根據標籤過濾
    selected_tag = None
    if tag_id:
        selected_tag = Tag.query.get_or_404(tag_id)
        query = query.filter(User.tags.any(Tag.id == tag_id))
    
    # 獲取所有標籤用於過濾選項
    all_tags = Tag.query.order_by(Tag.display_order).all()
    
    # 排序和分頁
    users_pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    users = users_pagination.items
    
    return render_template('admin_manage_users.html',
                           title='成員管理',
                           users=users,
                           pagination=users_pagination,
                           search_query=search_query,
                           all_tags=all_tags,
                           selected_tag=selected_tag,
                           now=datetime.now())

@main.route('/admin-panel/admin/toggle-verify-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_toggle_verify_user(user_id):
    """管理員切換用戶的驗證狀態（啟用/停用帳戶）"""
    user = User.query.get_or_404(user_id)
    
    # 確認不是管理員
    if user.is_admin:
        flash("無法變更管理員用戶的狀態", "danger")
        return redirect(url_for('main.admin_manage_users'))
    
    # 切換驗證狀態
    user.is_verified = not user.is_verified
    
    status = "啟用" if user.is_verified else "停用"
    
    try:
        db.session.commit()
        flash(f"用戶 {user.display_name or user.username} 已{status}", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"操作失敗: {str(e)}", "danger")
    
    # 獲取重定向參數
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    tag_id = request.args.get('tag_id', None, type=int)
    
    # 重定向回用戶列表頁面，保留搜尋和篩選狀態
    return redirect(url_for('main.admin_manage_users', 
                            page=page, 
                            search=search_query or None, 
                            tag_id=tag_id))

@main.route('/admin-panel/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    """管理員刪除用戶"""
    user = User.query.get_or_404(user_id)
    
    # 確認不是管理員
    if user.is_admin:
        flash("無法刪除管理員用戶", "danger")
        return redirect(url_for('main.admin_manage_users'))
    
    username = user.username
    display_name = user.display_name or username
    
    try:
        # 刪除用戶及其所有相關數據（會自動通過模型中的 cascade 設定刪除關聯資料）
        db.session.delete(user)
        db.session.commit()
        flash(f"用戶 {display_name} 已成功刪除", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"刪除失敗: {str(e)}", "danger")
    
    # 獲取重定向參數
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    tag_id = request.args.get('tag_id', None, type=int)
    
    # 重定向回用戶列表頁面，保留搜尋和篩選狀態
    return redirect(url_for('main.admin_manage_users', 
                            page=page, 
                            search=search_query or None, 
                            tag_id=tag_id))

@main.route('/admin-panel/admin/user/<int:user_id>/update-tags', methods=['POST'])
@login_required
@admin_required
def admin_update_user_tags(user_id):
    """更新用戶的標籤關聯"""
    user = User.query.get_or_404(user_id)
    
    # 獲取表單提交的標籤 ID 列表
    tag_ids = request.form.getlist('tags[]')
    
    # 刪除所有現有的用戶標籤關聯
    UserTag.query.filter_by(user_id=user.id).delete()
    
    # 創建新的用戶標籤關聯
    for tag_id in tag_ids:
        user_tag = UserTag(user_id=user.id, tag_id=int(tag_id))
        db.session.add(user_tag)
    
    db.session.commit()
    
    # 獲取重定向參數
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    tag_id = request.args.get('tag_id', None, type=int)
    
    flash(f'已成功更新 {user.display_name or user.username} 的標籤', 'success')
    
    # 重定向回成員管理頁面，保留搜尋和篩選狀態
    return redirect(url_for('main.admin_manage_users', page=page, search=search_query or None, tag_id=tag_id))

# === 管理員成員留言管理區域 ===
@main.route('/admin-panel/admin/manage-testimonials')
@login_required
@admin_required
def admin_manage_testimonials():
    """管理員管理成員留言"""
    # 獲取所有帶有留言的記錄
    testimonials = db.session.query(UserTestimonial, User).\
                  join(User, UserTestimonial.user_id == User.id).\
                  filter(UserTestimonial.message != None, UserTestimonial.message != '').\
                  order_by(UserTestimonial.updated_at.desc()).all()
    
    return render_template('admin_manage_testimonials.html',
                           title='成員留言管理',
                           testimonials=testimonials,
                           now=datetime.now())

@main.route('/admin-panel/admin/testimonial/<int:testimonial_id>/toggle-visibility', methods=['POST'])
@login_required
@admin_required
def admin_toggle_testimonial_visibility(testimonial_id):
    """管理員切換留言可見性"""
    testimonial = UserTestimonial.query.get_or_404(testimonial_id)
    
    testimonial.is_visible = not testimonial.is_visible
    testimonial.approved_by = current_user.id if testimonial.is_visible else None
    db.session.commit()
    
    status = "顯示" if testimonial.is_visible else "隱藏"
    flash(f'成員留言已設為{status}', 'success')
    return redirect(url_for('main.admin_manage_testimonials'))

@main.route('/admin-panel/admin/testimonial/<int:testimonial_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_testimonial(testimonial_id):
    """管理員刪除留言"""
    testimonial = UserTestimonial.query.get_or_404(testimonial_id)
    
    # 刪除留言內容，但保留記錄
    testimonial.message = None
    testimonial.is_visible = False
    testimonial.approved_by = None
    db.session.commit()
    
    flash('成員留言已成功刪除', 'success')
    return redirect(url_for('main.admin_manage_testimonials'))

@main.route('/admin-panel/admin/testimonial/<int:testimonial_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_testimonial(testimonial_id):
    """管理員編輯留言"""
    testimonial = UserTestimonial.query.get_or_404(testimonial_id)
    user = User.query.get_or_404(testimonial.user_id)
    
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        is_visible = 'is_visible' in request.form
        
        testimonial.message = message
        testimonial.is_visible = is_visible
        testimonial.approved_by = current_user.id if is_visible else None
        db.session.commit()
        
        flash('成員留言已成功更新', 'success')
        return redirect(url_for('main.admin_manage_testimonials'))
    
    return render_template('admin_edit_testimonial.html',
                           title='編輯成員留言',
                           testimonial=testimonial,
                           user=user,
                           now=datetime.now())

@main.route('/admin-panel/admin/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    """管理員編輯用戶頁面"""
    # 獲取頁碼和搜尋關鍵字參數（用於返回正確的頁面）
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    
    # 獲取用戶資料
    user_to_edit = User.query.get_or_404(user_id)
    
    # 確保不是管理員
    if user_to_edit.is_admin:
        flash("無法編輯管理員用戶，請使用管理員編輯功能", "warning")
        return redirect(url_for('main.admin_manage_users', page=page, search=search_query or None))
    
    # 獲取用戶個人資料和社交連結
    profile = UserProfile.get_or_create(user_to_edit.id)
    social_links = SocialLink.query.filter_by(user_id=user_to_edit.id).all()
    
    # 獲取所有可用標籤
    tags = Tag.query.order_by(Tag.display_order).all()
    
    # 處理 POST 請求（更新資料）
    if request.method == 'POST':
        # 更新用戶顯示名稱
        display_name = request.form.get('displayName', '').strip()
        user_to_edit.display_name = display_name if display_name else None
        
        # 更新個人資料
        profile.title = request.form.get('profileTitle', '').strip()
        profile.bio = request.form.get('profileBio', '').strip()
        profile.interests = request.form.get('profile_interests', '').strip()
        
        # 修復：更新背景漸層和主題色
        profile.background_gradient = request.form.get('background_gradient', '').strip()
        profile.main_color = request.form.get('main_color', '').strip()
        
        # 更新社交媒體連結
        SocialLink.query.filter_by(user_id=user_to_edit.id).delete()
        titles = request.form.getlist('social_titles[]')
        urls = request.form.getlist('social_urls[]')
        icons = request.form.getlist('social_icons[]')
        
        for i in range(min(len(titles), len(urls))):
            title = titles[i].strip() if i < len(titles) else ''
            url = urls[i].strip() if i < len(urls) else ''
            icon = icons[i] if i < len(icons) and icons[i] else 'fas fa-globe'
            
            if title and url:
                link = SocialLink(
                    user_id=user_to_edit.id,
                    title=title,
                    url=url,
                    icon_class=icon
                )
                db.session.add(link)
        
        # 儲存所有變更
        try:
            db.session.commit()
            flash(f"成功更新用戶 {user_to_edit.username} 的資料", "success")
            return redirect(url_for('main.admin_manage_users', page=page, search=search_query or None))
        except Exception as e:
            db.session.rollback()
            flash(f"更新失敗: {str(e)}", "danger")
    
    # 將社交連結轉換為 JSON 格式以供 JavaScript 使用
    social_links_json = []
    for link in social_links:
        social_links_json.append({
            'title': link.title,
            'url': link.url,
            'icon_class': link.icon_class
        })
    
    return render_template('admin_edit_user.html',
                          title=f'編輯用戶 - {user_to_edit.username}',
                          user_to_edit=user_to_edit,
                          profile=profile,
                          social_links=social_links_json,
                          tags=tags,
                          page=page,
                          search_query=search_query,
                          now=datetime.now())