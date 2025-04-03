#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform

def build_windows_exe():
    """构建Windows可执行文件"""
    print("开始构建Windows可执行文件...")
    
    # 确保在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 检测操作系统
    current_os = platform.system().lower()
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--name=个人所得税计算器2025",
        "--windowed",  # 不显示控制台窗口
        "--onefile",   # 打包成单个文件
    ]
    
    # 添加图标（如果存在）
    if os.path.exists("icon.ico"):
        cmd.append("--icon=icon.ico")
    
    # 添加依赖文件
    if current_os == "windows":
        cmd.append("--add-data=tax_calculator.py;.")
    else:
        cmd.append("--add-data=tax_calculator.py:.")
    
    # 添加主程序文件
    cmd.append("tax_calculator_gui.py")
    
    # 执行构建命令
    try:
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print("构建成功！可执行文件位于 dist 目录中。")
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    
    return True

def create_spec_file():
    """创建spec文件，用于跨平台构建"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tax_calculator_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('tax_calculator.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='个人所得税计算器2025',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    with open("个人所得税计算器2025.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("已创建spec文件: 个人所得税计算器2025.spec")

if __name__ == "__main__":
    # 创建spec文件
    create_spec_file()
    
    # 构建可执行文件
    build_windows_exe() 