#!/usr/bin/env python3
"""
Session 配置驗證腳本
用於檢查 session 相關配置是否正確

使用方法: python verify_session_config.py
"""

import os
import sys

def check_dependencies():
    """檢查必要的依賴是否安裝"""
    print("📦 檢查依賴...")
    
    try:
        import flask_session
        print("  ✅ flask-session 已安裝")
    except ImportError:
        print("  ❌ flask-session 未安裝")
        print("     執行: pip install flask-session")
        return False
    
    try:
        import cachelib
        print("  ✅ cachelib 已安裝")
    except ImportError:
        print("  ❌ cachelib 未安裝")
        print("     執行: pip install cachelib")
        return False
    
    return True

def check_session_directory():
    """檢查 session 目錄"""
    print("\n📁 檢查 session 目錄...")
    
    session_dir = "flask_session"
    
    if not os.path.exists(session_dir):
        print(f"  ❌ 目錄不存在: {session_dir}")
        print(f"     執行: mkdir {session_dir}")
        return False
    
    if not os.path.isdir(session_dir):
        print(f"  ❌ {session_dir} 不是目錄")
        return False
    
    if not os.access(session_dir, os.W_OK):
        print(f"  ❌ {session_dir} 沒有寫入權限")
        print(f"     執行: chmod 755 {session_dir}")
        return False
    
    print(f"  ✅ {session_dir} 目錄存在且可寫")
    
    # 檢查目錄內容
    files = os.listdir(session_dir)
    if files:
        print(f"  📊 當前 session 檔案數: {len(files)}")
    else:
        print(f"  ℹ️  目錄為空（應用運行後會自動生成）")
    
    return True

def check_app_config():
    """檢查應用配置"""
    print("\n⚙️  檢查應用配置...")
    
    try:
        from app import app
        
        # 檢查 SESSION_TYPE
        session_type = app.config.get('SESSION_TYPE')
        if session_type == 'filesystem':
            print(f"  ✅ SESSION_TYPE = 'filesystem'")
        else:
            print(f"  ⚠️  SESSION_TYPE = '{session_type}' (預期: 'filesystem')")
        
        # 檢查 SESSION_FILE_DIR
        session_dir = app.config.get('SESSION_FILE_DIR')
        if session_dir:
            print(f"  ✅ SESSION_FILE_DIR = {session_dir}")
        else:
            print(f"  ❌ SESSION_FILE_DIR 未設置")
            return False
        
        # 檢查其他配置
        configs = [
            'SESSION_PERMANENT',
            'SESSION_USE_SIGNER',
            'SESSION_COOKIE_HTTPONLY',
            'PERMANENT_SESSION_LIFETIME'
        ]
        
        for config in configs:
            value = app.config.get(config)
            if value is not None:
                print(f"  ✅ {config} = {value}")
            else:
                print(f"  ⚠️  {config} 未設置")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 無法加載應用配置: {e}")
        return False

def check_environment():
    """檢查環境變數"""
    print("\n🌍 檢查環境變數...")
    
    required_vars = ['SECRET_KEY', 'DISCORD_CLIENT_ID', 'DISCORD_CLIENT_SECRET']
    optional_vars = ['FLASK_DEBUG', 'SESSION_COOKIE_SECURE', 'REDIS_URL']
    
    all_ok = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var} 已設置")
        else:
            print(f"  ❌ {var} 未設置（必須）")
            all_ok = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"  ✅ {var} = {os.getenv(var)}")
        else:
            print(f"  ℹ️  {var} 未設置（可選）")
    
    return all_ok

def test_session_creation():
    """測試 session 創建"""
    print("\n🧪 測試 session 創建...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # 設置 session
            with client.session_transaction() as sess:
                sess['test_key'] = 'test_value'
            
            print("  ✅ Session 設置成功")
            
            # 讀取 session
            with client.session_transaction() as sess:
                value = sess.get('test_key')
                if value == 'test_value':
                    print("  ✅ Session 讀取成功")
                    return True
                else:
                    print("  ❌ Session 讀取失敗")
                    return False
                    
    except Exception as e:
        print(f"  ❌ Session 測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("🔍 Session 配置驗證")
    print("=" * 60)
    
    results = []
    
    results.append(("依賴檢查", check_dependencies()))
    results.append(("Session 目錄", check_session_directory()))
    results.append(("應用配置", check_app_config()))
    results.append(("環境變數", check_environment()))
    results.append(("Session 測試", test_session_creation()))
    
    print("\n" + "=" * 60)
    print("📊 檢查結果")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有檢查通過！可以部署到生產環境。")
        print("=" * 60)
        return 0
    else:
        print("❌ 部分檢查失敗，請修復後再部署。")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
