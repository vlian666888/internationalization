
1，第一步

创建脚本，在swift项目提取中文字符串
find_unlocalized_chinese_swift.py

2，第二步

运行脚本
python3 find_unlocalized_chinese_swift.py \

--code-dir ./Demo \

--strings ./Demo/zh-Hans.lproj/Localizable.strings

3，第三步

用大模型豆包把提取的中文字符串，按照字面意思分类，以及写成"im_sendMsg" = "发送消息";这种格式


4，第四步

写替换脚本
replace_strings_swift.py

5，第五步

把第三步整理的国际化文本的key的国际化格式化 替换项目中的字符串文本
运行脚本
python3 replace_strings_swift.py --code-dir ./QDZBLive --strings ./Demo/zh-Hans.lproj/Localizable.strings
