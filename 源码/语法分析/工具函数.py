def 构建语法树(token数组):
    """
    根据词法分析结果构建语法树
    
    Args:
        token数组: 词法分析后的二维数组，每个元素包含字词、类型、行号、列号
    
    Returns:
        语法树字典
    """
    语法树 = {
        "类型": "程序",
        "行号": 1,
        "列号": 1,
        "子节点": []
    }
    
    def 解析语句(行):
        """解析单行语句"""
        if not 行:
            return None
        
        第一个Token = 行[0]
        字词 = 第一个Token.get("字词")
        类型 = 第一个Token.get("类型")
        行号 = 第一个Token.get("行号")
        列号 = 第一个Token.get("列号")
        
        # 判断语句类型
        if 字词 == "定义" and 类型 == "关键字":
            return 解析定义语句(行)
        elif 字词 == "函数" and 类型 == "关键字":
            return 解析函数定义(行)
        elif 字词 in ["如果", "否则", "循环"] and 类型 == "关键字":
            return 解析控制语句(行)
        elif 类型 in ["内置函数", "标识符"]:
            return 解析表达式(行)
        else:
            return {
                "类型": "未知语句",
                "内容": [t.get("字词") for t in 行],
                "行号": 行号,
                "列号": 列号
            }
    
    def 解析定义语句(行):
        """解析定义语句: 定义 变量名 ： 类型 = 值"""
        if len(行) < 3:
            return None
        
        定义Token = 行[0]
        变量Token = 行[1]
        行号 = 定义Token.get("行号")
        列号 = 定义Token.get("列号")
        
        定义节点 = {
            "类型": "定义语句",
            "变量名": 变量Token.get("字词"),
            "行号": 行号,
            "列号": 列号,
            "子节点": []
        }
        
        # 查找冒号和类型
        索引 = 2
        if 索引 < len(行) and 行[索引].get("字词") == "：":
            # 有类型声明
            if 索引 + 1 < len(行):
                类型Token = 行[索引 + 1]
                定义节点["变量类型"] = 类型Token.get("字词")
                索引 += 2
        
        # 查找赋值运算符
        if 索引 < len(行) and 行[索引].get("字词") == "=":
            索引 += 1
            # 解析值
            if 索引 < len(行):
                # 收集值部分
                值部分 = 行[索引:]
                值节点 = 解析简单表达式(值部分)
                if 值节点:
                    定义节点["值"] = 值节点
                    定义节点["子节点"].append(值节点)
        else:
            # 没有赋值，默认为None
            定义节点["值"] = {
                "类型": "空值",
                "值": None
            }
        
        return 定义节点
    
    def 解析函数定义(行):
        """解析函数定义: 函数 函数名(参数)"""
        if len(行) < 4:
            return None
        
        函数Token = 行[0]
        函数名Token = 行[1]
        行号 = 函数Token.get("行号")
        列号 = 函数Token.get("列号")
        
        函数节点 = {
            "类型": "函数定义",
            "函数名": 函数名Token.get("字词"),
            "参数": [],
            "行号": 行号,
            "列号": 列号,
            "子节点": []
        }
        
        # 查找参数列表
        索引 = 2
        if 索引 < len(行) and 行[索引].get("字词") == "(":
            索引 += 1
            # 收集参数直到遇到 ")"
            while 索引 < len(行) and 行[索引].get("字词") != ")":
                参数Token = 行[索引]
                if 参数Token.get("类型") == "标识符":
                    函数节点["参数"].append(参数Token.get("字词"))
                elif 参数Token.get("字词") in [",", "，"]:
                    # 跳过逗号
                    pass
                索引 += 1
        
        return 函数节点
    
    def 解析控制语句(行):
        """解析控制语句: 如果/否则/循环 条件"""
        if len(行) < 2:
            return None
        
        关键字Token = 行[0]
        行号 = 关键字Token.get("行号")
        列号 = 关键字Token.get("列号")
        
        控制节点 = {
            "类型": f"{关键字Token.get('字词')}语句",
            "行号": 行号,
            "列号": 列号,
            "子节点": []
        }
        
        # 解析条件
        索引 = 1
        条件部分 = []
        while 索引 < len(行):
            条件部分.append(行[索引])
            索引 += 1
        
        if 条件部分:
            条件节点 = 解析简单表达式(条件部分)
            if 条件节点:
                控制节点["条件"] = 条件节点
                控制节点["子节点"].append(条件节点)
        
        return 控制节点
    
    def 解析表达式(行):
        """解析表达式: 函数调用、赋值等"""
        if not 行:
            return None
        
        第一个Token = 行[0]
        字词 = 第一个Token.get("字词")
        类型 = 第一个Token.get("类型")
        行号 = 第一个Token.get("行号")
        列号 = 第一个Token.get("列号")
        
        # 函数调用: 函数名(参数)
        if len(行) >= 3 and 行[1].get("字词") == "(":
            函数节点 = {
                "类型": "函数调用",
                "函数名": 字词,
                "函数类型": 类型,
                "参数": None,
                "行号": 行号,
                "列号": 列号,
                "子节点": []
            }
            
            # 提取参数
            索引 = 2
            if 索引 < len(行) and 行[索引].get("字词") != ")":
                # 收集参数部分（到 ")" 为止）
                参数部分 = []
                while 索引 < len(行) and 行[索引].get("字词") != ")":
                    参数部分.append(行[索引])
                    索引 += 1
                
                if 参数部分:
                    # 过滤掉括号和逗号
                    过滤后 = [t for t in 参数部分 if t.get("字词") not in ["(", ")", ",", "，"]]
                    if 过滤后:
                        参数节点 = 解析简单表达式(过滤后)
                        if 参数节点:
                            函数节点["参数"] = 参数节点
                            函数节点["子节点"].append(参数节点)
            
            return 函数节点
        
        # 赋值表达式: 变量 = 值
        elif len(行) >= 3:
            # 查找赋值运算符
            for i, token in enumerate(行):
                if token.get("字词") == "=":
                    赋值节点 = {
                        "类型": "赋值表达式",
                        "变量": 字词,
                        "行号": 行号,
                        "列号": 列号,
                        "子节点": []
                    }
                    
                    # 解析值部分
                    值部分 = 行[i+1:]
                    if 值部分:
                        值节点 = 解析简单表达式(值部分)
                        if 值节点:
                            赋值节点["值"] = 值节点
                            赋值节点["子节点"].append(值节点)
                    
                    return 赋值节点
        
        # 简单表达式
        return 解析简单表达式(行)
    
    def 解析简单表达式(行):
        """解析简单表达式: 字面量、变量引用等"""
        if not 行:
            return None
        
        token = 行[0]
        字词 = token.get("字词")
        类型 = token.get("类型")
        行号 = token.get("行号")
        列号 = token.get("列号")
        
        # 字符串常量
        if 类型 == "字符串常量":
            return {
                "类型": "字符串字面量",
                "值": 字词,
                "行号": 行号,
                "列号": 列号
            }
        
        # 数字常量
        elif 类型 == "数字常量":
            return {
                "类型": "数字字面量",
                "值": 字词,
                "行号": 行号,
                "列号": 列号
            }
        
        # 布尔常量
        elif 类型 == "布尔常量":
            return {
                "类型": "布尔字面量",
                "值": 字词 == "真" or 字词 == "True",
                "行号": 行号,
                "列号": 列号
            }
        
        # 标识符
        elif 类型 == "标识符":
            return {
                "类型": "变量引用",
                "变量名": 字词,
                "行号": 行号,
                "列号": 列号
            }
        
        # 运算表达式
        elif len(行) >= 3:
            # 检查是否包含运算符
            for i, t in enumerate(行):
                if t.get("类型") in ["赋值运算符", "算术运算符", "比较运算符"]:
                    # 左操作数
                    左操作数 = {
                        "类型": "变量引用",
                        "变量名": 行[0].get("字词"),
                        "行号": 行[0].get("行号"),
                        "列号": 行[0].get("列号")
                    }
                    # 右操作数
                    右操作数 = 解析简单表达式(行[i+1:])
                    
                    return {
                        "类型": "二元运算",
                        "运算符": t.get("字词"),
                        "左操作数": 左操作数,
                        "右操作数": 右操作数,
                        "行号": 行号,
                        "列号": 列号
                    }
        
        # 处理括号表达式 (表达式)
        if 字词 == "(" and len(行) >= 3:
            内部 = 行[1:-1]
            if 内部:
                return 解析简单表达式(内部)
        
        # 默认返回
        return {
            "类型": "其他",
            "值": 字词,
            "行号": 行号,
            "列号": 列号
        }
    
    # 处理每一行
    for 行 in token数组:
        语句节点 = 解析语句(行)
        if 语句节点:
            语法树["子节点"].append(语句节点)
    
    return 语法树

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

import json
import os

def 读取JSON文件(文件路径, 编码="utf-8"):
    """
    读取JSON文件并转换为Python对象
    
    Args:
        文件路径: JSON文件路径
        编码: 文件编码
    
    Returns:
        转换后的Python对象，失败返回None
    """
    try:
        with open(文件路径, 'r', encoding=编码) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {文件路径}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

