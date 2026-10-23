
"""语法分析

把词法分析得到的语法树转换成解释器使用的字典结构。

这里不再依赖 lark 的 Transformer：自己提供一个极简的「转换器」基类，
按节点名找到同名的转换方法即可，用法与原来的 Transformer 完全一致。
"""

from 词法分析 import 语法树


class 转换器:
    """按语法树节点名分派到同名方法的转换器。"""

    def 转换(self, 节点):
        if isinstance(节点, 语法树):
            项目 = [self.转换(子节点) for 子节点 in 节点.children]
            方法 = getattr(self, str(节点.data), None)
            if 方法 is not None:
                return 方法(项目)
            return 语法树(节点.data, 项目)
        词元对象 = 节点
        方法 = getattr(self, str(词元对象.词元类型), None)
        if 方法 is not None:
            return 方法(词元对象)
        return 词元对象


class 语法分析(转换器):

    def start(自己, 项目):
        return 项目[0]

    def statements(自己, 项目):
        return 项目

    def statement(自己, 项目):
        return 项目[0]

    def define(自己, 项目, 语句):
        return {
            "语句": 语句,
            "类型": str(项目[0]),
            "名称": str(项目[1]),
            "量值": 项目[2],
        }

    def define_quote(自己, 项目):
        return {
            "类型": "名称",
            "名称": str(项目[0]),
        }

    def define_type(自己, 项目):
        return 自己.define(项目, "类型定义")

    def define_constant(自己, 项目):
        return 自己.define(项目, "常量定义")

    def define_variable(自己, 项目):
        return 自己.define(项目, "变量定义")

    def define_capacity(自己, 项目):
        return 自己.define(项目, "容量定义")

    def struct(自己, 项目, 语句):
        return {
            "语句": 语句,
            "返回": str(项目[0]),
            "名称": str(项目[1]),
            "参数": 项目[2],
            "代码": 项目[3],
        }

    def struct_quote(自己, 项目):
        名称 = 项目[0]
        # 成员调用（模块.函数 或 值.方法）保留结构，运行期再判断
        if not isinstance(名称, dict):
            名称 = str(名称)
        return {
            "语句": "调用结构",
            "类型": "结构",
            "名称": 名称,
            "参数": 项目[1],
        }

    def struct_class(自己, 项目):
        return 自己.struct(项目, "模型结构")

    def struct_function(自己, 项目):
        return 自己.struct(项目, "函数结构")

    def control_loop(自己, 项目):
        return {
            "语句": "循环语句",
            "条件": 项目[0],
            "代码": 项目[1],
        }

    def control_select(自己, 项目):
        结果 = {
            "语句": "条件语句",
            "条件": 项目[0],
            "代码": 项目[1],
            "或者条件": None,
            "或者代码": [],
        }
        if len(项目) > 3:
            结果["或者条件"] = 项目[2]
            结果["或者代码"] = 项目[3]
        return 结果

    def access_pipe(自己, 项目):
        return {
            "语句": "管道访问",
            "名称": {},
            "属性": {},
        }

    # ── 表达式与新增语句 ────────────────────────────────────────

    def arithmetic(自己, 项目):
        return {
            "类型": "运算",
            "运算": str(项目[0]),
            "左": 项目[1],
            "右": 项目[2],
        }

    def 取反(自己, 项目):
        return {"类型": "取反", "量值": 项目[0] if 项目 else None}

    def logical(自己, 项目):
        return {
            "类型": "逻辑运算",
            "运算": str(项目[0]),
            "左": 项目[1],
            "右": 项目[2],
        }

    def membership(自己, 项目):
        return {
            "类型": "成员运算",
            "运算": str(项目[0]),
            "左": 项目[1],
            "右": 项目[2],
        }

    def compare(自己, 项目):
        return {
            "类型": "比较",
            "运算": str(项目[0]),
            "左": 项目[1],
            "右": 项目[2],
        }

    def return_statement(自己, 项目):
        return {
            "语句": "返回语句",
            "量值": 项目[0],
        }

    def 短路语句(自己, 项目):
        # 条件 && 赋值 / 自增
        return {
            "语句": "短路语句",
            "运算": str(项目[0]) if 项目 else "",
            "条件": 项目[1] if len(项目) > 1 else None,
            "动作": 项目[2] if len(项目) > 2 else None,
        }

    def 短路返回(自己, 项目):
        # 条件 && 返回 值
        return {
            "语句": "短路返回",
            "运算": str(项目[0]) if 项目 else "",
            "条件": 项目[1] if len(项目) > 1 else None,
            "量值": 项目[2] if len(项目) > 2 else None,
        }

    def list(自己, 项目):
        # 列表字面量：[值, 值, ...]
        return {"类型": "列表", "量值": 项目}

    def object(自己, 项目):
        return {"类型": "对象", "量值": 项目}

    def pair(自己, 项目):
        return {"键": 项目[0], "量值": 项目[1]}

    def key(自己, 项目):
        return 项目[0] if 项目 else None

    def integer(自己, 项目):
        return 项目[0] if 项目 else None

    def natural(自己, 项目):
        return 项目[0] if 项目 else None

    def 空值(自己, 项目):
        # 声明时没写初始值
        return {"类型": "空值"}

    def data(自己, 项目):
        # data 只包一层，取其内部结果
        return 项目[0] if 项目 else None

    def member_assign(自己, 项目):
        return {
            "语句": "成员赋值",
            "对象": str(项目[0]),
            "成员": str(项目[1]),
            "量值": 项目[2],
        }

    def subscript_assign(自己, 项目):
        # 形如 名称[键1][键2] = 值
        return {
            "语句": "下标赋值",
            "名称": str(项目[0]),
            "键列表": 项目[1:-1],
            "量值": 项目[-1],
        }

    def assign(自己, 项目):
        return {
            "语句": "赋值语句",
            "名称": str(项目[0]),
            "量值": 项目[1],
        }

    def increment(自己, 项目):
        return {
            "语句": "自增语句",
            "运算": str(项目[0]),
            "名称": str(项目[1]),
        }

    def pipe(自己, 项目):
        return {
            "类型": "结构",
            "管道": 项目[0],
            "结构": 项目[1],
        }

    def access_option(自己, 项目):
        return {}

    def access_object(自己, 项目):
        return {}

    def module_path(自己, 项目):
        # 模块路径的各片段拼接起来，如 工具 / 数学
        路径 = ''.join(str(项) for 项 in 项目)
        # 用引号写成的路径要去掉引号，如 "./工具/数学"
        if len(路径) >= 2 and 路径[0] in ('"', "'") and 路径[-1] == 路径[0]:
            路径 = 路径[1:-1]
        return 路径

    def select(自己, 项目):
        # 只取名字，过滤掉其它内容
        return [str(项) for 项 in 项目 if isinstance(项, str)]

    def module_import(自己, 项目):
        # 项目[0] = 模块路径，项目[1] = 选择列表，项目[2] = 别名
        别名 = 项目[2] if len(项目) > 2 and 项目[2] else None
        return {
            "语句": "导入模块",
            "模块": 项目[0],
            "选择": 项目[1],
            "别名": str(别名) if 别名 else None,
        }

    def module_export(自己, 项目):
        return {
            "语句": "选择导出",
            "选择": 项目[0],
        }

    def export_function(自己, 项目):
        # 导出 add(a, b) { ... }：先当作函数定义，再登记到导出表
        return {
            "语句": "导出函数",
            "函数": 项目[0],
        }

    def type(自己, 项目):
        # 参数省略类型时，类型节点为空
        return 项目[0] if 项目 else ""

    def name(自己, 项目):
        return 项目[0]

    def subscript(自己, 项目):
        return {
            "类型": "下标",
            "对象": 项目[0],
            "位置": 项目[1] if len(项目) > 1 else None,
        }

    def slice_start(自己, 项目):
        return ("起", 项目[0])

    def slice_end(自己, 项目):
        return ("止", 项目[0])

    def slice(自己, 项目):
        结果 = {"类型": "切片", "对象": 项目[0], "起点": None, "终点": None}
        for 项 in 项目[1:]:
            if isinstance(项, tuple) and len(项) == 2:
                if 项[0] == "起":
                    结果["起点"] = 项[1]
                else:
                    结果["终点"] = 项[1]
        return 结果

    def member(自己, 项目):
        # 成员访问，如 数.add、文本.upper、" ".join
        # 左边可能是模块别名、变量名，也可能是字面量，运行期再判断
        对象 = 项目[0]
        if not isinstance(对象, dict):
            对象 = str(对象)
        return {"类型": "成员", "对象": 对象, "成员": str(项目[1])}

    def value(自己, 项目):
        return 项目[0]

    def string(自己, 项目):
        if 项目:
            数值 = 项目[0]
            数值 = 数值[1:-1]
            return {"类型": "文本", "数值": 数值}
        return None

    def number(自己, 项目):
        if 项目:
            数值 = 项目[0]
            return {"类型": "数字", "数值": 数值}
        return None

    def params(自己, 项目):
        return 项目

    def 匿名函数(自己, 项目):
        # 匿名函数：(参数) { 语句 }，只出现在参数位置
        return {
            "类型": "函数值",
            "参数": 项目[0],
            "代码": 项目[1],
        }

    def varargs(自己, 项目):
        # 参数收集：名称... ；写了类型时记录为元素类型
        结果 = {"类型": "收集", "量值": str(项目[0]) if 项目 else "",
                "元素类型": None}
        if len(项目) > 1 and 项目[1]:
            结果["元素类型"] = str(项目[1])
        return 结果

    def param(自己, 项目):
        结果 = {
            "类型": str(项目[0]),
            "量值": str(项目[1]),
        }
        # 有默认值时记下来，调用时少传的参数用它补齐
        if len(项目) > 2:
            结果["默认值"] = 项目[2]
        return 结果

    def arguments(自己, 项目):
        return 项目

    def keyword(自己, 项目):
        # 关键字参数，如 encoding="utf-8"
        return {"关键字": str(项目[0]), "量值": 项目[1]}

    def argument(自己, 项目):
        return 项目[0]


分析工具 = 语法分析()


def 语言语法分析(词元列表):
    """把 lark 风格的语法树转换为解释器使用的结构。"""
    return 分析工具.转换(词元列表)
