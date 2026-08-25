
from os import path
from lark import Lark
from pathlib import Path
from 通用函数 import 读取文本文件

源码目录 = Path(__file__).parent
语法文件 = path.join(源码目录, '语法规则.lark')
语法规则 = 读取文本文件(语法文件)
代码工具 = Lark(语法规则, parser='lalr') 

def 中文代码分析(中文代码):
  return 代码工具.parse(中文代码)