
from 内置函数 import (索引内置函数, 运行内置函数, 取得内置对象,
                      执行内置函数)


def 比较(运算, 左, 右):
    """执行一次比较运算。"""
    try:
        match 运算:
            case "==": return 左 == 右
            case "!=": return 左 != 右
            case "<": return 左 < 右
            case "<=": return 左 <= 右
            case ">": return 左 > 右
            case ">=": return 左 >= 右
    except TypeError:
        print(f"「{左}」与「{右}」无法用「{运算}」比较")
        return False
    print("未知比较运算符", 运算)
    return False

def 算术(运算, 左, 右):
    """执行一次算术运算。"""
    try:
        match 运算:
            case "+": return 左 + 右
            case "-": return 左 - 右
            case "*": return 左 * 右
            case "/": return 左 / 右
            case "%": return 左 % 右
    except TypeError:
        print(f"「{左}」与「{右}」无法用「{运算}」运算")
        return None
    except ZeroDivisionError:
        print("除数不能为零")
        return None
    print("未知运算符", 运算)
    return None


# 类型名 → 判断函数。用于检查实参与形参的类型标注是否相符。
类型判断 = {
    "文本": lambda 值: isinstance(值, str),
    "数字": lambda 值: isinstance(值, (int, float)) and not isinstance(值, bool),
    "状态": lambda 值: isinstance(值, bool),
    "大小": lambda 值: isinstance(值, (int, float)) and not isinstance(值, bool),
    "列表": lambda 值: isinstance(值, (list, tuple)),   # 元素任意类型
    # 「数组」不在这里定义：它要求元素同类型，由 类型相符 单独处理
    "对象": lambda 值: isinstance(值, dict),
    "空白": lambda 值: True,      # 不限制
    "任意": lambda 值: True,      # 不限制
}


def 转真假(值):
    """把语言里的真假值统一转成布尔。

    「真」「假」是文本，直接 bool() 会得到 True，必须先识别。
    """
    if isinstance(值, str):
        if 值 in ("真", "True"):
            return True
        if 值 in ("假", "False", ""):
            return False
        return True
    return bool(值)


def 元素类型一致(值):
    """数组要求所有元素同类型；空数组或只有一个元素时视为一致。"""
    if not isinstance(值, (list, tuple)):
        return False
    类型集合 = {值类型名(项) for 项 in 值}
    return len(类型集合) <= 1


def 类型相符(类型名, 值):
    """判断值是否符合类型标注；未知类型名一律放行。

    数组：元素必须全部同类型，但具体是哪种类型不限。
    列表：元素可以是任意类型。
    """
    if not 类型名:
        return True

    类型名 = str(类型名)
    if 类型名 == "数组":
        return 元素类型一致(值)

    判断 = 类型判断.get(类型名)
    if 判断 is None:
        return True
    return 判断(值)


def 类型说明(类型名, 值):
    """给出不匹配时的具体原因，便于提示。"""
    if str(类型名) == "数组" and isinstance(值, (list, tuple)) \
            and not 元素类型一致(值):
        种类 = []
        for 项 in 值:
            名 = 值类型名(项)
            if 名 not in 种类:
                种类.append(名)
        return f"元素类型不一致（出现了{'、'.join(种类)}）"
    return 值类型名(值)


def 值类型名(值):
    """给出值的大致类型名，用于错误提示。"""
    if isinstance(值, bool):
        return "状态"
    if isinstance(值, (int, float)):
        return "数字"
    if isinstance(值, str):
        return "文本"
    if isinstance(值, (list, tuple)):
        return "列表"
    if isinstance(值, dict):
        return "对象"
    return type(值).__name__


# 全局常量：名字 → 值。这些名字不允许被重新定义或赋值。
全局常量 = {
    "操作系统": None,   # 运行时填入实际系统名
    # 正负无穷大：正无穷大于一切数，负无穷小于一切数
    "正无穷大": float('inf'),
    "负无穷大": float('-inf'),
    # 空文本，用作判断「没有内容」时的默认值
    "空白文本": "",
}


def 初始化全局常量():
    from 内置函数 import 取得操作系统名称
    全局常量["操作系统"] = 取得操作系统名称()


初始化全局常量()


class 代码解释:
    def __init__(自己, 变量列表 = None, 文件目录 = None):
        自己.结构列表 = {}
        自己.函数列表 = {}
        自己.函数返回 = None
        自己.变量列表 = 变量列表 if 变量列表 is not None else {}
        自己.文件目录 = 文件目录      # 用于解析「导入」的相对路径
        自己.父作用域 = None          # 外层作用域，用于逐层查找变量
        自己.本模块函数 = set()       # 本文件里定义的函数名，用于区分内部调用
        自己.在模块文件 = False       # 是否正在加载模块文件
        自己.导出表 = {}              # 本模块对外公开的名字 → 函数
        自己.已导出 = set()           # 已登记的选择导出名字
        自己.未找到的名字 = set()     # 选择导出里找不到的函数名

    def 解释列表(自己, 语法列表):
        for 语法单元 in 语法列表:
            自己.解释单元(语法单元)
            # 执行到返回语句就立刻停下，不再执行后面的语句
            if 自己.函数返回 is not None:
                return 自己.函数返回
        if 自己.函数返回 is not None:
            return 自己.函数返回

    def 解释单元(自己, 语法单元):
        语句类型 = 语法单元.get("语句")
        match 语句类型:
            case "类型定义":
                自己.解释类型定义(语法单元)
            case "常量定义":
                自己.解释常量定义(语法单元)
            case "变量定义":
                自己.解释变量定义(语法单元)
            case "容量定义":
                自己.解释容量定义(语法单元)
            case "调用结构":
                自己.解释调用语句(语法单元)
            case "自增语句":
                自己.解释自增语句(语法单元)
            case "赋值语句":
                自己.解释赋值语句(语法单元)
            case "下标赋值":
                自己.解释下标赋值(语法单元)
            case "成员赋值":
                自己.解释成员赋值(语法单元)
            case "导入模块":
                自己.解释导入模块(语法单元)
            case "导出函数":
                自己.解释导出函数(语法单元)
            case "选择导出":
                自己.解释选择导出(语法单元)
            case "模型结构":
                自己.解释模型结构(语法单元)
            case "结构定义":
                自己.解释结构定义(语法单元)
            case "函数结构":
                自己.解释函数结构(语法单元)
            case "循环语句":
                自己.解释循环语句(语法单元)
            case "对于语句":
                自己.解释对于语句(语法单元)
            case "条件语句":
                自己.解释条件语句(语法单元)
            case "分支语句":
                自己.解释分支语句(语法单元)
            case "返回语句":
                自己.解释返回语句(语法单元)
            case "短路返回":
                自己.解释短路返回(语法单元)
            case "短路语句":
                自己.解释短路语句(语法单元)
            case "管道访问":
                自己.解释管道访问(语法单元)
            case "数据访问":
                自己.解释管道访问(语法单元)
            case "安全访问":
                自己.解释管道访问(语法单元)

            case _:
                print("未知语句类型", 语句类型)

    def 解释调用结构(自己, 语法单元):
        # 管道调用：把左边的值作为第一个参数，右边调用照常求值
        管道值 = 语法单元.get("管道")
        if 管道值 is not None:
            调用单元 = 语法单元.get("结构") or {}
            参数列表 = [自己.解析参数单元(管道值)]
            参数列表 += 自己.解释参数列表(调用单元.get("参数") or [])
            return 自己.执行调用(调用单元.get("名称"), 参数列表)

        return 自己.执行调用(语法单元.get("名称"),
                             自己.解释参数列表(语法单元.get("参数")))

    def 解释调用语句(自己, 语法单元):
        """调用出现在语句位置：如果它有返回值，提示结果被丢弃。"""
        结果 = 自己.解释调用结构(语法单元)
        名称 = 语法单元.get("名称") or (语法单元.get("结构") or {}).get("名称")
        if 结果 is not None and 自己.有返回值(名称):
            print(f"提示：「{名称}」的返回值没有被使用，"
                  f"如需保存请写成「变量 文本:结果 = {名称}(...)」")

    def 有返回值(自己, 结构名称):
        """判断一个函数是否写了返回语句。"""
        if not isinstance(结构名称, str):
            return False
        结构对象 = 自己.索引定义结构(结构名称)
        if not 结构对象:
            return False
        return any(语句.get("语句") == "返回语句"
                   for 语句 in 结构对象.get("代码") or []
                   if isinstance(语句, dict))

    def 执行调用(自己, 结构名称, 参数列表):
        """参数已是求值后的值，直接按名称找到函数或内置函数执行。"""
        # 传入的是匿名函数：直接执行它
        if isinstance(结构名称, dict) and 结构名称.get("类型") == "匿名函数":
            return 自己.运行定义结构("匿名函数", 参数列表, 内置结构=结构名称)

        # 成员调用：模块别名.函数 或 值.方法
        if isinstance(结构名称, dict) and 结构名称.get("类型") == "成员":
            return 自己.执行成员调用(结构名称.get("对象"), 结构名称.get("成员"),
                                     参数列表)
        # 字面量直接调用方法，如 " ".join(...)
        if 结构名称.__class__.__name__ == "语法树":
            return 自己.执行属性调用(结构名称, 参数列表)

        结构名称 = str(结构名称) if 结构名称 is not None else ''

        # 「模块.函数」：到别名模块的导出表里找
        if '.' in 结构名称:
            模块别名, 成员 = 结构名称.split('.', 1)
            模块 = 自己.结构列表.get(模块别名)
            if isinstance(模块, dict) and 模块.get("类型") == "模块":
                if 成员 in 模块.get("函数", {}):
                    位置参数, _ = 自己.拆分参数(参数列表)
                    return 自己.运行定义结构(成员, 位置参数,
                                           内置结构=模块["函数"][成员],
                                           内部调用=True)
                print(f"模块「{模块别名}」没有导出的函数「{成员}」")
                return None
            print(f"没有名为「{模块别名}」的模块，请先导入")
            return None

        位置参数, 关键字参数 = 自己.拆分参数(参数列表)

        # 变量里存的是函数值时，直接调用它
        值 = 自己.逐层查找(结构名称)
        if isinstance(值, dict) and 值.get("类型") == "匿名函数":
            return 自己.运行定义结构("匿名函数", 位置参数, 内置结构=值)

        定义 = 自己.索引定义结构(结构名称)
        if 定义:
            return 自己.运行定义结构(结构名称, 位置参数,
                                   内置结构=定义,
                                   内部调用=(结构名称 in 自己.本模块函数
                                             or bool(定义.get("所属模块函数"))))
        if 索引内置函数(结构名称):
            return 执行内置函数(结构名称, 位置参数, 关键字参数)
        print(f"未定义的函数「{结构名称}」")

    def 执行属性调用(自己, 成员节点, 参数列表):
        """成员节点形如 member(值, 名称)，左值先求值再取方法。"""
        子节点 = 成员节点.children
        if len(子节点) < 2:
            print("成员调用写法不正确")
            return None
        对象 = 自己.解析参数单元(子节点[0])
        成员名 = str(子节点[1])
        方法 = getattr(对象, 成员名, None)
        if not callable(方法):
            print(f"值没有方法「{成员名}」")
            return None
        try:
            return 方法(*参数列表)
        except Exception as 错误:
            print(f"调用「{成员名}」失败：{错误}")
            return None

    def 执行成员调用(自己, 对象名, 成员名, 参数列表):
        """先看是不是模块别名，不是就当作值的方法调用。"""
        # 左边是字面量或表达式时，先求值再取方法
        if isinstance(对象名, dict):
            对象 = 自己.解析参数单元(对象名)
            方法 = getattr(对象, str(成员名), None)
            if callable(方法):
                try:
                    return 方法(*参数列表)
                except Exception as 错误:
                    print(f"调用「{成员名}」失败：{错误}")
                    return None
            print(f"值没有方法「{成员名}」")
            return None

        对象名 = str(对象名) if 对象名 is not None else ''
        模块 = 自己.结构列表.get(对象名)
        if isinstance(模块, dict) and 模块.get("类型") == "模块":
            if 成员名 in 模块.get("函数", {}):
                模块函数集 = 模块["函数"].get(成员名, {}).get("所属模块函数") or set()
                内部 = (自己.本模块函数 is 模块函数集
                        or bool(模块["函数"][成员名].get("所属模块函数")))
                return 自己.运行定义结构(成员名, 参数列表,
                                       内置结构=模块["函数"][成员名],
                                       内部调用=内部)
            print(f"模块「{对象名}」没有导出的函数「{成员名}」")
            return None

        # Python 标准库，如 json.dumps(...)
        from 内置函数 import 取得标准库
        标准库 = 取得标准库(对象名)
        if 标准库 is not None:
            方法 = getattr(标准库, str(成员名), None)
            if callable(方法):
                位置参数, 关键字参数 = 自己.拆分参数(参数列表)
                try:
                    return 方法(*位置参数, **关键字参数)
                except Exception as 错误:
                    print(f"调用「{对象名}.{成员名}」失败：{错误}")
                    return None
            print(f"标准库「{对象名}」没有「{成员名}」")
            return None

        # 当作值的方法调用，如 文本.upper()、列表.append(项)
        if 对象名 in 自己.变量列表:
            值 = 自己.变量列表[对象名]
            方法 = getattr(值, str(成员名), None)
            if callable(方法):
                try:
                    return 方法(*参数列表)
                except Exception as 错误:
                    print(f"调用「{对象名}.{成员名}」失败：{错误}")
                    return None
            print(f"「{对象名}」没有方法「{成员名}」")
            return None

        print(f"没有名为「{对象名}」的模块或变量，请先导入或定义")
        return None

    def 解释对于语句(自己, 语法单元):
        """对于 (列表, 索引, 元素)：依次遍历列表。"""
        列表 = 自己.解析参数单元(语法单元.get("列表"))
        if 列表 is None:
            return None
        序号名 = 语法单元.get("索引")
        元素名 = 语法单元.get("元素")
        代码 = 语法单元.get("代码") or []

        序号 = 1
        for 元素 in 列表:
            自己.变量列表[序号名] = 序号
            自己.变量列表[元素名] = 元素
            自己.解释列表(代码)
            序号 += 1
        return None

    def 解释循环语句(自己, 语法单元):
        while 自己.求条件(语法单元.get("条件")):
            自己.解释列表(语法单元.get("代码") or [])
            if 自己.函数返回 is not None:
                return 自己.函数返回

    def 解释条件语句(自己, 语法单元):
        if 自己.求条件(语法单元.get("条件")):
            return 自己.解释列表(语法单元.get("代码") or [])
        # 「或者」分支有自己的条件，需要再判断一次
        或者条件 = 语法单元.get("或者条件")
        if 或者条件 is not None and 自己.求条件(或者条件):
            return 自己.解释列表(语法单元.get("或者代码") or [])
        # 「否则」分支条件恒成立，前面都不成立时执行
        否则条件 = 语法单元.get("否则条件")
        if 否则条件 is not None and 自己.求条件(否则条件):
            return 自己.解释列表(语法单元.get("否则代码") or [])
        return None

    def 解释短路语句(自己, 语法单元):
        """条件 && 赋值：条件成立才执行后面的动作。"""
        if not 自己.求条件(语法单元.get("条件")):
            return None
        动作 = 语法单元.get("动作")
        if isinstance(动作, dict):
            自己.解释单元(动作)
        return None

    def 解释短路返回(自己, 语法单元):
        """条件 && 返回 值：条件成立时立刻返回。

        && 与 || 效果相同：只要条件成立就返回，
        写成 || 只是读起来更顺（如「为空 || 返回 真」），语义一致。
        """
        if not 自己.求条件(语法单元.get("条件")):
            return None

        自己.函数返回 = 自己.解析参数单元(语法单元.get("量值"))
        return 自己.函数返回

    def 解释返回语句(自己, 语法单元):
        自己.函数返回 = 自己.解析参数单元(语法单元.get("量值"))
        return 自己.函数返回

    def 解释赋值语句(自己, 语法单元):
        名称 = 语法单元.get("名称")
        if 名称 in 全局常量:
            print(f"「{名称}」是全局常量，不能赋值")
            return
        自己.变量列表[名称] = 自己.解析参数单元(语法单元.get("量值"))

    def 解释成员赋值(自己, 语法单元):
        对象 = 自己.查找变量(语法单元.get("对象"))
        值 = 自己.解析参数单元(语法单元.get("量值"))
        try:
            setattr(对象, str(语法单元.get("成员")), 值)
            return 值
        except Exception as 错误:
            print(f"成员赋值失败：{错误}")
            return None

    def 解释下标赋值(自己, 语法单元):
        名称 = 语法单元.get("名称")
        键列表 = 自己.解释参数列表(语法单元.get("键列表") or [])
        值 = 自己.解析参数单元(语法单元.get("量值"))
        容器 = 自己.查找变量(名称)
        try:
            # 逐层深入到最后一级容器再赋值
            目标 = 容器
            for 键 in 键列表[:-1]:
                目标 = 目标[键]
            if 键列表:
                目标[键列表[-1]] = 值
            return 值
        except (IndexError, TypeError, KeyError) as 错误:
            print(f"下标赋值失败：{错误}")
            return None

    def 解释自增语句(自己, 语法单元):
        名称 = 语法单元.get("名称")
        if 名称 in 全局常量:
            print(f"「{名称}」是全局常量，不能自增")
            return
        运算 = 语法单元.get("运算")
        当前值 = 自己.查找变量(名称)
        if not isinstance(当前值, int):
            print(f"「{名称}」不是数字，无法自增")
            return
        自己.变量列表[名称] = 当前值 + (1 if 运算 == "++" else -1)

    def 求条件(自己, 项):
        """求一个条件的真假：比较表达式或单个值。"""
        if not isinstance(项, dict):
            # 裸字符串可能是变量名，先按变量求值
            if isinstance(项, str):
                值 = 自己.逐层查找(项)
                if 值 is not None:
                    return 转真假(值)
            return 转真假(项)
        if 项.get("类型") == "比较":
            左 = 自己.解析参数单元(项.get("左"))
            右 = 自己.解析参数单元(项.get("右"))
            return 比较(项.get("运算"), 左, 右)
        return 转真假(自己.解析参数单元(项))
    
    def 索引定义结构(自己, 结构名称:str):
        if not isinstance(结构名称, str):
            return None
        return 自己.结构列表.get(结构名称)

    def 运行定义结构(自己, 结构名称:str, 参数列表:list, 内置结构=None,
                     内部调用=False):
        结构对象 = 内置结构 or 自己.索引定义结构(结构名称)
        if 结构对象 is None:
            if 结构名称 != "匿名函数":
                print(f"未定义的函数「{结构名称}」")
            return None
        语句列表 = 结构对象["代码"]
        # 只在当前作用域里放形参，外层变量通过父作用域查找
        变量列表 = {}
        形参列表 = 结构对象.get("参数") or []

        # 参数收集：名称... 把剩余的实参全部收进一个列表
        收集名 = None
        收集类型 = None
        if 形参列表 and isinstance(形参列表[-1], dict) \
                and 形参列表[-1].get("类型") == "收集":
            收集项 = 形参列表[-1]
            收集名 = 收集项.get("量值")
            收集类型 = 收集项.get("元素类型")
            形参列表 = 形参列表[:-1]

        for 序号, (形参, 实参) in enumerate(zip(形参列表, 参数列表), 1):
            类型名 = 形参.get("类型")
            # 模块内部互相调用时不检查类型，只检查外部调用
            if not 内部调用 and not 类型相符(类型名, 实参):
                print(f"「{结构名称}」第 {序号} 个参数「{形参.get('量值')}」"
                      f"需要{类型名}，却收到{类型说明(类型名, 实参)}")
            变量列表[形参.get("量值")] = 实参
        if 收集名 is not None:
            剩余 = list(参数列表[len(形参列表):])
            # 逐个检查收集到的实参是否符合元素类型
            for 序号, 项 in enumerate(剩余, len(形参列表) + 1):
                if not 内部调用 and not 类型相符(收集类型, 项):
                    print(f"「{结构名称}」第 {序号} 个参数需要{收集类型}，"
                          f"却收到{类型说明(收集类型, 项)}")
            变量列表[收集名] = 剩余
        else:
            # 少传的参数：有默认值就用默认值，否则当作空文本
            for 形参 in 形参列表[len(参数列表):]:
                名称 = 形参.get("量值")
                if "默认值" in 形参:
                    变量列表[名称] = 自己.解析参数单元(形参.get("默认值"))
                else:
                    变量列表.setdefault(名称, "")
        子解释器 = 代码解释(变量列表)
        子解释器.父作用域 = 自己
        # 优先使用函数定义时所在的模块环境
        子解释器.结构列表 = 结构对象.get("所属结构表") or 自己.结构列表
        子解释器.函数列表 = 结构对象.get("所属函数表") or 自己.函数列表
        # 继承「本模块函数」与「是否在模块文件」，
        # 这样模块内部互相调用时同样不做类型检查
        子解释器.本模块函数 = 自己.本模块函数
        子解释器.在模块文件 = (自己.在模块文件
                               or bool(结构对象.get("所属模块函数")))
        return 子解释器.解释列表(语句列表)

    def 解释结构定义(自己, 单元):
        """结构：名称注册为函数，内部的「函数()」作为它的入口体。

        结构 示例() {
            函数() {
                返回 42
            }
        }
        调用 示例() 时执行内部那个函数的花括号。
        """
        名称 = 单元.get("名称")
        if not 名称:
            print("结构缺少名称")
            return

        入口 = None
        for 语句 in 单元.get("代码") or []:
            if isinstance(语句, dict) and 语句.get("语句") == "函数结构" \
                    and not 语句.get("名称"):
                入口 = 语句
                break

        if 入口 is None:
            # 没有内部入口，就用结构自身的参数与代码
            登记 = {"类型": "函数", "名称": 名称,
                    "参数": 单元.get("参数") or [],
                    "代码": 单元.get("代码") or [],
                    "返回": 单元.get("返回") or "",
                    "所属结构表": 自己.结构列表,
                    "所属函数表": 自己.函数列表}
        else:
            # 内部的「函数()」就是结构被调用时执行的实现。
            # 结构里其他语句（变量、常量等）排在前面先执行，
            # 这样入口能用到它们定义的值。
            参数 = 入口.get("参数") or 单元.get("参数") or []
            前置 = [语句 for 语句 in (单元.get("代码") or [])
                    if 语句 is not 入口
                    and not (isinstance(语句, dict)
                            and 语句.get("语句") == "函数结构")]
            登记 = {"类型": "函数", "名称": 名称,
                    "参数": 参数,
                    "代码": 前置 + list(入口.get("代码") or []),
                    "返回": 单元.get("返回") or 入口.get("返回") or "",
                    "所属结构表": 自己.结构列表,
                    "所属函数表": 自己.函数列表}
        自己.结构列表[名称] = 登记
        自己.函数列表[名称] = 登记

        # 结构里具名的辅助函数也一并登记，入口可以调用它们
        for 语句 in 单元.get("代码") or []:
            if not isinstance(语句, dict) or 语句.get("语句") != "函数结构":
                continue
            子名称 = 语句.get("名称")
            if not 子名称 or 语句 is 入口:
                continue
            自己.结构列表[子名称] = 语句
            自己.函数列表[子名称] = 语句

    def 解释模型结构(自己, 单元):
        """模型：登记模型本身，并把内部的函数也登记到结构表。"""
        名称 = 单元.get("名称")
        if 名称:
            自己.结构列表[名称] = 单元
            自己.函数列表[名称] = 单元
        for 语句 in 单元.get("代码") or []:
            if isinstance(语句, dict) and 语句.get("语句") == "函数结构":
                自己.解释函数结构(语句)

    def 解释类型定义(自己, 单元):
        # 类型定义只是给名字起别名，暂时不需要做任何事
        pass

    # ── 导入与导出 ──────────────────────────────────────────────

    def 解释导入模块(自己, 语法单元):
        """导入 模块名 [命名 别名] [选择 名字, 名字...]"""
        模块名 = 语法单元.get("模块")
        选择 = 语法单元.get("选择") or []
        别名 = 语法单元.get("别名")

        模块函数 = 载入模块(模块名, 自己.文件目录)
        if 模块函数 is None:
            return

        # 命名空间名：写了别名就用别名，否则用模块名本身
        命名空间 = 别名 if 别名 else 模块名取名字(模块名)

        if 选择:
            缺失 = [名字 for 名字 in 选择 if 名字 not in 模块函数]
            for 名字 in 缺失:
                print(f"模块「{模块名}」没有导出「{名字}」")
            选中 = {名字: 模块函数[名字] for 名字 in 选择
                    if 名字 in 模块函数}
        else:
            选中 = dict(模块函数)

        # 挂成命名空间，用「数组.长度(...)」这样的写法访问
        自己.导出表[命名空间] = {"类型": "模块", "函数": 选中}
        自己.结构列表[命名空间] = {"类型": "模块", "函数": 选中,
                                   "代码": [], "参数": []}

        # 没有指定选择时，函数同时平铺到当前命名空间，
        # 这样既可以写「数组.长度(...)」，也可以直接写「长度(...)」
        if not 选择 and not 别名:
            for 名字, 函数 in 选中.items():
                自己.安装模块函数(名字, 函数)

    def 安装模块函数(自己, 名字, 函数):
        自己.结构列表[名字] = 函数
        自己.函数列表[名字] = 函数

    def 解释导出函数(自己, 语法单元):
        """导出 add(a, b) { ... }：定义的同时登记到导出表。"""
        函数 = 语法单元.get("函数")
        if not isinstance(函数, dict):
            return
        # 结构要走向结构定义的登记逻辑，才能把内部「函数()」当成入口
        if 函数.get("语句") == "结构定义":
            自己.解释结构定义(函数)
            登记 = 自己.索引定义结构(函数.get("名称"))
            if isinstance(登记, dict):
                自己.导出表[函数.get("名称")] = 登记
                自己.已导出.add(函数.get("名称"))
            return
        自己.解释函数结构(函数)
        自己.导出表[函数.get("名称")] = 函数
        自己.已导出.add(函数.get("名称"))

    def 解释选择导出(自己, 语法单元):
        """导出 add, sub：把已有函数登记到导出表。"""
        for 名字 in 语法单元.get("选择") or []:
            函数 = 自己.索引定义结构(名字)
            if 函数 is None:
                自己.未找到的名字.add(名字)
                continue
            自己.导出表[名字] = 函数
        自己.已导出.update(语法单元.get("选择") or [])

    def 检查选择导出(自己):
        """执行结束后，提示那些「导出了但没定义」的名字。"""
        for 名字 in sorted(自己.未找到的名字):
            if 名字 in 自己.结构列表:
                continue
            print(f"导出失败：没有找到函数「{名字}」")

    def 解释函数结构(自己, 单元):
        名称 = 单元.get("名称")
        # 记下定义它的模块环境，被别的模块导入后仍能找到它依赖的函数
        单元.setdefault("所属结构表", 自己.结构列表)
        单元.setdefault("所属函数表", 自己.函数列表)
        # 只有模块文件里定义的函数才算「内部函数」；
        # 主程序里定义的函数被调用时仍做类型检查
        if 自己.在模块文件:
            自己.本模块函数.add(名称)
            单元.setdefault("所属模块函数", 自己.本模块函数)
        自己.函数列表[名称] = 单元
        自己.结构列表[名称] = 单元

    def 解释常量定义(自己, 语法单元):
        名称 = 语法单元.get("名称")
        量值 = 语法单元.get("量值")
        量值 = 自己.解析参数单元(量值)

        # 声明时没写初始值，按类型给默认值
        if 量值 is None:
            类型名 = str(语法单元.get("类型") or "")
            默认值 = {"文本": "", "数字": 0, "状态": False,
                      "列表": [], "数组": [], "对象": {}}
            量值 = 默认值.get(类型名, "")

        if 名称 in 全局常量:
            print(f"「{名称}」是全局常量，不能重新定义")
            return
        自己.变量列表[名称] = 量值

    def 解释变量定义(自己, 语法单元):
        自己.解释常量定义(语法单元)

    def 解释容量定义(自己, 语法单元):
        自己.解释常量定义(语法单元)

    def 解释参数列表(自己, 单元列表):
        """求值实参列表。写 名称... 时把同名收集参数逐个展开。"""
        参数列表 = []
        for 参数单元 in 单元列表:
            # 收集参数展开：把同名收集参数里的每一项当作一个实参
            if isinstance(参数单元, dict) and 参数单元.get("类型") == "展开":
                收集 = 自己.逐层查找(参数单元.get("名称"))
                if isinstance(收集, (list, tuple)):
                    参数列表.extend(收集)
                else:
                    参数列表.append(收集)
                continue
            # 关键字参数原样交给执行调用处理
            if isinstance(参数单元, dict) and 参数单元.get("关键字"):
                参数列表.append(参数单元)
                continue
            参数量值 = 自己.解析参数单元(参数单元)
            参数列表.append(参数量值)
        return 参数列表

    def 拆分参数(自己, 参数列表):
        """把位置参数与关键字参数分开。"""
        位置参数 = []
        关键字参数 = {}
        for 项 in 参数列表:
            if isinstance(项, dict) and 项.get("关键字"):
                关键字参数[项["关键字"]] = 自己.解析参数单元(项.get("量值"))
            else:
                位置参数.append(项)
        return 位置参数, 关键字参数

    
    def 对象键(自己, 键):
        """取出对象的键名。"""
        if isinstance(键, dict):
            数值 = 键.get("数值")
            return str(数值) if 数值 is not None else str(键)
        return str(键)

    def 解析参数单元(自己, 参数单元):
        # 直接给出名称或裸值时（例如 返回 当前文本），按名称查变量
        if not isinstance(参数单元, dict):
            if isinstance(参数单元, str):
                名称 = str(参数单元)
                if 名称 in ("真", "True"):
                    return True
                if 名称 in ("假", "False"):
                    return False
                if 名称 == "None":
                    return None
                # Python 类型名与内置函数可直接作为值，如 optionxform = str
                if 名称 in 自己.变量列表 or 自己.逐层查找(名称) is not None:
                    return 自己.查找变量(名称)
                内置对象 = 取得内置对象(名称)
                if 内置对象 is not None:
                    return 内置对象
                return 自己.查找变量(名称)
            return 参数单元

        # 直接给出调用结构时（如比较的左右两侧）
        if 参数单元.get("语句") == "调用结构":
            return 自己.解释调用结构(参数单元)

        参数类型 = 参数单元.get("类型")
        match 参数类型:
            case "结构":
                return 自己.解释调用结构(参数单元)
            case "文本":
                return 参数单元.get("数值")
            case "数字":
                文本 = str(参数单元.get("数值"))
                # 带小数点的是小数，否则是整数
                return float(文本) if '.' in 文本 else int(文本)
            case "名称":
                名称 = str(参数单元.get("名称"))
                # 真 / 假 是状态字面量，不是变量
                if 名称 in ("真", "True"):
                    return True
                if 名称 in ("假", "False"):
                    return False
                if 名称 == "None":
                    return None
                # Python 类型名与内置函数可直接作为值，如 optionxform = str
                if 名称 in 自己.变量列表 or 自己.逐层查找(名称) is not None:
                    return 自己.查找变量(名称)
                内置对象 = 取得内置对象(名称)
                if 内置对象 is not None:
                    return 内置对象
                return 自己.查找变量(名称)
            case "列表":
                return [自己.解析参数单元(项) for 项 in (参数单元.get("量值") or [])]
            case "对象":
                # 键是字面量，不做变量查找；只有引号键需要取出引号里的内容
                return {自己.对象键(对.get("键")): 自己.解析参数单元(对.get("量值"))
                        for 对 in (参数单元.get("量值") or [])}
            case "切片":
                对象 = 自己.解析参数单元(参数单元.get("对象"))
                起点 = 参数单元.get("起点")
                终点 = 参数单元.get("终点")
                起点 = None if 起点 is None else 自己.解析参数单元(起点)
                终点 = None if 终点 is None else 自己.解析参数单元(终点)
                try:
                    return 对象[起点:终点]
                except TypeError as 错误:
                    print(f"切片失败：{错误}")
                    return None
            case "下标":
                对象 = 自己.解析参数单元(参数单元.get("对象"))
                位置 = 自己.解析参数单元(参数单元.get("位置"))
                # 字典按键取值；文本与列表按位置取值，位置从 1 开始数
                键 = 位置
                if isinstance(对象, (list, tuple, str)):
                    键 = 位置
                    # 位置写成数字时从 1 开始数；写成变量时按语言的下标规则从 0 开始数
                    if isinstance(位置, int) and not isinstance(位置, bool) \
                            and not (isinstance(参数单元.get("位置"), dict)
                                     and 参数单元["位置"].get("类型") == "名称"):
                        键 = 位置 - 1
                try:
                    return 对象[键]
                except (IndexError, TypeError, KeyError) as 错误:
                    print(f"下标访问失败：{错误}")
                    return None
            case "运算":
                return 算术(参数单元.get("运算"),
                            自己.解析参数单元(参数单元.get("左")),
                            自己.解析参数单元(参数单元.get("右")))
            case "空值":
                return None
            case "展开":
                # 收集参数展开：单独取值时得到收集参数本身
                收集 = 自己.逐层查找(参数单元.get("名称"))
                return 收集
            case "函数值":
                return {"类型": "匿名函数",
                        "参数": 参数单元.get("参数") or [],
                        "代码": 参数单元.get("代码") or []}
            case "取反":
                return not bool(自己.解析参数单元(参数单元.get("量值")))
            case "逻辑运算":
                运算 = str(参数单元.get("运算"))
                左 = 自己.解析参数单元(参数单元.get("左"))
                # and / && 短路：左边为假就不再算右边
                if 运算 in ("and", "&&"):
                    return 自己.解析参数单元(参数单元.get("右")) if 左 else 左
                # or / || 短路：左边为真就不再算右边
                return 左 if 左 else 自己.解析参数单元(参数单元.get("右"))
            case "成员运算":
                左 = 自己.解析参数单元(参数单元.get("左"))
                右 = 自己.解析参数单元(参数单元.get("右"))
                返回 = 左 in 右
                if 参数单元.get("运算") == "not in":
                    返回 = not 返回
                return 返回
            case "比较":
                return 自己.求条件(参数单元)
            case _:
                print("未知参数类型", 参数类型)

    def 逐层查找(自己, 名称):
        """只看名字是否存在，不打印提示。"""
        if 名称 in 全局常量:
            return 全局常量[名称]
        作用域 = 自己
        while 作用域 is not None:
            if 名称 in 作用域.变量列表:
                return 作用域.变量列表[名称]
            作用域 = 作用域.父作用域
        return None

    def 查找变量(自己, 名称):
        # 全局常量优先，任何作用域都覆盖不了它
        if 名称 in 全局常量:
            return 全局常量[名称]
        作用域 = 自己
        while 作用域 is not None:
            if 名称 in 作用域.变量列表:
                return 作用域.变量列表[名称]
            作用域 = 作用域.父作用域
        print(f"变量「{名称}」未定义")
        return None

    def 求值(自己, 项):
        if isinstance(项, dict):
            类型 = 项.get("类型")
            数值 = 项.get("数值")
            if 类型 == "文本":
                return str(数值)
            if 类型 == "数字":
                return int(数值) -1
            return 数值

        # 字符串形态：可能是变量名，也可能是字面量
        if isinstance(项, str):
            if 项 in 自己.变量表:
                return 自己.变量表[项]
            # 尝试当数字
            try:
                return int(项)
            except ValueError:
                return 项

        return 项


解释工具 = 代码解释()
def 语言代码解释(语法列表, 文件目录=None):
    # 语言层的每次调用都要消耗多层 Python 栈，这里放宽上限
    import sys
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))
    if 文件目录 is not None:
        解释工具.文件目录 = 文件目录
    结果 = 解释工具.解释列表(语法列表)
    解释工具.检查选择导出()
    return 结果

# ══════════════════════════════════════════════════════════════════
# 模块加载
# ══════════════════════════════════════════════════════════════════

# 模块缓存：模块路径 → 该模块导出的函数表
模块缓存 = {}


# 模块文件的后缀名。导入时可以写全，也可以省略。
模块后缀 = '.模块'


def 查找模块文件(模块名, 当前目录):
    """把模块名或相对路径解析成实际文件路径，找不到返回 None。

    查找顺序：
      1. 原名（导入时已经写了 .模块）
      2. 原名 + .模块（导入时省略了后缀）
      3. 原名 + .象 / .燃梦（兼容旧的模块文件）
    """
    from os import path as 路径工具

    模块名 = str(模块名).strip()
    基准目录 = 当前目录 or '.'

    候选文件 = []
    if 模块名.startswith('.') or '/' in 模块名:
        # 形如 "./工具/数学" 或 "../公共/数学"
        候选文件.append(路径工具.join(基准目录, 模块名))
    else:
        # 形如「数学」「工具/数学」：在当前目录下找
        候选文件.append(路径工具.join(基准目录, 模块名))

    # 省略后缀时自动补上
    if not 模块名.endswith(模块后缀):
        候选文件.append(路径工具.join(基准目录, 模块名 + 模块后缀))

    # 兼容旧的模块文件写法
    for 旧后缀 in ('.象', '.燃梦'):
        if not 模块名.endswith(旧后缀):
            候选文件.append(路径工具.join(基准目录, 模块名 + 旧后缀))

    for 候选 in 候选文件:
        候选 = 路径工具.normpath(候选)
        if 路径工具.isfile(候选):
            return 候选
    return None


def 模块名取名字(模块名):
    """从模块路径里取出模块名：模块/数组 → 数组，../模块/数组 → 数组。"""
    模块名 = str(模块名).strip().strip('"\'')
    # 去掉 .模块 后缀
    模块名 = 模块名[:-len(模块后缀)] if 模块名.endswith(模块后缀) else 模块名
    片段 = [项 for 项 in 模块名.replace('\\', '/').split('/') if 项]
    return 片段[-1] if 片段 else 模块名


def 载入模块(模块名, 当前目录):
    """加载一个模块，返回它导出的函数表；失败返回 None。"""
    from os import path as 路径工具

    文件路径 = 查找模块文件(模块名, 当前目录)
    if 文件路径 is None:
        print(f"找不到模块「{模块名}」")
        return None

    真实路径 = 路径工具.abspath(文件路径)
    if 真实路径 in 模块缓存:
        return 模块缓存[真实路径]
    if 真实路径 in 模块缓存.get('__加载中__', set()):
        print(f"模块「{模块名}」存在循环导入")
        return None

    # 先占位，避免同一模块被重复解析
    模块缓存['__加载中__'] = 模块缓存.get('__加载中__', set()) | {真实路径}

    from 文件管理 import 读取文本文件
    from 词法分析 import 语言词法分析, 词法错误
    from 语法分析 import 语言语法分析

    try:
        代码文本 = 读取文本文件(文件路径)
        语法列表 = 语言语法分析(语言词法分析(代码文本, 语法分析=True)[1])
    except 词法错误 as 错误:
        print(f"加载模块「{模块名}」失败：{错误}")
        模块缓存.pop(真实路径, None)
        return None

    解释器 = 代码解释(文件目录=路径工具.dirname(真实路径))
    解释器.在模块文件 = True
    解释器.解释列表(语法列表)
    解释器.检查选择导出()

    导出函数 = dict(解释器.导出表)
    模块缓存[真实路径] = 导出函数
    模块缓存['__加载中__'] = 模块缓存.get('__加载中__', set()) - {真实路径}
    return 导出函数
