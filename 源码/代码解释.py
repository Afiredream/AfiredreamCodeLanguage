
import 内置函数

def 索引内置函数(函数名称):
    return 函数名称 in globals()

def 语言代码解释(代码对象):
    for 语法单元 in 代码对象:
        if 语法单元["语句"] == "结构调用":
            名称 = 语法单元["名称"]
            参数列表 = 语法单元["参数"]
            参数目标 = []
            for 参数 in 参数列表:
                参数目标.append(参数["数值"])
            函数 = getattr(内置函数, 名称, None)
            if callable(函数):
                函数(*参数目标)
        elif 语法单元["语句"] == "定义常量":
            pass