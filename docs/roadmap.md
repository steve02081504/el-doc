# 学习地图

> 大多数人学一门新语言，不是停在第一页，而是停在“下一步该读什么”上。这张地图负责回答这个问题。

!!! abstract "🎯 这张地图能帮你"
    - 用 3–5 分钟看清整份教程的形状与先后顺序
    - 判断自己现在在哪一站、下一站读什么
    - 知道每一站的终点长什么样，合格了就走

    <span class="el-chip">⏱ 约 5 分钟</span> <span class="el-chip">随时回来查</span>

## 全貌：五站，一条主线

教程按“先跑起来，再懂原理，最后做出东西”排列。每一站都有明确产出和自检清单，不用等学完才发现自己会不会。

<div class="el-road" markdown>
<div class="el-road__item" markdown>
<p class="el-road__num">00</p>
<div class="el-road__body" markdown>

### 起步：让第一行代码跑起来

跑通 `hello.el`，用 REPL 改几个值，再花 15 分钟把主要语法扫一遍。这一站结束，你就有一台能立刻验证想法的机器。

- 读：[安装与第一个程序](getting-started.md) → [15 分钟速览](tour.md)
- 时间：约 40 分钟
- 产出：一个能跑、能改的 `hello.el`

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">01</p>
<div class="el-road__body" markdown>

### 语言基础：写出独立的小程序

值、类型、运算符、控制流、函数。这一站只教“日常写代码真正会用到的那部分”，深水区留给下一站。

- 读：[读语言之前](language/before-you-start.md) → [值与类型](language/values.md) → [数值与位类型](language/numeric-types.md) → [运算符与表达式](language/operators.md) → [控制流](language/control-flow.md) → [函数与闭包](language/functions.md)
- 时间：约 3 小时
- 产出：能写几十行、自己调试的小脚本

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">02</p>
<div class="el-road__body" markdown>

### 语言进阶：管住对象、模块与失败

生命周期、类、内存布局、模块、shell、错误与异步、性能、外部接口。页面开始变重，阅读时把“可选 · 深入”折叠块当作加餐，跳过不影响主线。

- 读：[生命周期与析构](language/lifetimes.md) → [类与对象](language/classes.md) → [模块与包](language/modules.md) → [错误处理与异步](language/errors-async.md) → [Shell 语法](language/shell.md) → [内存布局与 GC 钩子](language/memory-layout.md) → [性能与底层优化](language/performance.md) → [外部接口与 ABI](language/foreign.md)
- 时间：约 4–5 小时
- 产出：能拆成多文件、能处理失败、能并发的项目骨架

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">03</p>
<div class="el-road__body" markdown>

### 标准库：让程序接触真实世界

输出与日志、集合与文本、文件与网络、GUI、声音、神经网络、测试。可以按项目需要跳读，遇到不知道从哪开始时先看[标准库总览](stdlib/index.md)。

- 读：[标准库总览](stdlib/index.md) → 按需挑章节
- 时间：约 3 小时（全读），20 分钟（挑两三页）
- 产出：能读写文件、发请求、开窗口、发声音

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">04</p>
<div class="el-road__body" markdown>

### 交付：把代码变成产物

构建、跨平台产物、调试与发布模式、缓存与退出码。工具链只有一页，但值得在写第一个真项目之前读完。

- 读：[工具链](toolchain.md)
- 时间：约 30 分钟
- 产出：能为别的系统构建可执行文件，并知道怎么清理构建产物

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">05</p>
<div class="el-road__body" markdown>

### 实战：把前面的东西串成项目

两个完整项目练手，四篇多范式教程换脑子。这里不再有新语法，重点是“什么时候该用哪种写法”。

- 读：[命令行工具](practice/cli-tool.md) → [图形程序](practice/gui-app.md) → [手写 JSON 解析器](practice/json-parser.md) → [规则式下棋机器人](practice/logic-game.md) → [定理证明](practice/proofs.md) → [矩阵与数值脚本](practice/numerics.md)
- 时间：每个项目 30–60 分钟
- 产出：可交付的命令行工具与图形程序

</div>
</div>
</div>

## 每一站怎么算“过了”

不要用“读完了”当进度，用“做出来了”当进度。每站结束前，试着不看教程完成下面这些事；卡住就回去补对应页面。

!!! success "自检：起步"
    - [ ] `el run hello.el` 能打印你自己写的文字
    - [ ] 用 `el repl` 算一个表达式，不用新建文件
    - [ ] 能说出 EL 和 JavaScript 的三处语法差别

!!! success "自检：语言基础"
    - [ ] 写出 FizzBuzz，用 `if` 表达式而不是提前声明结果变量
    - [ ] 用 `for (let x in ...)` 和一个闭包处理数组
    - [ ] 解释 `1 / 3 * 3` 为什么正好等于 `1`

!!! success "自检：语言进阶"
    - [ ] 把一段长代码拆成两个模块并正确导入
    - [ ] 用 `try`/`catch` 把失败变成值，而不是让程序崩掉
    - [ ] 说清一个对象在块结束时按什么顺序析构

!!! success "自检：标准库与工具链"
    - [ ] 读一个文件、统计行数、把结果写到 stdout
    - [ ] 用 `el build --release` 生成产物，并用 `el formatter --check` 检查格式
    - [ ] 用 `el test` 跑过自己写的一个测试

## 三条常见路线

地图是默认顺序，不是唯一顺序。

=== "第一次学编程"

    按 00 → 05 顺序读，每页的代码都亲手敲一遍。看到“实现状态”的标注可以跳过；看到“可选 · 深入”先跳过，等主线走完再回来。卡住时先查[常见问题](appendix/faq.md)。

=== "会别的语言，想快速上手"

    先读[15 分钟速览](tour.md)和[从其他语言过来](appendix/coming-from.md)，再挑你关心的主题跳读。最容易踩的四个坑：`async`/`await` 是宏、逻辑运算是 `&`/`|`、`^` 是乘方、类必须写 `@assign`。

=== "只想查写法"

    [语言](language/index.md)部分每页开头就是结论和最小例子；[工具链](toolchain.md)有完整命令表；[常见问题](appendix/faq.md)按主题分组。用右上角的搜索比翻目录快。

## 卡住了，先看这里

- **跑不起来。** 先看[安装与第一个程序](getting-started.md)的“常见问题”，再看[工具链](toolchain.md)的“出问题时”。
- **看得懂例子，自己写就错。** 多半是模块路径或赋值语义的问题：[模块与包](language/modules.md)、[类与对象](language/classes.md)。
- **不确定某个写法现在能不能用。** 看[规范与实现边界](appendix/implementation-status.md)，那里说明教程里三种说法的区别。
- **不知道读哪页。** 用页脚的“随便翻一页”，或者回到这张地图。

## 下一站

- [安装与第一个程序](getting-started.md)：从 00 站开始，先让程序跑起来。
- [语言总览](language/index.md)：想看整章结构时从这里进。
