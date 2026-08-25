覆写文本文件("/home/usr/燃梦中文语言/测试/测试文件.ast", ast.dump(语言对象, indent=4))
代码文本 = ast.unparse(语言对象)
print(语言对象)
print(ast.unparse(语言对象))


覆写文本文件("/home/usr/燃梦中文语言/测试/测试文件.py", 代码文本)