#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文明图标材质注入器

读取模组输出的 civilizations.json, 找出 internal_name 以 "Ezs" 开头的 EZS 文明,
将其对应的文明图标材质条目追加到 materials.json (不删除原版条目)。

每个 EZS 文明新增以下材质 (emblem 暂不处理):
  1. 大厅文明选择菜单图标 <Name>Icon
     - MaterialDef:  Type=Atlas, Blend=InverseAlpha, AtlasRef=defaultwidgets
     - AtlasTexture: textures/menu/civs/<lower>.png
  2. 科技树按钮三态 IconsMenuTechtree<Name>{,Hover,Pressed}
     - MaterialDef:  Type=Atlas, Blend=InverseAlpha, AtlasRef=ingameicons
     - AtlasTexture: textures/ingame/icons/civ_techtree_buttons/menu_techtree_<lower>{,_hover,_pressed}.png

UV 坐标 (imageTLX/TLY/BRX/BRY) 暂用占位值; 实际坐标由 build_atlas.ps1
读取 materials.json 后用 texassemble 重新打包 atlas DDS 时回写。
重复运行安全: 已存在的 RefName / MaterialDef.Name 会被更新而非重复添加。
"""

import copy
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (OFFICIAL_MATERIALS_FILE, OUTPUT_MATERIALS_FILE,
                   OUTPUT_CIVILIZATIONS_FILE)

os.chdir(Path(__file__).parent)

# EZS 文明 internal_name 前缀
EZS_PREFIX = "Ezs"

# 占位 UV 坐标 (与 Icons and Materials Editor.py 的默认值一致)
DEFAULT_COORDS = {
    "imageTLX": "0.037109",
    "imageTLY": "0.740813",
    "imageBRX": "0.074002",
    "imageBRY": "0.777705",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    # 与官方 materials.json 保持一致: 2 空格缩进
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_ezs_civ(civ):
    name = civ.get("internal_name", "")
    return isinstance(name, str) and name.startswith(EZS_PREFIX)


def upsert_material(materials_list, name, atlas_ref):
    """在 Materials 列表中新增或更新一个 MaterialDef"""
    new_material = {
        "MaterialDef": {
            "Name": name,
            "Type": "Atlas",
            "Blend": "InverseAlpha",
            "TextureRef": name,
            "AtlasRef": atlas_ref,
        }
    }
    for i, m in enumerate(materials_list):
        if m.get("MaterialDef", {}).get("Name") == name:
            materials_list[i] = new_material
            return False  # 已存在, 更新
    materials_list.append(new_material)
    return True  # 新增


def upsert_atlas_texture(materials_data, atlas_name, ref_name, file_name):
    """在指定 atlas 的 Textures 中新增或更新一条纹理"""
    for atlas in materials_data.get("AtlasTextures", []):
        if atlas.get("AtlasDef", {}).get("Name") == atlas_name:
            textures = atlas["AtlasDef"]["Textures"]
            for tex in textures:
                if tex.get("RefName") == ref_name:
                    tex.update({"RefName": ref_name, "FileName": file_name, **DEFAULT_COORDS})
                    return False
            textures.append({"RefName": ref_name, "FileName": file_name, **DEFAULT_COORDS})
            return True
    print(f"  警告: 未找到 atlas '{atlas_name}'")
    return False


def add_civ_icons(materials_data, internal_name):
    """为一个 EZS 文明注入菜单图标 + 科技树按钮三态材质。
    返回 (新增数, 更新数)。"""
    added, updated = 0, 0
    lower = internal_name.lower()

    # 1. 大厅文明选择菜单图标
    menu_mat_name = f"{internal_name}Icon"
    menu_file = f"textures/menu/civs/{lower}.png"
    if upsert_material(materials_data["Materials"], menu_mat_name, "defaultwidgets"):
        added += 1
    else:
        updated += 1
    if upsert_atlas_texture(materials_data, "defaultwidgets", menu_mat_name, menu_file):
        added += 1
    else:
        updated += 1

    # 2. 科技树按钮三态
    for suffix, file_suffix in (("", ""), ("Hover", "_hover"), ("Pressed", "_pressed")):
        btn_mat_name = f"IconsMenuTechtree{internal_name}{suffix}"
        btn_file = f"textures/ingame/icons/civ_techtree_buttons/menu_techtree_{lower}{file_suffix}.png"
        if upsert_material(materials_data["Materials"], btn_mat_name, "ingameicons"):
            added += 1
        else:
            updated += 1
        if upsert_atlas_texture(materials_data, "ingameicons", btn_mat_name, btn_file):
            added += 1
        else:
            updated += 1

    return added, updated


def main():
    civs_data = load_json(str(OUTPUT_CIVILIZATIONS_FILE))

    # 优先读取模组已有的 materials.json (保留其他编辑器如 Icons and Materials Editor 的改动),
    # 不存在时回退到官方 materials.json 作为基底
    source_materials = OUTPUT_MATERIALS_FILE if OUTPUT_MATERIALS_FILE.exists() else OFFICIAL_MATERIALS_FILE
    materials_data = load_json(str(source_materials))
    print(f"基底 materials.json: {source_materials}")

    ezs_civs = [c for c in civs_data.get("civilization_list", []) if is_ezs_civ(c)]
    if not ezs_civs:
        print(f"未在 {OUTPUT_CIVILIZATIONS_FILE} 中找到 EZS 文明 (internal_name 以 '{EZS_PREFIX}' 开头), 跳过")
        return

    print(f"找到 {len(ezs_civs)} 个 EZS 文明, 开始注入文明图标材质...")
    total_added, total_updated = 0, 0
    for civ in ezs_civs:
        name = civ["internal_name"]
        tech_tree = civ.get("tech_tree_name", "?")
        a, u = add_civ_icons(materials_data, name)
        total_added += a
        total_updated += u
        print(f"  {tech_tree} -> {name}: 新增 {a} 条, 更新 {u} 条")

    save_json(materials_data, str(OUTPUT_MATERIALS_FILE))
    print(f"\n完成: materials.json 已保存到 {OUTPUT_MATERIALS_FILE}")
    print(f"合计: 新增 {total_added} 条, 更新 {total_updated} 条 (每文明 8 条 = 1 菜单图标 + 3 按钮材质 + 3 按钮纹理 + 1 菜单纹理)")


if __name__ == "__main__":
    main()
