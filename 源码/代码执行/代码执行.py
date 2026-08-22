#!/bin/env python3
import sys

from 工具函数 import  AST转Python代码改进版, 读取JSON文件, 保存代码
from ...工具函数 import 覆写文本文件

语法大树 = 读取JSON文件(sys.argv[1])
代码文本 = AST转Python代码改进版(语法大树)
覆写文本文件(sys.argv[2], 代码文本)