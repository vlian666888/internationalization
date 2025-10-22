#!/usr/bin/env python3
import os
import re
import sys

# 用法:
# python3 replace_strings.py <项目源码目录> <Localizable.strings 文件路径>

if len(sys.argv) < 3:
    print("用法: python3 replace_strings.py <项目目录> <Localizable.strings路径>")
    sys.exit(1)

PROJECT_DIR = sys.argv[1]
STRINGS_FILE = sys.argv[2]

# 读取 Localizable.strings，建立 value -> key 的映射
pattern_kv = re.compile(r'"(.*?)"\s*=\s*"(.*?)";')
value_to_key = {}

with open(STRINGS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        m = pattern_kv.search(line)
        if m:
            key, value = m.group(1), m.group(2)
            value_to_key[value] = key

print(f"✅ 从 {STRINGS_FILE} 读取到 {len(value_to_key)} 个 key-value 对")

# 匹配 Objective-C 字符串 @"xxx"
string_pattern = re.compile(r'@\"([^"]+)\"')

# 忽略的函数前缀
ignore_prefixes = ["NSLog", "Klog"]

def should_ignore(line: str) -> bool:
    stripped = line.lstrip()
    return any(stripped.startswith(prefix) for prefix in ignore_prefixes)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    new_lines = []

    for line in lines:
        if should_ignore(line):
            new_lines.append(line)
            continue

        def replace_match(m):
            value = m.group(1)
            if value in value_to_key:
                key = value_to_key[value]
                return f'KLocalized(@"{key}")'
            return m.group(0)  # 不在字典里的，保持不变

        new_line = string_pattern.sub(replace_match, line)
        if new_line != line:
            modified = True
        new_lines.append(new_line)

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"🔄 已处理: {file_path}")

def scan_directory(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".m") or file.endswith(".h"):
                process_file(os.path.join(root, file))

print(f"开始扫描目录: {PROJECT_DIR}")
scan_directory(PROJECT_DIR)
print("🎉 替换完成！")