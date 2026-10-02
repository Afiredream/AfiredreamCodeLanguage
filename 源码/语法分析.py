
from lark import Transformer, Token, Tree

class 语法分析(Transformer):

    def start(自己, 项目):
        return 项目[0]
    def statement(自己, 项目):
        return 项目[0]
    def statements(自己, 项目):
        return 项目

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
            "名称": str(项目[0])
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
            "代码": 项目[3]
        }
    def struct_quote(自己, 项目):
        return {
            "语句": "调用结构",
            "类型": "结构",
            "名称": str(项目[0]),
            "参数": 项目[1]
        }
    def struct_class(自己, 项目):
        return 自己.struct(项目, "模型结构")
    def struct_function(自己, 项目):
        return 自己.struct(项目, "函数结构")

    def control_loop(自己, 项目):
        return {}
    def control_selest(自己, 项目):
        return {}

    def access_pipe(自己, 项目):
        return {
            "语句": "管道访问",
            "名称": {},
            "属性": {}
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
        if (项目):
          数值 = 项目[0]
          数值 = 数值[1:-1]
          return {"类型":"文本","数值": 数值}
        else:
          return None

    def number(自己, 项目):
        if (项目):
          数值 = 项目[0]
          return {"类型":"数字","数值": 数值}
    
    def params(自己, 项目):
        return 项目
    def param(自己, 项目):
        return {
            "类型": str(项目[0]),
            "量值": str(项目[1])
        }
    
    def arguments(自己, 项目):
        return 项目
    def argument(自己, 项目):
        return 项目[0]

分析工具 = 语法分析()
def 语言语法分析(词元列表):
  return 分析工具.transform(词元列表)