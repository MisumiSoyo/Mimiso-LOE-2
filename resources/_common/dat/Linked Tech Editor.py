import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from paths import OFFICIAL_LINKED_TECHS_FILE, LT_CHANGES_FILE, OUTPUT_LINKED_TECHS_FILE

os.chdir(Path(__file__).parent)

def load_json_file(file_path):
    """加载JSON文件并返回内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(data, file_path):
    """将数据保存到JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_linked_techs(base_data, changes):
    """根据修改指令添加一组相关的科技"""
    # 需要排除的字段：note 用于备注，action 用于控制指令
    excluded_fields = {"note", "action"}

    for change in changes:
        if change.get("action") == "add":
            if "note" in change:
                print(f"Note: {change['note']}")

            # 复制 change 中除排除字段外的所有内容；NameId 不再自动生成，
            # 有提供则原样写入，没有则该条目不带 NameId
            new_tech_group = {k: v for k, v in change.items() if k not in excluded_fields}

            base_data["LinkedTechs"].append(new_tech_group)
    return base_data

def main():
    # 加载原始游戏数据文件
    base_data = load_json_file(str(OFFICIAL_LINKED_TECHS_FILE))

    # 加载修改指令文件
    changes = load_json_file(str(LT_CHANGES_FILE))

    # 根据修改指令修改游戏数据
    modified_data = add_linked_techs(base_data, changes)

    # 保存修改后的数据到新文件
    save_json_file(modified_data, str(OUTPUT_LINKED_TECHS_FILE))

    print(f"修改完成，已保存到文件：{OUTPUT_LINKED_TECHS_FILE}")

if __name__ == "__main__":
    main()
