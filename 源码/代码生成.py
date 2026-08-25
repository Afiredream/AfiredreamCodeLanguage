
import ast
from os import path
from pathlib import Path
from 文件管理 import 读取文本文件

源码目录 = Path(__file__).parent
脚本文件 = path.join(源码目录, '内置函数.py')
内置函数 = 读取文本文件(脚本文件)

def 生成目标代码(对象结构):
  return 内置函数 + ast.unparse(对象结构)