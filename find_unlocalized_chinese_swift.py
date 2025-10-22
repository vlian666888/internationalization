import os
import re
import argparse

def load_strings(strings_file):
    """读取 Localizable.strings 文件，构建 value->key 映射"""
    strings_dict = {}
    with open(strings_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("/*") or line.startswith("//") or not line:
                continue
            match = re.match(r'"(.*?)"\s*=\s*"(.*?)";', line)
            if match:
                key, value = match.groups()
                strings_dict[value] = key
    return strings_dict

def find_chinese_strings_in_swift(code_dir, strings_dict):
    """扫描 Swift 文件，找出未国际化的中文字符串"""
    chinese_regex = re.compile(r'"[^"]*[\u4E00-\u9FA5]+[^"\n]*?"')

    for root, _, files in os.walk(code_dir):
        for file in files:
            if not file.endswith(".swift"):  # 只处理 Swift 文件
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    # 忽略日志行
                    if any(skip in line for skip in ["NSLog(", "print(", "KLog("]):
                        continue

                    matches = chinese_regex.findall(line)
                    for match in matches:
                        text = match.strip('"')
                        if text not in strings_dict:
                            #print(f"{file_path}:{lineno} 未国际化 -> {text}")
                            print(f"{lineno} : {text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find unlocalized Chinese strings in Swift code")
    parser.add_argument("--code-dir", required=True, help="Path to Swift project source code")
    parser.add_argument("--strings", required=True, help="Path to Localizable.strings file")
    args = parser.parse_args()

    strings_dict = load_strings(args.strings)
    find_chinese_strings_in_swift(args.code_dir, strings_dict)