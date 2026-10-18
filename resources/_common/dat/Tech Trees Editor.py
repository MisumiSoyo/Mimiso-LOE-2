"""
统一科技树/未来可用物品编辑器
读取 ctt_changes.json 一份改动文件, 同时生成:
  1. CivTechTrees/*.json (文明科技树, 下称 CTT)
  2. futuravailableunits.json (未来可用物品显示, 下称 FAU)

改动格式:
- CTT 风格 (含 "civ_id"): 默认同时作用于 CTT 与 FAU ("apply_to": "both"),
  可用 "apply_to": "ctt" 限定只改 CTT。FAU 仅改动请使用 FAU 风格。
- FAU 风格 (含 "civilizations"): 沿用旧 fau_changes.json 格式, 只作用于 FAU,
  无需提供 CTT 必需字段。
- 顶层 "includes": ["其他 JSON"] 可引用外部改动文件 (如 techtrees.json, 路径相对
  本文件所在目录), 其 changes/civ_groups 按引用顺序追加/合并到本文件的改动之后。

CTT 操作: add / modify / move / delete / replace / deleteciv / template / disable / enable / sync_from_dat
- sync_from_dat: 按 dat 实际值重置科技树节点的 Name String ID / Help String ID /
  Picture Index (对应 dat 的 language_dll_name / language_dll_help / icon_id),
  跳过 dat 中 language_dll_name 为 0 的空对象; 只改 CTT, 不动 FAU。
  可用 "node_ids": [...] 限定对象 (缺省=全部节点), "exclude": [...] 排除对象。
- template: 以指定文明科技树为模板覆盖目标文明:
    1. 所有 Node Status 为 NotAvailable 的节点改为启用: 有前置要求
       (Prerequisite IDs/Types 含非空项) 置 ResearchRequired, 否则置
       ResearchedCompleted;
    2. 移除 Node Type 含 Unique 的节点; 含 Regional 的节点默认一并移除,
       可用 "exclude_regional": false 保留 (此时 FAU 参照池中的区域条目也保留);
    3. FAU 以 FullTechCiv 为全量参照池按结果科技树整体重建:
       池中条目 (含 trigger tech、Prereq* 字段、列表顺序) 原样借用,
       池外的模组新增节点回退为 CTT 派生条目。
       注意 template 会重建整个文明的 FAU, FAU 风格改动须排在 template 之后。
- disable: 将目标节点 Node Status 改为 NotAvailable, 同时删除其 FAU 条目;
    目标的 Trigger Tech ID 对应科技一并从 FAU 删除 ("remove_trigger": false 可关闭),
    "affect_fau": false 可仅改 CTT 状态而不动 FAU。
    推荐写法 "UnitIDs": [...] / "TechIDs": [...] 各自数组: Unit 含 Building
    (同属单位 ID 空间, 在单位与建筑列表中同时查找), Tech 单列避免与单位 ID
    撞号 (如 12/77)。兼容旧写法 "Node ID" + "Use Type"。
- enable: disable 的逆操作 —— 将目标节点置为启用并补回 FAU 条目 (条目从 CTT
    节点派生, 含 trigger tech); 可在原版科技树基础上启用某科技/单位。
    Node Status 分两种: 有前置要求 (Prerequisite IDs/Types 两数组含非空项) 置
    ResearchRequired, 无前置要求置 ResearchedCompleted。
    目标 ID 写法同 disable, "affect_fau": false 可只改 CTT。
- add/replace: FAU 条目自动从节点派生 (ID/Name/RequiredAge=Age ID/所在建筑=Building ID),
    可用 "FAU": {...} 指定额外 FAU 属性 (如 RequiredTech);
    Trigger Tech ID != -1 时自动在 FAU 同建筑 Techs 写入该科技,
    "fau_trigger": false 可排除 (按节点变体生效, 同 Node ID 的多建筑变体互不影响)。
    同一 Node ID 允许多个节点 (多建筑生产, 如城堡/兵营), FAU 各写入所属建筑。
    新节点可省略常用字段, 自动补默认值: Draw Node Type 按 Use Type 派生,
    Trigger Tech ID=-1; Name String ID / Help String ID / Picture Index 未显式
    给出时读取 dat 实际值 (language_dll_name / language_dll_help / icon_id),
    dat 查不到时回退 Help String ID=Name String ID+100000;
    Prerequisite IDs/Types 未指定时不写入。
- delete: 同时删除 FAU 条目与其 Trigger Tech (同样可用 "remove_trigger": false 关闭)。
- modify: Node Status 改动同步 FAU 增删 (NotAvailable→删, 启用→增);
    Age ID 改动同步 FAU 既有条目的 RequiredAge;
    Building ID 标量写入且实际改变时同步 FAU 跨建筑移动 (条目从旧建筑删除、
    按节点新建筑补回; 单位的 Trigger Tech 一并移动); Building ID 为列表时仅作过滤。

FAU 同步采用"增量记录"模型: 只增删改动波及的条目, 不做全量镜像,
以保持与官方 FAU 既有约定 (如升时代科技不列入、基础建筑不挂 Builder 等) 一致。

第三产出 unitlines.json (AI 兵种线):
add/replace 单位节点可带 "UnitLine": <负数 LineID> 声明该单位所属兵种线;
不带该字段的节点不挂任何兵种线。
同一 LineID 的节点按在本文件中的出现顺序组成 IDChain (基础单位天然写在更靠前),
同一 Node ID 跨文明重复出现时自动去重 (如魏武卒出现在两个文明的条目中);
add 取 Node ID, replace 取 new_node_id (即模组新单位 ID)。
两种归属:
- 引用官方既有线 (LineID 已存在于官方 unitlines.json): 把新成员并入该线的
  IDChain 输出, 不新增条目, Name/Identifier/Building 沿用官方定义;
  "UnitLineBuilding" 必须与官方线的 Building 标记一致。
  默认并入链尾; 带 "UnitLineIndex": 0 等整数时插入官方链指定下标
  (用于把新的基础形态插到官方链首, 如早期长矛兵 → 长矛兵线)。
- LOE 新线 (LineID 不在官方文件中): Name 取链上第一个节点的 Name,
  输出为 "LOE <Name> Line"; Identifier 由 Name 派生为 "loe-<slug>-line"。
建筑线 (整链都是 UniqueBuilding 等) 才加 "UnitLineBuilding": true。
LineID 必须严格位于 (-400, -199);
引用官方线用其既有 LineID, LOE 新线从 -397 起避开官方 ID。
只有一个成员的 LOE 新链 (如火牛、韩卒) 在输出阶段过滤, 不写入 unitlines.json;
标注保留在 ctt_changes.json 中, 将来若追加精锐变体将自动成链。
"""

import json
import copy
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from paths import (OFFICIAL_CIVTECHTREES_FOLDER, CTT_CHANGES_FILE, OUTPUT_CIVTECHTREES_FOLDER,
                   OFFICIAL_FUTUR_AVAILABLE_UNITS_FILE, OUTPUT_FUTUR_AVAILABLE_UNITS_FILE,
                   OFFICIAL_UNITLINES_FILE, OUTPUT_UNITLINES_FILE,
                   OFFICIAL_CIVILIZATIONS_FILE, OUTPUT_CIVILIZATIONS_FILE,
                   OUTPUT_DATA_FILE)

os.chdir(Path(__file__).parent)

BUILDER_ID = 118  # FAU 中"建筑工"建筑 ID, 可建造建筑挂在其 Units 下
AGE_UP_TECH_IDS = {101, 102, 103}  # 升时代科技按官方约定不收录进 FAU
# CTT civ_id (全大写) 到 FAU 文明键名的特殊映射, 其余按 title() 规则转换
FAU_NAME_SPECIAL = {"MAGYAR": "Magyars"}

CTT_CONTROL_FIELDS = {"action", "civ_id", "position", "target_id", "target_type", "note",
                      "apply_to", "FAU", "fau_trigger", "remove_trigger", "affect_fau",
                      "new_node_id", "template_id", "exclude_regional",
                      "UnitLine", "UnitLineBuilding", "UnitLineIndex",
                      "node_ids", "exclude"}
FAU_META_FIELDS = {"civilizations", "note", "type", "building_id", "unit_id", "tech_id",
                   "position", "target_id"}


# ---------------------------------------------------------------- dat 读取

_DAT_CACHE = None


def get_dat():
    """惰性加载项目 dat (fork 事实源, 即 OUTPUT_DATA_FILE)。
    用于读取节点文本 ID / 图标的 dat 实际值。"""
    global _DAT_CACHE
    if _DAT_CACHE is None:
        from genieutils.datfile import DatFile
        _DAT_CACHE = DatFile.parse(str(OUTPUT_DATA_FILE))
    return _DAT_CACHE


def dat_node_info(node_id, use_type):
    """从 dat 读取对象的 (Name String ID, Help String ID, Picture Index)。
    Unit/Building 查 civs[0].units[node_id], Tech 查 techs[node_id]。
    对象不存在或 language_dll_name 为 0 (空对象) 时返回 None;
    Help/Icon 缺失时对应位置为 None (不回退)。"""
    if node_id is None:
        return None
    data = get_dat()
    try:
        if use_type == "Tech":
            obj = data.techs[node_id]
        else:  # Unit / Building 同属单位 ID 空间
            obj = data.civs[0].units[node_id]
    except (IndexError, AttributeError, TypeError):
        return None
    name_sid = getattr(obj, "language_dll_name", 0) or 0
    if name_sid == 0:
        return None
    help_sid = getattr(obj, "language_dll_help", 0) or None
    icon = getattr(obj, "icon_id", None)
    return name_sid, help_sid, icon


# ---------------------------------------------------------------- 基础 IO

def load_civs_from_folder(folder_path):
    """从 CivTechTrees 文件夹加载所有文明数据"""
    civs = []
    civ_files = {}
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")
    for json_file in folder.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            civ_data = json.load(f)
        if isinstance(civ_data, dict) and "civ_id" in civ_data:
            civs.append(civ_data)
            civ_files[civ_data["civ_id"]] = json_file.name
        elif isinstance(civ_data, list):
            for civ in civ_data:
                if "civ_id" in civ:
                    civs.append(civ)
                    civ_files[civ["civ_id"]] = json_file.name
    return {"civs": civs}, civ_files


def save_civs_to_folder(output_folder, civs_data, civ_files_mapping):
    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)
    for civ in civs_data["civs"]:
        civ_id = civ["civ_id"]
        file_name = civ_files_mapping.get(civ_id, f"{civ_id}.json")
        with open(folder / file_name, 'w', encoding='utf-8') as f:
            json.dump(civ, f, indent=4, ensure_ascii=False)


def fau_civ_name(civ_id, fau_data, internal_name_map=None):
    """CTT civ_id -> FAU 键名; 该文明不在 FAU 中时返回 None。

    internal_name_map 为 tech_tree_name -> internal_name 映射时优先按映射查找
    (不再依赖大小写转换); 否则回退到 .title() 规则 (含 MAGYAR 特例)。"""
    if internal_name_map is not None:
        name = internal_name_map.get(civ_id)
        if name is not None:
            return name if name in fau_data else None
    name = FAU_NAME_SPECIAL.get(civ_id, civ_id.title())
    return name if name in fau_data else None


def build_internal_name_map(civs_data):
    """从 civilizations.json 数据构建 tech_tree_name -> internal_name 映射。"""
    return {c.get("tech_tree_name"): c.get("internal_name")
            for c in civs_data.get("civilization_list", [])
            if c.get("tech_tree_name") and c.get("internal_name")}


# ---------------------------------------------------------------- 参照池

def build_pool(fau_data):
    """以 FullTechCiv 为全量参照池: {(kind, entry_id): (池中建筑ID, 条目, 列表内顺序索引)}
    FullTechCiv 收录所有通用单位/科技/建筑 (含各文明单独缺失的条目),
    且字段 (Prereq*/RequiredUnitID) 与顺序均为官方标准。"""
    pool = {}
    ft = fau_data.get("FullTechCiv", {})
    for b in ft.get("Buildings", []):
        bid = b["ID"]
        if bid == BUILDER_ID:
            for idx, u in enumerate(b.get("Units", [])):
                pool[("Building", u["ID"])] = (bid, u, idx)
        else:
            for idx, u in enumerate(b.get("Units", [])):
                pool.setdefault(("Unit", u["ID"]), (bid, u, idx))
            for idx, t in enumerate(b.get("Techs", [])):
                pool.setdefault(("Tech", t["ID"]), (bid, t, idx))
    return pool


def build_regional_ids(civs_data):
    """扫描所有文明科技树, 收集 Node Type 含 Regional 的节点 ID:
    {"Unit": set, "Tech": set, "Building": set}。
    用于 template 排除区域条目; 须在应用 changes 前对官方数据调用。"""
    result = {"Unit": set(), "Tech": set(), "Building": set()}
    for civ in civs_data["civs"]:
        for node in civ.get("civ_techs_units", []):
            if "Regional" in node.get("Node Type", ""):
                use_type = node.get("Use Type")
                if use_type in ("Unit", "Tech"):
                    result[use_type].add(node["Node ID"])
        for node in civ.get("civ_techs_buildings", []):
            if "Regional" in node.get("Node Type", ""):
                result["Building"].add(node["Node ID"])
    return result


def derive_entry(node, kind, units=None):
    """从 CTT 节点派生 FAU 条目 (池外条目回退用)"""
    entry = {"ID": node["Node ID"], "Name": node.get("Name", ""), "RequiredAge": node.get("Age ID", 1)}
    if kind == "Unit":
        fill_required_unit(entry, node, units)
    return entry


def fill_required_unit(entry, node, units):
    """条目缺 RequiredUnitID 时按 CTT Link ID 回填; units 值为变体列表"""
    if "RequiredUnitID" in entry or units is None:
        return
    link_id = node.get("Link ID", -1)
    variants = units.get(link_id)
    if link_id != -1 and variants \
            and any(v.get("Node Status") != "NotAvailable" for v in variants):
        entry["RequiredUnitID"] = link_id


def borrow_entry(pool, node, kind, units=None):
    """优先借用 FullTechCiv 池中的官方条目; RequiredAge 以 CTT 节点为准,
    缺失的 RequiredUnitID 按 Link ID 回填; 池外节点回退为 CTT 派生条目。"""
    p = pool.get((kind, node["Node ID"]))
    if p is not None:
        entry = copy.deepcopy(p[1])
        entry["RequiredAge"] = node.get("Age ID", entry.get("RequiredAge", 1))
        if kind == "Unit":
            fill_required_unit(entry, node, units)
        return entry, p[2]
    return derive_entry(node, kind, units), None


# ---------------------------------------------------------------- 状态跟踪

def get_state(states, civ_id):
    return states.setdefault(civ_id, {
        "touched": False,                      # CTT 被改动且需要同步 FAU
        "added": {"Unit": set(), "Tech": set(), "Building": set()},
        "removed": {"Unit": set(), "Tech": set(), "Building": set()},
        "excluded_triggers": set(),            # fau_trigger: false 排除的节点 (id(node)), 按变体生效
        "moved_triggers": set(),               # modify Building ID 移动时豁免 re-add skip
        "fau_overrides": {},                   # (kind, node_id) -> 额外 FAU 属性
        "fau_positions": {},                   # (kind, node_id) -> (position, target_id), 新增条目插入位置
    })


def node_kind(use_type):
    return use_type if use_type in ("Unit", "Tech", "Building") else None


def find_node(civ, use_type, node_id):
    """按 Use Type 在 CTT 中查找节点"""
    if use_type in ("Unit", "Tech"):
        for item in civ["civ_techs_units"]:
            if item["Node ID"] == node_id and item.get("Use Type") == use_type:
                return item
    elif use_type == "Building":
        for item in civ["civ_techs_buildings"]:
            if item["Node ID"] == node_id:
                return item
    return None


def record_add_fau(state, use_type, item, change):
    """add/replace 生成新节点后, 记录 FAU 侧新增"""
    kind = node_kind(use_type)
    if kind is None:
        return
    state["added"][kind].add(item["Node ID"])
    state["removed"][kind].discard(item["Node ID"])
    fau_extra = change.get("FAU")
    if fau_extra:
        state["fau_overrides"][(kind, item["Node ID"])] = fau_extra
    if "position" in change:
        state["fau_positions"][(kind, item["Node ID"])] = \
            (change["position"], change.get("target_id"))
    trigger = item.get("Trigger Tech ID", -1)
    if trigger != -1 and change.get("fau_trigger", True) is False:
        state["excluded_triggers"].add(id(item))


def record_remove_fau(state, civ, use_type, node_ids, remove_trigger=True):
    """delete/replace/disable 移除节点后, 记录 FAU 侧删除"""
    kind = node_kind(use_type)
    if kind is None:
        return
    for nid in node_ids:
        state["removed"][kind].add(nid)
        state["added"][kind].discard(nid)
        if remove_trigger:
            node = find_node(civ, use_type, nid)
            if node is not None:
                trigger = node.get("Trigger Tech ID", -1)
                if trigger != -1:
                    state["removed"]["Tech"].add(trigger)


def rebuild_fau_from_pool(civ, pool, excluded_triggers=frozenset(), exclude_ids=None):
    """template 专用: 以 FullTechCiv 参照池按结果 CTT 整体重建一个文明的 FAU。
    池中条目深拷贝借用 (保持官方字段与顺序), 池外节点回退为 CTT 派生条目。
    exclude_ids 为 build_regional_ids 形式的 {"Unit"/"Tech"/"Building": set} 时,
    名单内 ID 一律不收录 (区域单位排除用)。
    返回新的 {"Buildings": [...]} 结构。"""
    units, techs, blds = {}, {}, {}
    for n in civ["civ_techs_units"]:
        if n.get("Use Type") == "Unit":
            # 同一 Node ID 可有多建筑变体, 保留全部 (fill_required_unit 依赖列表结构)
            units.setdefault(n["Node ID"], []).append(n)
        elif n.get("Use Type") == "Tech":
            techs[n["Node ID"]] = n
    for n in civ["civ_techs_buildings"]:
        blds[n["Node ID"]] = n

    new_fau = {"Buildings": []}
    bmap = {}

    def ensure_building(bid, name="", age=1):
        b = bmap.get(bid)
        if b is None:
            b = {"ID": bid, "Name": name, "Techs": [], "Units": []}
            bmap[bid] = b
            new_fau["Buildings"].append(b)
        return b

    # 建筑: 所有启用建筑建立独立条目; Builder Units 仅收录池中有的建筑 (官方约定)
    excluded_blds = exclude_ids["Building"] if exclude_ids else frozenset()
    for n in civ["civ_techs_buildings"]:
        if n.get("Node Status") == "NotAvailable" or n["Node ID"] in excluded_blds:
            continue
        ensure_building(n["Node ID"], n.get("Name", ""), n.get("Age ID", 1))
    builder = ensure_building(BUILDER_ID, "Builder", 1)
    for n in civ["civ_techs_buildings"]:
        if n.get("Node Status") == "NotAvailable" or n["Node ID"] in excluded_blds:
            continue
        p = pool.get(("Building", n["Node ID"]))
        if p is not None:
            builder["Units"].append(copy.deepcopy(p[1]))
    builder["Units"].sort(key=lambda u: pool[("Building", u["ID"])][2])

    # 单位与科技: 按 CTT 节点的 Building ID 放置, 池中有则借池条目
    staged = {}  # (bid, list_key) -> {entry_id: (顺序索引或None, entry)}
    for n in civ["civ_techs_units"]:
        if n.get("Node Status") == "NotAvailable":
            continue
        kind = n.get("Use Type")
        if kind not in ("Unit", "Tech"):
            continue
        if exclude_ids and n["Node ID"] in exclude_ids[kind]:
            continue
        if kind == "Tech" and n["Node ID"] in AGE_UP_TECH_IDS:
            continue
        bid = n.get("Building ID")
        if bid in (None, -1):
            continue
        p = pool.get((kind, n["Node ID"]))
        if p is not None:
            entry, idx = borrow_entry(pool, n, kind, units)
        else:
            entry, idx = derive_entry(n, kind, units), None
        bnode = blds.get(bid)
        ensure_building(bid, bnode.get("Name", "") if bnode else "",
                        bnode.get("Age ID", 1) if bnode else 1)
        list_key = "Units" if kind == "Unit" else "Techs"
        staged.setdefault((bid, list_key), {})[n["Node ID"]] = (idx, entry)

    # trigger tech: 启用单位/建筑的 Trigger Tech ID 写入同建筑 Techs
    trigger_sources = [(n, n.get("Building ID"), "Unit") for n in civ["civ_techs_units"]
                       if n.get("Use Type") == "Unit"]
    trigger_sources += [(n, n["Node ID"], "Building") for n in civ["civ_techs_buildings"]]
    for n, bid, kind in trigger_sources:
        if n.get("Node Status") == "NotAvailable":
            continue
        trigger = n.get("Trigger Tech ID", -1)
        if trigger == -1 or id(n) in excluded_triggers:
            continue
        if exclude_ids and trigger in exclude_ids["Tech"]:
            continue
        p = pool.get(("Tech", trigger))
        if p is not None:
            entry, idx = copy.deepcopy(p[1]), p[2]
            entry["RequiredAge"] = n.get("Age ID", entry.get("RequiredAge", 1))
        else:
            entry, idx = {"ID": trigger, "Name": n.get("Name", ""),
                          "RequiredAge": n.get("Age ID", 1)}, None
        if bid in bmap:
            staged.setdefault((bid, "Techs"), {}).setdefault(trigger, (idx, entry))

    # 落盘: 池中条目按池顺序排前, 池外条目排尾
    for (bid, list_key), entries in staged.items():
        ordered = sorted(entries.values(),
                         key=lambda ie: (ie[0] is None, ie[0] if ie[0] is not None else 0))
        bmap[bid][list_key] = [e for _, e in ordered]
    return new_fau


# ---------------------------------------------------------------- CTT 通用工具

def move_item_in_list(target_list, item, position="last", target_id=None, search_list=None, target_type=None):
    if item in target_list:
        target_list.remove(item)
    insert_position = len(target_list)
    position = position.lower() if position else "last"
    if position == "first":
        insert_position = 0
    elif position in ["before", "after"] and target_id is not None:
        lookup_list = search_list if search_list is not None else target_list
        for idx, existing_item in enumerate(lookup_list):
            if existing_item.get("Node ID") == target_id:
                if target_type is None or existing_item.get("Use Type") == target_type:
                    insert_position = idx if position == "before" else idx + 1
                    break
    target_list.insert(insert_position, item)
    return insert_position


def resolve_search_list(civ, target_list, target_type):
    if target_type in ("Unit", "Tech"):
        return civ["civ_techs_units"]
    if target_type == "Building":
        return civ["civ_techs_buildings"]
    return target_list


def use_type_matches(item, use_type):
    return (item.get("Use Type") == use_type
            or (item.get("Use Type") == "Building" and use_type == "Unit"))


# ---------------------------------------------------------------- CTT 操作

def group_members(defn):
    """取 civ_groups 组定义中的所有成员 token (供未知成员校验)。"""
    if isinstance(defn, list):
        return list(defn)
    if isinstance(defn, dict):
        tokens = []
        for key in ("include", "exclude"):
            value = defn.get(key)
            if value is None:
                continue
            tokens.extend(value if isinstance(value, list) else [value])
        return tokens
    return []


def load_changes_with_includes(path):
    """加载改动文件, 并把顶层 "includes" 引用的外部 JSON 的 changes/civ_groups
    合并进来 (被引用文件的改动排在本文件之后, 与 dat 侧 inputs.py 约定一致)。
    include 路径相对被加载文件所在目录解析。只解析顶层 includes, 不递归。"""
    with open(str(path), 'r', encoding='utf-8-sig') as f:
        changes = json.load(f)
    base_dir = Path(path).resolve().parent
    for include in changes.get("includes", []):
        include_file = Path(include)
        if not include_file.is_absolute():
            include_file = base_dir / include_file
        with open(str(include_file), 'r', encoding='utf-8-sig') as f:
            included = json.load(f)
        changes.setdefault("changes", []).extend(included.get("changes", []))
        for name, defn in included.get("civ_groups", {}).items():
            changes.setdefault("civ_groups", {}).setdefault(name, defn)
    return changes


def expand_civ_group(name_or_def, civ_groups, all_civ_ids, stack=(), note=""):
    """把 civ_groups 组定义展开成有序去重的具体文明 ID 列表。

    组定义支持两种写法:
      显式列表  ["FRANKS", "VIKINGS"]              成员可为具体文明或嵌套组名
      对象      {"all": true, "include": [...], "exclude": [...]}
        all       基础是否含全部文明 (缺省 false)
        include   基础附加的具体文明/组 (缺省空)
        exclude   从基础中排除的具体文明/组 (缺省空)
    all/include/exclude 三个键均可省略或组合; 仅写 exclude 而未给 all/include 时,
    基础取全部文明 (即 "全部文明排除若干")。组名可嵌套引用其他组 (循环引用报错)。
    """
    all_civ_ids = all_civ_ids or []
    known = set(all_civ_ids)

    if isinstance(name_or_def, str):
        if name_or_def in civ_groups:
            if name_or_def in stack:
                raise ValueError(f"civ_groups 存在循环引用: {' -> '.join(stack + (name_or_def,))}")
            return expand_civ_group(civ_groups[name_or_def], civ_groups, all_civ_ids,
                                    stack + (name_or_def,), note)
        if name_or_def == "all":
            return list(all_civ_ids)
        if name_or_def not in known:
            print(f"  Warning: civ_id '{name_or_def}' 不是已知文明或 civ_groups 组名, "
                  f"按具体 ID 透传 (note: {note})")
        return [name_or_def]

    if isinstance(name_or_def, list):
        result, seen = [], set()
        for token in name_or_def:
            for cid in expand_civ_group(token, civ_groups, all_civ_ids, stack, note):
                if cid not in seen:
                    seen.add(cid)
                    result.append(cid)
        return result

    if isinstance(name_or_def, dict):
        include = name_or_def.get("include") or []
        exclude = name_or_def.get("exclude") or []
        if name_or_def.get("all") or (not include and exclude):
            base = list(all_civ_ids)
        else:
            base = []
        seen = set(base)
        for token in (include if isinstance(include, list) else [include]):
            for cid in expand_civ_group(token, civ_groups, all_civ_ids, stack, note):
                if cid not in seen:
                    seen.add(cid)
                    base.append(cid)
        removed = set()
        for token in (exclude if isinstance(exclude, list) else [exclude]):
            removed.update(expand_civ_group(token, civ_groups, all_civ_ids, stack, note))
        return [cid for cid in base if cid not in removed]

    raise ValueError(f"非法 civ_groups 定义: {name_or_def!r}")


def resolve_civ_ids(raw, civ_groups, all_civ_ids, note=""):
    """把一条 change 的 civ_id 展开成具体文明 ID 列表 (保序去重)。

    支持的写法:
      "FRANKS"                 单个具体文明 ID
      "all"                    全部文明 (延迟到应用阶段处理)
      ["JURCHENS", "VIKINGS"]  显式列表
      "模组文明"                引用顶层 civ_groups 中定义的组 (列表或对象形式)
    列表元素可混用组名与具体 ID; 组定义中也允许嵌套引用其他组 (循环引用报错)。
    未知名 (非 all、非组名、非官方文明 ID) 只警告不中断, 避免拼错组名时静默落空。
    """
    civ_groups = civ_groups or {}
    all_civ_ids = all_civ_ids or []
    known = set(all_civ_ids)
    items = raw if isinstance(raw, list) else [raw]
    resolved = []
    seen = set()

    for value in items:
        if isinstance(value, dict) or (isinstance(value, str) and value in civ_groups):
            for cid in expand_civ_group(value, civ_groups, all_civ_ids, (), note):
                if cid not in seen:
                    seen.add(cid)
                    resolved.append(cid)
            continue
        if value != "all" and value not in known:
            print(f"  Warning: civ_id '{value}' 不是已知文明或 civ_groups 组名, "
                  f"按具体 ID 透传 (note: {note})")
        if value not in seen:
            seen.add(value)
            resolved.append(value)
    return resolved


def apply_template(change, civs_data, civ_files, states, fau_data, pool, regional_ids, internal_name_map):
    """template: 以模板文明科技树覆盖目标文明"""
    template_id = change.get("template_id")
    if not template_id:
        raise ValueError("template 操作必须提供 template_id")
    src = next((c for c in civs_data["civs"] if c["civ_id"] == template_id), None)
    if src is None:
        print(f"  Warning: template 源文明 {template_id} 不存在, 跳过")
        return
    civ_ids = change["civ_id"] if isinstance(change["civ_id"], list) else [change["civ_id"]]
    affect_fau = change.get("apply_to", "both") != "ctt"
    exclude_regional = change.get("exclude_regional", True)

    for civ_id in civ_ids:
        new_civ = copy.deepcopy(src)
        new_civ["civ_id"] = civ_id
        stripped = []
        newly_enabled = []
        for list_key in ("civ_techs_units", "civ_techs_buildings"):
            kind = "Building" if list_key == "civ_techs_buildings" else "Unit"
            kept = []
            for node in new_civ[list_key]:
                node_type = node.get("Node Type", "")
                if "Unique" in node_type or (exclude_regional and "Regional" in node_type):
                    stripped.append(node)
                    continue
                if node.get("Node Status") == "NotAvailable":
                    node["Node Status"] = "ResearchRequired" if has_prerequisite(node) else "ResearchedCompleted"
                    newly_enabled.append((kind, node))
                kept.append(node)
            new_civ[list_key] = kept

        # 替换或新增文明条目
        existing = next((c for c in civs_data["civs"] if c["civ_id"] == civ_id), None)
        if existing is not None:
            idx = civs_data["civs"].index(existing)
            civs_data["civs"][idx] = new_civ
        else:
            civs_data["civs"].append(new_civ)

        if affect_fau:
            state = get_state(states, civ_id)
            state["touched"] = True
            # 重建已体现"启用全部+剔除独特", 此前的增量记录清零
            for kind in ("Unit", "Tech", "Building"):
                state["added"][kind].clear()
                state["removed"][kind].clear()
            if change.get("fau_trigger", True) is False:
                for kind, node in newly_enabled:
                    if node.get("Trigger Tech ID", -1) != -1:
                        state["excluded_triggers"].add(id(node))

            # FAU 以 FullTechCiv 参照池按结果 CTT 整体重建
            dst_fau_name = fau_civ_name(civ_id, fau_data, internal_name_map)
            if dst_fau_name:
                fau_data[dst_fau_name] = rebuild_fau_from_pool(
                    new_civ, pool, state["excluded_triggers"],
                    regional_ids if exclude_regional else None)
        regional_note = "排除区域条目" if exclude_regional else "保留区域条目"
        print(f"  template: {template_id} -> {civ_id}, 启用 {len(newly_enabled)} 个节点, "
              f"移除 {len(stripped)} 个独特/区域节点 ({regional_note})")


def parse_switch_ids(change):
    """解析 enable/disable 的目标 ID, 返回 (unit_ids, tech_ids) 两个集合。
    推荐写法: "UnitIDs": [...] / "TechIDs": [...] 各自数组。Unit 含 Building
    (同属单位 ID 空间); Tech 与单位 ID 可能撞号 (如 12/77), 故单列避免误伤。
    便捷写法: "IDs": [...] 同时匹配单位/建筑与科技两个 ID 空间 (撞号时可能同时命中);
    兼容旧写法: "Node ID" + "Use Type" (Unit/Tech/Building 或其列表)。"""
    unit_ids = set(change.get("UnitIDs") or [])
    tech_ids = set(change.get("TechIDs") or [])
    both_ids = set(change.get("IDs") or [])
    unit_ids |= both_ids
    tech_ids |= both_ids
    if "Node ID" in change:
        nid = change["Node ID"]
        node_ids = set(nid if isinstance(nid, list) else [nid])
        use_types = change.get("Use Type", [])
        if isinstance(use_types, str):
            use_types = [use_types]
        if any(ut in ("Unit", "Building") for ut in use_types):
            unit_ids |= node_ids
        if "Tech" in use_types:
            tech_ids |= node_ids
    return unit_ids, tech_ids


def apply_disable(change, civ, state, affect_fau):
    """disable: CTT 置 NotAvailable + FAU 删除条目与 trigger tech。
    推荐写法: "UnitIDs": [...] / "TechIDs": [...] 各自数组; 便捷写法 "IDs": [...]
    (同时匹配单位/建筑与科技)。兼容旧写法: "Node ID" + "Use Type"。
    "remove_trigger": false 可关闭 trigger tech 连带删除;
    "affect_fau": false 可仅改 CTT 状态而不动 FAU。"""
    unit_ids, tech_ids = parse_switch_ids(change)
    if not unit_ids and not tech_ids:
        print(f"  Warning: disable 缺少 UnitIDs/TechIDs/IDs 或有效的 Use Type, 跳过: {change.get('note', '')}")
        return
    remove_trigger = change.get("remove_trigger", True)
    hit_fau = affect_fau and change.get("affect_fau", True)
    hits = 0
    for item in civ["civ_techs_units"] + civ["civ_techs_buildings"]:
        nid = item["Node ID"]
        if nid not in unit_ids and nid not in tech_ids:
            continue
        item_type = item.get("Use Type")
        if item_type in ("Unit", "Building"):
            if nid not in unit_ids:
                continue
        elif item_type == "Tech":
            if nid not in tech_ids:
                continue
        else:
            continue
        item["Node Status"] = "NotAvailable"
        hits += 1
        if hit_fau:
            state["removed"][item_type].add(nid)
            state["added"][item_type].discard(nid)
            if remove_trigger:
                trigger = item.get("Trigger Tech ID", -1)
                if trigger != -1:
                    state["removed"]["Tech"].add(trigger)
    if hits < len(unit_ids | tech_ids):
        print(f"  Warning: disable 仅命中 {hits}/{len(unit_ids | tech_ids)} 个节点 "
              f"(UnitIDs {sorted(unit_ids)} / TechIDs {sorted(tech_ids)})")


def has_prerequisite(item):
    """节点是否存在真实前置要求: "Prerequisite IDs"/"Prerequisite Types" 两数组中
    含非空项即为有 (None/-1/0、"None"/空串视为占位空值)。"""
    prereq_ids = item.get("Prerequisite IDs") or []
    prereq_types = item.get("Prerequisite Types") or []
    if any(v not in (None, -1, 0) for v in prereq_ids):
        return True
    if any(v not in (None, -1, "", "None") for v in prereq_types):
        return True
    return False


def apply_enable(change, civ, state, affect_fau):
    """enable: disable 的逆操作 —— 启用节点 + FAU 新增条目
    (条目从 CTT 节点派生, 含 trigger tech), 可在原版科技树基础上启用某科技/单位。
    有前置要求 (Prerequisite IDs/Types 含非空项) 的节点置 ResearchRequired,
    否则置 ResearchedCompleted。
    目标 ID 解析同 disable ("UnitIDs"/"TechIDs"/"IDs" 或 "Node ID" + "Use Type")。
    "affect_fau": false 可仅改 CTT 状态而不动 FAU。
    注意: 若目标所在建筑本身为 NotAvailable, FAU 不写入该条目 (与 sync_fau 一致)。"""
    unit_ids, tech_ids = parse_switch_ids(change)
    if not unit_ids and not tech_ids:
        print(f"  Warning: enable 缺少 UnitIDs/TechIDs/IDs 或有效的 Use Type, 跳过: {change.get('note', '')}")
        return
    hit_fau = affect_fau and change.get("affect_fau", True)
    hits = 0
    for item in civ["civ_techs_units"] + civ["civ_techs_buildings"]:
        nid = item["Node ID"]
        if nid not in unit_ids and nid not in tech_ids:
            continue
        item_type = item.get("Use Type")
        if item_type in ("Unit", "Building"):
            if nid not in unit_ids:
                continue
        elif item_type == "Tech":
            if nid not in tech_ids:
                continue
        else:
            continue
        item["Node Status"] = "ResearchRequired" if has_prerequisite(item) else "ResearchedCompleted"
        hits += 1
        if hit_fau:
            state["added"][item_type].add(nid)
            state["removed"][item_type].discard(nid)
    if hits < len(unit_ids | tech_ids):
        print(f"  Warning: enable 仅命中 {hits}/{len(unit_ids | tech_ids)} 个节点 "
              f"(UnitIDs {sorted(unit_ids)} / TechIDs {sorted(tech_ids)})")


def apply_node_defaults(item, target_list=None):
    """为 add/replace 的新节点补默认字段 (change 中显式给出的不覆盖):
    - Draw Node Type 按 Use Type 派生 (Building→Building, 其余→UnitTech);
    - Node Type 按 Use Type 派生 (Unit→Unit, Tech→Research, Building→BuildingNonTech);
      升级单位/独特/区域变体须显式写 Node Type 覆盖;
    - Link 规则 (对照官方科技树统计): 不给 Link ID = 线内第一个 (挂建筑),
      Link Node Type 默认 BuildingTech; 给了 Link ID 但没给 Link Node Type =
      连线到该单位/科技, 自动取目标节点的 Node Type; 两个都显式给出 =
      只排版到目标下方, 不连线 (Link Node Type 一般写 BuildingTech);
    - Trigger Tech ID = -1; Help String ID = Name String ID + 100000
      (游戏自动 -79000 换算)。Prerequisite IDs/Types 未指定时不写入;
    - Name String ID / Help String ID / Picture Index 未显式指定时读取 dat
      实际值 (language_dll_name / language_dll_help / icon_id);
      dat 查不到时回退: Help = Name + 100000。"""
    if "Draw Node Type" not in item:
        item["Draw Node Type"] = "Building" if item.get("Use Type") == "Building" else "UnitTech"
    if "Node Type" not in item:
        use_type = item.get("Use Type")
        item["Node Type"] = {"Unit": "Unit", "Tech": "Research"}.get(use_type, "BuildingNonTech")
    if "Link Node Type" not in item:
        link_type = None
        link_id = item.get("Link ID")
        if link_id not in (None, -1) and target_list:
            ref = next((n for n in target_list if n.get("Node ID") == link_id), None)
            if ref is not None:
                link_type = ref.get("Node Type")
        item["Link Node Type"] = link_type or "BuildingTech"
    item.setdefault("Trigger Tech ID", -1)
    info = dat_node_info(item.get("Node ID"), item.get("Use Type"))
    if info is not None:
        name_sid, help_sid, icon = info
        item.setdefault("Name String ID", name_sid)
        if help_sid is not None:
            item.setdefault("Help String ID", help_sid)
        if icon is not None:
            item.setdefault("Picture Index", icon)
    if "Help String ID" not in item:
        name_sid = item.get("Name String ID")
        if name_sid is not None:
            item["Help String ID"] = name_sid + 100000


def apply_ctt_change(change, civs_data, civ_files, states, fau_data, pool, regional_ids, internal_name_map):
    action = change["action"]
    apply_to = change.get("apply_to", "both")
    if apply_to == "fau":
        print(f"  Warning: civ_id 风格改动不支持 apply_to=fau, 请改用 civilizations 风格书写, 已跳过: {change.get('note', '')}")
        return
    affect_fau = apply_to != "ctt"
    civ_ids = change["civ_id"] if isinstance(change["civ_id"], list) else [change["civ_id"]]
    use_type = change.get("Use Type", "")

    if action == "deleteciv":
        civs_data["civs"] = [c for c in civs_data["civs"] if c["civ_id"] not in civ_ids]
        for cid in civ_ids:
            civ_files.pop(cid, None)
            if affect_fau:
                name = fau_civ_name(cid, fau_data, internal_name_map)
                if name:
                    del fau_data[name]
        return

    if action == "template":
        apply_template(change, civs_data, civ_files, states, fau_data, pool, regional_ids, internal_name_map)
        return

    for civ_id in civ_ids:
        target_civs = civs_data["civs"] if civ_id == "all" else \
            [c for c in civs_data["civs"] if c["civ_id"] == civ_id]

        for civ in target_civs:
            state = get_state(states, civ["civ_id"])
            if affect_fau:
                state["touched"] = True

            if action == "disable":
                apply_disable(change, civ, state, affect_fau)
                continue

            if action == "enable":
                apply_enable(change, civ, state, affect_fau)
                continue

            if action == "sync_from_dat":
                node_ids = change.get("node_ids")
                if node_ids is not None and not isinstance(node_ids, list):
                    node_ids = [node_ids]
                exclude = set(change.get("exclude", []))
                synced = 0
                for lst in (civ["civ_techs_units"], civ["civ_techs_buildings"]):
                    for node in lst:
                        nid = node["Node ID"]
                        if node_ids is not None and nid not in node_ids:
                            continue
                        if nid in exclude:
                            continue
                        info = dat_node_info(nid, node.get("Use Type"))
                        if info is None:
                            continue
                        name_sid, help_sid, icon = info
                        node["Name String ID"] = name_sid
                        if help_sid is not None:
                            node["Help String ID"] = help_sid
                        if icon is not None:
                            node["Picture Index"] = icon
                        synced += 1
                print(f"  {civ['civ_id']}: sync_from_dat 重置 {synced} 个节点")
                continue

            if use_type in ("Unit", "Tech"):
                target_list = civ["civ_techs_units"]
            elif use_type == "Building":
                target_list = civ["civ_techs_buildings"]
            else:
                continue

            if action == "add":
                new_item = {k: v for k, v in change.items() if k not in CTT_CONTROL_FIELDS}
                apply_node_defaults(new_item, target_list)
                building_ids = new_item.get("Building ID")
                if isinstance(building_ids, list):
                    add_items = []
                    for bid in building_ids:
                        item_copy = copy.deepcopy(new_item)
                        item_copy["Building ID"] = bid
                        add_items.append(item_copy)
                else:
                    add_items = [new_item]
                position = change.get("position", "last").lower()
                target_id = change.get("target_id")
                target_type = change.get("target_type")
                search_list = resolve_search_list(civ, target_list, target_type)
                insert_position = len(target_list)
                if position == "first":
                    insert_position = 0
                elif position in ["before", "after"] and target_id is not None:
                    for idx, item in enumerate(search_list):
                        if item["Node ID"] == target_id:
                            if target_type is None or item.get("Use Type") == target_type:
                                insert_position = idx if position == "before" else idx + 1
                                break
                for offset, item_to_add in enumerate(add_items):
                    target_list.insert(insert_position + offset, item_to_add)
                    if affect_fau:
                        record_add_fau(state, use_type, item_to_add, change)

            elif action == "modify":
                node_ids = change["Node ID"] if isinstance(change["Node ID"], list) else [change["Node ID"]]
                position = change.get("position")
                target_id = change.get("target_id")
                target_type = change.get("target_type")
                building_filter = change.get("Building ID")
                building_filter = building_filter if isinstance(building_filter, list) else None
                search_list = resolve_search_list(civ, target_list, target_type) if target_type else None
                status_change = change.get("Node Status")

                for node_id in node_ids:
                    for item in target_list:
                        if item["Node ID"] == node_id and use_type_matches(item, use_type) \
                                and (building_filter is None or item.get("Building ID") in building_filter):
                            old_bid = item.get("Building ID")
                            old_trigger = item.get("Trigger Tech ID", -1)
                            for key, value in change.items():
                                if key not in CTT_CONTROL_FIELDS and key != "Node ID" \
                                        and not (key == "Building ID" and building_filter is not None):
                                    item[key] = value
                            # Age ID 改动同步 FAU 既有条目的 RequiredAge
                            if affect_fau and "Age ID" in change:
                                fname = fau_civ_name(civ["civ_id"], fau_data, internal_name_map)
                                if fname:
                                    list_key = "Techs" if use_type == "Tech" else "Units"
                                    for b in fau_data[fname].get("Buildings", []):
                                        for e in b.get(list_key, []):
                                            if e.get("ID") == node_id:
                                                e["RequiredAge"] = change["Age ID"]
                            if affect_fau and status_change is not None:
                                kind = node_kind(use_type)
                                if status_change == "NotAvailable":
                                    state["removed"][kind].add(node_id)
                                    state["added"][kind].discard(node_id)
                                else:
                                    state["added"][kind].add(node_id)
                                    state["removed"][kind].discard(node_id)
                            # Building ID 标量写入且实际改变: 同步 FAU 跨建筑移动
                            # (removed+added 同时记录, sync_fau 先全局删再按新建筑重加;
                            #  trigger tech 随单位移动, 靠 moved_triggers 豁免第四遍 skip)
                            if affect_fau and building_filter is None and "Building ID" in change \
                                    and item.get("Building ID") != old_bid:
                                kind = node_kind(use_type)
                                state["removed"][kind].add(node_id)
                                if item.get("Node Status") != "NotAvailable":
                                    state["added"][kind].add(node_id)
                                # 仅旧 trigger 进 removed (新 trigger 可能靠 explicit FAU add
                                # 在同 change 立即落地, 进 removed 会被 sync 第一遍误删);
                                # 新 trigger 只进 moved_triggers 作第四遍 skip 豁免
                                new_trigger = item.get("Trigger Tech ID", -1)
                                if old_trigger not in (-1, None):
                                    state["removed"]["Tech"].add(old_trigger)
                                    state["moved_triggers"].add(old_trigger)
                                if new_trigger not in (-1, None) and new_trigger != old_trigger:
                                    state["moved_triggers"].add(new_trigger)
                            if position is not None:
                                move_item_in_list(target_list, item, position, target_id, search_list, target_type)
                            break

            elif action == "move":
                node_ids = change["Node ID"] if isinstance(change["Node ID"], list) else [change["Node ID"]]
                position = change.get("position", "last").lower()
                target_id = change.get("target_id")
                target_type = change.get("target_type")
                search_list = resolve_search_list(civ, target_list, target_type)
                for node_id in node_ids:
                    for item in target_list:
                        if item["Node ID"] == node_id and use_type_matches(item, use_type):
                            move_item_in_list(target_list, item, position, target_id, search_list, target_type)
                            break

            elif action == "delete":
                node_ids = change["Node ID"] if isinstance(change["Node ID"], list) else [change["Node ID"]]
                if affect_fau:
                    record_remove_fau(state, civ, use_type, node_ids,
                                      remove_trigger=change.get("remove_trigger", True))
                node_id_set = set(node_ids)
                target_list[:] = [
                    item for item in target_list
                    if item["Node ID"] not in node_id_set or not use_type_matches(item, use_type)
                ]

            elif action == "replace":
                node_ids = change["Node ID"] if isinstance(change["Node ID"], list) else [change["Node ID"]]
                node_id_set = set(node_ids)
                new_node_id = change.get("new_node_id")
                if new_node_id is None:
                    raise ValueError("replace 操作必须提供 new_node_id 作为新条目的 Node ID")

                new_item = {k: v for k, v in change.items() if k not in CTT_CONTROL_FIELDS and k != "Node ID"}
                new_item["Node ID"] = new_node_id
                apply_node_defaults(new_item, target_list)
                building_ids = new_item.get("Building ID")
                if isinstance(building_ids, list):
                    add_items = []
                    for bid in building_ids:
                        item_copy = copy.deepcopy(new_item)
                        item_copy["Building ID"] = bid
                        add_items.append(item_copy)
                else:
                    add_items = [new_item]

                if affect_fau:
                    record_remove_fau(state, civ, use_type, node_ids,
                                      remove_trigger=change.get("remove_trigger", True))

                kept = []
                inplace_index = None
                for item in target_list:
                    if item.get("Node ID") in node_id_set and use_type_matches(item, use_type):
                        if inplace_index is None:
                            inplace_index = len(kept)
                    else:
                        kept.append(item)
                removed = len(target_list) - len(kept)
                if removed == 0:
                    print(f"  Warning: replace 未找到目标节点 {node_ids} (Use Type {use_type}), 仅执行添加")
                target_list[:] = kept

                explicit_position = change.get("position")
                if explicit_position is None:
                    insert_position = inplace_index if inplace_index is not None else len(target_list)
                else:
                    position = explicit_position.lower()
                    target_id = change.get("target_id")
                    target_type = change.get("target_type")
                    search_list = resolve_search_list(civ, target_list, target_type)
                    insert_position = len(target_list)
                    if position == "first":
                        insert_position = 0
                    elif position in ["before", "after"] and target_id is not None:
                        for idx, item in enumerate(search_list):
                            if item["Node ID"] == target_id:
                                if target_type is None or item.get("Use Type") == target_type:
                                    insert_position = idx if position == "before" else idx + 1
                                    break

                for offset, item_to_add in enumerate(add_items):
                    target_list.insert(insert_position + offset, item_to_add)
                    if affect_fau:
                        record_add_fau(state, use_type, item_to_add, change)
                print(f"  replace: 删除 {removed} 个节点 {node_ids}, 插入新节点 {new_node_id} x{len(add_items)} @ {insert_position}")


# ---------------------------------------------------------------- FAU 风格操作 (仅 FAU)

def resolve_fau_civs(change, fau_data, civ_groups=None, all_civ_ids=None, internal_name_map=None):
    """把一条 FAU change 的 civilizations 展开为 FAU 键名列表 (保序去重)。

    civilizations 支持: 单个 FAU 文明名 / CTT 文明 ID、'all'、列表,
    以及顶层 civ_groups 组名 (列表或对象形式) 与内联对象定义。
    组 / CTT 文明 ID 经 fau_civ_name 映射为 FAU 键名; 无对应 FAU 条目者跳过。
    """
    civ_groups = civ_groups or {}
    all_civ_ids = all_civ_ids or []
    raw = change.get('civilizations')
    if raw is None:
        print("Error: FAU change 缺少 'civilizations'。")
        return []
    tokens = raw if isinstance(raw, list) else [raw]

    result = []
    seen = set()

    def add_name(name):
        if name and name != 'Gaia' and name in fau_data and name not in seen:
            seen.add(name)
            result.append(name)

    def add_civ_id(civ_id):
        # 已是 FAU 键名 (如 FullTechCiv / Incas) 直接使用, 避免 title() 改写导致丢失
        if civ_id in fau_data:
            add_name(civ_id)
            return
        name = fau_civ_name(civ_id, fau_data, internal_name_map)
        if name is None:
            print(f"  Warning: 文明 '{civ_id}' 在 FAU 中无对应条目, 跳过")
        else:
            add_name(name)

    for token in tokens:
        if isinstance(token, dict) or (isinstance(token, str) and token in civ_groups):
            for cid in expand_civ_group(token, civ_groups, all_civ_ids):
                add_civ_id(cid)
        elif token == 'all':
            for name in fau_data:
                add_name(name)
        else:
            add_civ_id(token)
    return result


def fau_insert_entry(entry_list, entry, position, target_id):
    """按 position 插入 FAU 条目; 默认末尾"""
    if position == 'after' and target_id is not None:
        for i, e in enumerate(entry_list):
            if e.get('ID') == target_id:
                entry_list.insert(i + 1, entry)
                return
    elif position == 'before' and target_id is not None:
        for i, e in enumerate(entry_list):
            if e.get('ID') == target_id:
                entry_list.insert(i, entry)
                return
    elif position == 'start':
        entry_list.insert(0, entry)
        return
    entry_list.append(entry)


def apply_fau_change(change, fau_data, civ_groups=None, all_civ_ids=None, internal_name_map=None):
    civs = resolve_fau_civs(change, fau_data, civ_groups, all_civ_ids, internal_name_map)
    if not civs:
        return
    note = change.get('note')
    if note:
        print(f"Note: {note}")
    operation_type = change.get('type', '')
    position = change.get('position', 'end')
    target_id = change.get('target_id')

    if operation_type == 'delete':
        id_key = 'unit_id' if 'unit_id' in change else 'tech_id' if 'tech_id' in change else None
        if id_key is None:
            print("Error: Delete operation requires 'unit_id' or 'tech_id'.")
            return
        list_key = 'Units' if id_key == 'unit_id' else 'Techs'
        ids = change[id_key] if isinstance(change[id_key], list) else [change[id_key]]
        building_ids = change.get('building_id')
        if building_ids is not None and not isinstance(building_ids, list):
            building_ids = [building_ids]
        for civ in civs:
            if civ not in fau_data:
                print(f"Warning: Civilization '{civ}' not found.")
                continue
            for building in fau_data[civ].get('Buildings', []):
                if building_ids is not None and building.get('ID') not in building_ids:
                    continue
                entries = building.get(list_key, [])
                entries[:] = [e for e in entries if e.get('ID') not in ids]
        return

    if 'unit_id' in change or 'tech_id' in change:
        id_key = 'unit_id' if 'unit_id' in change else 'tech_id'
        list_key = 'Units' if id_key == 'unit_id' else 'Techs'
        entry_id = change[id_key]
        building_ids = change.get('building_id')
        if building_ids is not None and not isinstance(building_ids, list):
            building_ids = [building_ids]
        entry_data = {k: v for k, v in change.items() if k not in FAU_META_FIELDS}
        entry_data['ID'] = entry_id

        for civ in civs:
            if civ not in fau_data:
                print(f"Warning: Civilization '{civ}' not found.")
                continue
            buildings = fau_data[civ].get('Buildings', [])
            found = False
            for building in buildings:
                if building_ids is not None and building.get('ID') not in building_ids:
                    continue
                for entry in building.get(list_key, []):
                    if entry.get('ID') == entry_id:
                        for key, value in entry_data.items():
                            entry[key] = value
                        found = True
                        break
            if not found:
                if building_ids is None:
                    print(f"Warning: ID {entry_id} not found in '{civ}' and no 'building_id' provided to add it.")
                    continue
                for building_id in building_ids:
                    target_building = next((b for b in buildings if b.get('ID') == building_id), None)
                    if target_building is None:
                        print(f"Warning: Building ID {building_id} not found in civilization '{civ}'.")
                        continue
                    entries = target_building.setdefault(list_key, [])
                    if any(e.get('ID') == entry_id for e in entries):
                        print(f"Warning: ID {entry_id} already exists in building {building_id} of '{civ}'.")
                        continue
                    fau_insert_entry(entries, entry_data.copy(), position, target_id)
                    print(f"Added {list_key[:-1]} ID {entry_id} to building {building_id} of '{civ}'.")
        return

    if 'building_id' in change and operation_type == 'add':
        building_id = change['building_id']
        building_name = change.get('name')
        for civ in civs:
            if civ not in fau_data:
                print(f"Warning: Civilization '{civ}' not found.")
                continue
            buildings = fau_data[civ].get('Buildings', [])
            if any(b.get('ID') == building_id for b in buildings):
                print(f"Warning: Building ID {building_id} already exists in civilization '{civ}'.")
                continue
            buildings.append({'ID': building_id, 'Name': building_name, 'Techs': [], 'Units': []})
            print(f"Added building ID {building_id} to civilization '{civ}'.")
        return

    print("Error: FAU change item must contain 'unit_id', 'tech_id', or 'building_id' with type 'add'.")


# ---------------------------------------------------------------- FAU 同步 (增量记录模型)

def sync_fau(civ, fau_civ, state, pool):
    """按改动记录同步一个文明的 FAU:
    - 删除: removed 集合中的单位/科技/建筑 (含 disable/delete 连带删除的 trigger tech);
    - 新增: added 集合中的节点 (条目从 CTT 节点派生, 含 RequiredUnitID 与 trigger tech);
    - 其余条目一律原样保留 (遵循官方 FAU 的既有收录约定)。
    """
    removed = state["removed"]
    added = state["added"]
    units, techs, blds = {}, {}, {}
    for n in civ["civ_techs_units"]:
        if n.get("Use Type") == "Unit":
            # 同一 Node ID 可有多建筑变体 (如城堡/兵营双生产), 保留全部
            units.setdefault(n["Node ID"], []).append(n)
        elif n.get("Use Type") == "Tech":
            techs[n["Node ID"]] = n
    for n in civ["civ_techs_buildings"]:
        blds[n["Node ID"]] = n

    n_add_u, n_add_t, n_add_b, n_drop = 0, 0, 0, 0

    # 第一遍: 删除
    new_buildings = []
    for b in fau_civ["Buildings"]:
        bid = b["ID"]
        if bid != BUILDER_ID and bid in removed["Building"]:
            n_drop += 1
            continue
        before = len(b.get("Techs", [])) + len(b.get("Units", []))
        b["Techs"] = [t for t in b.get("Techs", []) if t["ID"] not in removed["Tech"]]
        if bid == BUILDER_ID:
            b["Units"] = [u for u in b.get("Units", []) if u["ID"] not in removed["Building"]]
        else:
            b["Units"] = [u for u in b.get("Units", []) if u["ID"] not in removed["Unit"]]
        n_drop += before - len(b.get("Techs", [])) - len(b.get("Units", []))
        new_buildings.append(b)
    fau_civ["Buildings"] = new_buildings
    bmap = {b["ID"]: b for b in new_buildings}

    def find_entry(bid, list_key, entry_id):
        b = bmap.get(bid)
        if b is None:
            return None
        return next((e for e in b.get(list_key, []) if e.get("ID") == entry_id), None)

    def ensure_building_entry(bid, node):
        """确保 FAU 中有该建筑的独立条目; 返回该条目"""
        b = bmap.get(bid)
        if b is None:
            b = {"ID": bid,
                 "Name": node.get("Name", "") if node else "",
                 "Techs": [], "Units": []}
            fau_civ["Buildings"].append(b)
            bmap[bid] = b
        return b

    # 第二遍: 新增建筑 (独立条目 + Builder 下的 Units 条目)
    for bid in added["Building"]:
        node = blds.get(bid)
        if node is None:
            continue
        ensure_building_entry(bid, node)
        builder = ensure_building_entry(BUILDER_ID, None)
        builder.setdefault("Units", [])
        if find_entry(BUILDER_ID, "Units", bid) is None:
            entry = {"ID": bid, "Name": node.get("Name", ""), "RequiredAge": node.get("Age ID", 1)}
            entry.update(state["fau_overrides"].get(("Building", bid), {}))
            builder["Units"].append(entry)
            n_add_b += 1

    # 第三遍: 新增单位与科技 (池中有官方条目则借用, 否则从 CTT 节点派生;
    # 同 Node ID 的多建筑变体各自写入所属建筑)
    for kind, nodes, list_key in (("Unit", units, "Units"), ("Tech", techs, "Techs")):
        for nid in added[kind]:
            if kind == "Tech" and nid in AGE_UP_TECH_IDS:
                continue
            variants = nodes.get(nid, []) if kind == "Unit" else (
                [nodes[nid]] if nid in nodes else [])
            for node in variants:
                bid = node.get("Building ID")
                if bid in (None, -1):
                    continue
                if bid not in bmap:
                    bnode = blds.get(bid)
                    if bnode is None or bnode.get("Node Status") == "NotAvailable":
                        continue
                    ensure_building_entry(bid, bnode)
                if find_entry(bid, list_key, nid) is not None:
                    continue
                p = pool.get((kind, nid))
                if p is not None:
                    entry, _ = borrow_entry(pool, node, kind, units)
                else:
                    entry = derive_entry(node, kind, units)
                entry.update(state["fau_overrides"].get((kind, nid), {}))
                pos, tid = state["fau_positions"].get((kind, nid), (None, None))
                fau_insert_entry(bmap[bid].setdefault(list_key, []), entry, pos, tid)
                if kind == "Unit":
                    n_add_u += 1
                else:
                    n_add_t += 1

    # 第四遍: 新增条目的 trigger tech 写入同建筑 Techs
    # (按节点变体逐一处理, fau_trigger: false 只排除其所属变体)
    for kind, nodes in (("Unit", units), ("Building", blds)):
        for nid in added[kind]:
            variants = nodes.get(nid, []) if kind == "Unit" else (
                [nodes[nid]] if nid in nodes else [])
            for node in variants:
                trigger = node.get("Trigger Tech ID", -1)
                if trigger == -1 or id(node) in state["excluded_triggers"] \
                        or (trigger in removed["Tech"] and trigger not in state["moved_triggers"]):
                    continue
                bid = node.get("Building ID") if kind == "Unit" else nid
                if bid not in bmap:
                    continue
                if find_entry(bid, "Techs", trigger) is not None:
                    continue
                p = pool.get(("Tech", trigger))
                if p is not None:
                    entry = copy.deepcopy(p[1])
                    entry["RequiredAge"] = node.get("Age ID", entry.get("RequiredAge", 1))
                else:
                    entry = {"ID": trigger, "Name": node.get("Name", ""),
                             "RequiredAge": node.get("Age ID", 1)}
                bmap[bid].setdefault("Techs", []).append(entry)
                n_add_t += 1

    print(f"  FAU sync {civ['civ_id']}: +{n_add_u} 单位 +{n_add_t} 科技 +{n_add_b} 建筑, -{n_drop} 条目")


# ---------------------------------------------------------------- 单位线 (unitlines.json)

UNITLINE_VALID_RANGE = (-400, -199)  # LineID 必须严格位于此开区间内


def line_slug(name):
    """War Chariot -> loe-war-chariot-line"""
    return "loe-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + "-line"


def collect_unit_lines(changes_list, official_lines=None):
    """从 add/replace 单位条目的 "UnitLine" 字段收集兵种线归属。

    返回 (loe_lines, official_merges):
    - loe_lines: LineID 不属于官方文件的新线条目 (按首次出现顺序);
    - official_merges: {官方 LineID: [新增 Node ID ...]}, 输出时并入官方既有线。

    规则:
    - 同一 LineID 的节点按文件出现顺序组成 IDChain (基础单位写在更靠前);
    - 同一单位 ID 跨文明/重复条目自动去重 (如魏武卒在两个文明条目中出现);
    - 同一单位不允许属于两条不同的线 (官方线成员同样参与冲突检测);
    - 引用官方线时 "UnitLineBuilding" 必须与该官方线的 Building 标记一致;
    - LOE 新线的链名取首个成员的 Name, 允许后续成员带 Elite/Veteran 前缀。
    """
    official_lines = official_lines or {}
    chains = {}        # line_id -> {"name", "building", "ids", "official"}
    ordered = []       # line_id 首次出现顺序
    unit_owner = {}    # unit_id -> line_id (含官方线成员)
    for line in official_lines.values():
        for uid in line["IDChain"]:
            unit_owner[uid] = line["LineID"]
    lo, hi = UNITLINE_VALID_RANGE

    for change in changes_list:
        line_id = change.get("UnitLine")
        if line_id is None:
            continue
        note = change.get("note", change.get("Name", ""))
        if "civilizations" in change:
            raise ValueError(f"UnitLine 不支持 FAU 风格条目: {note}")
        action = change.get("action")
        if action not in ("add", "replace"):
            raise ValueError(f"UnitLine 只能用于 add/replace 条目: {note}")
        if change.get("Use Type") != "Unit":
            raise ValueError(f"UnitLine 只能标在 Use Type=Unit 的节点上: {note}")
        unit_id = change["Node ID"] if action == "add" else change.get("new_node_id")
        if unit_id is None:
            raise ValueError(f"replace 条目缺 new_node_id, 无法确定兵种线成员: {note}")
        if not (isinstance(line_id, int) and lo < line_id < hi):
            raise ValueError(f"UnitLine 必须是 ({lo}, {hi}) 开区间内的整数: {note} -> {line_id}")
        is_building = bool(change.get("UnitLineBuilding", False))

        if line_id in official_lines:
            off = official_lines[line_id]
            if is_building != bool(off.get("Building", False)):
                raise ValueError(
                    f"UnitLineBuilding 与官方线 {line_id} ({off.get('Name')}) 的 Building 标记不一致: {note}")
            owner = unit_owner.get(unit_id)
            if owner is not None and owner != line_id:
                raise ValueError(f"单位 {unit_id} 已属于线 {owner}, 不能再并入官方线 {line_id}: {note}")
            if owner is None:
                chains.setdefault(line_id, {
                    "name": off.get("Name", ""), "building": is_building,
                    "ids": [], "official": True})
                if line_id not in ordered:
                    ordered.append(line_id)
                # ids 元素为 (unit_id, UnitLineIndex); index 为 None 时输出阶段并入链尾
                chains[line_id]["ids"].append((unit_id, change.get("UnitLineIndex")))
                unit_owner[unit_id] = line_id
            # 已在该官方线中 (官方原成员或跨文明重复条目): 去重跳过
            continue

        if line_id not in chains:
            if unit_id in unit_owner and unit_owner[unit_id] != line_id:
                raise ValueError(
                    f"单位 {unit_id} 已属于线 {unit_owner[unit_id]}, 不能再分配给 {line_id}: {note}")
            chains[line_id] = {"name": change["Name"], "building": is_building,
                               "ids": [unit_id], "official": False}
            unit_owner[unit_id] = line_id
            ordered.append(line_id)
            continue

        chain = chains[line_id]
        if chain["building"] != is_building:
            raise ValueError(f"同一 UnitLine {line_id} 的建筑标记不一致: {note}")
        owner = unit_owner.get(unit_id)
        if owner is not None and owner != line_id:
            raise ValueError(f"单位 {unit_id} 已属于线 {owner}, 不能再分配给 {line_id}: {note}")
        if owner is None:
            chain["ids"].append(unit_id)
            unit_owner[unit_id] = line_id
        # owner == line_id: 跨文明重复条目, 去重跳过

    loe_lines, official_merges = [], {}
    for line_id in ordered:
        chain = chains[line_id]
        if chain["official"]:
            official_merges[line_id] = chain["ids"]
            continue
        loe_lines.append({
            "Name": f"LOE {chain['name']} Line",
            "Identifier": line_slug(chain["name"]),
            "LineID": line_id,
            "IDChain": chain["ids"],
            **({"Building": True} if chain["building"] else {}),
        })
    return loe_lines, official_merges


def save_unit_lines(loe_lines, official_merges=None):
    """以官方 unitlines.json 为底: 官方线并入新成员, LOE 新线整组追加
    (每次重跑结果一致)。"""
    official_merges = official_merges or {}
    with open(str(OFFICIAL_UNITLINES_FILE), 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    official_by_id = {line["LineID"]: line for line in data["UnitLines"]}
    # 官方 Identifier 可能是字符串或字符串数组 (如鹰武士线的双别名), 统一摊平
    official_idents = set()
    for line in data["UnitLines"]:
        ident = line["Identifier"]
        official_idents.update(ident if isinstance(ident, list) else [ident])
    seen_ids, seen_idents = set(), set()
    for lid, new_ids in official_merges.items():
        if lid not in official_by_id:
            raise ValueError(f"官方兵种线 {lid} 不存在, 无法并入")
        chain = official_by_id[lid]["IDChain"]
        for uid, idx in new_ids:
            if uid not in chain:
                if idx is None:
                    chain.append(uid)
                else:
                    chain.insert(idx, uid)
    for entry in loe_lines:
        lid, ident = entry["LineID"], entry["Identifier"]
        if lid in official_by_id or lid in seen_ids:
            raise ValueError(f"LineID 与官方兵种线冲突或重复: {lid}")
        if ident in official_idents or ident in seen_idents:
            raise ValueError(f"Identifier 冲突或重复: {ident}")
        seen_ids.add(lid)
        seen_idents.add(ident)
        data["UnitLines"].append(entry)
    with open(str(OUTPUT_UNITLINES_FILE), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def validate_dangling_links(civs_data):
    """检查各文明节点的 Link ID 是否有匹配目标 (同 ID 且类型相容), 即悬空链接。
    典型来源: delete 删除某节点后, 原本挂在它下面的下游节点 Link ID 失效;
    也可能被同号对象掩盖 (如被删的单位 77 与科技 77 Plate Mail Armor 撞号)。
    仅打印 Warning, 不阻断生成。"""
    total = 0
    for civ in civs_data["civs"]:
        nodes = civ["civ_techs_units"] + civ["civ_techs_buildings"]
        types_by_id = {}
        for n in nodes:
            types_by_id.setdefault(n["Node ID"], set()).add(n.get("Node Type"))
        for n in nodes:
            link_id = n.get("Link ID")
            if link_id in (None, -1, 0):
                continue
            link_type = n.get("Link Node Type")
            target_types = types_by_id.get(link_id)
            ok = target_types is not None
            # Link Node Type 为 BuildingTech 时仅作排版挂靠, 不校验类型;
            # 其余须与目标节点的 Node Type 一致 (否则被同号对象掩盖, 如 77 科技)
            if ok and link_type not in (None, "BuildingTech"):
                ok = link_type in target_types
            if not ok:
                print(f"  Warning: {civ['civ_id']} 节点 {n['Node ID']} "
                      f"({n.get('Name', '')}) 的 Link ID {link_id} "
                      f"(Link Node Type {link_type}) 无匹配目标 (悬空链接)")
                total += 1
    if total:
        print(f"  Warning: 共 {total} 个悬空 Link ID; 请为这些节点重设 Link ID 或一并删除下游节点")


def main():
    civs_data, civ_files = load_civs_from_folder(str(OFFICIAL_CIVTECHTREES_FOLDER))
    with open(str(OFFICIAL_FUTUR_AVAILABLE_UNITS_FILE), 'r', encoding='utf-8') as f:
        fau_data = json.load(f)
    changes = load_changes_with_includes(CTT_CHANGES_FILE)

    # 加载官方与模组输出的 civilizations.json, 构建 tech_tree_name -> internal_name 映射
    with open(str(OFFICIAL_CIVILIZATIONS_FILE), 'r', encoding='utf-8') as f:
        official_civs = json.load(f)
    with open(str(OUTPUT_CIVILIZATIONS_FILE), 'r', encoding='utf-8') as f:
        output_civs = json.load(f)
    official_name_map = build_internal_name_map(official_civs)
    internal_name_map = build_internal_name_map(output_civs)

    # internal_name 被改名的文明: 不覆盖原版 FAU 条目, 而是深拷贝一份到新键名
    # (原版条目保留, 新键名上再叠加 LOE 改动)
    for tech_tree_name, new_name in internal_name_map.items():
        old_name = official_name_map.get(tech_tree_name)
        if old_name and new_name != old_name and old_name in fau_data \
                and new_name not in fau_data:
            fau_data[new_name] = copy.deepcopy(fau_data[old_name])
            print(f"  FAU: {old_name} -> {new_name} (深拷贝, 保留原版)")

    # unitlines.json 是全局数据, 与逐文明 CTT 处理无关, 先收集并输出
    with open(str(OFFICIAL_UNITLINES_FILE), 'r', encoding='utf-8-sig') as f:
        official_line_data = json.load(f)
    official_line_map = {line["LineID"]: line for line in official_line_data["UnitLines"]}
    loe_lines, official_merges = collect_unit_lines(changes["changes"], official_line_map)
    # 单员链 (如火牛、韩卒) 不属于兵种升级线, 最终输出阶段过滤; 官方既有线的并入不过滤
    multi_lines = [entry for entry in loe_lines if len(entry["IDChain"]) >= 2]
    skipped = [entry for entry in loe_lines if len(entry["IDChain"]) < 2]
    merged_desc = ", ".join(f"{lid}+{ids}" for lid, ids in sorted(official_merges.items()))
    save_unit_lines(multi_lines, official_merges)
    for entry in skipped:
        print(f"  Note: {entry['Name']} 仅有一个成员, 已跳过不写入 unitlines.json")
    print(f"完成: unitlines.json 已生成 (LOE 新增 {len(multi_lines)} 条兵种线"
          f"{f', 并入官方线 {len(official_merges)} 条 ({merged_desc})' if official_merges else ''}"
          f"{f', 跳过 {len(skipped)} 条单员链' if skipped else ''})")

    pool = build_pool(fau_data)
    regional_ids = build_regional_ids(civs_data)  # 官方数据, 须在应用 changes 前构建
    # 顶层 civ_groups: 具名文明组, 供各 change 的 civ_id / civilizations 直接引用
    civ_groups = changes.get("civ_groups", {})
    all_civ_ids = [civ["civ_id"] for civ in civs_data["civs"]]
    all_civ_id_set = set(all_civ_ids)
    unknown_members = sorted({m for defn in civ_groups.values() for m in group_members(defn)
                              if m != "all" and m not in all_civ_id_set and m not in civ_groups})
    if unknown_members:
        print(f"  Warning: civ_groups 含未知文明/组: {unknown_members}")
    states = {}
    for change in changes["changes"]:
        if "civilizations" in change:
            apply_fau_change(change, fau_data, civ_groups, all_civ_ids, internal_name_map)
            continue
        if "civ_id" in change:
            change["civ_id"] = resolve_civ_ids(
                change["civ_id"], civ_groups, all_civ_ids, change.get("note", ""))
        apply_ctt_change(change, civs_data, civ_files, states, fau_data, pool, regional_ids, internal_name_map)

    # 对被 CTT 改动波及的文明执行 FAU 同步
    for civ in civs_data["civs"]:
        civ_id = civ["civ_id"]
        state = states.get(civ_id)
        if state is None or not state["touched"]:
            continue
        name = fau_civ_name(civ_id, fau_data, internal_name_map)
        if name is None:
            print(f"  Note: {civ_id} 在 FAU 中无对应文明, 跳过 FAU 同步")
            continue
        sync_fau(civ, fau_data[name], state, pool)

    validate_dangling_links(civs_data)
    save_civs_to_folder(str(OUTPUT_CIVTECHTREES_FOLDER), civs_data, civ_files)
    with open(str(OUTPUT_FUTUR_AVAILABLE_UNITS_FILE), 'w', encoding='utf-8') as f:
        json.dump(fau_data, f, indent=4, ensure_ascii=False)
    print("完成: CivTechTrees 与 futuravailableunits.json 已生成")


if __name__ == '__main__':
    main()
