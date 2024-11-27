import json

def print_json_structure(json_obj, indent=0):
    """递归打印 JSON 结构"""
    if isinstance(json_obj, dict):
        for key in json_obj.keys():
            print(' ' * indent + str(key) + ':')
            print_json_structure(json_obj[key], indent + 2)
    elif isinstance(json_obj, list):
        print(' ' * indent + '[]')
        for item in json_obj:
            print_json_structure(item, indent + 2)
    else:
        print(' ' * indent + str(type(json_obj).__name__))

# 读取 JSON 文件
with open('table.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 打印 JSON 结构
print_json_structure(data)
