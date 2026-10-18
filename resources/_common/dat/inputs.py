import sys
sys.dont_write_bytecode = True

import json
from pathlib import Path

CHANGES_FILE = Path('changes.json')
with open(CHANGES_FILE, 'r', encoding='utf-8') as f:
    changes_json = json.load(f)

# 支持通过 "includes" 引用外部 JSON 文件, 各模块的改动列表会按引用顺序追加到主文件之后
_INCLUDE_MODULES = ("effect_adjustments", "unit_copies", "unit_changes", "tech_changes", "resource_changes", "tech_tree_changes")
for include_path in changes_json.get("includes", []):
    include_file = Path(include_path)
    if not include_file.is_absolute():
        include_file = CHANGES_FILE.parent / include_file
    with open(include_file, 'r', encoding='utf-8') as f:
        included_json = json.load(f)
    for module in _INCLUDE_MODULES + ("groups",):
        if module in included_json:
            changes_json.setdefault(module, []).extend(included_json[module])


# groups: 同一主题(如某个单位体系)的多类修改集中写在一个组里, 此处展开到各顶级列表。
# fork 架构下项目 dat 即事实源, 不再有跨文件复制(copy_from_old_datafile 已废弃)。
# 组格式:
#   {
#     "note": "剑士体系",          # 建议必填, 展开顺序 = 组出现顺序
#     "unit_changes": [...],       # 可选, 格式与顶级对应列表完全相同
#     "tech_changes": [...],
#     "effect_adjustments": [...],
#     ... 其余修改模块键同理 ...
#   }
for _group in changes_json.get("groups", []):
    for _module in _INCLUDE_MODULES:
        if _module in _group:
            changes_json.setdefault(_module, []).extend(_group[_module])


effect_change_list = changes_json["effect_adjustments"]
unit_copy_change_list = changes_json.get("unit_copies", [])
unit_change_list = changes_json["unit_changes"]
tech_change_list = changes_json["tech_changes"]
resource_change_list = changes_json["resource_changes"]
tech_tree_change_list = changes_json.get("tech_tree_changes", [])

changes_json = None
