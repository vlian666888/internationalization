import os
import re
import argparse

def load_strings(strings_file):
    """读取 .strings 文件，返回 {value: key} 映射"""
    mapping = {}
    with open(strings_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            match = re.match(r'"(.*?)"\s*=\s*"(.*?)";', line)
            if match:
                key, value = match.groups()
                mapping[value] = key
    return mapping

def replace_in_file(file_path, mapping):
    """替换 Swift 文件中的字符串，但忽略 print("xxx")"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for value, key in mapping.items():
        # 正则：匹配字符串，但忽略 print("xxx")
        pattern = re.compile(rf'(?<!print\()\s*"{re.escape(value)}"')
        new_content = pattern.sub(f'KLocalized("{key}")', new_content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ 已处理: {file_path}")

def process_directory(code_dir, mapping):
    """递归处理 Swift 文件"""
    for root, _, files in os.walk(code_dir):
        for file in files:
            if file.endswith(".swift"):
                replace_in_file(os.path.join(root, file), mapping)

def main():
    parser = argparse.ArgumentParser(description="Swift 国际化替换脚本")
    parser.add_argument("--code-dir", required=True, help="Swift 源代码目录路径")
    parser.add_argument("--strings", required=True, help=".strings 国际化文件路径")
    args = parser.parse_args()

    mapping = load_strings(args.strings)
    process_directory(args.code_dir, mapping)

if __name__ == "__main__":
    main()