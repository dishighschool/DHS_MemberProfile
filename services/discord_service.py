"""
Discord Bot 服務模組
用於與 Discord API 進行交互，獲取伺服器、身分組和成員資訊
注意：此模組不啟動 Bot 實例，僅使用 Bot Token 作為 API 權杖
"""
import requests
from typing import List, Dict, Optional

class DiscordService:
    """Discord API 服務類別"""
    
    DISCORD_API_BASE = "https://discord.com/api/v10"
    
    def __init__(self, bot_token: str):
        """
        初始化 Discord 服務
        
        Args:
            bot_token: Discord Bot Token
        """
        self.bot_token = bot_token
        self.headers = {
            'Authorization': f'Bot {bot_token}',
            'Content-Type': 'application/json'
        }
    
    def verify_token(self) -> bool:
        """
        驗證 Bot Token 是否有效
        
        Returns:
            bool: Token 是否有效
        """
        try:
            response = requests.get(
                f"{self.DISCORD_API_BASE}/users/@me",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"驗證 Token 失敗: {str(e)}")
            return False
    
    def get_bot_guilds(self) -> List[Dict]:
        """
        獲取 Bot 加入的所有伺服器列表
        
        Returns:
            List[Dict]: 伺服器列表，每個元素包含 id, name, icon 等資訊
        """
        try:
            response = requests.get(
                f"{self.DISCORD_API_BASE}/users/@me/guilds",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"獲取伺服器列表失敗: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"獲取伺服器列表時發生錯誤: {str(e)}")
            return []
    
    def get_guild_roles(self, guild_id: str) -> List[Dict]:
        """
        獲取指定伺服器的所有身分組
        
        Args:
            guild_id: Discord 伺服器 ID
            
        Returns:
            List[Dict]: 身分組列表，每個元素包含 id, name, color 等資訊
        """
        try:
            response = requests.get(
                f"{self.DISCORD_API_BASE}/guilds/{guild_id}/roles",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                roles = response.json()
                # 過濾掉 @everyone 身分組
                return [role for role in roles if role['name'] != '@everyone']
            else:
                print(f"獲取身分組列表失敗: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"獲取身分組列表時發生錯誤: {str(e)}")
            return []
    
    def get_guild_member(self, guild_id: str, user_id: str) -> Optional[Dict]:
        """
        獲取指定伺服器中的成員資訊
        
        Args:
            guild_id: Discord 伺服器 ID
            user_id: Discord 用戶 ID
            
        Returns:
            Optional[Dict]: 成員資訊，包含 roles 等，如果成員不在伺服器中則返回 None
        """
        try:
            response = requests.get(
                f"{self.DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"用戶 {user_id} 不在伺服器 {guild_id} 中")
                return None
            else:
                print(f"獲取成員資訊失敗: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"獲取成員資訊時發生錯誤: {str(e)}")
            return None
    
    def get_member_roles(self, guild_id: str, user_id: str) -> List[str]:
        """
        獲取指定成員的所有身分組 ID 列表
        
        Args:
            guild_id: Discord 伺服器 ID
            user_id: Discord 用戶 ID
            
        Returns:
            List[str]: 身分組 ID 列表
        """
        member = self.get_guild_member(guild_id, user_id)
        if member and 'roles' in member:
            return member['roles']
        return []
    
    def get_all_guild_members(self, guild_id: str, limit: int = 1000) -> List[Dict]:
        """
        獲取伺服器中的所有成員資訊（支持分頁）
        
        Args:
            guild_id: Discord 伺服器 ID
            limit: 最大獲取數量（預設 1000）
            
        Returns:
            List[Dict]: 成員列表，每個元素包含 user 和 roles 資訊
        """
        members = []
        after = None
        
        while len(members) < limit:
            try:
                params = {'limit': min(1000, limit - len(members))}  # Discord API 每次最多 1000 個
                if after:
                    params['after'] = after
                
                response = requests.get(
                    f"{self.DISCORD_API_BASE}/guilds/{guild_id}/members",
                    headers=self.headers,
                    params=params,
                    timeout=30  # 增加超時時間，因為批量請求可能較慢
                )
                
                if response.status_code == 200:
                    batch = response.json()
                    if not batch:  # 沒有更多成員
                        break
                    
                    members.extend(batch)
                    after = batch[-1]['user']['id']  # 設置下次請求的起始點
                    
                    if len(batch) < 1000:  # 這是最後一批
                        break
                else:
                    print(f"獲取成員列表失敗: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                print(f"獲取成員列表時發生錯誤: {str(e)}")
                break
        
        return members[:limit]  # 確保不超過限制
    
    def get_members_roles_dict(self, guild_id: str, limit: int = 1000) -> Dict[str, List[str]]:
        """
        獲取伺服器中所有成員的角色字典
        
        Args:
            guild_id: Discord 伺服器 ID
            limit: 最大獲取數量
            
        Returns:
            Dict[str, List[str]]: 用戶ID -> 角色ID列表 的字典
        """
        members = self.get_all_guild_members(guild_id, limit)
        return {member['user']['id']: member.get('roles', []) for member in members}
    
    def get_guild_info(self, guild_id: str) -> Optional[Dict]:
        """
        獲取伺服器的詳細資訊
        
        Args:
            guild_id: Discord 伺服器 ID
            
        Returns:
            Optional[Dict]: 伺服器資訊
        """
        try:
            response = requests.get(
                f"{self.DISCORD_API_BASE}/guilds/{guild_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"獲取伺服器資訊失敗: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"獲取伺服器資訊時發生錯誤: {str(e)}")
            return None
    
    @staticmethod
    def get_role_color_hex(color: int) -> str:
        """
        將 Discord 身分組顏色數值轉換為十六進制顏色碼
        
        Args:
            color: Discord 身分組顏色數值
            
        Returns:
            str: 十六進制顏色碼 (例如 #7289DA)
        """
        if color == 0:
            return '#99AAB5'  # Discord 預設灰色
        return f'#{color:06x}'


def sync_user_tags_from_discord(discord_id: str) -> tuple[bool, str]:
    """
    根據用戶的 Discord 身分組同步系統標籤
    
    Args:
        discord_id: Discord 用戶 ID
        
    Returns:
        tuple[bool, str]: (是否成功, 訊息)
    """
    from models.user import User, UserTag, DiscordConfig, RoleTagMapping, db
    
    # 獲取 Discord 配置
    config = DiscordConfig.get_active_config()
    if not config or not config.guild_id:
        return False, "Discord Bot 未配置或未選擇伺服器"
    
    # 獲取用戶
    user = User.get_by_discord_id(discord_id)
    if not user:
        return False, "找不到用戶"
    
    # 創建 Discord 服務
    discord_service = DiscordService(config.bot_token)
    
    # 批量獲取所有成員角色信息
    members_roles = discord_service.get_members_roles_dict(config.guild_id)
    
    # 檢查用戶是否在伺服器中
    if discord_id not in members_roles:
        return False, "用戶不在伺服器中"
    
    # 獲取用戶在伺服器中的身分組
    member_role_ids = members_roles[discord_id]
    
    # 獲取啟用的身分組標籤對應
    role_mappings = RoleTagMapping.get_active_mappings(config.id)
    
    # 找出應該擁有的標籤
    tag_ids_to_add = set()
    for mapping in role_mappings:
        if mapping.role_id in member_role_ids:
            tag_ids_to_add.add(mapping.tag_id)
    
    # 獲取所有映射的標籤 ID
    mapped_tag_ids = {m.tag_id for m in role_mappings}
    
    # 獲取用戶當前擁有的所有通過 Discord 對應的標籤
    current_mapped_tags = UserTag.query.filter(
        UserTag.user_id == user.id,
        UserTag.tag_id.in_(mapped_tag_ids)
    ).all()
    current_tag_ids = {ut.tag_id for ut in current_mapped_tags}
    
    # 計算需要添加和刪除的標籤
    tags_to_add = tag_ids_to_add - current_tag_ids
    tags_to_remove = current_tag_ids - tag_ids_to_add
    
    # 刪除不需要的標籤
    if tags_to_remove:
        UserTag.query.filter(
            UserTag.user_id == user.id,
            UserTag.tag_id.in_(tags_to_remove)
        ).delete(synchronize_session=False)
    
    # 添加新的標籤
    for tag_id in tags_to_add:
        user_tag = UserTag(user_id=user.id, tag_id=tag_id)
        db.session.add(user_tag)
    
    db.session.commit()
    
    # 構建詳細的同步結果訊息
    messages = []
    if tags_to_add:
        messages.append(f"添加 {len(tags_to_add)} 個標籤")
    if tags_to_remove:
        messages.append(f"移除 {len(tags_to_remove)} 個標籤")
    
    if not messages:
        return True, "標籤已是最新狀態，無需變更"
    
    return True, "，".join(messages)


def sync_all_users_tags_from_discord() -> tuple[bool, str]:
    """
    批量同步所有系統用戶的 Discord 標籤
    
    Returns:
        tuple[bool, str]: (是否成功, 訊息)
    """
    from models.user import User, UserTag, DiscordConfig, RoleTagMapping, db
    
    # 獲取 Discord 配置
    config = DiscordConfig.get_active_config()
    if not config or not config.guild_id:
        return False, "Discord Bot 未配置或未選擇伺服器"
    
    # 獲取所有已驗證的系統用戶
    system_users = User.query.filter_by(is_verified=True).all()
    if not system_users:
        return True, "沒有已驗證的用戶需要同步"
    
    # 創建 Discord 服務並批量獲取所有成員角色信息
    discord_service = DiscordService(config.bot_token)
    members_roles = discord_service.get_members_roles_dict(config.guild_id)
    
    # 獲取啟用的身分組標籤對應
    role_mappings = RoleTagMapping.get_active_mappings(config.id)
    if not role_mappings:
        return True, "沒有啟用的角色標籤映射"
    
    # 創建角色ID到標籤ID的映射字典
    role_to_tag_map = {mapping.role_id: mapping.tag_id for mapping in role_mappings}
    
    # 統計處理結果
    success_count = 0
    fail_count = 0
    total_changes = 0
    
    for user in system_users:
        try:
            # 檢查用戶是否在 Discord 伺服器中
            if user.discord_id not in members_roles:
                fail_count += 1
                continue
            
            # 獲取用戶在伺服器中的身分組
            member_role_ids = members_roles[user.discord_id]
            
            # 找出應該擁有的標籤
            tag_ids_to_add = set()
            for role_id in member_role_ids:
                if role_id in role_to_tag_map:
                    tag_ids_to_add.add(role_to_tag_map[role_id])
            
            # 獲取所有映射的標籤 ID
            mapped_tag_ids = set(role_to_tag_map.values())
            
            # 獲取用戶當前擁有的所有通過 Discord 對應的標籤
            current_mapped_tags = UserTag.query.filter(
                UserTag.user_id == user.id,
                UserTag.tag_id.in_(mapped_tag_ids)
            ).all()
            current_tag_ids = {ut.tag_id for ut in current_mapped_tags}
            
            # 計算需要添加和刪除的標籤
            tags_to_add = tag_ids_to_add - current_tag_ids
            tags_to_remove = current_tag_ids - tag_ids_to_add
            
            # 執行標籤變更
            changes_made = False
            
            # 刪除不需要的標籤
            if tags_to_remove:
                UserTag.query.filter(
                    UserTag.user_id == user.id,
                    UserTag.tag_id.in_(tags_to_remove)
                ).delete(synchronize_session=False)
                changes_made = True
            
            # 添加新的標籤
            for tag_id in tags_to_add:
                user_tag = UserTag(user_id=user.id, tag_id=tag_id)
                db.session.add(user_tag)
                changes_made = True
            
            if changes_made:
                total_changes += 1
            
            success_count += 1
            
        except Exception as e:
            print(f"同步用戶 {user.username} 時發生錯誤: {str(e)}")
            fail_count += 1
            continue
    
    db.session.commit()
    
    # 構建結果訊息
    result_message = f"批量同步完成：處理 {len(system_users)} 個用戶，成功 {success_count} 個，失敗 {fail_count} 個"
    if total_changes > 0:
        result_message += f"，共變更 {total_changes} 個用戶的標籤"
    
    return True, result_message
