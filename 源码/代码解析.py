#!/bin/env python3
import os
import ast
import json
from pathlib import Path
from lark import Lark, Transformer, Token, Tree
from 通用函数 import 读取文本文件, 覆写对象文件, 覆写文本文件

代码文本 = 读取文本文件("/home/usr/燃梦中文语言/测试/测试文件")

源码目录 = Path(__file__).parent

语法文件 = os.path.join(源码目录, '语法规则.lark')
语法文本 = 读取文本文件(语法文件)


代码工具 = Lark(语法文本, parser='lalr') 
代码结构 = 代码工具.parse(代码文本)


# print(代码结构)


class 代码转换(Transformer):

    def start(自己, 项目):
        return {"类型": "代码", "代码": 项目}
    def statement(自己, 项目):
        return 项目[0] if 项目 else None

    def 量值定义(自己, 项目, 语义):
        return {
            "语义": 语义,
            "类型": 自己.提取数值(项目[0]),
            "名称": 自己.提取数值(项目[1]),
            "数值": 自己.提取数值(项目[2]),
        }
    def define_constant(自己, 项目):
        return 自己.量值定义(项目, "定义常量")
    def define_variable(自己, 项目):
        return 自己.量值定义(项目, "定义变量")
    def define_capacity(自己, 项目):
        return 自己.量值定义(项目, "定义容量")
    def define_type(自己, 项目):
        return 自己.量值定义(项目, "定义类型")
    def define_property(自己, 项目):
        return 自己.量值定义(项目, "定义属性")

    def 结构定义(自己, 项目, 语义):
        return {
            "语义": 语义,
            "返回": 自己.提取数值(项目[0]),
            "名称": 自己.提取数值(项目[1]),
            "参数": 项目[2],
            "代码": 项目[3]
        }
    def define_function(自己, 项目):
        return 自己.结构定义(项目, "定义函数")
    def define_structure(自己, 项目):
        return 自己.结构定义(项目, "定义结构")

    def access_pipe(自己, 项目):
        return {
            "语义": "访问管道",
            "名称": 自己.提取数值(项目[0]),
            "属性": [自己.提取数值(项目[i]) for i in range(1, len(项目), 2)]
        }

    def function(自己, 项目):
        return {
            "语义": "调用函数",
            "名称": 自己.提取数值(项目[0]),
            "参数": 自己.提取数值(项目[1])
        }

    def type(自己, 项目):
        return 项目[0] if 项目 else None
    
    def name(自己, 项目):
        return 项目[0] if 项目 else None
    
    def value(自己, 项目):
        return 项目[0] if 项目 else None
    
    def string(自己, 项目):
        if (项目):
          数值 = 自己.提取数值(项目[0])
          数值 = 数值[1:-1]
          return {"类型":"文本","数值": 数值}
        else:
          return None
    
    def params(自己, 项目):
        params = []
        for i in range(0, len(项目), 2):
            if i+1 < len(项目):
                params.append({
                    "类型": 自己.提取数值(项目[i]),
                    "名称": 自己.提取数值(项目[i+1])
                })
        return params
    
    def arguments(自己, 项目):
        return [自己.提取数值(项目) for 项目 in 项目]
    
    def 提取数值(自身, 节点):
        if isinstance(节点, Tree):
            if 节点.data == 'name':
                return 自身, 节点.提取数值(节点.children[0]) if 节点.children else None
            elif 节点.data == 'value':
                return 自身, 节点.提取数值(节点.children[0]) if 节点.children else None
            elif 节点.data == 'string':
                return 节点.children[0].value if 节点.children else None
            elif 节点.data == 'type':
                return None
            else:
                return 自身.提取数值(节点.children[0]) if 节点.children else None
        elif isinstance(节点, Token):
            return 节点.value
        elif isinstance(节点, list):
            return [自身.提取数值(item) for item in 节点]
        return 节点
    
    def 提取参数(self, node):
        """提取参数列表"""
        if isinstance(node, Tree) and node.data == 'param':
            return [self.提取数值(child) for child in node.children if child]
        elif isinstance(node, Tree) and node.data == 'arguments':
            return [self.提取数值(child) for child in node.children if child]
        return []

转换工具 = 代码转换()
最终代码 = 转换工具.transform(代码结构)
# print(最终代码)

覆写对象文件("/home/usr/燃梦中文语言/测试/测试文件.json", 最终代码)

class 语法对象转换:

    def __init__(self):
        self.变量列表 = {} 
        
    def 转换对象(自己, 对象):
        节点列表 = 对象["代码"]
        节点列表 = 自己.转换列表(节点列表)
        语法模块 = ast.Module(body=节点列表, type_ignores=[])
        return 语法模块

    def 转换列表(自己, 列表):
        节点列表 = []
        for 语法节点 in 列表:
            节点 = 自己.转换节点(语法节点)
            if 节点: 节点列表.append(节点)
        return 节点列表

    def 转换节点(self, 节点):
            语义 = 节点["语义"]
            if 语义 == "定义常量":
                return self.转换变量(节点)
            elif 语义 == "定义变量":
                return self.转换变量(节点)
            elif 语义 == "定义容量":
                return self.转换变量(节点)
            elif 语义 == "定义函数":
                return self.转换函数(节点)
            elif 语义 == "调用函数":
                return self.转换调用(节点)
            else:
                print(节点)
    
    def 转换变量(self, 节点):

        名称 = 节点["名称"]
        类型 = 节点["类型"]
        数值 = 节点["数值"]["数值"]
        self.变量列表[名称] = {"类型": 类型, "数值": 数值}
        节点 = ast.Assign(
            targets=[ast.Name(id=名称, ctx=ast.Store())],
            value=ast.Constant(value=数值)
        )
        return ast.fix_missing_locations(节点)
    
    def 转换容量(self, 节点):
        """转换数组/容量定义"""
        变量名 = 节点["名称"]
        值 = 节点["数值"]
        
        # 创建列表节点
        if isinstance(值, dict) and 值.get("类型") == "文本":
            文本值 = 值["数值"].strip('"')
            值节点 = ast.List(
                elts=[ast.Constant(value=文本值)],
                ctx=ast.Load()
            )
        else:
            值节点 = self.转换值(值)
        
        return ast.Assign(
            targets=[ast.Name(id=变量名, ctx=ast.Store())],
            value=值节点
        )
    
    def 转换函数(自己, 节点):
        函数名称 = 节点["名称"]
        返回类型 = 节点["返回"]
        参数列表 = 节点["参数"]
        子代码块 = 节点["代码"]
        
        参数节点 = 自己.转换参数(参数列表)
        代码节点 = 自己.转换列表(子代码块)
 
        节点 =  ast.FunctionDef(
            name=函数名称,
            args=参数节点,
            body=代码节点,
            decorator_list=[],
            returns=None
        )
        return ast.fix_missing_locations(节点)
    
    def 转换参数(自己, 列表):
        参数列表 = []
        for 参数 in 列表:
            参数名称 = 参数["名称"]
            参数类型 = 参数["类型"]
            

            参数对象 = ast.arg(
                arg=参数名称,
                annotation=ast.Name(id=自己.类型映射(参数类型), ctx=ast.Load())
            )
            参数列表.append(参数对象)
        
        节点 = ast.arguments(
            posonlyargs=[],
            args=参数列表,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]
        )
        return ast.fix_missing_locations(节点)
    
    def 转换调用(自己, 节点):
        函数名称 = 节点["名称"]
        函数参数 = 节点["参数"]
        if 函数名称 == "输出": 函数名称 = "print"
        
        参数节点 = []
        for 参数 in 函数参数:
            if isinstance(参数, str):
                参数节点.append(ast.Name(id=参数, ctx=ast.Load()))
            else:
                参数节点.append(ast.Constant(value=参数["数值"]))
        
        节点 = ast.Expr(
            value=ast.Call(
                func=ast.Name(id=函数名称, ctx=ast.Load()),
                args=参数节点,
                keywords=[]
            )
        )
        return ast.fix_missing_locations(节点)
    
    def 转换值(self, 值节点):
        """转换值节点"""
        if isinstance(值节点, dict):
            类型 = 值节点.get("类型", "")
            数值 = 值节点.get("数值", "")
            
            if 类型 == "文本":
                # 移除引号
                文本 = 数值.strip('"')
                return ast.Constant(value=文本)
            elif 类型 == "数字":
                try:
                    return ast.Constant(value=int(数值))
                except:
                    return ast.Constant(value=float(数值))
            elif 类型 == "数组":
                # 处理数组
                return self.转换数组(数值)
            else:
                # 尝试作为变量引用
                return ast.Name(id=数值, ctx=ast.Load())
        else:
            # 直接值
            return ast.Constant(value=值节点)
    
    def 转换数组(self, 数组数据):
        """转换数组字面量"""
        if isinstance(数组数据, list):
            elts = [self.转换值(item) for item in 数组数据]
        else:
            # 处理字符串数组
            elts = [ast.Constant(value=数组数据)]
        return ast.List(elts=elts, ctx=ast.Load())
    
    def 转换表达式(self, 节点):
        """通用表达式转换"""
        # 处理各种表达式
        if "数值" in 节点:
            return self.转换值(节点)
        elif "名称" in 节点:
            return ast.Name(id=节点["名称"], ctx=ast.Load())
        else:
            return ast.Constant(value=str(节点))
    
    def 类型映射(self, 类型名):
        类型映射表 = {
            "文本": "str",
            "数字": "int",
            "数组": "list",
            "字典": "dict",
            "布尔": "bool"
        }
        return 类型映射表.get(类型名, "Any")
    

转化工具 = 语法对象转换()
语言对象 =  转化工具.转换对象(最终代码)


覆写文本文件("/home/usr/燃梦中文语言/测试/测试文件.ast", ast.dump(语言对象, indent=4))
代码文本 = ast.unparse(语言对象)
print(语言对象)
print(ast.unparse(语言对象))


覆写文本文件("/home/usr/燃梦中文语言/测试/测试文件.py", 代码文本)