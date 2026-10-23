
"""交互终端

不带参数运行「运行」时会进入这个终端，可以逐行输入燃梦中文代码并立即执行。

特点：
  · 变量、函数定义在多次输入之间保留
  · 多行结构（如 函数 … { … }）会自动等待闭合的 }
  · 支持内置命令，如 :帮助、:退出、:清空、:变量、:运行 文件
"""

import os
import sys

from 词法分析 import 语言词法分析, 词法错误
from 语法分析 import 语言语法分析
from 代码解释 import 语言代码解释, 解释工具
from 文件管理 import 读取文本文件


# ── 终端显示 ──────────────────────────────────────────────

def _支持颜色():
    return sys.stdout.isatty() and os.environ.get('NO_COLOR') is None


if _支持颜色():
    青 = '\033[36m'; 绿 = '\033[32m'; 黄 = '\033[33m'
    红 = '\033[31m'; 灰 = '\033[90m'; 粗 = '\033[1m'; 无 = '\033[0m'
else:
    青 = 绿 = 黄 = 红 = 灰 = 粗 = 无 = ''


提示符 = f'{青}燃梦{无}{灰}> {无}'
续行提示符 = f'{灰}...  {无}'


# ── 辅助命令 ──────────────────────────────────────────────

介绍 = f'''
{粗}燃梦中文语言 · 交互终端{无}

直接输入代码并按回车即可执行，例如：

    {绿}终端输出("你好，世界"){无}
    {绿}变量 文本:名字 = "张三"{无}
    {绿}终端输出(拼接("你好，", 名字)){无}

多行的结构会自动等待闭合，比如：

    {绿}函数 文本:问候(文本:谁) {{{无}
    {绿}    返回 拼接("你好，", 谁){无}
    {绿}}}{无}

输入 {黄}:帮助{无} 查看命令，{黄}:退出{无} 结束。
'''

命令说明 = f'''
{粗}可用命令{无}

    {黄}:帮助{无}          显示这份说明
    {黄}:退出{无}          退出终端（也可以按 Ctrl+D）
    {黄}:清空{无}          清空当前会话定义的变量与函数
    {黄}:变量{无}          列出已定义的变量
    {黄}:函数{无}          列出已定义的函数
    {黄}:运行 路径{无}     执行一个 .模块 或 源码文件
    {黄}:调试{无}          切换调试模式（显示词元与语法树）

    {灰}以 # 开头的行是注释，不会被当作命令{无}
'''


def 报错(信息):
    print(f'{红}{信息}{无}')


def 提示(信息):
    print(f'{灰}{信息}{无}')


# ── 语句完整性判断 ────────────────────────────────────────

def 需要续行(代码):
    """根据括号是否闭合，判断还要不要继续输入。"""
    深度 = 0
    在文本 = None
    上一字符 = ''
    for 字符 in 代码:
        if 在文本:
            if 字符 == 在文本:
                在文本 = None
            continue
        if 字符 in ('"', "'"):
            在文本 = 字符
        elif 字符 == '#':
            # 注释到行尾，跳过这一行剩余部分
            break
        elif 字符 in '({[':
            深度 += 1
        elif 字符 in ')}]':
            深度 -= 1
        上一字符 = 字符

    # 文本没闭合，也要继续输入
    if 在文本:
        return True
    return 深度 > 0


# ── 执行 ──────────────────────────────────────────────────

调试模式 = False


def 执行代码(代码, 文件目录=None):
    """执行一段代码，返回是否成功。"""
    try:
        词元列表, 词法语法树 = 语言词法分析(代码, 语法分析=True)
    except 词法错误 as 错误:
        报错(f'词法/语法错误：{错误}')
        return False
    except Exception as 错误:
        报错(f'解析出错：{错误}')
        return False

    if 调试模式:
        print(f'{灰}--- 词法分析结果 ---{无}')
        print(词法语法树.pretty())
        print(f'{灰}--------------------{无}')

    try:
        语法对象 = 语言语法分析(词法语法树)
    except Exception as 错误:
        报错(f'语法转换出错：{错误}')
        return False

    try:
        语言代码解释(语法对象, 文件目录=文件目录)
    except 词法错误 as 错误:
        报错(str(错误))
        return False
    except Exception as 错误:
        报错(f'运行出错：{type(错误).__name__}: {错误}')
        return False
    return True


# ── 内置命令 ──────────────────────────────────────────────

def 处理命令(行):
    """处理 : 开头的命令，返回 False 表示要退出。"""
    global 调试模式

    命令 = 行[1:].strip()
    词 = 命令.split(maxsplit=1)
    名称 = 词[0] if 词 else ''
    参数 = 词[1].strip() if len(词) > 1 else ''

    if 名称 in ('退出', 'quit', 'q', 'exit'):
        return False
    if 名称 in ('帮助', 'help', 'h', '?'):
        print(命令说明)
        return True
    if 名称 in ('清空', 'clear', 'reset'):
        from 代码解释 import 代码解释
        新解释器 = 代码解释()
        新解释器.文件目录 = 解释工具.文件目录
        解释工具.__dict__.clear()
        解释工具.__dict__.update(新解释器.__dict__)
        提示('已清空当前会话的变量与函数')
        return True
    if 名称 in ('变量', 'vars'):
        变量表 = 解释工具.变量列表
        if not 变量表:
            提示('还没有定义任何变量')
        else:
            for 名, 值 in 变量表.items():
                print(f'  {绿}{名}{无} = {值!r}')
        return True
    if 名称 in ('函数', 'funcs'):
        函数表 = 解释工具.结构列表
        如果空 = True
        for 名, 结构 in 函数表.items():
            if isinstance(结构, dict) and 结构.get('类型') == '模块':
                continue
            print(f'  {青}{名}{无}({len(结构.get("参数") or [])} 个参数)')
            如果空 = False
        if 如果空:
            提示('还没有定义任何函数')
        return True
    if 名称 in ('运行', 'run', 'load'):
        if not 参数:
            报错('用法：:运行 路径')
            return True
        if not os.path.isfile(参数):
            报错(f'文件不存在：{参数}')
            return True
        try:
            代码 = 读取文本文件(参数)
        except Exception as 错误:
            报错(f'读取失败：{错误}')
            return True
        提示(f'运行 {参数} …')
        执行代码(代码, 文件目录=os.path.dirname(os.path.abspath(参数)))
        return True
    if 名称 in ('调试', 'debug'):
        调试模式 = not 调试模式
        提示(f'调试模式：{"开" if 调试模式 else "关"}')
        return True

    报错(f'未知命令：{名称}（输入 :帮助 查看可用命令）')
    return True


# ── 主循环 ────────────────────────────────────────────────

def 主循环():
    print(介绍)

    缓冲 = []
    while True:
        try:
            提示文本 = 续行提示符 if 缓冲 else 提示符
            行 = input(提示文本)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            缓冲 = []
            continue

        # 空行：在续行状态里忽略，在普通状态里跳过
        if not 行.strip():
            if 缓冲:
                缓冲.append('')
                continue
            continue

        # 命令
        if not 缓冲 and 行.strip().startswith(':'):
            if not 处理命令(行.strip()):
                break
            continue

        缓冲.append(行)
        代码 = '\n'.join(缓冲)

        if 需要续行(代码):
            continue

        成功 = 执行代码(代码)
        缓冲 = []

    print(f'{灰}再见{无}')
    return 0


def 单次执行(代码, 文件目录=None):
    """执行一段代码后退出，供 -e 参数使用。"""
    return 0 if 执行代码(代码, 文件目录=文件目录) else 1


if __name__ == '__main__':
    sys.exit(主循环())
