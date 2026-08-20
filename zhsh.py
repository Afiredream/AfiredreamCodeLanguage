#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# zhsh -> zsh 编译器

import sys, os, subprocess, re

# ============ 全局控制开关 ============
保留中间文件 = False
直接运行 = False

# ============ 翻译映射表 ============
关键字映射 = {
    '导出': 'export',
    '如果': 'if',
    '或者': 'elif',
    '否则': 'else',
    '那么': 'then',
    '结束如果': 'fi',
    '对于': 'for',
    '在': 'in',
    '结束对于': 'done',
    '循环': 'while',
    '结束循环': 'done',
    '函数': 'function',
    '结束函数': '}',
    '返回': 'return',
    '本地': 'local',
    '整数': 'integer',   # zsh 中用 typeset -i
    '只读': 'readonly',
    '未设置': 'unset',
    '类型': 'typeset',
    '执行': 'eval',
    '来源': 'source',
    '目录路径': 'dir_path',  # 示例变量名，但不强制转换
    '文件路径': 'file_path',
}

# ============ 核心编译函数 ============
def 编译(源文件, 目标文件):
    """将zhsh脚本编译为zsh脚本"""
    with open(源文件, 'r', encoding='utf-8') as f:
        行列表 = f.readlines()

    新行列表 = []
    for 行 in 行列表:
        原始行 = 行
        行 = 行.rstrip('\n')

        # 1. 首行 #! 替换为 #!/bin/zsh
        if 行.strip().startswith('#!'):
            行 = '#!/bin/zsh'
        # 2. 注释行保留
        elif 行.strip().startswith('#'):
            pass  # 保持原样
        # 3. 关键字替换（整词匹配）
        else:
            for 中文, 英文 in 关键字映射.items():
                # 使用正则确保替换的是独立单词（边界匹配）
                行 = re.sub(r'\b' + 中文 + r'\b', 英文, 行)

        # 4. 处理特殊语法：目录路径="..." -> dir_path="..." (示例保持变量名)
        #    实际可根据需要扩展，这里保留原变量名
        新行列表.append(行 + '\n')

    # 写入目标文件
    with open(目标文件, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(新行列表)

    # 添加可执行权限
    os.chmod(目标文件, 0o755)

# ============ 主程序 ============
if __name__ == '__main__':
    # 解析命令行参数：-r 保留中间文件，-k 直接运行
    参数列表 = sys.argv[1:]
    源文件路径 = None
    for 参数 in 参数列表:
        if 参数.startswith('-'):
            if 'r' in 参数:
                保留中间文件 = True
            if 'k' in 参数:
                直接运行 = True
        else:
            源文件路径 = 参数

    if not 源文件路径:
        print("用法: python zhsh.py [-r] [-k] <源文件.zhsh>")
        sys.exit(1)

    if not os.path.isfile(源文件路径):
        print(f"错误: 文件 '{源文件路径}' 不存在")
        sys.exit(1)

    # 生成目标文件名
    基础名 = os.path.splitext(源文件路径)[0]
    目标文件路径 = 基础名 + '.zsh'

    # 执行编译
    编译(源文件路径, 目标文件路径)

    # 输出信息
    print(f"编译成功: {目标文件路径}")

    # 根据开关决定是否运行或保留中间文件
    if 直接运行:
        print("执行生成的脚本...")
        try:
            subprocess.run(['zsh', 目标文件路径], check=True)
        except subprocess.CalledProcessError as e:
            print(f"脚本执行失败，返回码: {e.returncode}")
        except FileNotFoundError:
            print("错误: 未找到 zsh，请确保已安装 zsh")
        # 如果未保留中间文件，则执行后删除
        if not 保留中间文件:
            os.remove(目标文件路径)
            print(f"已删除中间文件: {目标文件路径}")
    else:
        if 保留中间文件:
            print(f"中间文件已保留: {目标文件路径}")
        else:
            # 默认不保留
            os.remove(目标文件路径)
            print(f"已删除中间文件: {目标文件路径}")
