#!/bin/env python

import ast
from 词法分析 import 中文代码分析
from 语法分析 import 树状结构分析
from 结构转换 import 对象结构转换
from 代码生成 import 生成目标代码
from argparse import ArgumentParser
from 文件管理 import 读取文本文件, 覆写文本文件, 覆写对象文件

参数解析 = ArgumentParser(description='这是一个示例程序')
参数解析.add_argument('文件', type=str, help='输入文件路径（必选）')
参数解析.add_argument('--调试', action='store_true', help='启用详细输出')
参数对象 = 参数解析.parse_args()

代码文本 = 读取文本文件(参数对象.文件)

树状结构 = 中文代码分析(代码文本)
if 参数对象.调试: 覆写文本文件(f"{参数对象.文件}.token", 树状结构.pretty())

对象结构 = 树状结构分析(树状结构)
if 参数对象.调试: 覆写对象文件(f"{参数对象.文件}.json",对象结构)

目标结构 = 对象结构转换(对象结构)
if 参数对象.调试: 覆写文本文件(f"{参数对象.文件}.ast",ast.dump(目标结构, indent=2))

目标代码 = 生成目标代码(目标结构)
if 参数对象.调试: 覆写文本文件(f"{参数对象.文件}.py",目标代码)

exec(目标代码)