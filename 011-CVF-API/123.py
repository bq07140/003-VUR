import json

# 读取 openapi.json 文件
with open('./openapi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_dic = data['paths']
# # 打印字典内容
# keys = url_dic.keys()
url_dic_new = {}
for key, value in url_dic.items():
    # print(key, value)
    if value.get('get'):
        url_dic_new[key] = value['get']['description']
    elif value.get('post'):
        url_dic_new[key] = value['post']['description']
    elif value.get('put'):
        url_dic_new[key] = value['put']['description']
    elif value.get('delete'):
        url_dic_new[key] = value['delete']['description']
    else:
        url_dic_new[key] = "无说明"

# 将新字典写入 JSON 文件
with open('old/openapi_new.json', 'w', encoding='utf-8') as f:
    json.dump(url_dic_new, f, indent=4)






