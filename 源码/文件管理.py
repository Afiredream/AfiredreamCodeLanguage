import json

def 读取文本文件(文件路径):
    with open(文件路径, 'r', encoding='utf-8') as 文件对象:
        return 文件对象.read()

def 覆写文本文件(文件路径, 文本):
    with open(文件路径, 'w', encoding='utf-8') as 文件对象:
        文件对象.write(文本)

def 追加文本文件(文件路径, 文本):
    with open(文件路径, 'a', encoding='utf-8') as 文件对象:
        文件对象.write(文本)

def 读取对象文件(文件路径):
    with open(文件路径, 'r', encoding='utf-8') as 文件对象:
        return json.load(文件对象)

def 覆写对象文件(文件路径, 对象):
    with open(文件路径, 'w', encoding='utf-8') as 文件对象:
        json.dump(对象, 文件对象, ensure_ascii=False, indent=2)