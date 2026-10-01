#!/bin/env python

import ast
from 词法分析 import 语言词法分析
from 语法分析 import 语言语法分析
from 代码解释 import 语言代码解释
from argparse import ArgumentParser
from 文件管理 import 读取文本文件, 覆写文本文件, 覆写对象文件

参数解析 = ArgumentParser(description='这是一个示例程序')
参数解析.add_argument('文件', type=str, help='输入文件路径（必选）')
参数解析.add_argument('--调试', action='store_true', help='启用详细输出')
参数对象 = 参数解析.parse_args()

代码文本 = 读取文本文件(参数对象.文件)

词元列表 = 语言词法分析(代码文本)
if 参数对象.调试: 覆写文本文件(f"{参数对象.文件}.token", 词元列表.pretty())

语法对象 = 语言语法分析(词元列表)
if 参数对象.调试: 覆写对象文件(f"{参数对象.文件}.json",语法对象)

语言代码解释(语法对象)