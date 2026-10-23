
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

# 文本处理底层
#
# 语言里暂时不能写「文本.方法()」，所以把需要用到的字符串操作
# 在这里实现成可调用的函数，供模块代码使用。

def 编码长度(文本) -> int:
    """文本按 UTF-8 编码后的字节数。"""
    return len(str(文本).encode('utf-8'))

def 字符数量(文本) -> int:
    """文本的字符个数；传入列表时返回元素个数。"""
    if isinstance(文本, (list, tuple, dict, set)):
        return len(文本)
    return len(str(文本))

def 取子文本(文本, 起始, 长度) -> str:
    """从 1 开始数，从 起始 处取 长度 个字符。"""
    文本 = str(文本)
    起始 = int(起始) - 1
    if 起始 < 0:
        起始 = 0
    return 文本[起始:起始 + int(长度)]

def 查找子文本(文本, 子文本):
    """返回子文本第一次出现的序号（从 1 开始），找不到返回 0。"""
    位置 = str(文本).find(str(子文本))
    return 位置 + 1

def 是否包含(文本, 子文本) -> bool:
    return str(子文本) in str(文本)

def 按分隔符分割(文本, 分隔符):
    结果 = str(文本).split(str(分隔符))
    return 结果

def 按分隔符连接(列表, 分隔符) -> str:
    return str(分隔符).join(str(项) for 项 in 列表)

def 修剪空白(文本) -> str:
    return str(文本).strip()

def 去除左端空白(文本) -> str:
    return str(文本).lstrip()

def 去除右端空白(文本) -> str:
    return str(文本).rstrip()

def 转大写(文本) -> str:
    return str(文本).upper()

def 转小写(文本) -> str:
    return str(文本).lower()

def 首字母大写(文本) -> str:
    文本 = str(文本)
    return 文本[:1].upper() + 文本[1:]

def 替换文本(文本, 旧文本, 新文本) -> str:
    return str(文本).replace(str(旧文本), str(新文本))

def 开头是否(文本, 前缀) -> bool:
    return str(文本).startswith(str(前缀))

def 结尾是否(文本, 后缀) -> bool:
    return str(文本).endswith(str(后缀))

def 反转文本(文本) -> str:
    return str(文本)[::-1]

def 是否为数字(文本) -> bool:
    return str(文本).isdigit()

def 正则查找(文本, 格式):
    """找出所有匹配的片段，返回列表。"""
    import re
    return re.findall(str(格式), str(文本))

def 规范文本(文本) -> str:
    """规范化文本：
    统一换行、把连续空白压成一个、去掉两端空白，
    并把常见的全角标点换成半角。
    """
    文本 = str(文本).replace('\r\n', '\n').replace('\r', '\n')
    文本 = ' '.join(文本.split())
    标点对照 = {
        '，': ',', '。': '.', '：': ':', '；': ';',
        '！': '!', '？': '?', '（': '(', '）': ')',
        '【': '[', '】': ']', '“': '"', '”': '"',
        '‘': "'", '’': "'", '、': ',',
    }
    for 全角, 半角 in 标点对照.items():
        文本 = 文本.replace(全角, 半角)
    return 文本

def 正则替换(文本, 格式, 新文本) -> str:
    import re
    return re.sub(str(格式), str(新文本), str(文本))


# 路径处理底层
#
# 路径一律用正斜杠 / 表示，与语言里写的一致。

def 路径拼接(*片段) -> str:
    """把若干段路径拼起来，自动补上合适的斜杠。"""
    import posixpath
    片段 = [str(项) for 项 in 片段 if str(项) != '']
    if not 片段:
        return ''
    return posixpath.join(*片段)

def 路径目录(路径) -> str:
    """取出目录部分，如 a/b/c.txt → a/b。"""
    import posixpath
    return posixpath.dirname(str(路径))

def 路径名称(路径) -> str:
    """取出最后一段，如 a/b/c.txt → c.txt。"""
    import posixpath
    return posixpath.basename(str(路径).rstrip('/'))

def 路径文件名(路径) -> str:
    """取出不含扩展名的文件名，如 a/b/c.txt → c。"""
    import posixpath
    return posixpath.splitext(posixpath.basename(str(路径).rstrip('/')))[0]

def 路径拓展(路径) -> str:
    """取出扩展名（不带点），如 a/b/c.txt → txt；没有则返回空文本。"""
    import posixpath
    扩展名 = posixpath.splitext(posixpath.basename(str(路径).rstrip('/')))[1]
    return 扩展名[1:] if 扩展名.startswith('.') else 扩展名

def 路径规范(路径) -> str:
    """规范化路径：去掉多余的斜杠、处理 . 与 ..。"""
    import posixpath
    结果 = posixpath.normpath(str(路径))
    return 结果

def 是否为绝对路径(路径) -> bool:
    import posixpath
    return posixpath.isabs(str(路径))

def 路径段(路径):
    """把路径按斜杠拆成各段。"""
    路径 = str(路径).strip('/')
    return [] if not 路径 else 路径.split('/')

def 路径段前(路径, 数量):
    """取路径的前若干段，如 数量=2 时 a/b/c.txt → [a, b]。"""
    段 = 路径段(路径)
    return 段[:int(数量)]

def 追加列表(列表, 项):
    """返回追加了一项的新列表。"""
    结果 = list(列表)
    结果.append(项)
    return 结果

def 前几项(列表, 数量):
    return list(列表)[:int(数量)]

def 路径层级(路径) -> int:
    """路径的深度，如 a/b/c.txt → 3。"""
    return len(路径段(路径))

def 路径存在(路径) -> bool:
    import os
    return os.path.exists(str(路径))

def 是否为文件(路径) -> bool:
    import os
    return os.path.isfile(str(路径))

def 是否为目录(路径) -> bool:
    import os
    return os.path.isdir(str(路径))

def 绝对路径(路径) -> str:
    import os
    return os.path.abspath(str(路径))

def 删除路径(路径) -> bool:
    """删除一个文件。"""
    import os
    try:
        os.remove(str(路径))
        return True
    except OSError as 错误:
        print(f"删除文件失败：{错误}")
        return False


def 路径大小(路径) -> int:
    """文件大小（字节）；不是文件时返回 0。"""
    import os
    try:
        return os.path.getsize(str(路径))
    except OSError:
        return 0


# 函数

import builtins
import types

# 允许语言代码直接调用的 Python 内置对象。
# 只开放常用的纯计算函数，像 open、eval、exec、exit 这类不在此列。
开放的Python内置 = frozenset({
    'abs', 'round', 'min', 'max', 'sum', 'pow', 'divmod',
    'len', 'repr', 'ord', 'chr', 'format', 'bin', 'oct', 'hex',
    'list', 'sorted', 'reversed', 'enumerate', 'zip', 'range',
    'any', 'all', 'map', 'filter',
    # 文件读写
    'open',
    'print',
})

# 这些是 Python 标准库模块，供模块代码直接使用，如 json.dumps(...)
开放的标准库 = frozenset({'json', 'os', 're', 'html', 'posixpath',
                            'configparser', 'math'})

# 这些名字对应 Python 的类型，用于类型转换，如 int("12")、float("1.5")
开放的Python类型 = frozenset({
    'int', 'float', 'bool', 'str', 'list', 'tuple', 'dict', 'set',
})


def 取得内置对象(函数名称: str):
    """按名字取出可调用的对象：先找本文件，再找 Python 内置。"""
    函数对象 = globals().get(函数名称)
    if isinstance(函数对象, types.FunctionType) \
            and 函数对象.__module__ == __name__:
        return 函数对象

    if 函数名称 in 开放的Python内置 or 函数名称 in 开放的Python类型:
        候选 = getattr(builtins, 函数名称, None)
        if callable(候选):
            return 候选

    if 函数名称 in 开放的标准库:
        import importlib
        try:
            return importlib.import_module(函数名称)
        except ImportError:
            return None
    return None


def 取得标准库(名称):
    """按名字取出允许使用的标准库模块。"""
    if 名称 not in 开放的标准库:
        return None
    import importlib
    try:
        return importlib.import_module(名称)
    except ImportError:
        return None


def 索引内置函数(函数名称: str) -> bool:
    return 取得内置对象(函数名称) is not None


def 执行内置函数(函数名称: str, 参数列表: list, 关键字参数=None):
    """带关键字参数调用内置函数。"""
    函数对象 = 取得内置对象(函数名称)
    if 函数对象 is None:
        print(f"没有名为「{函数名称}」的内置函数")
        return None
    try:
        return 函数对象(*参数列表, **(关键字参数 or {}))
    except Exception as 错误:
        print(f"调用「{函数名称}」失败：{错误}")
        return None


def 运行内置函数(函数名称: str, 参数列表: list):
    函数对象 = 取得内置对象(函数名称)
    if 函数对象 is None:
        print(f"没有名为「{函数名称}」的内置函数")
        return None
    return 函数对象(*参数列表)


__all__ = ["索引内置函数", "运行内置函数", "取得内置对象",
           "开放的Python内置", "开放的Python类型"]


# 文件操作底层
#
# 涉及真删真改，所有出错都返回空文本或「假」，不抛异常打断程序。

def 读取文件(路径) -> str:
    try:
        with open(str(路径), 'r', encoding='utf-8') as 文件:
            return 文件.read()
    except OSError as 错误:
        print(f"读取文件失败：{错误}")
        return ""

def 写入文件(路径, 内容) -> bool:
    try:
        with open(str(路径), 'w', encoding='utf-8') as 文件:
            文件.write(str(内容))
        return True
    except OSError as 错误:
        print(f"写入文件失败：{错误}")
        return False

def 追加文件(路径, 内容) -> bool:
    try:
        with open(str(路径), 'a', encoding='utf-8') as 文件:
            文件.write(str(内容))
        return True
    except OSError as 错误:
        print(f"追加文件失败：{错误}")
        return False

def 复制文件(来源, 目标) -> bool:
    import shutil
    try:
        shutil.copy2(str(来源), str(目标))
        return True
    except OSError as 错误:
        print(f"复制文件失败：{错误}")
        return False

def 移动文件(来源, 目标) -> bool:
    import shutil
    try:
        shutil.move(str(来源), str(目标))
        return True
    except OSError as 错误:
        print(f"移动文件失败：{错误}")
        return False

def 删除文件(路径) -> bool:
    import os
    try:
        os.remove(str(路径))
        return True
    except OSError as 错误:
        print(f"删除文件失败：{错误}")
        return False


# 对象处理底层
#
# 对象在语言里就是 JSON 风格的数据：文本、数字、列表、字典。

def 转JSON文本(对象, 缩进) -> str:
    """把对象转成 JSON 文本；缩进为 0 时紧凑输出。"""
    import json
    try:
        缩进 = int(缩进)
    except (TypeError, ValueError):
        缩进 = 0
    if 缩进 <= 0:
        return json.dumps(对象, ensure_ascii=False)
    return json.dumps(对象, ensure_ascii=False, indent=缩进)

def 解析JSON文本(文本):
    """把 JSON 文本转成对象；失败返回空字典。"""
    import json
    try:
        return json.loads(str(文本))
    except (ValueError, TypeError) as 错误:
        print(f"解析 JSON 失败：{错误}")
        return {}

def 读取对象文件(路径):
    """读取 JSON 文件，返回其中的对象；失败返回空字典。"""
    import json
    try:
        with open(str(路径), 'r', encoding='utf-8') as 文件:
            return json.load(文件)
    except OSError as 错误:
        print(f"读取对象文件失败：{错误}")
        return {}
    except ValueError as 错误:
        print(f"对象文件内容不是合法 JSON：{错误}")
        return {}

def 写入对象文件(路径, 对象, 缩进) -> bool:
    """把对象写成 JSON 文件；失败返回「假」。"""
    import json
    try:
        with open(str(路径), 'w', encoding='utf-8') as 文件:
            json.dump(对象, 文件, ensure_ascii=False, indent=int(缩进 or 2))
        return True
    except (OSError, TypeError, ValueError) as 错误:
        print(f"写入对象文件失败：{错误}")
        return False

def 对象取(对象, 键):
    """按键取值，不存在时返回空文本。"""
    return 对象.get(str(键), "") if isinstance(对象, dict) else ""

def 对象设(对象, 键, 值):
    """返回设置了某一项的新对象。"""
    结果 = dict(对象) if isinstance(对象, dict) else {}
    结果[str(键)] = 值
    return 结果

def 对象有(对象, 键) -> bool:
    return isinstance(对象, dict) and str(键) in 对象

def 对象删(对象, 键):
    结果 = dict(对象) if isinstance(对象, dict) else {}
    结果.pop(str(键), None)
    return 结果

def 对象键列表(对象):
    return list(对象.keys()) if isinstance(对象, dict) else []

def 对象值列表(对象):
    return list(对象.values()) if isinstance(对象, dict) else []

def 对象项数(对象) -> int:
    return len(对象) if isinstance(对象, dict) else 0


# 配置（INI）底层
#
# 为了最大兼容，统一这样处理：
#   · 关闭 % 插值，值里的 % 原样保留
#   · 允许重复键，后出现的覆盖前面的
#   · 支持 # 与 ; 开头的注释、= 与 : 两种分隔符、多行值
#   · 段名与键名保持原样，不做大小写转换

def _新建解析器():
    import configparser
    解析器 = configparser.ConfigParser(
        interpolation=None,
        strict=False,
        allow_no_value=True,
        comment_prefixes=('#', ';'),
        inline_comment_prefixes=None,
        empty_lines_in_values=False,
        default_section='DEFAULT',
    )
    解析器.optionxform = str      # 保持键名原样
    解析器.read_dict({'DEFAULT': {}})
    return 解析器


def 解析INI文本(文本):
    """把 INI 文本解析成 {节: {键: 值}}；失败返回空字典。"""
    文本 = str(文本)
    if 文本.startswith('\ufeff'):
        文本 = 文本[1:]
    解析器 = _新建解析器()
    try:
        解析器.read_string(文本)
    except Exception as 错误:
        print(f"解析配置失败：{错误}")
        return {}
    结果 = {}
    for 节 in 解析器.sections():
        结果[节] = {键: (值 if 值 is not None else '')
                    for 键, 值 in 解析器.items(节) if 键 != 'DEFAULT'}
    return 结果


def 读取INI文件(路径):
    """读取 INI 文件；失败返回空字典。"""
    try:
        with open(str(路径), 'r', encoding='utf-8-sig') as 文件:
            return 解析INI文本(文件.read())
    except OSError as 错误:
        print(f"读取配置文件失败：{错误}")
        return {}


def 生成INI文本(配置) -> str:
    """把 {节: {键: 值}} 写成 INI 文本。"""
    if not isinstance(配置, dict):
        return ''
    行 = []
    for 节, 内容 in 配置.items():
        if not isinstance(内容, dict):
            continue
        行.append(f'[{节}]')
        for 键, 值 in 内容.items():
            行.append(f'{键} = {值}')
        行.append('')
    return '\n'.join(行)


def 写入INI文件(路径, 配置) -> bool:
    try:
        with open(str(路径), 'w', encoding='utf-8') as 文件:
            文件.write(生成INI文本(配置))
        return True
    except OSError as 错误:
        print(f"写入配置文件失败：{错误}")
        return False


def INI取段(配置, 节):
    return dict(配置.get(节, {})) if isinstance(配置, dict) else {}


def INI取(配置, 节, 键, 缺省):
    try:
        return 配置[节][键]
    except (KeyError, TypeError):
        return 缺省


def INI设(配置, 节, 键, 值):
    结果 = {段: dict(项) for 段, 项 in 配置.items()} if isinstance(配置, dict) else {}
    结果.setdefault(节, {})[键] = 值
    return 结果


def INI删(配置, 节, 键=None):
    结果 = {段: dict(项) for 段, 项 in 配置.items()} if isinstance(配置, dict) else {}
    if 键 is None:
        结果.pop(节, None)
    elif 节 in 结果:
        结果[节].pop(键, None)
    return 结果


def INI有段(配置, 节) -> bool:
    return isinstance(配置, dict) and 节 in 配置


def INI有键(配置, 节, 键) -> bool:
    return isinstance(配置, dict) and isinstance(配置.get(节), dict) and 键 in 配置[节]


def INI段列表(配置):
    return list(配置.keys()) if isinstance(配置, dict) else []


def INI键列表(配置, 节):
    return list(配置.get(节, {}).keys()) if isinstance(配置, dict) else []


def INI转数字(文本, 缺省):
    try:
        return int(str(文本).strip())
    except (TypeError, ValueError):
        return 缺省


def INI转状态(文本) -> bool:
    """把常见的真值写法统一成布尔。"""
    return str(文本).strip().lower() in ('真', '是', '1', 'true', 'yes', 'on', 'y')


# YAML 底层（自实现，不依赖第三方库）
#
# 支持常见的 YAML 写法：
#   键: 值            映射
#   - 项              列表
#   缩进嵌套           二空格或四空格都行
#   引号文本           单引号与双引号
#   # 注释
#   | 与 >            多行文本
#   真/假 是/否        布尔
#   数字与空值 null
# 不支持锚点、别名、复杂标签等高级语法。

def _去掉YAML注释(行):
    """去掉行尾注释，引号内的 # 不算注释。"""
    引号 = None
    结果 = []
    for 字符 in 行:
        if 引号:
            结果.append(字符)
            if 字符 == 引号:
                引号 = None
            continue
        if 字符 in ('"', "'"):
            引号 = 字符
            结果.append(字符)
            continue
        if 字符 == '#':
            break
        结果.append(字符)
    return ''.join(结果).rstrip()

def _转换YAML值(文本):
    """把 YAML 的标量文本转成合适的 Python 值。"""
    文本 = 文本.strip()
    if 文本 == '' or 文本 in ('~', 'null', 'Null', 'NULL'):
        return None
    if len(文本) >= 2 and 文本[0] == 文本[-1] and 文本[0] in ('"', "'"):
        内 = 文本[1:-1]
        if 文本[0] == '"':
            内 = 内.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
        else:
            内 = 内.replace("''", "'")
        return 内
    小写 = 文本.lower()
    if 小写 in ('true', 'yes', 'on', '真', '是'):
        return True
    if 小写 in ('false', 'no', 'off', '假', '否'):
        return False
    try:
        return int(文本)
    except ValueError:
        pass
    try:
        return float(文本)
    except ValueError:
        pass
    return 文本

def 解析YAML文本(文本):
    """把 YAML 文本解析为对象；失败返回空字典。"""
    try:
        return _解析YAML(str(文本))
    except Exception as 错误:
        print(f"解析 YAML 失败：{错误}")
        return {}

def _解析YAML(文本):
    原文行 = str(文本).replace('\r\n', '\n').replace('\r', '\n').split('\n')
    行列表 = []
    for 行 in 原文行:
        if not 行.strip():
            continue
        去掉注释 = _去掉YAML注释(行)
        if not 去掉注释.strip():
            continue
        缩进 = len(去掉注释) - len(去掉注释.lstrip())
        行列表.append((缩进, 去掉注释.strip()))

    位置 = [0]

    def 读块(当前缩进):
        if 位置[0] >= len(行列表):
            return None
        缩进, 内容 = 行列表[位置[0]]
        if 内容.startswith('- '):
            return 读列表(缩进)
        return 读映射(缩进)

    def 读列表(缩进):
        结果 = []
        while 位置[0] < len(行列表):
            当前缩进, 内容 = 行列表[位置[0]]
            if 当前缩进 < 缩进 or not 内容.startswith('- '):
                break
            if 当前缩进 > 缩进:
                break
            项文本 = 内容[2:].strip()
            位置[0] += 1
            if 项文本 == '':
                # 列表项下还有嵌套
                子 = 读块(缩进 + 1) if 位置[0] < len(行列表) else None
                结果.append(子)
            elif ':' in 项文本 and not 项文本.startswith(('"', "'")):
                # 列表项本身是映射，如「- 名: 甲」，后续缩进的行继续并入
                键, _, 值 = 项文本.partition(':')
                项 = {键.strip(): _转换YAML值(值) if 值.strip() else None}
                while 位置[0] < len(行列表):
                    内缩进, 内内容 = 行列表[位置[0]]
                    if 内缩进 <= 缩进 or 内内容.startswith('- '):
                        break
                    内键, _, 内值 = 内内容.partition(':')
                    位置[0] += 1
                    if 内值.strip() == '' and 位置[0] < len(行列表) \
                            and 行列表[位置[0]][0] > 内缩进:
                        项[内键.strip()] = 读块(行列表[位置[0]][0])
                    else:
                        项[内键.strip()] = _转换YAML值(内值)
                结果.append(项)
            else:
                结果.append(_转换YAML值(项文本))
        return 结果

    def 读映射(缩进):
        结果 = {}
        while 位置[0] < len(行列表):
            当前缩进, 内容 = 行列表[位置[0]]
            if 当前缩进 < 缩进:
                break
            if 当前缩进 > 缩进:
                # 比预期更深，跳过以免死循环
                位置[0] += 1
                continue
            if 内容.startswith('- '):
                break
            if ':' not in 内容 and not 内容.endswith(':'):
                位置[0] += 1
                continue
            键, _, 值 = 内容.partition(':')
            键 = 键.strip()
            if len(键) >= 2 and 键[0] == 键[-1] and 键[0] in ('"', "'"):
                键 = 键[1:-1]
            值 = 值.strip()
            位置[0] += 1
            if 值 in ('|', '>'):
                # 多行文本
                块行 = []
                while 位置[0] < len(行列表) and 行列表[位置[0]][0] > 缩进:
                    块行.append(行列表[位置[0]][1])
                    位置[0] += 1
                结果[键] = '\n'.join(块行) if 值 == '|' else ' '.join(块行)
            elif 值 == '':
                # 嵌套结构
                if 位置[0] < len(行列表) and 行列表[位置[0]][0] > 缩进:
                        结果[键] = 读块(行列表[位置[0]][0])
                else:
                    结果[键] = None
            else:
                结果[键] = _转换YAML值(值)
        return 结果

    if not 行列表:
        return {}
    return 读块(行列表[0][0])

def 生成YAML文本(对象, 缩进大小) -> str:
    """把对象写成 YAML 文本。"""
    空格 = ' ' * max(1, int(缩进大小 or 2))

    def 写值(值, 层级):
        填充 = 空格 * 层级
        注意 = []
        if isinstance(值, dict):
            if not 值:
                return ' {}'
            注意.append('')
            for 键, 项 in 值.items():
                if isinstance(项, (dict, list)) and 项:
                    注意.append(f'{填充}{键}:{写值(项, 层级 + 1)}')
                else:
                    注意.append(f'{填充}{键}: {标量(项)}')
            return '\n' + '\n'.join(注意[1:] if 注意 and 注意[0] == '' else 注意)
        if isinstance(值, list):
            if not 值:
                return ' []'
            注意.append('')
            for 项 in 值:
                if isinstance(项, (dict, list)) and 项:
                    注意.append(f'{填充}-{写值(项, 层级 + 1)}')
                else:
                    注意.append(f'{填充}- {标量(项)}')
            return '\n' + '\n'.join(注意[1:] if 注意 and 注意[0] == '' else 注意)
        return ' ' + 标量(值)

    def 标量(值):
        if 值 is None:
            return 'null'
        if 值 is True:
            return 'true'
        if 值 is False:
            return 'false'
        if isinstance(值, (int, float)):
            return str(值)
        文本 = str(值)
        if 文本 == '' or 需要引号(文本):
            return '"' + 文本.replace('"', '\\"') + '"'
        return 文本

    def 需要引号(文本):
        if 文本.strip() != 文本:
            return True
        if 文本[:1] in ('-', '#', '{', '[', '"', "'", '&', '*', '!'):
            return True
        return any(字符 in 文本 for 字符 in (':', '#', '\n'))

    return 写值(对象, 0).lstrip('\n')


# HTML 底层（基于标准库 html.parser，不依赖第三方库）
#
# 解析结果里每个元素写成：
#   { 标签: 名称, 属性: {属性名: 值}, 文本: 直接文本, 全部文本: 含子元素文本,
#     子元素: [...], 父元素: 父标签名 }
# 便于按键查找、取文本、取属性。

def _HTML转对象(文本, 保留空白):
    from html.parser import HTMLParser

    根 = {'标签': '#根', '属性': {}, '文本': [], '全部文本': '',
          '子元素': [], '父元素': None}

    class 解析器(HTMLParser):
        def __init__(自己):
            super().__init__(convert_charrefs=True)
            自己.栈 = [根]

        def handle_starttag(自己, 标签, 属性):
            节点 = {'标签': 标签, '属性': dict(属性),
                    '文本': [], '全部文本': '', '子元素': [],
                    '父元素': 自己.栈[-1]['标签']}
            父 = 自己.栈[-1]
            父['子元素'].append(节点)
            # 记下子元素在文本流中的位置，最后按顺序拼回来
            父['文本'].append('\x00' + str(len(父['子元素']) - 1) + '\x00')
            自己.栈.append(节点)

        def handle_startendtag(自己, 标签, 属性):
            节点 = {'标签': 标签, '属性': dict(属性),
                    '文本': [], '全部文本': '', '子元素': [],
                    '父元素': 自己.栈[-1]['标签']}
            父 = 自己.栈[-1]
            父['子元素'].append(节点)
            父['文本'].append('\x00' + str(len(父['子元素']) - 1) + '\x00')

        def handle_endtag(自己, 标签):
            for 序号 in range(len(自己.栈) - 1, 0, -1):
                if 自己.栈[序号]['标签'] == 标签:
                    del 自己.栈[序号:]
                    break

        def handle_data(自己, 数据):
            自己.栈[-1]['文本'].append(数据)

    解析器对象 = 解析器()
    try:
        HTMLParser_实例 = 解析器对象
        HTMLParser_实例.feed(str(文本))
    except Exception as 错误:
        print(f"解析 HTML 失败：{错误}")
        return {}

    def 整理(节点):
        子 = [整理(项) for 项 in 节点['子元素']]
        节点['子元素'] = 子
        # 还原「文本、子元素、文本…」的原始顺序
        流 = ''.join(节点['文本'])
        直接 = ''.join(段 for 段 in 节点['文本'] if not 段.startswith('\x00'))
        if not 保留空白:
            直接 = ' '.join(直接.split())
        节点['文本'] = 直接

        全部 = []
        位置 = 0
        while 位置 < len(流):
            if 流[位置] == '\x00':
                结束 = 流.find('\x00', 位置 + 1)
                if 结束 > 位置:
                    序号 = int(流[位置 + 1:结束])
                    if 0 <= 序号 < len(子):
                        全部.append(子[序号]['全部文本'])
                    位置 = 结束 + 1
                    continue
            全部.append(流[位置])
            位置 += 1
        全部 = ''.join(全部)
        if not 保留空白:
            全部 = ' '.join(全部.split())
        节点['全部文本'] = 全部
        return 节点

    return 整理(根)

def _展开HTML元素(节点, 结果列表):
    for 子 in 节点.get('子元素') or []:
        结果列表.append({
            '标签': 子['标签'],
            '属性': 子['属性'],
            '文本': 子['文本'],
            '全部文本': 子['全部文本'],
            '父元素': 子['父元素'],
        })
        _展开HTML元素(子, 结果列表)
    return 结果列表

def 解析HTML文本(文本):
    """把 HTML 解析为元素列表。"""
    根 = _HTML转对象(文本, False)
    return _展开HTML元素(根, [])

def 提取HTML文本(文本) -> str:
    """取出 HTML 的全部可见文本，标签被去掉。"""
    根 = _HTML转对象(文本, False)
    return 根.get('全部文本', '')

def 提取HTML属性(文本, 标签, 属性名) -> str:
    """取出第一个指定标签的某个属性值。"""
    for 项 in 解析HTML文本(文本):
        if 项['标签'] == str(标签).lower():
            return 项['属性'].get(str(属性名), '')
    return ''

def 查找HTML元素(文本, 标签):
    """按标签名找出全部元素。"""
    标签 = str(标签).lower()
    return [项 for 项 in 解析HTML文本(文本) if 项['标签'] == 标签]

def 提取HTML标签文本(文本, 标签) -> str:
    """取出第一个指定标签里的全部文本。"""
    标签 = str(标签).lower()
    for 项 in 解析HTML文本(文本):
        if 项['标签'] == 标签:
            return 项['全部文本']
    return ''

def 转义HTML文本(文本) -> str:
    from html import escape
    return escape(str(文本), quote=True)

def 反转义HTML文本(文本) -> str:
    from html import unescape
    return unescape(str(文本))


# 全局常量
#
# 这些名字在语言里可以直接使用，且不允许被重新定义。

def 取得操作系统名称() -> str:
    """当前操作系统的名称：Linux / Windows / Darwin。"""
    import platform
    return platform.system()


# 文件系统判断（用 Python 自带的 os 模块，模块里直接调用）

def 路径存在(路径) -> bool:
    import os
    return os.path.exists(str(路径))

def 路径是文件(路径) -> bool:
    import os
    return os.path.isfile(str(路径))

def 路径是目录(路径) -> bool:
    import os
    return os.path.isdir(str(路径))

def 路径大小(路径) -> int:
    import os
    try:
        return os.path.getsize(str(路径))
    except OSError:
        return 0
