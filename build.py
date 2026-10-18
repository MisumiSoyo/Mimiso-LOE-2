import sys
sys.dont_write_bytecode = True

import shutil
from pathlib import Path
from paths import get_tool_json_excludes

PROJECT_ROOT = Path(__file__).resolve().parent

MODS_LOCAL_PATH = Path(r"C:\Users\20725\Games\Age of Empires 2 DE\76561199076107470\mods\local")

# 与 package.py 一致: 分为数据模组和 UI 文本模组
DATA_MOD_NAME = "Mimiso LOE 2"
UI_MOD_NAME = "[Text UI] Mimiso LOE 2"

# 各模组包含的内容 (相对 PROJECT_ROOT), 与 package.py 的 7z 打包范围一致
# info.json 由游戏加载模组时自动生成, 不随模组分发
DATA_MOD_ITEMS = [
    "resources/_common",
]
UI_MOD_ITEMS = [
    "resources/en",
    "resources/zh",
    "widgetui",
]

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
    "*.doc",
    "*.docx",
    "*.xlsx",
] + get_tool_json_excludes()


def sync_mod(mod_name, items):
    """删除目标模组目录后按 items 重新复制, 等价于原 robocopy /PURGE 语义"""
    target_root = MODS_LOCAL_PATH / mod_name
    if target_root.exists():
        shutil.rmtree(target_root)

    ignore = shutil.ignore_patterns(*EXCLUDE_DIRS, *EXCLUDE_FILE_PATTERNS)
    count = 0
    for item in items:
        src = PROJECT_ROOT / item
        dst = target_root / item
        if not src.exists():
            print(f"  警告: 源不存在, 跳过: {item}")
            continue
        if src.is_dir():
            shutil.copytree(src, dst, ignore=ignore)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        count += 1
        print(f"  已复制: {item}")
    return count


def main():
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"本地模组根目录: {MODS_LOCAL_PATH}")
    print("=" * 60)

    if not PROJECT_ROOT.exists():
        print(f"错误: 项目根目录不存在: {PROJECT_ROOT}")
        sys.exit(1)

    if not MODS_LOCAL_PATH.exists():
        print(f"错误: 模组目录不存在: {MODS_LOCAL_PATH}")
        sys.exit(1)

    print(f"\n1. 部署数据模组 ({DATA_MOD_NAME}): resources/_common")
    data_count = sync_mod(DATA_MOD_NAME, DATA_MOD_ITEMS)

    print(f"\n2. 部署UI文本模组 ({UI_MOD_NAME}): resources/en, resources/zh, widgetui")
    ui_count = sync_mod(UI_MOD_NAME, UI_MOD_ITEMS)

    print("\n" + "=" * 60)
    print("构建完成！")
    print(f"  数据模组: {MODS_LOCAL_PATH / DATA_MOD_NAME} ({data_count} 项)")
    print(f"  UI模组: {MODS_LOCAL_PATH / UI_MOD_NAME} ({ui_count} 项)")

    try:
        input("按回车键退出...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
