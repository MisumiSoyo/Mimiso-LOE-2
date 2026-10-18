import sys
sys.dont_write_bytecode = True

from toolbox import *



import math

ANY = "any"
FLOAT_REL_TOL = 1e-5
FLOAT_ABS_TOL = 1e-6


def match_command(cmd, match_list):
    for match in match_list:
        m_type, m_a, m_b, m_c, m_d = match
        if not (m_type == ANY or cmd.type == m_type):
            continue
        if not (m_a == ANY or cmd.a == m_a):
            continue
        if not (m_b == ANY or cmd.b == m_b):
            continue
        if not (m_c == ANY or cmd.c == m_c):
            continue
        if m_d == ANY:
            return True
        if math.isclose(cmd.d, m_d, rel_tol=FLOAT_REL_TOL, abs_tol=FLOAT_ABS_TOL):
            return True
    return False


def apply_modification(cmd, field, op, value):
    current = getattr(cmd, field)
    if op == "set":
        new_value = value
    elif op == "add":
        new_value = current + value
    elif op == "mul":
        new_value = current * value
    else:
        raise ValueError(f"不支持的修改操作: {op}")
    setattr(cmd, field, type(current)(new_value))


def parseAttrPath(attr_path):
    import re
    return re.findall(r'[^\.\[\]]+|\[\d+\]', attr_path)


def setNestedAttribute(obj, attr_path, value):
    tokens = parseAttrPath(attr_path)
    current = obj
    for token in tokens[:-1]:
        if token.startswith('[') and token.endswith(']'):
            idx = int(token[1:-1])
            current = current[idx]
        else:
            current = getattr(current, token)
    last_token = tokens[-1]
    if last_token.startswith('[') and last_token.endswith(']'):
        idx = int(last_token[1:-1])
        current[idx] = value
    else:
        setattr(current, last_token, value)


def getNestedAttribute(obj, attr_path):
    tokens = parseAttrPath(attr_path)
    current = obj
    for token in tokens:
        if token.startswith('[') and token.endswith(']'):
            idx = int(token[1:-1])
            current = current[idx]
        else:
            current = getattr(current, token)
    return current


def normalizeIdList(ids):
    # None 或字符串 "all"(忽略大小写) 都表示搜索所有
    if ids is None or (isinstance(ids, str) and ids.lower() == "all"):
        return None
    if isinstance(ids, (int, float)):
        return [int(ids)]
    return [int(x) for x in ids]


# ==================== 搜索系统核心封装 ====================

def _compare_values(current, op, target):
    """
    底层值比较逻辑
    """
    if op in ("eq", "=", "=="):
        if isinstance(current, float) and isinstance(target, (int, float)):
            return math.isclose(current, target, rel_tol=FLOAT_REL_TOL, abs_tol=FLOAT_ABS_TOL)
        return current == target
    elif op in ("ne", "!=", "<>"):
        if isinstance(current, float) and isinstance(target, (int, float)):
            return not math.isclose(current, target, rel_tol=FLOAT_REL_TOL, abs_tol=FLOAT_ABS_TOL)
        return current != target
    elif op in ("gt", ">"):
        return current > target
    elif op in ("gte", ">=", "=>"):
        return current >= target
    elif op in ("lt", "<"):
        return current < target
    elif op in ("lte", "<=", "=<"):
        return current <= target
    elif op == "contains":
        return target in current
    elif op == "startswith":
        return str(current).startswith(str(target))
    elif op == "endswith":
        return str(current).endswith(str(target))
    elif op == "in":
        return current in target
    elif op in ("not in", "notin", "not_in"):
        return current not in target
    elif op == "range":
        min_val, max_val = target
        return min_val <= current <= max_val
    elif op == "regex":
        import re
        return re.search(target, str(current)) is not None
    else:
        raise ValueError(f"不支持的比较操作: {op}")


def _evaluate_single_condition(obj, condition):
    """
    评估单个条件字典 {field, op, value}
    """
    field = condition.get("field")
    if field is None:
        raise ValueError("搜索条件必须指定 field")
    
    op = condition.get("op", "eq")
    target_value = condition["value"]
    
    try:
        current_value = getNestedAttribute(obj, field)
    except (AttributeError, IndexError, KeyError):
        return False
    
    return _compare_values(current_value, op, target_value)


def evaluate_search(obj, search_config):
    """
    直接评估对象是否符合搜索配置
    """
    if search_config is None:
        return True
    
    if isinstance(search_config, list):
        return all(evaluate_search(obj, cond) for cond in search_config)
    
    if "and" in search_config:
        return all(evaluate_search(obj, cond) for cond in search_config["and"])
    if "or" in search_config:
        return any(evaluate_search(obj, cond) for cond in search_config["or"])
    
    return _evaluate_single_condition(obj, search_config)


def create_search_function(search_config):
    """
    将搜索配置编译为可复用的搜索函数，返回 callable(obj) -> bool
    """
    if search_config is None:
        return None
    
    if isinstance(search_config, list):
        if len(search_config) == 0:
            return lambda obj: True
        
        first_elem = search_config[0]
        is_single_condition = isinstance(first_elem, (str, int, float))
        
        if is_single_condition:
            if len(search_config) == 2:
                field, target_value = search_config
                op = "eq"
            elif len(search_config) == 3:
                field, op, target_value = search_config
            else:
                raise ValueError(f"单条件列表必须是 [field, value] 或 [field, op, value] 格式: {search_config}")
            
            def list_single_search(obj):
                try:
                    current_value = getNestedAttribute(obj, field)
                except (AttributeError, IndexError, KeyError):
                    return False
                return _compare_values(current_value, op, target_value)
            return list_single_search
        else:
            sub_funcs = [create_search_function(cond) for cond in search_config]
            def list_and_search(obj):
                return all(f(obj) for f in sub_funcs)
            return list_and_search
    
    if isinstance(search_config, dict):
        if "and" in search_config:
            sub_funcs = [create_search_function(cond) for cond in search_config["and"]]
            def and_search(obj):
                return all(f(obj) for f in sub_funcs)
            return and_search
        
        if "or" in search_config:
            sub_funcs = [create_search_function(cond) for cond in search_config["or"]]
            def or_search(obj):
                return any(f(obj) for f in sub_funcs)
            return or_search
        
        field = search_config.get("field")
        if field is None:
            raise ValueError("搜索条件必须指定 field")
        op = search_config.get("op", "eq")
        target_value = search_config["value"]
        
        def dict_single_search(obj):
            try:
                current_value = getNestedAttribute(obj, field)
            except (AttributeError, IndexError, KeyError):
                return False
            return _compare_values(current_value, op, target_value)
        return dict_single_search
    
    raise ValueError(f"不支持的搜索配置格式: {search_config}")


# ==================== 新增：列表元素搜索与修改 ====================

def find_in_list(obj_list, element_search_config):
    """
    在对象列表/元组中按条件查找匹配的元素，返回 (index, element) 列表
    
    element_search_config 格式与 create_search_function 相同
    """
    if obj_list is None:
        return []
    
    # 支持 list 和 tuple
    if not isinstance(obj_list, (list, tuple)):
        raise ValueError(f"属性不是列表或元组，实际类型: {type(obj_list).__name__}")
    
    search_func = create_search_function(element_search_config)
    results = []
    
    for idx, elem in enumerate(obj_list):
        if elem is None:
            continue
        if search_func is None or search_func(elem):
            results.append((idx, elem))
    
    return results


def applyListAdd(obj, list_attr_path, element_attrs):
    """
    在列表中添加新元素
    
    自动识别列表元素类型并创建实例，通过字典设置属性值
    
    参数:
        obj: 父对象
        list_attr_path: 列表属性路径，如 "creatable.resource_costs"
        element_attrs: 新元素的属性字典，如 {"type": 0, "amount": 100}
    """
    from copy import copy
    
    try:
        obj_list = getNestedAttribute(obj, list_attr_path)
    except (AttributeError, IndexError, KeyError):
        raise ValueError(f"无法找到列表属性: {list_attr_path}")
    
    if not isinstance(obj_list, list):
        raise ValueError(f"属性 {list_attr_path} 不是列表，实际类型: {type(obj_list).__name__}")
    
    if len(obj_list) > 0:
        elem_type = type(obj_list[0])
        new_elem = copy(obj_list[0])
    else:
        elem_type = None
        parent_obj = obj
        tokens = parseAttrPath(list_attr_path)
        for token in tokens[:-1]:
            if token.startswith('[') and token.endswith(']'):
                idx = int(token[1:-1])
                parent_obj = parent_obj[idx]
            else:
                parent_obj = getattr(parent_obj, token)
        
        list_name = tokens[-1]
        elem_type = infer_element_type(parent_obj, list_name)
        
        if elem_type is None:
            raise ValueError(f"无法推断空列表 {list_attr_path} 的元素类型，请确保列表不为空或在代码中显式处理")
        
        try:
            new_elem = elem_type(**element_attrs)
            obj_list.append(new_elem)
            return
        except TypeError:
            new_elem = elem_type.__new__(elem_type)
    
    for attr_name, attr_value in element_attrs.items():
        setattr(new_elem, attr_name, attr_value)
    
    obj_list.append(new_elem)


def infer_element_type(parent_obj, list_name):
    """
    从父对象和列表名推断列表元素类型
    """
    from genieutils.effect import EffectCommand
    from genieutils.unit import AttackOrArmor, ResourceStorage
    from genieutils.tech import ResearchLocation
    
    type_map = {
        "effect_commands": EffectCommand,
        "attacks": AttackOrArmor,
        "armours": AttackOrArmor,
        "resource_costs": ResourceStorage,
        "resource_storages": ResourceStorage,
        "research_locations": ResearchLocation,
    }
    
    return type_map.get(list_name)


def applyListElementChange(obj, list_attr_path, element_search_config, attr_change):
    """
    在列表/元组属性中查找匹配元素并修改或删除
    """
    try:
        obj_list = getNestedAttribute(obj, list_attr_path)
    except (AttributeError, IndexError, KeyError):
        return
    
    if not isinstance(obj_list, (list, tuple)):
        raise ValueError(f"属性 {list_attr_path} 不是列表或元组，实际类型: {type(obj_list).__name__}")
    
    matches = find_in_list(obj_list, element_search_config)
    
    # ========== 新增：删除匹配元素本身 ==========
    if attr_change == "del":
        if isinstance(obj_list, tuple):
            raise ValueError(f"属性 {list_attr_path} 是元组，不支持删除操作")
        for idx,_ in reversed(matches):
            del obj_list[idx]
        return
    # ==========================================
    
    for idx, elem in matches:
        if len(attr_change) == 2:
            attr_path, new_value = attr_change
            setNestedAttribute(elem, attr_path, new_value)
        elif len(attr_change) == 3:
            attr_path, op, value = attr_change
            current = getNestedAttribute(elem, attr_path)
            if op in ("set", None):
                final_value = value
            elif op == "add":
                final_value = current + value
            elif op == "mul":
                final_value = current * value
            else:
                raise ValueError(f"不支持的修改操作: {op}")
            setNestedAttribute(elem, attr_path, type(current)(final_value))
        else:
            raise ValueError(f"不支持的属性修改格式: {attr_change}")
