
# 终端

def 终端输出(*参数) -> None:
    print(*参数)

def 终端输入(文本: str) -> str:
    return input()

# 文本

def 文本长度(文本: str) -> int:
    return len(文本)

def 文本索引(文本: str, 索引: int) -> str:
    # 本语言从 1 开始数，第 1 个字符即文本首位
    return 文本[索引 - 1]

def 文本拼接(*参数) -> str:
    return ''.join(map(str, 参数))

# 函数  

import types
def 索引内置函数(函数名称: str) -> bool:
    函数对象 = globals().get(函数名称)
    if 函数对象 is None:
        return False
    if not isinstance(函数对象, types.FunctionType):
        return False
    return 函数对象.__module__ == __name__

def 运行内置函数(函数名称: str, 参数列表: list):
    函数对象 = globals()[函数名称]
    return 函数对象(*参数列表)

__all__ = ["索引内置函数", "调用内置函数"]