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
    
    # 獲取用戶在伺服器中的身分組
    member_role_ids = discord_service.get_member_roles(config.guild_id, discord_id)
    if not member_role_ids:
        return False, "用戶不在伺服器中或無法獲取身分組資訊"
    
    # 獲取啟用的身分組標籤對應
    role_mappings = RoleTagMapping.get_active_mappings(config.id)
    
    # 找出應該擁有的標籤
    tag_ids_to_add = set()
    for mapping in role_mappings:
        if mapping.role_id in member_role_ids:
            tag_ids_to_add.add(mapping.tag_id)
    
    # 刪除用戶現有的所有標籤（僅限通過 Discord 對應的標籤）
    mapped_tag_ids = {m.tag_id for m in role_mappings}
    UserTag.query.filter(
        UserTag.user_id == user.id,
        UserTag.tag_id.in_(mapped_tag_ids)
    ).delete(synchronize_session=False)
    
    # 添加新標籤
    for tag_id in tag_ids_to_add:
        user_tag = UserTag(user_id=user.id, tag_id=tag_id)
        db.session.add(user_tag)
    
    db.session.commit()
    
    return True, f"已同步 {len(tag_ids_to_add)} 個標籤"
