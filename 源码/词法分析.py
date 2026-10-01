
from os import path
from lark import Lark
from pathlib import Path
from 文件管理 import 读取文本文件

源码目录 = Path(__file__).parent
语法文件 = path.join(源码目录, '语法规则.lark')
语法文本 = 读取文本文件(语法文件)
分析工具 = Lark(语法文本, parser='lalr') 

def 语言词法分析(代码文本):
  return 分析工具.parse(代码文本)