#!/bin/env python3
import sys
from 工具函数 import 构建语法树, 将对象写入文件, 读取JSON文件

二维数组 = 读取JSON文件(sys.argv[1])
语法大树 = 构建语法树(二维数组)

将对象写入文件(语法大树, sys.argv[2])