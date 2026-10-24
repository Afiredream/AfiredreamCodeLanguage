#!/usr/bin/env python3
"""生成燃梦中文语言的文档页面（HTML）。

用法：python3 生成文档.py
输出：文档/index.html
"""

import json
import os

脚本目录 = os.path.dirname(os.path.abspath(__file__))
项目目录 = os.path.dirname(脚本目录)
输出目录 = os.path.join(项目目录, '文档')
数据文件 = os.path.join(脚本目录, '文档数据.json')


# ── 模块说明 ──────────────────────────────────────────────

模块说明 = {
    '文本': ('文本处理', '字符串的查找、切割、替换、大小写等操作。位置从 1 开始数。'),
    '数组': ('数组处理', '数组的增删改查、排序、遍历。元素可以任意，但声明为「数组」类型时要求同类型。'),
    '数学': ('数学运算', '取整、取余、幂、极值、统计、进制转换。'),
    '路径': ('路径处理', '路径的拼接、拆分、规范化与判断。'),
    '文件': ('文件读写', '读取、写入、复制、移动、删除文件与目录。'),
    '对象': ('对象与 JSON', '对象的增删查改，以及 JSON 的解析与生成。'),
    '配置': ('INI 配置', 'INI 配置文件的解析、读取与写入。'),
    'YAML': ('YAML 数据', 'YAML 的解析与生成。'),
    'HTML': ('HTML 解析', 'HTML 文本的提取、标签查找与转义。'),
}

关键字 = [
    ('变量', '定义可修改的变量', '变量 数字:计数 = 0'),
    ('常量', '定义不可修改的常量', '常量 数字:上限 = 100'),
    ('容量', '定义容量（可增长的容器）', '容量 列表:结果 = []'),
    ('类型', '定义类型别名', '类型 结构:点 = 原点'),
    ('函数', '定义函数', '函数 文本:问候(文本:谁) { 返回 谁 }'),
    ('模型', '定义数据结构模型', '模型 点(数字:x, 数字:y) { }'),
    ('导出', '定义并导出函数，或选择已定义的函数导出', '导出 文本:拼接(文本:参数...) { ... }'),
    ('导入', '导入模块，用「模块名.函数」访问', '导入 模块/文本'),
    ('如果', '条件判断，可带一个「或者」分支', '如果(甲 > 乙) { ... } 或者(真) { ... }'),
    ('循环', '按条件循环', '循环(序号 <= 10) { 序号++ }'),
    ('返回', '从函数返回一个值', '返回 结果'),
]

运算符 = [
    ('+', '加 / 拼接文本 / 合并数组', '1 + 2 → 3'),
    ('-', '减', '5 - 2 → 3'),
    ('*', '乘', '3 * 4 → 12'),
    ('/', '除', '10 / 2 → 5.0'),
    ('%', '取余', '17 % 5 → 2'),
    ('==', '等于', '甲 == 乙'),
    ('!=', '不等于', '甲 != 乙'),
    ('<', '小于', '甲 < 乙'),
    ('>', '大于', '甲 > 乙'),
    ('<=', '小于等于', '甲 <= 乙'),
    ('>=', '大于等于', '甲 >= 乙'),
    ('&&', '逻辑与；语句中表示「条件成立则执行」', '甲 > 0 && 返回 真'),
    ('||', '逻辑或；语句中效果同 &&（条件成立则执行）', '甲 == "" || 返回 真'),
    ('!', '取反（同 not）', '!在职'),
    ('++', '自增 1', '计数++'),
    ('--', '自减 1', '计数--'),
    ('|', '管道：把左边的值作为第一个参数传给右边', '内容|切割(1, 5)'),
    ('in', '成员判断（文本或数组）', '"书" in 爱好'),
]


def 转义(文本):
    return (str(文本).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def 渲染函数(项):
    参数 = '，'.join(项['参数']) if 项['参数'] else '无'
    返回 = 项['返回'] or '任意'
    return f'''
      <div class="fn">
        <div class="sig"><span class="ret">{转义(返回)}</span>
          <span class="sep">:</span><span class="name">{转义(项['名'])}</span>
          <span class="paren">(</span><span class="params">{转义(参数)}</span><span class="paren">)</span>
        </div>
      </div>'''


def 渲染模块(模块名, 函数列表):
    标题, 说明 = 模块说明.get(模块名, (模块名, ''))
    函数列表 = [f for f in 函数列表 if f['名'] != '数组']
    卡片 = ''.join(渲染函数(f) for f in 函数列表)
    return f'''
    <section class="module" id="mod-{转义(模块名)}">
      <h3>{转义(模块名)} <span class="sub">{转义(标题)}</span>
        <span class="count">{len(函数列表)} 个函数</span></h3>
      <p class="desc">{转义(说明)}</p>
      <div class="fns">{卡片}</div>
    </section>'''


def 生成():
    with open(数据文件, encoding='utf-8') as 文件:
        数据 = json.load(文件)

    关键字行 = ''.join(
        f'<tr><td><code>{转义(词)}</code></td><td>{转义(说明)}</td>'
        f'<td><code class="ex">{转义(例)}</code></td></tr>'
        for 词, 说明, 例 in 关键字)

    运算符行 = ''.join(
        f'<tr><td><code>{转义(符)}</code></td><td>{转义(说明)}</td>'
        f'<td><code class="ex">{转义(例)}</code></td></tr>'
        for 符, 说明, 例 in 运算符)

    模块导航 = ''.join(
        f'<a href="#mod-{转义(名)}">{转义(名)}</a>' for 名 in 数据)

    模块内容 = ''.join(渲染模块(名, 列表) for 名, 列表 in 数据.items())

    总数 = sum(len([f for f in 列表 if f['名'] != '数组'])
               for 列表 in 数据.values())

    页面 = 模板.replace('{{关键字行}}', 关键字行) \
                 .replace('{{运算符行}}', 运算符行) \
                 .replace('{{模块导航}}', 模块导航) \
                 .replace('{{模块内容}}', 模块内容) \
                 .replace('{{总数}}', str(总数))

    os.makedirs(输出目录, exist_ok=True)
    路径 = os.path.join(输出目录, 'index.html')
    with open(路径, 'w', encoding='utf-8') as 文件:
        文件.write(页面)
    return 路径


模板 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>燃梦中文语言 · 文档</title>
<style>
  :root {
    --bg: #0f1419; --panel: #161c24; --panel2: #1c242e;
    --border: #2a3441; --text: #d6dee8; --dim: #8a99ab;
    --accent: #5ec8f0; --accent2: #f0b45e; --green: #7ddc9a;
    --purple: #b48ef0; --red: #f07070;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: -apple-system, "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
    line-height: 1.75; font-size: 15px;
  }
  code, pre { font-family: "JetBrains Mono", "Cascadia Code", Consolas, monospace; }
  .wrap { display: flex; max-width: 1400px; margin: 0 auto; }

  /* 侧边栏 */
  nav {
    position: sticky; top: 0; height: 100vh; width: 220px; flex-shrink: 0;
    padding: 24px 16px; overflow-y: auto; border-right: 1px solid var(--border);
  }
  nav .brand { font-size: 17px; font-weight: 700; color: var(--accent); margin-bottom: 4px; }
  nav .ver { font-size: 12px; color: var(--dim); margin-bottom: 20px; }
  nav a {
    display: block; padding: 5px 10px; color: var(--dim); text-decoration: none;
    border-radius: 6px; font-size: 14px;
  }
  nav a:hover { background: var(--panel2); color: var(--accent); }
  nav .group { margin: 18px 0 6px; font-size: 12px; color: #5a6878; letter-spacing: 1px; }

  /* 正文 */
  main { flex: 1; padding: 40px 48px 120px; min-width: 0; }
  header h1 { font-size: 34px; margin: 0 0 8px; }
  header p { color: var(--dim); margin: 0 0 40px; }

  h2 {
    font-size: 23px; margin: 56px 0 20px; padding-bottom: 10px;
    border-bottom: 2px solid var(--border);
  }
  h2:first-of-type { margin-top: 0; }
  h3 { font-size: 18px; margin: 32px 0 10px; color: var(--accent); }
  h3 .sub { font-size: 13px; color: var(--dim); font-weight: 400; margin-left: 6px; }
  h3 .count {
    float: right; font-size: 12px; color: var(--dim); font-weight: 400;
    background: var(--panel2); padding: 2px 10px; border-radius: 10px;
  }

  p.desc { color: var(--dim); margin: 0 0 16px; }

  pre {
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 18px; overflow-x: auto; margin: 14px 0 20px; font-size: 13.5px;
    line-height: 1.7;
  }
  pre .c { color: #5a6878; }        /* 注释 */
  pre .k { color: var(--purple); }  /* 关键字 */
  pre .s { color: var(--green); }   /* 文本 */
  pre .n { color: var(--accent2); } /* 数字 */
  pre .f { color: var(--accent); }  /* 函数 */

  code {
    background: var(--panel2); padding: 1.5px 6px; border-radius: 4px;
    font-size: 13px; color: var(--accent2);
  }
  code.ex { color: var(--green); background: none; }

  table { width: 100%; border-collapse: collapse; margin: 14px 0 24px; font-size: 14px; }
  th, td { text-align: left; padding: 9px 12px; border-bottom: 1px solid var(--border); }
  th { color: var(--dim); font-weight: 500; font-size: 13px; }
  td:first-child { width: 130px; }
  td:last-child { width: 42%; }

  /* 函数卡片 */
  .fns { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 8px; }
  .fn {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 8px; padding: 9px 14px; font-size: 13.5px;
  }
  .fn:hover { border-color: var(--accent); }
  .ret { color: var(--purple); }
  .sep { color: var(--dim); }
  .name { color: var(--accent); font-weight: 600; }
  .paren { color: var(--dim); }
  .params { color: var(--green); }

  .note {
    background: rgba(94, 200, 240, .07); border-left: 3px solid var(--accent);
    padding: 12px 16px; border-radius: 0 8px 8px 0; margin: 18px 0;
    font-size: 14px; color: var(--dim);
  }
  .note b { color: var(--text); }

  @media (max-width: 900px) {
    nav { display: none; }
    main { padding: 28px 20px 80px; }
  }
</style>
</head>
<body>
<div class="wrap">

<nav>
  <div class="brand">燃梦中文语言</div>
  <div class="ver">用中文写程序</div>

  <div class="group">入门</div>
  <a href="#start">快速开始</a>
  <a href="#types">数据类型</a>
  <a href="#syntax">基础语法</a>
  <a href="#control">控制流程</a>
  <a href="#function">函数</a>
  <a href="#module">模块</a>
  <a href="#operators">运算符</a>
  <a href="#global">全局常量</a>
  <a href="#repl">交互终端</a>

  <div class="group">内置模块</div>
  {{模块导航}}
</nav>

<main>

<header>
  <h1>燃梦中文语言</h1>
  <p>一套用中文书写全部代码的编程语言，从词法分析到解释执行均由中文命名实现。</p>
</header>

<h2 id="start">快速开始</h2>

<pre><span class="k">变量</span> <span class="k">文本</span>:名字 = <span class="s">"张三"</span>
<span class="k">变量</span> <span class="k">数字</span>:年龄 = <span class="n">18</span>

<span class="f">如果</span>(年龄 >= <span class="n">18</span>) {
    <span class="f">终端输出</span>(<span class="s">"你好，"</span> + 名字 + <span class="s">"，已成年"</span>)
} <span class="k">或者</span>(<span class="k">真</span>) {
    <span class="f">终端输出</span>(<span class="s">"你好，"</span> + 名字)
}</pre>

<p>保存为 <code>.象</code> 或 <code>.模块</code> 文件后运行：</p>

<pre>./运行 我的程序.象      <span class="c"># 运行文件</span>
./运行                  <span class="c"># 不带参数进入交互终端</span>
./运行 -e '终端输出("你好")'  <span class="c"># 直接执行一段代码</span></pre>

<h2 id="types">数据类型</h2>

<table>
  <tr><th>类型</th><th>说明</th><th>示例</th></tr>
  <tr><td><code>文本</code></td><td>字符串</td><td><code>"你好"</code>、<code>'单引号'</code></td></tr>
  <tr><td><code>数字</code></td><td>整数或小数</td><td><code>42</code>、<code>3.14</code>、<code>-5</code></td></tr>
  <tr><td><code>状态</code></td><td>真或假</td><td><code>真</code>、<code>假</code></td></tr>
  <tr><td><code>数组</code></td><td>元素必须同类型</td><td><code>[1, 2, 3]</code>、<code>["甲", "乙"]</code></td></tr>
  <tr><td><code>列表</code></td><td>元素可以是任意类型</td><td><code>[1, "甲", 真]</code></td></tr>
  <tr><td><code>对象</code></td><td>键值对</td><td><code>{名称: "张三", 年龄: 18}</code></td></tr>
  <tr><td><code>任意</code></td><td>不限制类型</td><td>用于参数标注</td></tr>
  <tr><td><code>空白</code></td><td>不限制类型</td><td>用于参数标注</td></tr>
</table>

<div class="note">
  <b>数组与列表的区别：</b>声明为 <code>数组</code> 类型时，所有元素必须是同一类型，
  <code>[1, "甲"]</code> 会报错；声明为 <code>列表</code> 则允许混装。
</div>

<p>语言里的位置统一从 <b>1</b> 开始数：<code>文本[1]</code> 取第一个字符，<code>数组[1]</code> 取第一个元素。</p>

<h2 id="syntax">基础语法</h2>

<h3>定义</h3>

<pre><span class="k">变量</span> <span class="k">数字</span>:计数 = <span class="n">0</span>          <span class="c"># 可修改</span>
<span class="k">常量</span> <span class="k">数字</span>:上限 = <span class="n">100</span>         <span class="c"># 不可修改</span>
<span class="k">容量</span> <span class="k">列表</span>:结果 = []          <span class="c"># 可增长的容器</span>
<span class="k">变量</span> <span class="k">数字</span>:计数器              <span class="c"># 不写初始值，按类型给默认值（数字为 0）</span></pre>

<h3>关键字一览</h3>

<table>
  <tr><th>关键字</th><th>作用</th><th>写法</th></tr>
  {{关键字行}}
</table>

<h3>注释</h3>

<pre><span class="c"># 井号注释</span>
<span class="c">// 双斜杠注释也可以</span>
<span class="k">变量</span> <span class="k">数字</span>:甲 = <span class="n">1</span>   <span class="c">// 行尾注释</span></pre>

<h2 id="control">控制流程</h2>

<h3>如果</h3>

<pre><span class="f">如果</span>(分数 >= <span class="n">90</span>) {
    <span class="f">终端输出</span>(<span class="s">"优秀"</span>)
} <span class="k">或者</span>(分数 >= <span class="n">60</span>) {
    <span class="f">终端输出</span>(<span class="s">"及格"</span>)
}</pre>

<h3>短路语句（单行条件执行）</h3>

<p>条件成立就执行后面的动作，动作可以是 <code>返回</code>、赋值或自增：</p>

<pre><span class="k">导出</span> <span class="k">状态</span>:空白(<span class="k">数组</span>:内容) {
    长短(内容) == <span class="n">0</span> && <span class="k">返回</span> <span class="k">真</span>     <span class="c"># 为空则返回真</span>
    <span class="k">返回</span> <span class="k">假</span>
}

数值 > 结果 && 结果 = 数值        <span class="c"># 条件成立才赋值</span>
计数 < <span class="n">5</span> && 计数++              <span class="c"># 条件成立才自增</span></pre>

<h3>循环</h3>

<pre><span class="k">变量</span> <span class="k">数字</span>:序号 = <span class="n">1</span>
<span class="f">循环</span>(序号 <= <span class="n">10</span>) {
    <span class="f">终端输出</span>(序号)
    序号++
}</pre>

<h2 id="function">函数</h2>

<pre><span class="k">函数</span> <span class="k">文本</span>:问候(<span class="k">文本</span>:谁) {
    <span class="k">返回</span> <span class="s">"你好，"</span> + 谁
}

<span class="k">导出</span> <span class="k">数字</span>:求和(<span class="k">数字</span>:首个, <span class="k">数字</span>:其余...) {
    <span class="c"># 其余... 把后面的实参全部收进一个数组</span>
    <span class="k">返回</span> 首个
}</pre>

<h3>参数默认值</h3>

<pre><span class="k">导出</span> <span class="k">数字</span>:自增(<span class="k">数字</span>:数值, <span class="k">数字</span>:步长 = <span class="n">1</span>) {
    <span class="k">返回</span> 数值 + 步长
}

自增(<span class="n">5</span>)      <span class="c"># → 6，省略步长用默认值 1</span>
自增(<span class="n">5</span>, <span class="n">3</span>)   <span class="c"># → 8</span></pre>

<h3>匿名函数</h3>

<p>匿名函数只能写在参数位置，形式为 <code>(参数) { 代码 }</code>：</p>

<pre>数组.遍历([<span class="n">1</span>, <span class="n">2</span>, <span class="n">3</span>], (项, 序号) {
    <span class="f">终端输出</span>(<span class="s">"第"</span>, 序号, <span class="s">"项："</span>, 项)
})

数组.映射([<span class="n">1</span>, <span class="n">2</span>, <span class="n">3</span>], (项, 序号) {
    <span class="k">返回</span> 项 * <span class="n">10</span>
})   <span class="c"># → [10, 20, 30]</span></pre>

<h2 id="module">模块</h2>

<p>模块文件的后缀名是 <code>.模块</code>。导入时用「模块名.函数」访问，也可以起别名。</p>

<pre><span class="k">导入</span> ./模块/文本 命名 文本     <span class="c"># 起别名，用 文本.函数(...)</span>
<span class="k">导入</span> 模块/数组                <span class="c"># 不起别名，用 数组.函数(...)</span>
<span class="k">导入</span> 模块/数学 选择 最大值    <span class="c"># 只导入指定函数，可直接用 最大值(...)</span>

文本.切割(<span class="s">"测试文本一段长"</span>, <span class="n">1</span>, <span class="n">2</span>)   <span class="c"># → 测试</span></pre>

<h3>导出函数</h3>

<pre><span class="c"># 方式一：定义时直接导出</span>
<span class="k">导出</span> <span class="k">文本</span>:拼接(<span class="k">文本</span>:参数...) {
    <span class="k">返回</span> <span class="s">""</span>.join(参数)
}

<span class="c"># 方式二：选中已有函数导出</span>
<span class="k">导出</span> 拼接, 切割</pre>

<div class="note">
  <b>命名空间：</b>函数名与变量名共用同一个命名空间，同名会互相遮蔽。
  建议不要让参数名与函数名重名（例如参数叫 <code>长度</code> 会遮蔽同名函数）。
</div>

<h2 id="operators">运算符</h2>

<table>
  <tr><th>运算符</th><th>说明</th><th>示例</th></tr>
  {{运算符行}}
</table>

<h3>管道</h3>

<p><code>|</code> 把左边的值作为第一个参数传给右边的调用，可以串起来写：</p>

<pre>结果 = 内容|切割(<span class="n">1</span>, <span class="n">5</span>)|追加(<span class="s">"…"</span>)
位置 = 位置|数学.自增()</pre>

<h2 id="global">全局常量</h2>

<table>
  <tr><th>名称</th><th>值</th><th>说明</th></tr>
  <tr><td><code>操作系统</code></td><td>系统名称</td><td>如 <code>Linux</code>、<code>Windows</code></td></tr>
  <tr><td><code>正无穷大</code></td><td>大于一切数</td><td>常用于求最大值的初始值</td></tr>
  <tr><td><code>负无穷大</code></td><td>小于一切数</td><td>常用于求最小值的初始值</td></tr>
  <tr><td><code>空白文本</code></td><td><code>""</code></td><td>空字符串，作为累加初始值</td></tr>
</table>

<p>全局常量不能被重新定义或赋值：</p>

<pre>变量 数字:正无穷大 = <span class="n">1</span>
<span class="c"># → 「正无穷大」是全局常量，不能重新定义</span></pre>

<h2 id="repl">交互终端</h2>

<p>不带参数运行 <code>./运行</code> 会进入交互终端，可以逐行输入代码立即执行，变量在多次输入之间保留。</p>

<pre>燃梦> <span class="k">变量</span> <span class="k">文本</span>:名字 = <span class="s">"张三"</span>
燃梦> <span class="f">终端输出</span>(<span class="s">"你好，"</span> + 名字)
你好，张三</pre>

<table>
  <tr><th>命令</th><th>作用</th></tr>
  <tr><td><code>:帮助</code></td><td>显示可用命令</td></tr>
  <tr><td><code>:退出</code></td><td>退出终端（也可按 Ctrl+D）</td></tr>
  <tr><td><code>:清空</code></td><td>清空当前会话的变量与函数</td></tr>
  <tr><td><code>:变量</code></td><td>列出已定义的变量</td></tr>
  <tr><td><code>:函数</code></td><td>列出已定义的函数</td></tr>
  <tr><td><code>:运行 路径</code></td><td>执行一个文件</td></tr>
  <tr><td><code>:调试</code></td><td>切换词元与语法树显示</td></tr>
</table>

<h2 id="builtin">内置模块</h2>

<p>以下模块位于 <code>模块/</code> 目录，导入后即可使用。共 {{总数}} 个。</p>

{{模块内容}}

</main>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    路径 = 生成()
    print(f'已生成：{路径}')
