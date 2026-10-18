import sys
sys.dont_write_bytecode = True

import re
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

MOD_FILE = "key-value-modded-strings-utf8.txt"
OFFICIAL_FILE = "C:/Steam/steamapps/common/AoE2DE/resources/zh/strings/key-value/key-value-strings-utf8.txt"
OFFICIAL_PAPHOS_FILE = "C:/Steam/steamapps/common/AoE2DE/resources/zh/strings/key-value/key-value-paphos-strings-utf8.txt"
OUTPUT_FILE = "key-value-merge.txt"

def validate_line(line, line_num, check_non_ascii=True):
    """
    检测单行格式错误：
    - 跳过空行和注释行（//开头）
    - 1. 反斜杠\后紧跟非'n'的字符
    - 2. 不符合'n "string"'格式的行
    - 3. 包含多余双引号（>2个）的行
    - 4. 非ASCII字符检测（仅英文版，排除"•"）
    """
    errors = []
    
    line_stripped = line.strip()
    
    if line_stripped == '' or line_stripped.startswith('//'):
        return errors
    
    # ===== 1. 反斜杠后非n字符检测 =====
    i = 0
    while i < len(line):
        if line[i] == '\\':
            if i == len(line) - 1:
                errors.append(f"行 {line_num} [反斜杠错误]：行尾单独反斜杠")
                break
            else:
                next_char = line[i + 1]
                if next_char != 'n':
                    errors.append(f"行 {line_num} [反斜杠错误]：'\\{next_char}'")
                i += 1
        i += 1
    
    # ===== 2. 多余双引号检测 =====
    quote_count = line.count('"')
    if quote_count > 2:
        errors.append(f"行 {line_num} [多余双引号]：共{quote_count}个引号")
    
    # ===== 3. 数字+"字符串"或IDS_标识符+"字符串"格式检测 =====
    if not re.match(r'^(\d+|IDS_\w+)\s+".*"$', line_stripped):
        errors.append(f"行 {line_num} [格式错误]：'{line_stripped}'")
    
    # ===== 4. 非ASCII字符检测（英文版专用）=====
    if check_non_ascii:
        EXCEPTION_CHAR = '\u2022'
        non_ascii_chars = []
        for col, char in enumerate(line_stripped, 1):
            if ord(char) > 127 and char != EXCEPTION_CHAR:
                non_ascii_chars.append(f"'{char}'（位置{col}）")
        if non_ascii_chars:
            errors.append(f"行 {line_num} [非ASCII字符]：{', '.join(non_ascii_chars)}")
    
    return errors

def validate_file(file_path, check_non_ascii=True):
    """验证整个文件的格式"""
    all_errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n\r')
                errors = validate_line(line, line_num, check_non_ascii)
                all_errors.extend(errors)
    except FileNotFoundError:
        all_errors.append(f"错误：文件 '{file_path}' 不存在")
    except UnicodeDecodeError:
        all_errors.append(f"错误：文件 '{file_path}' 编码问题")
    
    return all_errors

def parse_file(file_path):
    """解析字符串文件，返回 {key: value} 字典"""
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n\r').strip()
                if line == '' or line.startswith('//'):
                    continue
                match = re.match(r'^(\d+|IDS_\w+)\s+"(.*)"$', line)
                if match:
                    key_str = match.group(1)
                    key = int(key_str) if key_str.isdigit() else key_str
                    value = match.group(2)
                    data[key] = value
    except FileNotFoundError:
        print(f"警告：文件 '{file_path}' 不存在，跳过")
    except UnicodeDecodeError:
        print(f"警告：文件 '{file_path}' 编码问题，跳过")
    
    return data

def merge_files(mod_path, official_path, paphos_path):
    """合并三个文件，模组文件优先"""
    mod_data = parse_file(mod_path)
    official_data = parse_file(official_path)
    paphos_data = parse_file(paphos_path)
    
    merged = {}
    
    merged.update(official_data)
    merged.update(paphos_data)
    merged.update(mod_data)
    
    return merged

def write_output(data, output_path):
    """写入ANSI格式的输出文件"""
    num_keys = sorted([k for k in data.keys() if isinstance(k, int)])
    str_keys = sorted([k for k in data.keys() if isinstance(k, str)])
    sorted_keys = num_keys + str_keys
    
    lines = []
    for key in sorted_keys:
        value = data[key]
        lines.append(f"{key} \"{value}\"")
    
    with open(output_path, 'w', encoding='ansi', errors='replace') as f:
        for line in lines:
            f.write(line + '\n')

def main():
    print("=== 格式检测 ===")
    mod_errors = validate_file(MOD_FILE, check_non_ascii=False)
    
    if mod_errors:
        print("模组文件格式错误：")
        for error in mod_errors:
            print(f"  {error}")
        print("\n继续合并...")
    else:
        print("√ 模组文件格式检测通过")
    
    print("\n=== 合并文件 ===")
    merged_data = merge_files(MOD_FILE, OFFICIAL_FILE, OFFICIAL_PAPHOS_FILE)
    
    print(f"官方文件条目数：{len(parse_file(OFFICIAL_FILE))}")
    print(f"Paphos文件条目数：{len(parse_file(OFFICIAL_PAPHOS_FILE))}")
    print(f"模组文件条目数：{len(parse_file(MOD_FILE))}")
    print(f"合并后总条目数：{len(merged_data)}")
    
    write_output(merged_data, OUTPUT_FILE)
    print(f"\n√ 合并完成！输出文件：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    input("\n按回车键退出...")