
from lark import Transformer, Token, Tree

class 语法分析(Transformer):

    def start(自己, 项目):
        return 项目[0]

    def statements(自己, 项目):
        return 项目

    def statement(自己, 项目):
        return 项目[0] if 项目 else None

    def 定义语法(自己, 项目, 语句):
        return {
            "语句": 语句,
            "类型": 自己.提取数值(项目[0]),
            "名称": 自己.提取数值(项目[1]),
            "量值": 自己.提取数值(项目[2]),
        }
    def define_quote(自己, 项目):
        return {
            "类型": "名称",
            "名称": 项目[0]
        }
    def define_type(自己, 项目):
        return 自己.定义语法(项目, "类型定义")
    def define_constant(自己, 项目):
        return 自己.定义语法(项目, "常量定义")
    def define_variable(自己, 项目):
        return 自己.定义语法(项目, "变量定义")
    def define_capacity(自己, 项目):
        return 自己.定义语法(项目, "容量定义")


    def 结构语法(自己, 项目, 语句):
        return {
            "语句": 语句,
            "返回": 自己.提取数值(项目[0]),
            "名称": 自己.提取数值(项目[1]),
            "参数": 项目[2],
            "代码": 项目[3]
        }
    def struct_quote(自己, 项目):
        return {
            "语句": "调用结构",
            "类型": "结构",
            "名称": 项目[0],
            "参数": 项目[1]
        }
    def struct_class(自己, 项目):
        return 自己.结构语法(项目, "函数定义")
    def struct_function(自己, 项目):
        return 自己.结构语法(项目, "模型定义")


    def control_loop(自己, 项目):
        return {}
    def control_selest(自己, 项目):
        return {}

    def access_pipe(自己, 项目):
        return {
            "语句": "访问管道",
            "名称": 自己.提取数值(项目[0]),
            "属性": [自己.提取数值(项目[i]) for i in range(1, len(项目), 2)]
        }

    def access_object(自己, 项目):
        return {}

    def type(自己, 项目):
        return 项目[0] if 项目 else None
    
    def name(自己, 项目):
        return 项目[0] if 项目 else None
    
    def value(自己, 项目):
        return 项目[0] if 项目 else None
    
    def string(自己, 项目):

        if (项目):
          数值 = 自己.提取数值(项目[0])
          数值 = 数值[1:-1]
          return {"类型":"文本","数值": 数值}
        else:
          return None

    def number(自己, 项目):
        if (项目):
          数值 = 自己.提取数值(项目[0])
          return {"类型":"数字","数值": 数值}
        else:
          return None
    
    def params(自己, 项目):
        params = []
        for i in range(0, len(项目), 2):
            if i+1 < len(项目):
                params.append({
                    "类型": 自己.提取数值(项目[i]),
                    "名称": 自己.提取数值(项目[i+1])
                })
        return params
    
    def arguments(自己, 项目):
        return [自己.提取数值(项目) for 项目 in 项目]
    
    def 提取数值(自身, 节点):
        if isinstance(节点, Tree):
            if 节点.data == 'name':
                return 自身, 节点.提取数值(节点.children[0]) if 节点.children else None
            elif 节点.data == 'value':
                return 自身, 节点.提取数值(节点.children[0]) if 节点.children else None
            elif 节点.data == 'string':
                return 节点.children[0].value if 节点.children else None
            elif 节点.data == 'type':
                return None
            else:
                return 自身.提取数值(节点.children[0]) if 节点.children else None
        elif isinstance(节点, Token):
            return 节点.value
        elif isinstance(节点, list):
            return [自身.提取数值(item) for item in 节点]
        return 节点
    
    def 提取参数(自己, 节点):
        if isinstance(节点, Tree) and 节点.data == 'param':
            return [self.提取数值(child) for child in 节点.children if child]
        elif isinstance(节点, Tree) and 节点.data == 'arguments':
            return [self.提取数值(child) for child in 节点.children if child]
        return []

分析工具 = 语法分析()
def 语言语法分析(词元列表):
  return 分析工具.transform(词元列表)