# 语言总览

> 语言部分有 14 页。但真正决定你能不能写出程序的，只有前 6 页。

!!! abstract "🎯 这一章能帮你"
    - 知道 14 页里哪些必须按顺序读、哪些可以跳
    - 用一句话说出每页解决什么问题
    - 在“读不下去”或“想查写法”时快速找到出口

    <span class="el-chip">⏱ 约 5 分钟</span> <span class="el-chip">前置：[15 分钟速览](../tour.md)</span>

## 两段路

语言部分刻意分成两段。**地基**是每天都会用到的部分，读完就能写小程序；**进阶**处理对象的生死、模块边界、失败与并发，读不完也能写出能用的程序。

### 第一段：地基（必读）

<div class="el-grid" markdown>
<div class="el-card" markdown>
<span class="el-card__num">01</span>
### [读语言之前](before-you-start.md)
先看一眼“能跑但可能是未定义行为”的代码。它决定你在 EL 里怎么判断对错。
<span class="el-card__meta">5 分钟 · 无前置</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">02</span>
### [值与类型](values.md)
`Number` 是精确有理数，`Text` 按 Unicode 标量计数，`t`/`nil`/`void` 是三种不同的“空”。
<span class="el-card__meta">12 分钟 · 前置：01</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">03</span>
### [数值与位类型](numeric-types.md)
需要定宽、无界、浮点或位集合时，用标准库里对应的数值类型，而不是硬凑 `Number`。
<span class="el-card__meta">10 分钟 · 前置：02</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">04</span>
### [运算符与表达式](operators.md)
`&`/`|`、`^` 是乘方、`??` 是空值合并。运算符是 EL 和别的语言差别最集中的地方。
<span class="el-card__meta">12 分钟 · 前置：02</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">05</span>
### [控制流](control-flow.md)
`if`、`try`、块都能产生值；控制流写成表达式后，很多样板代码会消失。
<span class="el-card__meta">12 分钟 · 前置：02、04</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">06</span>
### [函数与闭包](functions.md)
`fn`、箭头 lambda、闭包捕获、定向返回。读完就能把代码组织成可复用的块。
<span class="el-card__meta">15 分钟 · 前置：05</span>
</div>
</div>

### 第二段：进阶（按需读）

<div class="el-grid" markdown>
<div class="el-card" markdown>
<span class="el-card__num">07</span>
### [生命周期与析构](lifetimes.md)
对象什么时候复制、什么时候共享、什么时候析构。资源规则是语言合同的一部分。
<span class="el-card__meta">15 分钟</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">08</span>
### [类与对象](classes.md)
`@assign`、`constructor`、私有成员、继承与运算符重载。需要行为时用它，不要用对象字面量硬撑。
<span class="el-card__meta">15 分钟</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">09</span>
### [内存布局与 GC 钩子](memory-layout.md)
需要控制存储位置、对齐或自定义清理时才读。写业务代码可以跳过。
<span class="el-card__meta">12 分钟 · 偏底层</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">10</span>
### [模块与包](modules.md)
导入映射、`index.el`、项目文件。代码超过一个文件之前先读这一页。
<span class="el-card__meta">12 分钟</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">11</span>
### [Shell 语法](shell.md)
把 EL 当脚本语言用：直接执行命令、管道、退出码。写自动化时很省事。
<span class="el-card__meta">12 分钟</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">12</span>
### [错误处理与异步](errors-async.md)
`throw`/`try` 是表达式，`spawn`/`.get()` 管并发，`async`/`await` 是宏。这是最容易和别的语言搞混的一页。
<span class="el-card__meta">18 分钟 · 重点</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">13</span>
### [性能与底层优化](performance.md)
先测量再优化。介绍布局控制、内联、边界检查与 release 模式的真实差别。
<span class="el-card__meta">15 分钟 · 偏底层</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">14</span>
### [外部接口与 ABI](foreign.md)
调用 C、导出入口、回调与指针。只有要接原生库时才需要。
<span class="el-card__meta">18 分钟 · 偏底层</span>
</div>
</div>

## 怎么读这一章

- **第一次学 EL。** 从 01 读到 06，中途不要跳。每页的“动手”都做一遍，比读三遍有用。
- **只想先能写东西。** 读 01、02、05、06，然后去[实战](../practice/cli-tool.md)。遇到问题再回来补。
- **查写法。** 每页开头就是结论和最小例子，右上角目录可以直接跳小节。
- **读不下去时。** 每页都有“带走这三样”，先看那个；细节折在“可选 · 深入”里，不影响后续阅读。

!!! tip "一句话的取舍"
    语言部分不是用来背的。==遇到不确定的语义，先写五行代码验证，再回来查规范==。教程给的是地图，不是法典。

## 下一站

- 按顺序读：[读语言之前](before-you-start.md)：先建立“什么算正确”的直觉。
- 换条路走：[标准库总览](../stdlib/index.md)：先看能调什么，再回来补语法。
