import sys
sys.dont_write_bytecode = True

import re
import os
from pathlib import Path
from typing import Set, List, Dict, Optional, Callable, Union, Any
from genieutils.datfile import DatFile
from genieutils.unit import AttackOrArmor, ResourceStorage
from genieutils.effect import EffectCommand
from genieutils.task import Task
from copy import copy
from dataclasses import fields

os.chdir(Path(__file__).parent)

sync_effect_type = {0, 4, 5, 10, 14, 15, 20, 24, 25, 30, 34, 35, 40, 44, 45, 200, 201, 202}

# GetIdByName key
key_getters: dict[str, Callable[[Any], Optional[Union[int, float, Set]]]] = {
    "name": lambda u: getattr(u, "language_dll_name", None),
    "creation": lambda u: getattr(u, "language_dll_creation", None),
    "class_": lambda u: getattr(u, "class_", None),
    "hp": lambda u: getattr(u, "hit_points", None),
    "size": lambda u: getattr(u, "collision_size_x", None),
    "loc": lambda u: getattr(getattr(u, "creatable", None), "train_location_id", None),
    "storage_1st": lambda u: getattr(u.resource_storages[0], "amount", None),
    "attack_type": lambda u: (
        {x.class_ for x in getattr(getattr(u, "type_50", None), "attacks", [])}
    ),
    "armor_type": lambda u: (
        {x.class_ for x in getattr(getattr(u, "type_50", None), "armours", [])}
    )
}

# Costs translation
COST_PATTERN = re.compile(r'([+-]?\d+)([FWGS])')
def parse_costs_regex(cost_str) -> Dict[str, int]:
    resource_map = {
        'F': 'food_cost',
        'W': 'wood_cost',
        'G': 'gold_cost',
        'S': 'stone_cost',
    }
    result = {r: 0 for r in resource_map.values()}
    matches = COST_PATTERN.findall(cost_str.upper())
    for num_str, res_code in matches:
        key = resource_map.get(res_code)
        if key:
            result[key] = int(num_str)
    return result

resource_mapping = {
    0: "food_cost",
    1: "wood_cost",
    2: "stone_cost",
    3: "gold_cost",
}

# SetAttacksOrArmours display map
display_map = {
    ("attacks", 3): ("type_50", "displayed_attack"),
    ("attacks", 4): ("type_50", "displayed_attack"),
    ("armours", 3): ("creatable", "displayed_pierce_armor"),
    ("armours", 4): ("type_50", "displayed_melee_armour"),
}

# Fields
field_mapping = {
    "hp": "hit_points",
    "los": "line_of_sight",
    "range": {
        ("type_50", "max_range"),
        ("type_50", "displayed_range"),
        ("bird", "search_radius"),
        "line_of_sight"
    },
    "max_range": {
        ("type_50", "max_range"),
        ("type_50", "displayed_range")
    },
    "rof": {
        ("type_50", "reload_time"),
        ("type_50", "displayed_reload_time")
    },
    "projectiles": {
        ("creatable", "total_projectiles"),
        ("creatable", "max_total_projectiles")
    },
    "size": {
        "collision_size_x",
        "collision_size_y",
        "outline_size_x",
        "outline_size_y",
        ("clearance_size", 0),
        ("clearance_size", 1),
    },
    "time": ("creatable", "train_time"),
    "loc": ("creatable", "train_location_id"),
    "storage_value": {
        ("resource_storages", 0, "amount"),
        ("resource_storages", 1, "amount"),
        ("resource_storages", 2, "amount"),
    },
    "storage_1st": ("resource_storages", 0, "amount"),
    "storage_2nd": ("resource_storages", 1, "amount"),
    "storage_3rd": ("resource_storages", 2, "amount"),
}
direct_fields = {
    "class_",
    "speed",
    "trait",
    "garrison_capacity",
    "resource_capacity",
    "resource_decay",
    "dead_unit_id",
    "blood_unit_id",
    "collision_size_x",
    "collision_size_y",
    "collision_size_z",
    "outline_size_x",
    "outline_size_y",
    "outline_size_z",
    "clearance_size",
}
module_fields = {
    "type_50": {
        "accuracy_percent",
        "accuracy_dispersion",
        "min_range",
        "frame_delay",
        "blast_width",
        "blast_attack_level",
        "blast_damage",
        "projectile_unit_id",
        "bonus_damage_resistance",
        "break_off_combat",
    },
    "creatable": {
        "max_charge",
        "recharge_rate",
        "charge_event",
        "charge_type",
        "charge_target",
        "charge_projectile_unit",
        "min_conversion_time_mod",
        "max_conversion_time_mod",
        "conversion_chance_mod",
        "total_projectiles",
        "max_total_projectiles",
        "projectile_spawning_area",
        "secondary_projectile_unit",
        "special_ability",
        "flank_attack_modifier",
    },
    "bird": {
        "work_rate",
        "task_swap_group",
        "drop_sites",
    },
    "building": {"tech_id"},
    "projectile": {
        "hit_mode",
        "vanish_mode",
        "projectile_arc",
    }
}
field_mapping.update({key: key for key in direct_fields})
for module, keys in module_fields.items():
    for key in keys:
        field_mapping[key] = (module, key)
valid_fields = set(field_mapping.keys())
valid_fields.update({
    "name",
    "civ",
    "ids",
    "id_by_key",
    "key_type",
    "reverse",
    "id_by_key_2",
    "key_type_2",
    "reverse_2",
    "atk",
    "attacks",
    "pa",
    "ma",
    "armors",
    "costs",
    "food_cost",
    "wood_cost",
    "gold_cost",
    "stone_cost",
    "add_cost_type",
    "remove_cost_type",
    "copy_from_civ",
    "copy_from_unit",
    "storages",
    "create_task",
    "task_modify",
    "atk_anim_duration"
})

default_task = {
    'task_type': 1,
    'id': -1,
    'is_default': 0,
    'action_type': 0,
    'class_id': -1,
    'unit_id': -1,
    'terrain_id': -1,
    'resource_in': -1,
    'resource_multiplier': -1,
    'resource_out': -1,
    'unused_resource': -1,
    'work_value_1': 0.0,
    'work_value_2': 0.0,
    'work_range': 0.0,
    'auto_search_targets': 0,
    'search_wait_time': 0.0,
    'enable_targeting': 0,
    'combat_level_flag': 0,
    'gather_type': 0,
    'work_flag_2': 0,
    'target_diplomacy': 0,
    'carry_check': 0,
    'pick_for_construction': 0,
    'moving_graphic_id': -1,
    'proceeding_graphic_id': -1,
    'working_graphic_id': -1,
    'carrying_graphic_id': -1,
    'resource_gathering_sound_id': -1,
    'resource_deposit_sound_id': -1,
    'wwise_resource_gathering_sound_id': 0,
    'wwise_resource_deposit_sound_id': 0
}

task_fields = {f.name for f in fields(Task)}


def to_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    elif isinstance(value, (set, range)):
        return list(value)
    else:
        return [value]


def to_set(value):
    if value is None:
        return set()
    if isinstance(value, set):
        return value
    elif isinstance(value, (list, range)):
        return set(value)
    else:
        return {value}


def apply_modifier(value, modifier):
    if isinstance(modifier, str):
        if not modifier.startswith("fx:"):
            raise ValueError(f"表达式格式错误: {modifier}")
        expr = modifier[3:]  # 去掉 "fx:"
        try:
            # 安全警告：eval 有风险，请确保输入可控
            func = eval(f"lambda x: {expr}")
            return func(value)
        except Exception as e:
            raise ValueError(f"无法解析表达式: {expr}") from e
    else:
        return modifier
