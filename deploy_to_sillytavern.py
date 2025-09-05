#!/usr/bin/env python3
"""
ChronoForge插件部署脚本
自动将插件文件复制到SillyTavern插件目录
"""
import os
import shutil
from pathlib import Path

def find_sillytavern_plugins_dir():
    """尝试找到SillyTavern的第三方插件目录"""
    possible_paths = [
        Path("../SillyTavern/public/scripts/extensions/third-party"),  # 相对路径
        Path("../../SillyTavern/public/scripts/extensions/third-party"),
        Path("../../../SillyTavern/public/scripts/extensions/third-party"),
        Path.home() / "SillyTavern/public/scripts/extensions/third-party",
        Path("D:/SillyTavern/public/scripts/extensions/third-party"),  # 常见路径
        Path("C:/SillyTavern/public/scripts/extensions/third-party"),
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"找到SillyTavern插件目录: {path}")
            return path
    
    return None

def deploy_plugin():
    """部署插件到SillyTavern"""
    source_dir = Path(__file__).parent / "sillytavern_plugin"
    
    if not source_dir.exists():
        print("❌ 找不到插件源代码目录")
        return False
    
    plugins_dir = find_sillytavern_plugins_dir()
    if not plugins_dir:
        print("❌ 找不到SillyTavern第三方插件目录")
        print("请手动指定SillyTavern的 public/scripts/extensions/third-party 目录路径")
        manual_path = input("请输入完整路径（或按回车跳过）: ").strip()
        if manual_path:
            plugins_dir = Path(manual_path)
        else:
            return False
    
    target_dir = plugins_dir / "chronoforge-memory"
    
    try:
        # 如果目标目录存在，先备份
        if target_dir.exists():
            backup_dir = plugins_dir / "chronoforge-memory.backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.move(str(target_dir), str(backup_dir))
            print(f"📦 已备份旧版本到: {backup_dir}")
        
        # 复制插件文件
        shutil.copytree(str(source_dir), str(target_dir))
        print(f"✅ 插件已部署到: {target_dir}")
        
        print("\n🎯 接下来的步骤:")
        print("1. 启动ChronoForge UI: python run_ui.py")
        print("2. 启动SillyTavern")
        print("3. 在SillyTavern设置中启用 'ChronoForge RAG Enhancer' 插件")
        print("4. 创建或选择一个角色开始对话测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ChronoForge插件部署工具")
    print("=" * 50)
    
    success = deploy_plugin()
    
    if success:
        print("\n🎉 部署完成！")
    else:
        print("\n💥 部署失败，请检查上述错误信息")