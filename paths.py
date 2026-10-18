import sys
sys.dont_write_bytecode = True

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

STEAM_PATH = Path("C:/Steam")
AOE2DE_PATH = STEAM_PATH / "steamapps" / "common" / "AoE2DE"

AOE2DE_DAT_PATH = AOE2DE_PATH / "resources" / "_common" / "dat"
AOE2DE_WIDGETUI_PATH = AOE2DE_PATH / "widgetui"

PROJECT_DAT_PATH = PROJECT_ROOT / "resources" / "_common" / "dat"
PROJECT_WIDGETUI_PATH = PROJECT_ROOT / "widgetui"

OFFICIAL_DATA_FILE = AOE2DE_DAT_PATH / "empires2_x2_p1.dat"
OFFICIAL_CIVILIZATIONS_FILE = AOE2DE_DAT_PATH / "civilizations.json"
OFFICIAL_CIVTECHTREES_FOLDER = AOE2DE_DAT_PATH / "CivTechTrees"
OFFICIAL_LINKED_TECHS_FILE = AOE2DE_DAT_PATH / "linkedTechs.json"
OFFICIAL_DROPSITES_FILE = AOE2DE_DAT_PATH / "dropsites.json"
OFFICIAL_FUTUR_AVAILABLE_UNITS_FILE = AOE2DE_DAT_PATH / "futuravailableunits.json"
OFFICIAL_UNITLINES_FILE = AOE2DE_DAT_PATH / "unitlines.json"
OFFICIAL_ICONS_FILE = AOE2DE_WIDGETUI_PATH / "icons.json"
OFFICIAL_MATERIALS_FILE = AOE2DE_WIDGETUI_PATH / "materials.json"

OUTPUT_DATA_FILE = PROJECT_DAT_PATH / "empires2_x2_p1.dat"
OUTPUT_CIVILIZATIONS_FILE = PROJECT_DAT_PATH / "civilizations.json"
OUTPUT_CIVTECHTREES_FOLDER = PROJECT_DAT_PATH / "CivTechTrees"
OUTPUT_LINKED_TECHS_FILE = PROJECT_DAT_PATH / "linkedTechs.json"
OUTPUT_DROPSITES_FILE = PROJECT_DAT_PATH / "dropsites.json"
OUTPUT_FUTUR_AVAILABLE_UNITS_FILE = PROJECT_DAT_PATH / "futuravailableunits.json"
OUTPUT_UNITLINES_FILE = PROJECT_DAT_PATH / "unitlines.json"
OUTPUT_ICONS_FILE = PROJECT_WIDGETUI_PATH / "icons.json"
OUTPUT_MATERIALS_FILE = PROJECT_WIDGETUI_PATH / "materials.json"

CHANGES_FILE = PROJECT_DAT_PATH / "changes.json"
CIV_CHANGES_FILE = PROJECT_DAT_PATH / "civ_changes.json"
CTT_CHANGES_FILE = PROJECT_DAT_PATH / "ctt_changes.json"
LT_CHANGES_FILE = PROJECT_DAT_PATH / "lt_changes.json"
DR_CHANGES_FILE = PROJECT_DAT_PATH / "dr_changes.json"
IM_CHANGES_FILE = PROJECT_WIDGETUI_PATH / "im_changes.json"
COST_CHANGES_FILE = PROJECT_DAT_PATH / "cost_changes.json"


def get_tool_json_excludes():
    """
    返回工具链专用、不应打包/同步进模组目录的 JSON 文件名列表（按 basename 匹配，
    robocopy /XF 和 7z -xr! 均支持跨目录按文件名排除）。

    来源：
    1. 各编辑器固定读取的 changes 文件（含 changes.json、cost_changes.json）；
    2. changes.json 与 ctt_changes.json 顶层 "includes" 引用的外部 JSON
       （如 techtrees.json），以后新增 include 文件无需再改 build.py / package.py。
    注意：与 inputs.py 保持一致，只解析顶层 includes，不递归。
    """
    import json

    names = [
        CHANGES_FILE.name,
        COST_CHANGES_FILE.name,
        CIV_CHANGES_FILE.name,
        CTT_CHANGES_FILE.name,
        LT_CHANGES_FILE.name,
        DR_CHANGES_FILE.name,
        IM_CHANGES_FILE.name,
    ]

    for changes_file in (CHANGES_FILE, CTT_CHANGES_FILE):
        try:
            with open(changes_file, "r", encoding="utf-8") as f:
                changes_data = json.load(f)
            for include in changes_data.get("includes", []):
                names.append(Path(include).name)
        except (OSError, ValueError):
            pass

    result = []
    for name in names:
        if name not in result:
            result.append(name)
    return result