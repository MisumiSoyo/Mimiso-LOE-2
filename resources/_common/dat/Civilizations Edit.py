#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Civilizations 变更处理器
读取官方 civilizations.json, 按 civ_changes.json 的指令增删改文明条目,
输出到模组目录的 civilizations.json。

change 格式 (与 ctt_changes.json 风格一致):
{
    "changes": [
        {
            "note": "备注, 可选",
            "action": "modify",          // modify / add / delete
            "civ_id": "JURCHENS",        // tech_tree_name, 支持列表或 "all"
            "name_string_id": 10322,     // modify: 其余键值直接写入条目
            ...
        },
        {
            "action": "add",
            "position": "after",         // last(默认) / first / before / after
            "target_id": "JURCHENS",     // position 为 before/after 时的参照文明
            "internal_name": "...",      // add: 其余键值组成新文明条目
            "tech_tree_name": "...",
            ...
        },
        {
            "action": "delete",
            "civ_id": ["XXX"]
        }
    ]
}

civ_id 优先按 tech_tree_name 精确匹配, 其次按 internal_name 忽略大小写匹配。
"""

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from paths import OFFICIAL_CIVILIZATIONS_FILE, CIV_CHANGES_FILE, OUTPUT_CIVILIZATIONS_FILE

os.chdir(Path(__file__).parent)

# change 中的控制字段, 不会作为文明属性写入
META_FIELDS = {"action", "civ_id", "note", "position", "target_id"}


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data, file_path):
    # 与官方 civilizations.json 保持一致: 2 空格缩进, 无末尾换行
    # (Windows 文本模式下 \n 自动写为 CRLF, 与官方文件行尾一致)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def normalize_civ_ids(civ_id):
    """civ_id 支持单个字符串或列表, 统一转成列表"""
    if isinstance(civ_id, list):
        return civ_id
    return [civ_id]


def civ_matches(civ, civ_id):
    """优先 tech_tree_name 精确匹配, 其次 internal_name 忽略大小写"""
    if civ.get("tech_tree_name") == civ_id:
        return True
    internal = civ.get("internal_name")
    return isinstance(internal, str) and internal.lower() == str(civ_id).lower()


def find_civs(civ_list, civ_id):
    """按一个 civ_id 找出所有匹配条目, "all" 匹配全部"""
    if civ_id == "all":
        return list(civ_list)
    return [civ for civ in civ_list if civ_matches(civ, civ_id)]


def resolve_index(civ_list, target_id):
    """解析 position 参照文明的下标, 找不到返回 None"""
    if target_id is None:
        return None
    for idx, civ in enumerate(civ_list):
        if civ_matches(civ, target_id):
            return idx
    return None


def apply_modify(civ_list, change):
    ids = normalize_civ_ids(change["civ_id"])
    updates = {k: v for k, v in change.items() if k not in META_FIELDS}
    if not updates:
        print("  Warning: modify 没有提供任何要修改的字段")
        return

    for civ_id in ids:
        targets = find_civs(civ_list, civ_id)
        if not targets:
            print(f"  Warning: 未找到文明 '{civ_id}', 跳过")
            continue
        for civ in targets:
            name = civ.get("tech_tree_name", civ_id)
            for key, value in updates.items():
                civ[key] = value
            print(f"  修改文明 {name}: {', '.join(updates.keys())}")


def apply_add(civ_list, change):
    new_civ = {k: v for k, v in change.items() if k not in META_FIELDS}

    missing = [f for f in ("internal_name", "tech_tree_name") if f not in new_civ]
    if missing:
        raise ValueError(f"add 缺少必填字段: {missing}")

    tech_tree_name = new_civ["tech_tree_name"]
    if any(civ.get("tech_tree_name") == tech_tree_name for civ in civ_list):
        print(f"  Warning: tech_tree_name '{tech_tree_name}' 已存在, 跳过添加")
        return

    position = change.get("position", "last")
    target_id = change.get("target_id")
    insert_index = len(civ_list)  # 默认 last

    if position == "first":
        insert_index = 0
    elif position in ("before", "after"):
        ref_index = resolve_index(civ_list, target_id)
        if ref_index is None:
            print(f"  Warning: 参照文明 '{target_id}' 未找到, 改为追加到末尾")
        else:
            insert_index = ref_index if position == "before" else ref_index + 1
    elif position != "last":
        print(f"  Warning: 未知 position '{position}', 改为追加到末尾")

    civ_list.insert(insert_index, new_civ)
    print(f"  添加文明 {tech_tree_name} (位置: {position})")


def apply_delete(civ_list, change):
    ids = normalize_civ_ids(change["civ_id"])
    to_remove = set()
    for civ_id in ids:
        targets = find_civs(civ_list, civ_id)
        if not targets:
            print(f"  Warning: 未找到文明 '{civ_id}', 跳过")
            continue
        for civ in targets:
            to_remove.add(id(civ))
            print(f"  删除文明 {civ.get('tech_tree_name', civ_id)}")
    if to_remove:
        civ_list[:] = [civ for civ in civ_list if id(civ) not in to_remove]


def apply_changes(base_data, changes):
    civ_list = base_data["civilization_list"]
    for i, change in enumerate(changes, 1):
        note = change.get("note")
        action = change.get("action", "").lower()
        print(f"[{i}/{len(changes)}] action: {action}" + (f" ({note})" if note else ""))

        if action == "modify":
            if "civ_id" not in change:
                print("  Warning: modify 缺少 civ_id, 跳过")
                continue
            apply_modify(civ_list, change)
        elif action == "add":
            apply_add(civ_list, change)
        elif action == "delete":
            if "civ_id" not in change:
                print("  Warning: delete 缺少 civ_id, 跳过")
                continue
            apply_delete(civ_list, change)
        else:
            raise NotImplementedError(f"不支持的 action: {action}")

    return base_data


def main():
    base_data = load_json_file(str(OFFICIAL_CIVILIZATIONS_FILE))
    changes_data = load_json_file(str(CIV_CHANGES_FILE))
    changes = changes_data.get("changes", [])

    print(f"已加载 {len(base_data['civilization_list'])} 个文明, {len(changes)} 条变更")
    apply_changes(base_data, changes)

    save_json_file(base_data, str(OUTPUT_CIVILIZATIONS_FILE))
    print(f"修改完成, 已保存到: {OUTPUT_CIVILIZATIONS_FILE}")
    print(f"当前文明数: {len(base_data['civilization_list'])}")


if __name__ == "__main__":
    main()
