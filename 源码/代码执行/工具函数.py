def AST转Python代码改进版(AST树):
    """改进版本：更好地处理字符串和变量"""
    
    python代码 = []
    缩进 = 0
    已定义变量 = set()
    
    def 获取缩进():
        return "    " * 缩进
    
    def 清理字符串(值):
        """清理字符串值"""
        if not 值:
            return '""'
        
        值 = str(值)
        # 移除可能的多余引号
        if 值.startswith('"') and 值.endswith('"'):
            值 = 值[1:-1]
        elif 值.startswith("'") and 值.endswith("'"):
            值 = 值[1:-1]
        
        # 处理中文引号
        值 = 值.replace('“', '').replace('”', '')
        值 = 值.replace('『', '').replace('』', '')
        
        # 转义内部引号
        值 = 值.replace('"', '\\"')
        
        return f'"{值}"'
    
    def 处理节点(节点):
        nonlocal 缩进
        类型 = 节点.get("类型")
        
        if 类型 == "程序":
            for 子节点 in 节点.get("子节点", []):
                处理节点(子节点)
        
        elif 类型 == "定义语句":
            变量名 = 节点.get("变量名")
            值节点 = 节点.get("值")
            
            # 记录已定义变量
            已定义变量.add(变量名)
            
            if 值节点:
                值代码 = 处理表达式(值节点)
                python代码.append(f"{获取缩进()}{变量名} = {值代码}")
            else:
                python代码.append(f"{获取缩进()}{变量名} = None")
        
        elif 类型 == "函数定义":
            函数名 = 节点.get("函数名")
            参数列表 = 节点.get("参数", [])
            
            # 记录函数
            已定义变量.add(函数名)
            
            python代码.append(f"{获取缩进()}def {函数名}({', '.join(参数列表)}):")
            缩进 += 1
            
            子节点 = 节点.get("子节点", [])
            if 子节点:
                for 子节点 in 子节点:
                    处理节点(子节点)
            else:
                python代码.append(f"{获取缩进()}pass")
            
            缩进 -= 1
        
        elif 类型 == "函数调用":
            函数名 = 节点.get("函数名")
            参数节点 = 节点.get("参数")
            
            # 映射内置函数
            if 函数名 == "输出":
                函数名 = "print"
            elif 函数名 == "输入":
                函数名 = "input"
            
            if 参数节点:
                参数代码 = 处理表达式(参数节点)
                python代码.append(f"{获取缩进()}{函数名}({参数代码})")
            else:
                python代码.append(f"{获取缩进()}{函数名}()")
    
    def 处理表达式(节点):
        if not 节点:
            return "None"
        
        类型 = 节点.get("类型")
        
        if 类型 == "字符串字面量":
            值 = 节点.get("值", "")
            return 清理字符串(值)
        
        elif 类型 == "变量引用":
            变量名 = 节点.get("变量名")
            # 清理变量名
            if 变量名:
                变量名 = 变量名.replace('"', '').replace("'", '')
                变量名 = 变量名.replace('“', '').replace('”', '')
            return 变量名
        
        elif 类型 == "数字字面量":
            return str(节点.get("值", 0))
        
        elif 类型 == "布尔字面量":
            return "True" if 节点.get("值", False) else "False"
        
        elif 类型 == "空值":
            return "None"
        
        else:
            return str(节点.get("值", "None"))
    
    处理节点(AST树)
    return '\n'.join(python代码)

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

def 保存代码(代码, 文件路径):
    """保存代码到文件"""
    with open(文件路径, 'w', encoding='utf-8') as f:
        f.write(代码.replace('\\n', '\n'))
    print(f"✅ 已保存: {文件路径}")


