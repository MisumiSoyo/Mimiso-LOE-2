#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dropsites 变更处理器
读取官方 dropsites.json, 按 dr_changes.json 的指令增删改存放点 (DropSite) 条目,
输出到模组目录的 dropsites.json (部署时覆盖游戏同名文件)。

官方文件结构:
{
    "drop_site_list": [
        {
            "name": "Saw Mill",                 # 开发用名 (必填, 参与条目身份)
            "building_id": 562,                  # 建筑 ID (必填, 参与条目身份)
            "worker_object_group": 4,           # 工人对象组: 4=村民, 21=渔船
            "worker_object_list": [2333, 2334], # 或指定工人单位 ID 列表 (与 group 二选一)
            "target_civs": [55],                # 限定文明索引 (列表顺序); 省略=所有文明
            "accepts_livestock": true,
            "auto_work": false,
            "target_list": [                    # 接受存放的资源来源
                {"name": "Trees", "object_group": 15, "attribute_type": 1}
            ],
            "update_ai_resource_types": [       # 通知 AI 的资源类型
                {"resource_type": 1}
            ]
        }
    ]
}

同一 building_id 可以有多条变体 (如码头 Dock 按村民/渔船/特定渔船 ID 有 3 条),
因此条目标的定位除 building_id 外还可用 name / worker_object_group /
worker_object_list / target_civs 进一步限定。target_civs 省略表示全文明通用条目。

dr_changes.json 格式 (与 ctt_changes.json / civ_changes.json 风格一致):
{
    "civ_groups": { "组名": ["VIKINGS", ...] },   // 可选, 定义文明组供 target_civs 引用
    "changes": [ ... ]
}
也兼容旧版直接写列表 [ ... ]。文明可写 tech_tree_name (如 "VIKINGS")、
civilization_list 顺序索引 (如 11) 或组名; 写 "all" 表示全文明 (输出时省略 target_civs)。

支持操作: add / modify / delete

1. add —— 新增存放点条目:
{
    "note": "备注, 可选",
    "action": "add",
    "name": "My Building",
    "building_id": 2500,
    "worker_object_group": 4,
    "target_list": [...],
    "position": "after",            // last(默认) / first / before / after
    "target": {"building_id": 109}  // before/after 的参照条目定位
}

2. modify —— 修改已有条目:
{
    "action": "modify",
    "building_id": 562,                          // 定位键 (必须提供 building_id)
    "name": "Saw Mill",                         // 可选定位键
    "worker_object_group": 4,                   // 可选定位键
    "worker_object_list": [...],                // 可选定位键
    "civs": "THRACIANS",                        // 可选定位键: 只选文明限定条目; "all"=只选通用条目
    "match": "first",                           // first(默认, 多命中报错) / all (全部改)
    "accepts_livestock": true,                  // 其余键直接写入条目 (标量覆盖)
    "target_civs": ["VIKINGS", "MALAY"],        // 数据字段: 重设文明归属; "all"=去掉限制变通用
    "target_list": [                            // 默认按 (name, object_group) 合并:
        {"name": "Trees", "object_group": 15}   //   已存在则更新字段, 不存在则追加
    ],
    "remove_targets": ["Oysters", 63],          // 从 target_list 删除项: 按 name 或 object_group
    "replace_target_list": true,                // target_list 整体替换而非合并
    "update_ai_resource_types": [{"resource_type": 1}],  // 默认按 resource_type 合并
    "remove_ai_resource_types": [3],            // 删除 AI 资源类型
    "replace_ai_resource_types": true           // 整体替换 update_ai_resource_types
}
定位用 "civs", 写入归属用 "target_civs", 二者分离:
如 {"building_id": 79, "civs": "THRACIANS", "target_civs": "all"} 表示
选中色雷斯专属塔条目并把它改为全文明通用。

3. delete —— 删除条目 (定位语义同 modify, 默认删除全部命中):
{
    "action": "delete",
    "building_id": 79,
    "civs": "THRACIANS"
}
"""

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from paths import (OFFICIAL_DROPSITES_FILE, OFFICIAL_CIVILIZATIONS_FILE,
                   DR_CHANGES_FILE, OUTPUT_DROPSITES_FILE)

os.chdir(Path(__file__).parent)

# change 中的控制字段, 不会作为条目属性写入
META_FIELDS = {
    "action", "type", "note", "match", "position", "target", "civs",
    "replace_target_list", "replace_ai_resource_types",
    "remove_targets", "remove_ai_resource_types",
}

# 定位键 (用于在 drop_site_list 中选择条目)
# 注意: 选择文明限定条目用 "civs"; "target_civs" 是数据字段 (modify 时写入)。
# 这样才能表达 "选中色雷斯专属条目再把它改成全文明通用" 这类文明归属变更。
MATCHER_KEYS = ("building_id", "name", "worker_object_group",
                "worker_object_list", "civs")


# ---------------------------------------------------------------- 基础 IO

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data, file_path):
    # 与官方 dropsites.json 一致: 4 空格缩进, 末尾换行
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')


# ---------------------------------------------------------------- 文明解析

def build_civ_index(civ_data):
    """构建 tech_tree_name / internal_name(lower) -> civilization_list 索引映射"""
    name_to_idx = {}
    for idx, civ in enumerate(civ_data.get("civilization_list", [])):
        ttn = civ.get("tech_tree_name")
        if ttn:
            name_to_idx[ttn] = idx
        internal = civ.get("internal_name")
        if internal:
            name_to_idx.setdefault(str(internal).lower(), idx)
    return name_to_idx


def resolve_civ_list(raw, civ_groups, name_to_idx, note=""):
    """把 target_civs 的值展开成有序去重的文明索引列表。

    支持: 整数索引, tech_tree_name/internal_name 字符串, 组名, 及上述的列表;
    "all" 返回 None 表示全文明 (条目中应省略 target_civs)。
    """
    if raw is None:
        return None
    if isinstance(raw, str) and raw == "all":
        return None

    items = raw if isinstance(raw, list) else [raw]
    resolved = []
    seen = set()

    def add(value, stack):
        if isinstance(value, str) and value in civ_groups:
            if value in stack:
                raise ValueError(f"civ_groups 存在循环引用: {' -> '.join(stack + [value])}")
            for member in civ_groups[value]:
                add(member, stack + [value])
            return
        if isinstance(value, bool):  # bool 是 int 子类, 提前拦截
            raise ValueError(f"target_civs 不接受布尔值: {value!r} (note: {note})")
        if isinstance(value, int):
            idx = value
        elif isinstance(value, str):
            if value not in name_to_idx:
                print(f"  Warning: 未知文明 '{value}', 按原样透传 (note: {note})")
                resolved.append(value)  # 保留原值, 不参与 int 去重
                return
            idx = name_to_idx[value]
        else:
            raise ValueError(f"target_civs 元素必须是文明名或索引: {value!r} (note: {note})")
        if idx not in seen:
            seen.add(idx)
            resolved.append(idx)

    for value in items:
        add(value, [])
    return resolved


def resolve_target_civs(raw, civ_groups, name_to_idx, note=""):
    """解析 target_civs 字段值; None/"all" -> None (全文明)"""
    return resolve_civ_list(raw, civ_groups, name_to_idx, note)


# ---------------------------------------------------------------- 条目定位

def _civs_equal(entry, civ_indices):
    """条目自身 target_civs 与给定文明索引列表是否相同集合"""
    entry_civs = entry.get("target_civs")
    if civ_indices is None:
        return entry_civs is None
    if entry_civs is None:
        return False
    return set(entry_civs) == set(civ_indices)


def entry_matches(entry, matcher, civ_groups, name_to_idx):
    """按定位键判断条目是否命中。matcher 中提供的键全部相等才算命中;
    target_civs="all" 表示只匹配无 target_civs 的通用条目。"""
    for key in MATCHER_KEYS:
        if key not in matcher or matcher[key] is None:
            continue
        if key == "building_id":
            wanted = matcher[key]
            wanted = wanted if isinstance(wanted, list) else [wanted]
            if entry.get("building_id") not in wanted:
                return False
        elif key in ("worker_object_group", "name"):
            if entry.get(key) != matcher[key]:
                return False
        elif key == "worker_object_list":
            if entry.get(key) != matcher[key]:
                return False
        elif key == "civs":
            wanted = resolve_civ_list(matcher[key], civ_groups, name_to_idx)
            if not _civs_equal(entry, wanted):
                return False
    return True


def find_entries(drop_list, matcher, civ_groups, name_to_idx):
    return [i for i, ds in enumerate(drop_list)
            if entry_matches(ds, matcher, civ_groups, name_to_idx)]


def matcher_from_change(change):
    """从 change 提取定位键; building_id 必填"""
    matcher = {k: change[k] for k in MATCHER_KEYS if k in change and change[k] is not None}
    return matcher


def describe_entry(entry):
    """生成条目简述用于日志"""
    parts = [f"id={entry.get('building_id')}", entry.get("name", "?")]
    if "worker_object_group" in entry:
        parts.append(f"group={entry['worker_object_group']}")
    if "worker_object_list" in entry:
        parts.append(f"workers={entry['worker_object_list']}")
    if entry.get("target_civs"):
        parts.append(f"civs={entry['target_civs']}")
    return " ".join(parts)


# ---------------------------------------------------------------- 校验

def validate_entry(entry):
    if "building_id" not in entry:
        raise ValueError(f"条目缺少必填字段 building_id: {entry}")
    if "name" not in entry:
        raise ValueError(f"条目缺少必填字段 name: {entry}")
    for target in entry.get("target_list", []):
        if "name" not in target or "object_group" not in target:
            raise ValueError(f"target_list 项缺少 name/object_group: {target}")
    for res in entry.get("update_ai_resource_types", []):
        if "resource_type" not in res:
            raise ValueError(f"update_ai_resource_types 项缺少 resource_type: {res}")


# ---------------------------------------------------------------- target_list 合并

def _target_key(target):
    return (target.get("name"), target.get("object_group"))


def merge_target_list(existing_targets, new_targets):
    """按 (name, object_group) 合并资源项: 已存在则字段覆盖, 不存在追加"""
    merged = [dict(t) for t in existing_targets]
    index = {_target_key(t): i for i, t in enumerate(merged)}
    for new_t in new_targets:
        key = _target_key(new_t)
        if key in index:
            merged[index[key]].update(new_t)
        else:
            merged.append(dict(new_t))
            index[key] = len(merged) - 1
    return merged


def remove_targets(existing_targets, removers):
    """按 name (字符串) 或 object_group (整数) 删除资源项; 字典按 (name,object_group) 精确删"""
    result = []
    for t in existing_targets:
        drop = False
        for rm in removers:
            if isinstance(rm, str) and t.get("name") == rm:
                drop = True
                break
            if isinstance(rm, int) and not isinstance(rm, bool) \
                    and t.get("object_group") == rm:
                drop = True
                break
            if isinstance(rm, dict) \
                    and _target_key(t) == _target_key(rm):
                drop = True
                break
        if not drop:
            result.append(t)
    return result


def merge_ai_types(existing, new_types):
    """按 resource_type 合并 AI 资源类型"""
    merged = [dict(r) for r in existing]
    known = {r.get("resource_type") for r in merged}
    for new_r in new_types:
        if new_r.get("resource_type") not in known:
            merged.append(dict(new_r))
            known.add(new_r.get("resource_type"))
    return merged


# ---------------------------------------------------------------- 操作

def build_entry_from_change(change, civ_groups, name_to_idx):
    """从 change 的非控制字段构造新条目, 解析 target_civs"""
    entry = {k: v for k, v in change.items()
             if k not in META_FIELDS and v is not None}

    if "target_civs" in entry:
        civs = resolve_target_civs(entry["target_civs"], civ_groups, name_to_idx,
                                   change.get("note", ""))
        if civs is None:
            entry.pop("target_civs")  # "all" -> 通用条目
        else:
            entry["target_civs"] = civs
    validate_entry(entry)
    return entry


def apply_add(drop_list, change, civ_groups, name_to_idx):
    entry = build_entry_from_change(change, civ_groups, name_to_idx)

    # 完全相同身份的条目已存在时警告 (building_id+name+worker变体+target_civs)
    dup_matcher = {k: entry[k] for k in ("building_id", "name") if k in entry}
    if "worker_object_group" in entry:
        dup_matcher["worker_object_group"] = entry["worker_object_group"]
    if "worker_object_list" in entry:
        dup_matcher["worker_object_list"] = entry["worker_object_list"]
    if "target_civs" in entry:
        dup_matcher["civs"] = entry["target_civs"]  # 已是解析后的索引列表
    if find_entries(drop_list, dup_matcher, civ_groups, name_to_idx):
        print(f"  Warning: 已存在相同身份条目, 仍按指令重复添加: {describe_entry(entry)}")

    position = (change.get("position") or "last").lower()
    if position in ("before", "after"):
        target = change.get("target")
        if not target:
            raise ValueError(f"position={position} 必须提供 target 定位参照条目")
        hits = find_entries(drop_list, target, civ_groups, name_to_idx)
        if not hits:
            raise ValueError(f"position 参照条目未找到: {target}")
        idx = hits[0]
        drop_list.insert(idx + 1 if position == "after" else idx, entry)
    elif position == "first":
        drop_list.insert(0, entry)
    else:
        if position != "last":
            print(f"  Warning: 未知 position '{position}', 按 last 处理")
        drop_list.append(entry)
    print(f"  add: {describe_entry(entry)}")


def apply_modify(drop_list, change, civ_groups, name_to_idx):
    matcher = matcher_from_change(change)
    if "building_id" not in matcher:
        raise ValueError(f"modify 必须提供 building_id 作为定位 (note: {change.get('note', '')})")

    hits = find_entries(drop_list, matcher, civ_groups, name_to_idx)
    if not hits:
        print(f"  Warning: modify 未命中任何条目: {matcher} (note: {change.get('note', '')})")
        return
    match_mode = change.get("match", "first")
    if len(hits) > 1 and match_mode != "all":
        raise ValueError(
            f"modify 命中 {len(hits)} 个条目, 请补充 name/worker_object_group/"
            f"worker_object_list/civs 限定, 或设置 \"match\": \"all\":\n  "
            + "\n  ".join(describe_entry(drop_list[i]) for i in hits))

    # 数据字段 (标量直接写入; 两个列表有专门合并语义)
    scalar_fields = {k: v for k, v in change.items()
                     if k not in META_FIELDS
                     and k not in ("target_list", "update_ai_resource_types")
                     and v is not None}

    for idx in hits:
        entry = drop_list[idx]
        for key, value in scalar_fields.items():
            if key == "target_civs":
                civs = resolve_target_civs(value, civ_groups, name_to_idx,
                                           change.get("note", ""))
                if civs is None:
                    entry.pop("target_civs", None)  # "all" -> 恢复通用
                else:
                    entry["target_civs"] = civs
            else:
                entry[key] = value

        # target_list: 删除 -> (整体替换 | 合并)
        if "remove_targets" in change:
            entry["target_list"] = remove_targets(entry.get("target_list", []),
                                                  change["remove_targets"])
        if "target_list" in change and change["target_list"] is not None:
            if change.get("replace_target_list"):
                entry["target_list"] = [dict(t) for t in change["target_list"]]
            else:
                entry["target_list"] = merge_target_list(entry.get("target_list", []),
                                                         change["target_list"])

        # update_ai_resource_types: 删除 -> (整体替换 | 合并)
        if "remove_ai_resource_types" in change:
            rm = set(change["remove_ai_resource_types"])
            entry["update_ai_resource_types"] = [
                r for r in entry.get("update_ai_resource_types", [])
                if r.get("resource_type") not in rm]
        if "update_ai_resource_types" in change and change["update_ai_resource_types"] is not None:
            if change.get("replace_ai_resource_types"):
                entry["update_ai_resource_types"] = [dict(r) for r in change["update_ai_resource_types"]]
            else:
                entry["update_ai_resource_types"] = merge_ai_types(
                    entry.get("update_ai_resource_types", []),
                    change["update_ai_resource_types"])

        validate_entry(entry)
        print(f"  modify: {describe_entry(entry)}")


def apply_delete(drop_list, change, civ_groups, name_to_idx):
    matcher = matcher_from_change(change)
    if not matcher:
        raise ValueError("delete 必须至少提供一个定位键 (building_id/name/worker_*/target_civs)")
    hits = set(find_entries(drop_list, matcher, civ_groups, name_to_idx))
    if not hits:
        print(f"  Warning: delete 未命中任何条目: {matcher} (note: {change.get('note', '')})")
        return
    for idx in sorted(hits, reverse=True):
        print(f"  delete: {describe_entry(drop_list[idx])}")
        del drop_list[idx]


# ---------------------------------------------------------------- 主流程

def load_changes(changes_file):
    """读取 dr_changes.json, 兼容 {"civ_groups":..., "changes":[...]} 与裸列表两种格式"""
    data = load_json_file(changes_file)
    if isinstance(data, list):
        return {}, data
    if isinstance(data, dict):
        return data.get("civ_groups", {}), data.get("changes", [])
    raise ValueError(f"{changes_file} 顶层必须是列表或对象")


def main():
    base_data = load_json_file(str(OFFICIAL_DROPSITES_FILE))
    civ_data = load_json_file(str(OFFICIAL_CIVILIZATIONS_FILE))
    civ_groups, changes = load_changes(str(DR_CHANGES_FILE))
    name_to_idx = build_civ_index(civ_data)

    drop_list = base_data["drop_site_list"]
    print(f"官方 dropsites 条目数: {len(drop_list)}, 改动指令: {len(changes)} 条")

    for i, change in enumerate(changes, 1):
        action = (change.get("action") or change.get("type") or "add").lower()
        note = change.get("note", "")
        print(f"[{i}/{len(changes)}] {action}  {note}")

        if action == "add":
            apply_add(drop_list, change, civ_groups, name_to_idx)
        elif action == "modify":
            apply_modify(drop_list, change, civ_groups, name_to_idx)
        elif action == "delete":
            apply_delete(drop_list, change, civ_groups, name_to_idx)
        else:
            raise ValueError(f"不支持的操作类型: {action} (note: {note})")

    save_json_file(base_data, str(OUTPUT_DROPSITES_FILE))
    print(f"\n完成! 输出条目数: {len(drop_list)} -> {OUTPUT_DROPSITES_FILE}")

    try:
        input("按回车键退出...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
