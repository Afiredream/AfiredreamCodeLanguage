#!/bin/env python

from argparse import ArgumentParser

参数解析 = ArgumentParser(
    description='燃梦中文语言运行器',
    epilog='不带参数运行时会进入交互终端。'
)
参数解析.add_argument('文件', nargs='?', type=str,
                     help='要运行的文件；省略则进入交互终端')
参数解析.add_argument('--调试', action='store_true', help='输出词元与语法树')
参数解析.add_argument('-e', '--执行', dest='代码', type=str,
                     help='直接执行一段代码后退出')
参数解析.add_argument('--帮助', '--help-text', dest='帮助', action='store_true',
                     help='显示详细说明')
参数对象 = 参数解析.parse_args()

if 参数对象.帮助:
    参数解析.print_help()
    print('''
示例：
  ./运行                        进入交互终端
  ./运行 测试/测试01：你好世界    运行一个文件
  ./运行 -e '终端输出("你好")'    直接执行一段代码
  ./运行 --调试 文件              输出词元与语法树
''')
    raise SystemExit(0)


# ── 直接执行一段代码 ──────────────────────────────────────

if 参数对象.代码 is not None:
    import 交互终端
    交互终端.调试模式 = 参数对象.调试
    raise SystemExit(交互终端.单次执行(参数对象.代码, 文件目录='.'))


# ── 没有文件参数：进入交互终端 ────────────────────────────

if 参数对象.文件 is None:
    import 交互终端
    交互终端.调试模式 = 参数对象.调试
    raise SystemExit(交互终端.主循环())


# ── 运行一个文件 ──────────────────────────────────────────

from 词法分析 import 语言词法分析
from 语法分析 import 语言语法分析
from 代码解释 import 语言代码解释
from 文件管理 import 读取文本文件, 覆写文本文件, 覆写对象文件
from os import path as 路径工具

if not 路径工具.isfile(参数对象.文件):
    print(f'错误：文件不存在 -> {参数对象.文件}')
    raise SystemExit(1)

代码文本 = 读取文本文件(参数对象.文件)

# 词法分析：得到词元列表与语法树
词元列表, 词法语法树 = 语言词法分析(代码文本, 语法分析=True)
if 参数对象.调试:
    覆写文本文件(f"{参数对象.文件}.token", 词法语法树.pretty())

# 语法分析：把语法树转换为解释器使用的结构
语法对象 = 语言语法分析(词法语法树)
if 参数对象.调试:
    覆写对象文件(f"{参数对象.文件}.json", 语法对象)

语言代码解释(语法对象, 文件目录=路径工具.dirname(路径工具.abspath(参数对象.文件)))
