import sys
sys.dont_write_bytecode = True

import re
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

MOD_FILE = "key-value-modded-strings-utf8.txt"
OFFICIAL_FILE = "C:/Steam/steamapps/common/AoE2DE/resources/en/strings/key-value/key-value-strings-utf8.txt"
OFFICIAL_PAPHOS_FILE = "C:/Steam/steamapps/common/AoE2DE/resources/en/strings/key-value/key-value-paphos-strings-utf8.txt"
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
                errors.append(f"Line {line_num} [Backslash Error]: Backslash at end of line")
                break
            else:
                next_char = line[i + 1]
                if next_char != 'n':
                    errors.append(f"Line {line_num} [Backslash Error]: '\\{next_char}'")
                i += 1
        i += 1
    
    # ===== 2. Extra quotes detection =====
    quote_count = line.count('"')
    if quote_count > 2:
        errors.append(f"Line {line_num} [Extra Quotes]: {quote_count} quotes found")
    
    # ===== 3. Number+"string" or IDS_identifier+"string" format detection =====
    if not re.match(r'^(\d+|IDS_\w+)\s+".*"$', line_stripped):
        errors.append(f"Line {line_num} [Format Error]: '{line_stripped}'")
    
    # ===== 4. Non-ASCII character detection (English version only) =====
    if check_non_ascii:
        EXCEPTION_CHAR = '\u2022'
        non_ascii_chars = []
        for col, char in enumerate(line_stripped, 1):
            if ord(char) > 127 and char != EXCEPTION_CHAR:
                non_ascii_chars.append(f"'{char}' (col {col})")
        if non_ascii_chars:
            errors.append(f"Line {line_num} [Non-ASCII Characters]: {', '.join(non_ascii_chars)}")
    
    return errors

def validate_file(file_path, check_non_ascii=True):
    """Validate entire file format"""
    all_errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n\r')
                errors = validate_line(line, line_num, check_non_ascii)
                all_errors.extend(errors)
    except FileNotFoundError:
        all_errors.append(f"Error: File '{file_path}' not found")
    except UnicodeDecodeError:
        all_errors.append(f"Error: Encoding issue with file '{file_path}'")
    
    return all_errors

def parse_file(file_path):
    """Parse string file, return {key: value} dict"""
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
        print(f"Warning: File '{file_path}' not found, skipping")
    except UnicodeDecodeError:
        print(f"Warning: Encoding issue with file '{file_path}', skipping")
    
    return data

def merge_files(mod_path, official_path, paphos_path):
    """Merge three files, mod file has priority"""
    mod_data = parse_file(mod_path)
    official_data = parse_file(official_path)
    paphos_data = parse_file(paphos_path)
    
    merged = {}
    
    merged.update(official_data)
    merged.update(paphos_data)
    merged.update(mod_data)
    
    return merged

def write_output(data, output_path):
    """Write output file in ANSI format"""
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
    print("=== Format Validation ===")
    mod_errors = validate_file(MOD_FILE, check_non_ascii=True)
    
    if mod_errors:
        print("Mod file format errors:")
        for error in mod_errors:
            print(f"  {error}")
        print("\nContinuing with merge...")
    else:
        print("√ Mod file format validation passed")
    
    print("\n=== Merging Files ===")
    merged_data = merge_files(MOD_FILE, OFFICIAL_FILE, OFFICIAL_PAPHOS_FILE)
    
    print(f"Official file entries: {len(parse_file(OFFICIAL_FILE))}")
    print(f"Paphos file entries: {len(parse_file(OFFICIAL_PAPHOS_FILE))}")
    print(f"Mod file entries: {len(parse_file(MOD_FILE))}")
    print(f"Merged total entries: {len(merged_data)}")
    
    write_output(merged_data, OUTPUT_FILE)
    print(f"\n√ Merge complete! Output file: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")