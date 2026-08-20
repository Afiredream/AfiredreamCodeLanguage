#!/bin/sh

File="$1"
Root="$(dirname "$0")"
$Root/词法分析/词法分析.py "$1" "$1.json"
$Root/语法分析/语法分析.py "$1.json" "$1.ast"
$Root/代码执行/代码执行.py "$1.ast" "$1.py"