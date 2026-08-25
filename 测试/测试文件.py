
import os
import sys
import math
import random
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union, List, Any, Optional
import shutil


# ============================================================
# 1. 终端函数 (function_terminal)
# ============================================================

def 输入(prompt: str = "") -> str:
    """从终端获取用户输入"""
    return input(prompt)


def 错误(message: str) -> None:
    """输出错误信息到标准错误"""
    print(f"❌ 错误: {message}", file=sys.stderr)


def 警告(message: str) -> None:
    """输出警告信息"""
    print(f"⚠️  警告: {message}")


def 调试(message: str) -> None:
    """输出调试信息"""
    print(f"🔍 调试: {message}")


def 输出(*args, sep: str = " ", end: str = "\n") -> None:
    """输出内容到终端"""
    print(*args, sep=sep, end=end)


# ============================================================
# 2. 文本函数 (function_string)
# ============================================================

def 文本长度(text: str) -> int:
    """获取文本长度"""
    return len(text)


def 文本索引(text: str, index: int) -> str:
    """获取文本指定位置的字符"""
    try:
        return text[index]
    except IndexError:
        raise IndexError(f"索引 {index} 超出文本范围")


def 文本拼接(*args) -> str:
    """拼接多个文本"""
    return ''.join(str(arg) for arg in args)


def 文本提取(text: str, start: int, end: Optional[int] = None) -> str:
    """提取文本片段（切片）"""
    return text[start:end]


def 文本分割(text: str, separator: str = ",") -> List[str]:
    """分割文本"""
    return text.split(separator)


def 文本匹配(text: str, pattern: str) -> bool:
    """检查文本是否匹配正则表达式"""
    return bool(re.search(pattern, text))


def 文本搜索(text: str, keyword: str, start: int = 0) -> int:
    """搜索关键词在文本中的位置"""
    return text.find(keyword, start)


def 文本替换(text: str, old: str, new: str, count: int = -1) -> str:
    """替换文本中的内容"""
    return text.replace(old, new, count)


def 文本过滤(text: str, keep: str) -> str:
    """过滤文本，只保留指定字符"""
    return ''.join(char for char in text if char in keep)


# ============================================================
# 3. 数学函数 (function_math)
# ============================================================

def 取最大值(*args) -> float:
    """取最大值"""
    return max(args)


def 取最小值(*args) -> float:
    """取最小值"""
    return min(args)


def 取随机数(start: int, end: int) -> int:
    """生成随机整数"""
    return random.randint(start, end)


def 取绝对值(number: Union[int, float]) -> float:
    """取绝对值"""
    return abs(number)


def 取相反数(number: Union[int, float]) -> float:
    """取相反数"""
    return -number


def 四舍五入(number: float, ndigits: int = 0) -> float:
    """四舍五入"""
    return round(number, ndigits)


def 向上取整(number: float) -> int:
    """向上取整"""
    return math.ceil(number)


def 向下取整(number: float) -> int:
    """向下取整"""
    return math.floor(number)


def 指数运算(base: float, exponent: float) -> float:
    """指数运算"""
    return base ** exponent


def 对数运算(value: float, base: float = math.e) -> float:
    """对数运算"""
    return math.log(value, base)


def 公式运算(expression: str) -> float:
    """计算数学公式（安全模式）"""
    # 只允许安全的数学函数
    safe_dict = {
        'abs': abs, 'ceil': math.ceil, 'floor': math.floor,
        'sqrt': math.sqrt, 'pow': pow, 'exp': math.exp,
        'log': math.log, 'sin': math.sin, 'cos': math.cos,
        'tan': math.tan, 'pi': math.pi, 'e': math.e
    }
    try:
        return eval(expression, {"__builtins__": {}}, safe_dict)
    except Exception as e:
        raise ValueError(f"公式运算错误: {e}")


# ============================================================
# 4. 类型转换函数 (function_conversion)
# ============================================================

def 数据类型(value: Any) -> str:
    """获取数据类型名称"""
    return type(value).__name__


def 转化整数(value: Any) -> int:
    """转化为整数"""
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"无法将 {value} 转化为整数")


def 转化小数(value: Any) -> float:
    """转化为浮点数"""
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(f"无法将 {value} 转化为小数")


def 转化文本(value: Any) -> str:
    """转化为字符串"""
    return str(value)


def 转化真假(value: Any) -> bool:
    """转化为布尔值"""
    return bool(value)


# ============================================================
# 5. 列表函数 (function_list)
# ============================================================

def 列表长度(lst: List[Any]) -> int:
    """获取列表长度"""
    return len(lst)


def 列表合并(*lists) -> List[Any]:
    """合并多个列表"""
    result = []
    for lst in lists:
        result.extend(lst)
    return result


def 列表索引(lst: List[Any], index: int) -> Any:
    """获取列表指定位置的元素"""
    try:
        return lst[index]
    except IndexError:
        raise IndexError(f"索引 {index} 超出列表范围")


def 列表搜索(lst: List[Any], value: Any) -> int:
    """搜索元素在列表中的位置"""
    try:
        return lst.index(value)
    except ValueError:
        return -1


def 列表排序(lst: List[Any], reverse: bool = False) -> List[Any]:
    """对列表排序"""
    return sorted(lst, reverse=reverse)


def 列表插入(lst: List[Any], index: int, value: Any) -> List[Any]:
    """在列表指定位置插入元素"""
    new_lst = lst.copy()
    new_lst.insert(index, value)
    return new_lst


def 列表过滤(lst: List[Any], condition) -> List[Any]:
    """
    过滤列表元素
    condition: 条件函数，返回 True/False
    """
    return [item for item in lst if condition(item)]


def 列表移除(lst: List[Any], value: Any) -> List[Any]:
    """移除列表中所有匹配的元素"""
    return [item for item in lst if item != value]


def 列表修改(lst: List[Any], index: int, value: Any) -> List[Any]:
    """修改列表指定位置的元素"""
    new_lst = lst.copy()
    try:
        new_lst[index] = value
    except IndexError:
        raise IndexError(f"索引 {index} 超出列表范围")
    return new_lst


def 列表去重(lst: List[Any]) -> List[Any]:
    """去除列表中的重复元素（保持顺序）"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def 列表切片(lst: List[Any], start: int, end: Optional[int] = None) -> List[Any]:
    """对列表进行切片"""
    return lst[start:end]


# ============================================================
# 6. 时间函数 (function_time)
# ============================================================

def 当前时间(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间"""
    return datetime.now().strftime(format)


def 时间差值(start: str, end: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """计算两个时间的差值"""
    start_time = datetime.strptime(start, format)
    end_time = datetime.strptime(end, format)
    diff = end_time - start_time
    return str(diff)


# ============================================================
# 7. 文件函数 (function_file)
# ============================================================

def 文件读取(filepath: str, encoding: str = "utf-8") -> str:
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")
    except Exception as e:
        raise IOError(f"读取文件失败: {e}")


def 文件覆写(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """覆写文件"""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


def 文件追加(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """追加内容到文件"""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, 'a', encoding=encoding) as f:
        f.write(content)


def 文件大小(filepath: str) -> int:
    """获取文件大小（字节）"""
    try:
        return os.path.getsize(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")


def 文件信息(filepath: str) -> dict:
    """获取文件详细信息"""
    try:
        stat = os.stat(filepath)
        return {
            '路径': filepath,
            '大小': stat.st_size,
            '创建时间': datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            '修改时间': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            '访问时间': datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            '是否目录': os.path.isdir(filepath),
            '是否文件': os.path.isfile(filepath),
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")


def 文件存在(filepath: str) -> bool:
    """检查文件是否存在"""
    return os.path.exists(filepath)


# ============================================================
# 8. 路径函数 (function_path)
# ============================================================

def 路径拼接(*paths) -> str:
    """拼接路径"""
    return os.path.join(*paths)


def 路径索引(path: str) -> dict:
    """解析路径的基本信息"""
    p = Path(path)
    return {
        '目录': str(p.parent),
        '文件名': p.name,
        '扩展名': p.suffix,
        '无扩展名': p.stem,
        '绝对路径': str(p.absolute()),
        '是否绝对': p.is_absolute(),
        '驱动': p.drive if hasattr(p, 'drive') else '',
    }


def 路径解析(path: str) -> dict:
    """完整解析路径"""
    p = Path(path)
    return {
        '父目录': str(p.parent),
        '文件名': p.name,
        '扩展名': p.suffix,
        '无扩展名': p.stem,
        '绝对路径': str(p.resolve()) if p.exists() else str(p.absolute()),
        '是否存在': p.exists(),
        '是否目录': p.is_dir() if p.exists() else False,
        '是否文件': p.is_file() if p.exists() else False,
        '大小': p.stat().st_size if p.exists() and p.is_file() else 0,
        '修改时间': datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S") if p.exists() else None,
    }

测试 = '一串文本'
名称 = '测试内容'
名称 = '测试内容'

def 函数名称(参数1: str, 参数2: int):
    测试名称 = '12'

    def 函数名(特别参数: int):
        print('测试')
    print(测试名称)
print(测试)
错误('测试错误')
调试('测试调试')