import sys
sys.dont_write_bytecode = True

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from utils import *
from inputs import effect_change_list, unit_copy_change_list, unit_change_list, tech_change_list, resource_change_list, tech_tree_change_list
from paths import OUTPUT_DATA_FILE

# fork 架构：项目 dat 即事实源，就地编辑（输入=输出=同一文件）。
# changes.json 条目为一次性批量操作，跑完即清空；单体微调直接用 AGE 改 dat。
# 官方更新时人工看官方新旧 dat 的 diff，把新内容适配进 fork。
save_file = str(OUTPUT_DATA_FILE)

def run():
    data = DatFile.parse(save_file)
    customChanges(data)
    data.save(save_file)


# ==================== 各修改模块（集成搜索） ====================


def applyEffectChanges(data, effect_change_list):
    for effect_change in effect_change_list:
        effect_ids = effect_change.get("effect_id")
        effect_ids = normalizeIdList(effect_ids)  # None 表示所有
        if effect_ids is None:
            effect_ids = range(len(data.effects))  # 遍历所有效果

        change_type = effect_change.get("type", "adjustment")
        search_config = effect_change.get("search")
        search_func = create_search_function(search_config)

        for effect_id in effect_ids:
            if effect_id >= len(data.effects):
                continue
                
            effect = data.effects[effect_id]
            
            if change_type == "add":
                commands = effect_change["commands"]
                if isinstance(commands[0], (int, float)):
                    commands = [commands]
                
                position = effect_change.get("position", None)
                effect_commands = effect.effect_commands
                skip_duplicate = effect_change.get("skip_duplicate", False)
                
                for cmd in commands:
                    cmd_type, a, b, c, d = cmd
                    d = float(d)
                    
                    if skip_duplicate and any(
                        match_command(existing, [[cmd_type, a, b, c, d]])
                        for existing in effect_commands
                    ):
                        continue
                    
                    new_cmd = EffectCommand(type=cmd_type, a=a, b=b, c=c, d=d)
                    
                    if position is None:
                        effect_commands.append(new_cmd)
                    else:
                        pos = int(position)
                        if pos < 0:
                            pos = max(0, len(effect_commands) + pos + 1)
                        pos = min(pos, len(effect_commands))
                        effect_commands.insert(pos, new_cmd)
                        position = pos + 1
                    
            elif change_type == "delete":
                match_list = effect_change.get("match", [])
                if isinstance(match_list[0], (int, float, str)):
                    match_list = [match_list]
                
                def should_delete(cmd):
                    if search_func and not search_func(cmd):
                        return False
                    return match_command(cmd, match_list)
                
                data.effects[effect_id].effect_commands = [
                    cmd for cmd in data.effects[effect_id].effect_commands 
                    if not should_delete(cmd)
                ]
                
            elif change_type == "modify":
                match_list = effect_change.get("match", [])
                if isinstance(match_list[0], (int, float, str)):
                    match_list = [match_list]
                modifications = effect_change.get("modifications", [])
                if modifications and isinstance(modifications[0], str):
                    modifications = [modifications]
                
                for cmd in data.effects[effect_id].effect_commands:
                    if search_func and not search_func(cmd):
                        continue
                    if match_command(cmd, match_list):
                        for field, op, value in modifications:
                            apply_modification(cmd, field, op, value)
                            
            elif change_type == "replace":
                # 清空整个 effect 组的所有命令，再写入 commands 中的命令。
                # 如需按条件删除部分命令，请用 delete + add 两个 change 组合。
                data.effects[effect_id].effect_commands = []

                commands = effect_change.get("commands", [])
                if commands:
                    if isinstance(commands[0], (int, float)):
                        commands = [commands]

                    position = effect_change.get("position", None)
                    effect_commands = data.effects[effect_id].effect_commands
                    skip_duplicate = effect_change.get("skip_duplicate", False)

                    for cmd in commands:
                        cmd_type, a, b, c, d = cmd
                        d = float(d)

                        if skip_duplicate and any(
                            match_command(existing, [[cmd_type, a, b, c, d]])
                            for existing in effect_commands
                        ):
                            continue

                        new_cmd = EffectCommand(type=cmd_type, a=a, b=b, c=c, d=d)

                        if position is None:
                            effect_commands.append(new_cmd)
                        else:
                            pos = int(position)
                            if pos < 0:
                                pos = max(0, len(effect_commands) + pos + 1)
                            pos = min(pos, len(effect_commands))
                            effect_commands.insert(pos, new_cmd)
                            position = pos + 1

            else:
                function_id = effect_change["function_id"]
                skip_duplicate = effect_change.get("skip_duplicate", False)
                effect_commands = data.effects[effect_id].effect_commands
                
                if skip_duplicate and any(
                    match_command(existing, [[1, 33, 0, -1, function_id]])
                    for existing in effect_commands
                ):
                    continue
                
                effect_commands.append(EffectCommand(type=1, a=33, b=0, c=-1, d=function_id))


def applyAttributeChange(obj, attr_change):
    """
    应用单个属性修改，支持列表元素搜索修改、删除或添加
    
    格式1: [path, value]                    -> 直接赋值
    格式2: [path, op, value]                -> 运算修改
    格式3: [list_path, "list_search", element_search, elem_attr_change]  
                                          -> 在列表中搜索元素并修改或删除
    格式4: [list_path, "list_add", {"attr1": val1, "attr2": val2, ...}]  
                                          -> 在列表中添加新元素
    
    element_search 支持:
        - 单层列表: ["field", "op", value] 或 ["field", value]  单条件
        - 两层列表: [["field1", "op1", val1], ["field2", "op2", val2]]  多条件AND
        - 字典: {"and": [...]} 或 {"or": [...]}  复杂组合
    
    elem_attr_change 支持:
        - "delete"                              删除匹配元素本身
        - [attr_path, value]                    直接赋值
        - [attr_path, op, value]                运算修改 (set/add/mul)
    """
    if len(attr_change) == 2:
        attr_path, new_value = attr_change
        setNestedAttribute(obj, attr_path, new_value)
    
    elif len(attr_change) == 3:
        attr_path, op, value = attr_change
        
        if op == "list_search":
            raise ValueError(
                "list_search 格式需要4个元素: [list_path, 'list_search', element_search_config, elem_attr_change]. "
                "例如: ['resource_costs', 'list_search', ['type', '=', 0], ['amount', 'add', 50]]"
            )
        
        if op == "list_add":
            applyListAdd(obj, attr_path, value)
            return
        
        current = getNestedAttribute(obj, attr_path)
        if op == "set":
            final_value = value
        elif op == "add":
            final_value = current + value
        elif op == "mul":
            final_value = current * value
        else:
            raise ValueError(f"不支持的修改操作: {op}")
        setNestedAttribute(obj, attr_path, type(current)(final_value))
    
    elif len(attr_change) == 4:
        list_path, op, element_search, elem_attr_change = attr_change
        
        if op == "list_search":
            applyListElementChange(obj, list_path, element_search, elem_attr_change)
        elif op == "list_add":
            applyListAdd(obj, list_path, element_search)
        else:
            raise ValueError(f"4元素格式只支持 list_search 和 list_add 操作，当前 op={op}")
    
    else:
        raise ValueError(f"不支持的属性修改格式: {attr_change}")


def applyUnitCopies(data, unit_copy_change_list):
    """
    从指定源文明复制单位到目标文明。

    change 字段:
      source_civ : int                   源文明 ID (必填)
      unit_id    : int | list | "all"    要复制的单位 ID; 单个 / 列表 / 全部 (省略同 "all")
      civs       : list | "all"          目标文明, 默认 "all"
      attributes : None | str | list     复制的属性:
                                           省略/None -> 复制单位全部属性
                                           字符串    -> 单个属性
                                           列表      -> 属性列表
                                         支持嵌套路径 (同 unit_changes), 如 "creatable.train_locations[0].train_time"
      search     : 搜索配置              对源单位生效, 符合条件才复制; 规则与 unit_changes 相同

    示例:
      {"source_civ": 6, "unit_id": [529, 1541], "civs": [52]}
      {"source_civ": 6, "unit_id": "all", "civs": [18],
       "attributes": ["hit_points", "creatable.train_locations[0].train_time"],
       "search": ["creatable.train_locations[0].unit_id", "=", 45]}
    """
    from copy import deepcopy

    for change in unit_copy_change_list:
        source_civ_id = change["source_civ"]
        if source_civ_id >= len(data.civs):
            raise ValueError(f"源文明 ID 超出范围: {source_civ_id}")
        source_civ = data.civs[source_civ_id]

        unit_ids = normalizeIdList(change.get("unit_id"))  # None 表示所有
        if unit_ids is None:
            unit_ids = range(len(source_civ.units))

        civs = change.get("civs", "all")
        target_civs = range(len(data.civs)) if civs == "all" else civs

        raw_attributes = change.get("attributes")
        if raw_attributes is None:
            attr_paths = None                       # 复制全部属性
        elif isinstance(raw_attributes, str):
            attr_paths = [raw_attributes]
        else:
            attr_paths = list(raw_attributes)

        search_func = create_search_function(change.get("search"))

        # Unit 本身没有 id/civ_id 字段（genieutils 结构），搜索时用代理暴露
        # id = 单位下标, civ_id = 源文明 ID，属性读取仍落在真实 unit 上
        class _UnitProxy:
            def __init__(self, unit, unit_id, civ_id):
                self._unit = unit
                self.id = unit_id
                self.civ_id = civ_id
            def __getattr__(self, name):
                return getattr(self._unit, name)

        for target_civ_id in target_civs:
            target_civ = data.civs[target_civ_id]
            copied_count = 0

            for unit_id in unit_ids:
                if unit_id >= len(source_civ.units):
                    continue

                source_unit = source_civ.units[unit_id]

                if search_func and not search_func(_UnitProxy(source_unit, unit_id, source_civ_id)):
                    continue

                # 目标单位槽位不足时，用目标文明的空单位 (999) 补齐
                if unit_id >= len(target_civ.units):
                    blank = target_civ.units[999] if len(target_civ.units) > 999 else source_civ.units[999]
                    while unit_id >= len(target_civ.units):
                        target_civ.units.append(copy(blank))

                if attr_paths is None:
                    # 整体深拷贝：源与目标同处一个 DatFile，避免嵌套子对象共享
                    target_civ.units[unit_id] = deepcopy(source_unit)
                else:
                    target_unit = target_civ.units[unit_id]
                    for attr_path in attr_paths:
                        try:
                            value = getNestedAttribute(source_unit, attr_path)
                        except (AttributeError, IndexError, KeyError):
                            # 源单位不存在该子结构 (如无 creatable/type_50 的特殊单位): 无值可复制, 跳过
                            continue
                        setNestedAttribute(target_unit, attr_path, deepcopy(value))
                copied_count += 1

            if "note" in change:
                print(f"Note: {change['note']}: civ {source_civ_id} -> civ {target_civ_id}, {copied_count} 个单位")


def applyUnitChanges(data, unit_change_list):
    for change in unit_change_list:
        unit_ids = change.get("unit_id")
        unit_ids = normalizeIdList(unit_ids)  # None 表示所有
        if unit_ids is None:
            unit_ids = range(len(data.civs[0].units))  # 遍历所有单位ID
        
        civs = change.get("civs", "all")
        attributes = change.get("attributes", [])
        search_config = change.get("search")
        search_func = create_search_function(search_config)
        
        if civs == "all":
            target_civs = range(len(data.civs))
        else:
            target_civs = civs
        
        for civ_idx in target_civs:
            civ = data.civs[civ_idx]
            
            for unit_id in unit_ids:
                if unit_id >= len(civ.units):
                    continue

                unit = civ.units[unit_id]
                
                if search_func and not search_func(unit):
                    continue
                
                for attr_change in attributes:
                    applyAttributeChange(unit, attr_change)


def applyResourceChanges(data, resource_change_list):
    for change in resource_change_list:
        resource_ids = change.get("resource_id")
        resource_ids = normalizeIdList(resource_ids)  # None 表示所有
        if resource_ids is None:
            resource_ids = range(len(data.civs[0].resources))  # 遍历所有资源
        
        civs = change.get("civs", "all")
        op = change.get("op", "set")
        num = change["num"]
        search_config = change.get("search")
        search_func = create_search_function(search_config)
        
        if civs == "all":
            target_civs = range(len(data.civs))
        else:
            target_civs = civs
        
        # num 为列表时, 按目标文明顺序逐一取值, 长度必须匹配; 标量则所有文明同值
        num_is_list = isinstance(num, list)
        if num_is_list and len(num) != len(target_civs):
            raise ValueError(
                f"num 列表长度 ({len(num)}) 与目标文明数 "
                f"({len(target_civs)}) 不匹配: {change.get('note', '')}"
            )
        for i, civ_idx in enumerate(target_civs):
            civ = data.civs[civ_idx]
            value = num[i] if num_is_list else num
            
            for resource_id in resource_ids:
                if resource_id >= len(civ.resources):
                    continue
                
                current = civ.resources[resource_id]
                
                if search_func:
                    resource_wrapper = type('ResourceWrapper', (), {
                        'value': current, 
                        'id': resource_id,
                        'civ_id': civ_idx
                    })()
                    if not search_func(resource_wrapper):
                        continue
                
                if op == "set":
                    new_value = value
                elif op == "add":
                    new_value = current + value
                elif op == "mul":
                    new_value = current * value
                else:
                    raise ValueError(f"不支持的资源修改操作: {op}")
                
                civ.resources[resource_id] = type(current)(new_value)


def applyTechChanges(data, tech_change_list):
    for change in tech_change_list:
        tech_ids = change.get("tech_id")
        tech_ids = normalizeIdList(tech_ids)  # None 表示所有
        if tech_ids is None:
            tech_ids = range(len(data.techs))  # 遍历所有科技
        
        attributes = change.get("attributes", [])
        search_config = change.get("search")
        search_func = create_search_function(search_config)
        
        for tech_id in tech_ids:
            if tech_id >= len(data.techs):
                continue
                
            tech = data.techs[tech_id]

            if search_func:
                # Tech 对象本身没有 id 字段（genieutils 结构），搜索时用代理暴露 id = 列表下标，
                # 属性修改仍然落在真实 tech 对象上
                class _TechProxy:
                    def __init__(self, tech, tech_id):
                        self._tech = tech
                        self.id = tech_id
                    def __getattr__(self, name):
                        return getattr(self._tech, name)
                if not search_func(_TechProxy(tech, tech_id)):
                    continue

            for attr_change in attributes:
                applyAttributeChange(tech, attr_change)


def applyTechTreeChanges(data, tech_tree_change_list):
    """
    处理指定文明科技树效果组 (civ.tech_tree_id 指向的 effect) 的科技开关。

    每个 change 的字段:
      civ_id 或 effect_id (二选一):
        civ_id    —— int 或 int 列表 (省略=全部文明), 按各文明 tech_tree_id
                    定位目标效果组 (历史行为)
        effect_id —— int 或 int 列表, 绕过文明查找, 直接修改指定 effect 组。
                    适合操作不属于文明科技树的自定义效果组。
                    与 civ_id 同时给出会报错, 避免目标歧义。
      enable/disable:         科技 ID 列表, 生成 (8, 科技ID, 12, -1, 1/0) 命令
      mode (可选, 默认 "rebuild"):
        "rebuild" —— 清空目标组全部 EffectCommand, 只写入 enable/disable 命令。
                     历史默认行为。注意会一并清掉原组中的 type 102 科技树条目、
                     101/103 文明加成命令, 以及任何自定义命令
                     (例如 (1, 33, 0, -1, 10001) 的 XS 引导; 该模块在
                     applyEffectChanges 之后执行, 后加进同组的命令也会被清掉)。
        "merge"   —— 保留目标组原有命令, 只把 enable/disable 合并到组尾。
                     同一科技若已存在 (8, id, 12, ...) 开关, 先剔除旧开关再写入,
                     避免重复或 1/0 冲突; 其他来源 (b != 12) 的开关和非 type 8
                     命令一律保留。适合"只在宿主科技树上开关个别科技, 其余保留"
                     或需要让 XS 引导等自定义命令存活的场景。
    """
    for change in tech_tree_change_list:
        has_civ = "civ_id" in change
        has_effect = "effect_id" in change
        if has_civ and has_effect:
            raise ValueError(
                f"tech_tree_changes 不能同时指定 civ_id 和 effect_id, 请二选一, "
                f"note: {change.get('note', '')}"
            )

        # 目标效果组解析: effect_id 直接定位; 否则按文明 tech_tree_id 查找
        # (省略 civ_id 时沿用历史行为 = 全部文明)
        if has_effect:
            direct_ids = normalizeIdList(change["effect_id"])
            if direct_ids is None:
                direct_ids = list(range(len(data.effects)))
            targets = [(None, eid) for eid in direct_ids]
        else:
            civ_ids = normalizeIdList(change.get("civ_id"))
            if civ_ids is None:
                civ_ids = range(len(data.civs))
            targets = []
            for civ_id in civ_ids:
                if civ_id >= len(data.civs):
                    continue
                targets.append((civ_id, data.civs[civ_id].tech_tree_id))

        enable_ids = change.get("enable", [])
        disable_ids = change.get("disable", [])
        if isinstance(enable_ids, (int, float)):
            enable_ids = [enable_ids]
        if isinstance(disable_ids, (int, float)):
            disable_ids = [disable_ids]
        enable_ids = [int(x) for x in enable_ids]
        disable_ids = [int(x) for x in disable_ids]
        mode = change.get("mode", "rebuild")
        if mode not in ("rebuild", "merge"):
            raise ValueError(
                f"不支持的 tech_tree_changes 模式: {mode} (仅支持 'rebuild' / 'merge'), "
                f"note: {change.get('note', '')}"
            )

        new_commands = [
            EffectCommand(type=8, a=int(tech_id), b=12, c=-1, d=1.0)
            for tech_id in enable_ids
        ] + [
            EffectCommand(type=8, a=int(tech_id), b=12, c=-1, d=0.0)
            for tech_id in disable_ids
        ]
        toggle_ids = set(enable_ids) | set(disable_ids)

        for civ_id, effect_id in targets:
            if effect_id >= len(data.effects):
                continue
            group = data.effects[effect_id].effect_commands

            if mode == "merge":
                # 剔除本组中同一科技的旧 (8, id, 12, ...) 开关, 其余命令全部保留
                preserved = [
                    cmd for cmd in group
                    if not (cmd.type == 8 and cmd.b == 12 and cmd.a in toggle_ids)
                ]
                data.effects[effect_id].effect_commands = preserved + list(new_commands)
                kept = len(preserved)
            else:
                data.effects[effect_id].effect_commands = list(new_commands)
                kept = 0

            if "note" in change:
                target_desc = f"effect {effect_id}" if civ_id is None else f"civ {civ_id}, effect {effect_id}"
                print(f"Note: {change['note']} ({target_desc}, {mode}): "
                      f"{len(enable_ids)} enabled, {len(disable_ids)} disabled, "
                      f"{kept} original commands kept")


def customChanges(data):
    if 'effect_change_list' in globals():
        applyEffectChanges(data, effect_change_list)

    if 'unit_copy_change_list' in globals():
        applyUnitCopies(data, unit_copy_change_list)

    if 'unit_change_list' in globals():
        applyUnitChanges(data, unit_change_list)

    if 'resource_change_list' in globals():
        applyResourceChanges(data, resource_change_list)

    if 'tech_change_list' in globals():
        applyTechChanges(data, tech_change_list)

    if 'tech_tree_change_list' in globals():
        applyTechTreeChanges(data, tech_tree_change_list)

    return


if __name__ == "__main__":
    run()
