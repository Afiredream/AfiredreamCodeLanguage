import re
from 词法规则 import 关键字词, 运算符号, 函数名称

def 过滤空白元素(数组):


def 遍历一维数组(数组, 函数):
    return [函数(元素) for 元素 in 数组]

def 空格分割文本(文本):
    数组 = 文本.splitlines()
    数组 = 遍历一维数组(数组, )

def 按照换行空格解析文本(text):
    # 第一步：按换行分割，去除空行
    lines = text.splitlines()  # splitlines() 会自动处理各种换行符
    lines = [line for line in lines if line.strip() != '']  # 去除空行或只有空格的行
    
    # 第二步：按空格分割每行，保留空元素
    result = []
    for line in lines:
        # 使用 split(' ') 按单个空格分割，保留空字符串
        words = line.split(' ')  # 注意：这里使用单空格作为分隔符
        # 即使 words 包含空字符串，也添加到结果中
        result.append(words)
    
    return result

def 读取文本文件(file_path):
    """
    读取文件内容并返回文本
    
    参数:
        file_path: 文件路径（相对路径或绝对路径）
        
    返回:
        文件内容的字符串
        
    异常:
        FileNotFoundError: 文件不存在
        PermissionError: 没有读取权限
        UnicodeDecodeError: 编码问题
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()



def 解析二维数组符号(arr_2d):
    # 定义需要分裂的标点符号
    punctuations = ['：', ':', '；', ';', '，', ',', '。', '.', '！', '!', '？', '?', 
                    '（', '(', '）', ')', '【', '[', '】', ']', '{', '}', '《', '<', '》', '>', '"', "'", '、']
    pattern = '([' + '|'.join(re.escape(p) for p in punctuations) + '])'
    
    result = []
    for row in arr_2d:
        new_row = []
        for element in row:
            if isinstance(element, str):
                parts = re.split(pattern, element)
                new_row.extend(parts)  # 保留空元素
            else:
                new_row.append(element)
        result.append(new_row)
    return result
    




def 解析字词类型(二维数组):
    """
    解析二维数组中的每个元素，返回包含字词和类型的对象列表
    
    Args:
        二维数组: 二维列表
    
    Returns:
        二维列表，每个元素为 {"字词": 值, "类型": 类型名}
    """
    # 构建所有符号的查找集合
    所有关键字 = set(关键字词.get("关键词语", []))
    所有标识符 = set(关键字词.get("标识名称", []))
    所有数据类型 = set(关键字词.get("数据类型", []))
    所有逻辑词 = set(关键字词.get("逻辑运算符", []))
    所有内置函数 = set(关键字词.get("内置函数", []))
    
    # 运算符号分类
    赋值符 = set(运算符号.get("赋值运算符", []))
    算术符 = set(运算符号.get("算术运算符", []))
    比较符 = set(运算符号.get("比较运算符", []))
    逻辑符 = set(运算符号.get("逻辑运算符", []))
    位运算符 = set(运算符号.get("位运算符", []))
    分隔符 = set(运算符号.get("分隔符号", []))
    注释符 = set(运算符号.get("注释符号", []))
    特殊符 = set(运算符号.get("特殊符号", []))
    
    # 函数名称分类
    基础函数 = set(函数名称.get("基础函数", []))
    数学函数 = set(函数名称.get("数学函数", []))
    字符串函数 = set(函数名称.get("字符串函数", []))
    列表函数 = set(函数名称.get("列表函数", []))
    字典函数 = set(函数名称.get("字典函数", []))
    文件函数 = set(函数名称.get("文件函数", []))
    时间函数 = set(函数名称.get("时间函数", []))
    类型函数 = set(函数名称.get("类型函数", []))
    
    # 合并所有函数
    所有函数 = (基础函数 | 数学函数 | 字符串函数 | 列表函数 | 
               字典函数 | 文件函数 | 时间函数 | 类型函数)
    
    # 合并所有符号
    所有符号 = (赋值符 | 算术符 | 比较符 | 逻辑符 | 位运算符 | 
               分隔符 | 注释符 | 特殊符)
    
    def 判断类型(字词):
        """判断单个字词的类型"""
        if not isinstance(字词, str):
            return "未知"
        
        # 去除首尾空格
        字词 = 字词.strip()
        
        if not 字词:
            return "空元素"
        
        # 检查是否为关键字
        if 字词 in 所有关键字:
            return "关键字"
        
        # 检查是否为标识符
        if 字词 in 所有标识符:
            return "标识符"
        
        # 检查是否为数据类型
        if 字词 in 所有数据类型:
            return "数据类型"
        
        # 检查是否为逻辑运算符
        if 字词 in 所有逻辑词:
            return "逻辑运算符"
        
        # 检查是否为内置函数
        if 字词 in 所有内置函数:
            return "内置函数"
        
        # 检查是否为函数名称
        if 字词 in 所有函数:
            # 判断具体是哪种函数
            if 字词 in 基础函数:
                return "基础函数"
            elif 字词 in 数学函数:
                return "数学函数"
            elif 字词 in 字符串函数:
                return "字符串函数"
            elif 字词 in 列表函数:
                return "列表函数"
            elif 字词 in 字典函数:
                return "字典函数"
            elif 字词 in 文件函数:
                return "文件函数"
            elif 字词 in 时间函数:
                return "时间函数"
            elif 字词 in 类型函数:
                return "类型转换函数"
            return "函数"
        
        # 检查是否为运算符号
        if 字词 in 所有符号:
            if 字词 in 赋值符:
                return "赋值运算符"
            elif 字词 in 算术符:
                return "算术运算符"
            elif 字词 in 比较符:
                return "比较运算符"
            elif 字词 in 逻辑符:
                return "逻辑运算符"
            elif 字词 in 位运算符:
                return "位运算符"
            elif 字词 in 分隔符:
                return "分隔符"
            elif 字词 in 注释符:
                return "注释符"
            elif 字词 in 特殊符:
                return "特殊符号"
            return "运算符号"
        
        # 数字检查
        if 字词.replace('.', '').replace('-', '').isdigit():
            return "数字常量"
        
        # 字符串检查（带引号）
        if (字词.startswith('"') and 字词.endswith('"')) or \
           (字词.startswith("'") and 字词.endswith("'")):
            return "字符串常量"
        
        # 布尔值
        if 字词 in ["True", "False", "true", "false"]:
            return "布尔常量"
        
        # 空值
        if 字词 in ["None", "null", "undefined"]:
            return "空值"
        
        # 默认标识符
        return "标识符"
    
    # 处理二维数组
    result = []
    for row in 二维数组:
        new_row = []
        for element in row:
            if isinstance(element, str):
                # 使用之前的解析函数分割字词
                parts = 解析二维数组符号([[element]])[0]
                for part in parts:
                    if part:  # 忽略空字符串
                        new_row.append({
                            "字词": part,
                            "类型": 判断类型(part)
                        })
            else:
                new_row.append({
                    "字词": str(element),
                    "类型": "其他"
                })
        result.append(new_row)
    
    return result

def 添加行号和列号(token数组):
    """
    为词法分析结果添加行号和列号
    
    Args:
        token数组: 词法分析后的二维数组
    
    Returns:
        带有行号和列号的Token数组
    """
    result = []
    行号 = 1
    
    for 行 in token数组:
        列号 = 1
        新行 = []
        for token in 行:
            # 复制原token并添加行号和列号
            新token = token.copy() if isinstance(token, dict) else dict(token)
            新token["行号"] = 行号
            新token["列号"] = 列号
            新行.append(新token)
            
            # 更新列号（根据字词长度）
            字词长度 = len(token.get("字词", ""))
            列号 += 字词长度 + 1  # +1 是为了下一个token之间的间距
        
        result.append(新行)
        行号 += 1
    
    return result

import json
import os

def 将对象写入文件(数据, 文件路径, 格式="json", 缩进=2, 编码="utf-8"):
    """
    将对象转换为文本并写入文件，支持多种格式
    
    Args:
        数据: 要写入的对象（字典、列表等）
        文件路径: 文件路径
        格式: 输出格式 ("json", "python", "yaml", "text", "pretty")
        缩进: 缩进空格数
        编码: 文件编码
    
    Returns:
        bool: 是否写入成功
    """
    try:
        # 创建目录（如果不存在）
        目录 = os.path.dirname(文件路径)
        if 目录 and not os.path.exists(目录):
            os.makedirs(目录)
        
        # 根据格式转换
        if 格式 == "json":
            文本 = json.dumps(数据, ensure_ascii=False, indent=缩进)
        
        elif 格式 == "python":
            文本 = 对象转Python文本(数据, 缩进)
        
        elif 格式 == "pretty":
            文本 = 对象转美观文本(数据, 缩进)
        
        elif 格式 == "yaml":
            文本 = 对象转YAML(数据)
        
        else:  # text
            文本 = str(数据)
        
        # 写入文件
        with open(文件路径, 'w', encoding=编码) as f:
            f.write(文本)
        
        return True
        
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False