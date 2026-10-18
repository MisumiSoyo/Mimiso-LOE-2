import sys
sys.dont_write_bytecode = True

import os
import subprocess
from pathlib import Path
from paths import get_tool_json_excludes

PROJECT_ROOT = Path(__file__).resolve().parent

SEVEN_ZIP_PATH = r"C:\Program Files\7-Zip\7z.exe"

EXCLUDE_DIRS = [
    ".git",
    "__pycache__",
    ".trae",
    "Mod Tools",
    "文档",
]

EXCLUDE_FILE_PATTERNS = [
    "*.py",
    "*.md",
    "Patch Notes.txt",
    ".gitignore",
    "*.code-workspace",
    "key-value-merge.txt",
    "*.doc",
    "*.docx",
    "*.xlsx",
] + get_tool_json_excludes()

def build_exclude_args():
    args = []
    for dir_name in EXCLUDE_DIRS:
        args.append(f"-xr!{dir_name}")
    for pattern in EXCLUDE_FILE_PATTERNS:
        args.append(f"-xr!{pattern}")
    return args

def run_7zip(command, cwd=None):
    print(f"执行命令: {' '.join(command)}")
    if cwd:
        print(f"工作目录: {cwd}")
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore', cwd=cwd)
    
    if result.returncode == 0:
        print("  成功！")
        return True
    else:
        print(f"  失败！错误码: {result.returncode}")
        if result.stderr:
            print("  错误输出:")
            print(result.stderr)
        return False

def main():
    print(f"项目根目录: {PROJECT_ROOT}")
    print("=" * 60)
    
    if not PROJECT_ROOT.exists():
        print(f"错误: 项目根目录不存在: {PROJECT_ROOT}")
        sys.exit(1)
    
    if not Path(SEVEN_ZIP_PATH).exists():
        print(f"错误: 7zip未找到: {SEVEN_ZIP_PATH}")
        print("请检查7zip安装路径是否正确")
        sys.exit(1)
    
    exclude_args = build_exclude_args()
    
    data_zip = PROJECT_ROOT / "Mimiso LOE 2.zip"
    ui_zip = PROJECT_ROOT / "[Text UI] Mimiso LOE 2.zip"
    
    if data_zip.exists():
        data_zip.unlink()
        print(f"已删除旧文件: {data_zip}")
    
    if ui_zip.exists():
        ui_zip.unlink()
        print(f"已删除旧文件: {ui_zip}")
    
    print("\n1. 打包数据模块 (resources/_common/) -> Mimiso LOE 2.zip")
    data_cmd = [
        SEVEN_ZIP_PATH,
        "a",
        "-tzip",
        "-mx5",
        "-r",
        str(data_zip),
        "resources\\_common",
    ] + exclude_args
    
    success1 = run_7zip(data_cmd, cwd=PROJECT_ROOT)
    
    print("\n2. 打包UI模块 (resources/en, resources/zh, widgetui) -> [Text UI] Mimiso LOE 2.zip")
    ui_cmd = [
        SEVEN_ZIP_PATH,
        "a",
        "-tzip",
        "-mx5",
        "-r",
        str(ui_zip),
        "resources\\en",
        "resources\\zh",
        "widgetui",
    ] + exclude_args
    
    success2 = run_7zip(ui_cmd, cwd=PROJECT_ROOT)
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("打包完成！")
        print(f"  数据模块: {data_zip}")
        print(f"  UI模块: {ui_zip}")
    else:
        print("打包失败！")
        sys.exit(1)
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()