# 燃梦中文语言 VSCode 插件

为「燃梦中文语言」（象语言）提供语法高亮与语言配置。

## 文件类型

| 扩展名 | 说明 |
|---|---|
| `.象` | 燃梦语言源文件 |
| `.燃梦` | 同上（兼容写法） |
| `测试文件` | 仓库中有无扩展名的测试文件 |

## 安装

### 方式一：直接复制

```bash
cp -r 插件/vscode-燃梦中文语言 ~/.vscode/extensions/
```

重启 VSCode 即可生效。

### 方式二：打包成 vsix

```bash
cd 插件/vscode-燃梦中文语言
npx @vscode/vsce package
code --install-extension ranmeng-chinese-language-0.1.0.vsix
```

### 方式三：开发调试

用 VSCode 打开 `插件/vscode-燃梦中文语言` 目录，按 `F5` 启动扩展开发宿主窗口。

## 高亮范围

| 元素 | 示例 | 配色类别 |
|---|---|---|
| 注释 | `# 说明` | comment |
| 文本 | `"你好"`、`'单引号'` | string |
| 数字 | `12`、`3.14`、`-5` | constant.numeric |
| 状态 | `真` `假` `True` `False` `None` | constant.language |
| 定义语句 | `变量` `常量` `容量` `类型` | storage.type |
| 类型名 | `文本` `数字` `列表` `对象` `状态` `任意` | entity.name.type |
| 结构定义 | `函数` `模型` `导出` | storage.type.function |
| 函数名 | `导出 文本:索引(` 中的 `索引` | entity.name.function |
| 控制语句 | `如果` `或者` `否则` `循环` `执行` | keyword.control |
| 导入导出 | `导入` `导出` `命名` `选择` | keyword.control.import |
| 返回 | `返回` | keyword.control.flow |
| 运算符 | `+ - * / % <= == != and or not in ...` | keyword.operator |
| 参数 | `文本:a` 中的 `a` | variable.parameter |
| 变量名 | `变量 数字:名称` 中的 `名称` | variable.other |
| 内置函数 | `终端输出`、`文本拼接` 等 | support.function.builtin |

## 语言配置

- 行注释：`#`
- 括号自动配对：`{}` `[]` `()` `""` `''`
- 输入 `{` 回车自动缩进，输入 `}` 自动反缩进
- 单词选择以中文为整体单位，双击「变量名」不会拆成单个汉字

## 目录结构

```
vscode-燃梦中文语言/
├── package.json                              插件清单
├── language-configuration/
│   └── language-configuration.json           括号、注释、缩进规则
├── syntaxes/
│   └── ranmeng.tmLanguage.json               语法高亮规则
└── README.md
```

## 已知限制

- 仅提供**语法高亮**与**编辑辅助**，不含编译、运行、跳转定义等功能
- 高亮基于正则匹配，不做语义分析。例如变量名恰好叫 `真` 时会被当作状态字面量
- 多行文本（跨行字符串）内部的高亮可能不完整，因为语言允许字符串跨行

## 许可

MIT
