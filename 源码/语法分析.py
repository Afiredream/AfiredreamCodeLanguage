
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
            "量值": 项目[2].children[0],
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
        return {
            "语句": "调用结构",
            "类型": "结构",
            "名称": str(项目[0]),
            "参数": 项目[1],
        }

    def struct_class(自己, 项目):
        return 自己.struct(项目, "模型结构")

    def struct_function(自己, 项目):
        return 自己.struct(项目, "函数结构")

    def control_loop(自己, 项目):
        return {}

    def control_select(自己, 项目):
        return {}

    def access_pipe(自己, 项目):
        return {
            "语句": "管道访问",
            "名称": {},
            "属性": {},
        }

    def access_option(自己, 项目):
        return {}

    def access_object(自己, 项目):
        return {}

    def module_import(自己, 项目):
        return {}

    def module_export(自己, 项目):
        return {}

    def type(自己, 项目):
        return 项目[0]

    def name(自己, 项目):
        return 项目[0]

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

    def param(自己, 项目):
        return {
            "类型": str(项目[0]),
            "量值": str(项目[1]),
        }

    def arguments(自己, 项目):
        return 项目

    def argument(自己, 项目):
        return 项目[0]


分析工具 = 语法分析()


def 语言语法分析(词元列表):
    """把 lark 风格的语法树转换为解释器使用的结构。"""
    return 分析工具.转换(词元列表)
