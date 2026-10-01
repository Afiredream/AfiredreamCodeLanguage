
# 终端

def 终端输出(*参数) -> None:
    print(*参数)

def 终端输入(文本: str) -> str:
    return input()

# 文本

def 文本长度(文本: str) -> int:
    return len(文本)

def 文本索引(文本: str, 索引: int) -> str:
    return 文本[索引]

def 文本拼接(*参数) -> str:
    return ''.join(map(str, 参数))

__all__ = ["终端输出", "终端输入", "文本长度", "文本索引", "文本拼接"]