import json
import re


txt_file_path = r'input.txt'
json_file_path = r'input.json'


def txt_to_json_array(txt_file_path, json_file_path):
    # 读取TXT文件内容
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式分割段落
    # 这里使用两个或更多连续换行符作为段落分隔符
    paragraphs = re.split(r'\n\s*\n', content)

    # 清理每个段落：移除首尾空白字符，并过滤空段落
    cleaned_paragraphs = []
    for para in paragraphs:
        cleaned_para = para.strip()
        if cleaned_para:  # 只保留非空段落
            cleaned_paragraphs.append(cleaned_para)

    # 将段落数组保存为JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(cleaned_paragraphs, json_file, ensure_ascii=False, indent=2)

    print(f"转换完成！JSON文件已保存至: {json_file_path}")
    print(f"共转换了 {len(cleaned_paragraphs)} 个段落")


txt_to_json_array(txt_file_path, json_file_path)


# 定义用于去除控制字符的正则表达式
control_chars = re.compile(r'[\x00-\x1F\x7F]')

# 定义函数用于清理控制字符
def remove_control_characters(s):
    return control_chars.sub('', s)

# 初始化空字符串存储清理后的内容
cleaned_content = ''

# 逐行读取并清理文件
with open('input.json', 'r', encoding='utf-8') as f:
    for line in f:
        cleaned_content += remove_control_characters(line)

# 打印部分内容进行调试
print(cleaned_content[1234170:1234200])  # 打印清理后的前1000个字符以检查是否有问题

# 解析为 JSON 对象
try:
    data = json.loads(cleaned_content)
    print("JSON 文件成功解析")
except json.JSONDecodeError as e:
    print(f"解析 JSON 时出错: {e}")
    exit(1)

# 定义递归函数清理数据中的控制字符
def clean_data(obj):
    if isinstance(obj, str):
        return remove_control_characters(obj)
    elif isinstance(obj, list):
        return [clean_data(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_data(value) for key, value in obj.items()}
    else:
        return obj

# 清理 JSON 数据中的控制字符
cleaned_data = clean_data(data)

# 保存清理后的 JSON 文件
with open('train.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)