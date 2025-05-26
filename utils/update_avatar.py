import os
import requests
from flask_apscheduler import APScheduler
from models.user import db, User

# 背景排程任務
def set_auto_update_avatar(app):
    def update_user_avatars():
        with app.app_context(): # 確保在應用程式上下文中執行資料庫操作
            print("開始更新使用者頭像...")
            update_count = 0
            same_count = 0
            error_count = 0
            users = User.query.all()
            user_count = User.query.count()
            for user in users:
                if user.discord_id:
                    # print(f"正在更新使用者 {user.username} (ID: {user.discord_id}) 的頭像...")
                    try:
                        discord_api_url = f"https://discord.com/api/v10/users/{user.discord_id}"
                        headers = {"Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}"}
                        response = requests.get(discord_api_url, headers=headers)
                        response.raise_for_status() # 如果請求失敗則拋出例外
                        data = response.json()    
                        avatar_hash = data.get('avatar')
                        
                        if avatar_hash:
                            new_avatar_url = f"https://cdn.discordapp.com/avatars/{user.discord_id}/{avatar_hash}.png"
                            # print(f"獲取到新的頭像 URL: {new_avatar_url}")
                            if user.avatar != new_avatar_url:
                                print(f"發現不同頭像，更新使用者 {user.username} 的頭像: {new_avatar_url}")
                                user.avatar = new_avatar_url
                                update_count+=1
                            else:
                                same_count+=1
                        else:
                            print(f"使用者 {user.username} 沒有 Discord 頭像或無法獲取。")
                            error_count+=1
                    except requests.exceptions.RequestException as e:
                        print(f"透過 Discord API 獲取使用者 {user.username} (ID: {user.discord_id}) 的頭像失敗: {e}")
                        error_count+=1
                    except Exception as e:
                        print(f"更新使用者 {user.username} 的頭像時發生錯誤: {e}")
                        error_count+=1
            db.session.commit()
            print(f"頭像更新完成: 共 {user_count} 位使用者，成功更新 {update_count} 位，無變更 {same_count} 位，錯誤 {error_count} 次。")

    # 初始化 APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # 新增排程任務到 APScheduler
    # 檢查是否已經有這個任務，避免重複新增 (尤其是在 debug 模式下 app 重載時)
    if not scheduler.get_job('update_avatars_job'):
        scheduler.add_job(id='update_avatars_job', func=update_user_avatars, trigger='interval', hours=3)
        print("已新增每 3 小時更新一次使用者頭像的排程任務。")