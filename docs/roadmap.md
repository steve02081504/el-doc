# 学习地图

> 大多数人学一门新语言，不是停在第一页，而是停在“下一步该读什么”上。这张地图负责回答这个问题。

!!! abstract "🎯 这张地图能帮你"
    - 用 3–5 分钟看清整份教程的形状与先后顺序
    - 判断自己现在在哪一站、下一站读什么
    - 知道每一站的终点长什么样，合格了就走

    <span class="el-chip">⏱ 约 5 分钟</span> <span class="el-chip">随时回来查</span>

## 第一次学编程：先走这条短路线

先完成[第一个程序](getting-started.md)，再按[零基础路线](beginner/index.md)学习：零花钱计算 → 预算判断 → 阅读记录 → 总价函数 → 文具采购小助手。它只要求会加减乘除，不要求先读类型、内存或异步章节。

一次学一小节即可，不用赶页面上的时间估算。每次先照例子运行，再改一项，最后尝试独立完成页尾任务。下次开始时，先试着不看答案写出上次的一小段；忘了就回看。

完成的标志是：能给自己的采购计划算总价，而且能检查预算够、不够、刚好的情况。访问完页面和抄完代码都不能代替这个检查。

## 完整章节：按需要继续

教程按“先跑起来，再懂原理，最后做出东西”排列。每一站都有明确产出和自检清单，不用等学完才发现自己会不会。

<div class="el-road" markdown>
<div class="el-road__item" markdown>
<p class="el-road__num">00</p>
<div class="el-road__body" markdown>

### 起步：让第一行代码跑起来

跑通 `hello.el`。第一次编程的读者接着走零基础路线；已经会编程的读者可以看速览。

- 读：[第一个程序](getting-started.md) → [零基础路线](beginner/index.md)；有经验时改走[速览](tour.md)
- 时间：按每节的检查点推进，可以分多次完成
- 产出：一个能跑、能改的 `hello.el`

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">01</p>
<div class="el-road__body" markdown>

### 语言基础：写出独立的小程序

值、类型、运算符、控制流、函数。这些是更完整的规则说明；做完零基础项目后可按问题查阅，定宽数值等专题留到实际需要时读。

- 读：[读语言之前](language/before-you-start.md) → [值与类型](language/values.md) → [数值与位类型](language/numeric-types.md) → [运算符与表达式](language/operators.md) → [控制流](language/control-flow.md) → [函数与闭包](language/functions.md)
- 时间：约 3 小时
- 产出：能写几十行、自己调试的小脚本

</div>
</div>
<div class="el-road__item" markdown>
<p class="el-road__num">02</p>
<div class="el-road__body" markdown>

### 语言进阶：管住对象、模块与失败

生命周期、类、内存布局、模块、文件预处理、shell、错误与异步、性能、外部接口。页面开始变重，阅读时把“可选 · 深入”折叠块当作加餐，跳过不影响主线。

- 读：[生命周期与析构](language/lifetimes.md) → [类与对象](language/classes.md) → [模块与包](language/modules.md) → [文件预处理](language/preprocessing.md) → [Shell 语法](language/shell.md) → [错误处理与异步](language/errors-async.md) → [内存布局与 GC 钩子](language/memory-layout.md) → [性能与底层优化](language/performance.md) → [外部接口与 ABI](language/foreign.md)
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
    - [ ] 改一条提醒，保存后重新运行，看到新文字
    - [ ] 能区分终端命令、EL 代码和输出

!!! success "自检：语言基础"
    - [ ] 为采购清单计算合计，增添一项后结果仍然正确
    - [ ] 检查预算够、不够、刚好三种情况
    - [ ] 解释 `1 / 3 * 3` 为什么正好等于 `1`

!!! success "自检：语言进阶"
    - [ ] 把一段长代码拆成两个模块并正确导入
    - [ ] 用 `#if` 给不同构建选一段代码，并说清 `#include` 与 `import` 的区别
    - [ ] 用 `try`/`catch` 把失败变成值，而不是让程序崩掉
    - [ ] 说清一个对象在块结束时按什么顺序析构

!!! success "自检：标准库与工具链"
    - [ ] 读一个文件、统计行数、把结果写到 stdout
    - [ ] 用 `el build --release` 生成产物，并用 `el formatter --check` 检查格式
    - [ ] 用 `el test` 跑过自己写的一个测试

## 三条常见路线

地图是默认顺序，不是唯一顺序。

=== "第一次学编程"

    先走[第一个程序](getting-started.md) → [零基础路线](beginner/index.md)。完成采购项目后，按实际问题选后续章节；不要求从 00 一直读到 05 才能写程序。

=== "会别的语言，想快速上手"

    先读[15 分钟速览](tour.md)和[从其他语言过来](appendix/coming-from.md)，再挑你关心的主题跳读。最容易踩的四个坑：`async`/`await` 是宏、逻辑运算是 `&`/`|`、`^` 是乘方、类必须写 `@assign`。

=== "只想查写法"

    [语言](language/index.md)部分每页开头就是结论和最小例子；[工具链](toolchain.md)有完整命令表；[常见问题](appendix/faq.md)按主题分组。用右上角的搜索比翻目录快。

## 卡住了，先看这里

- **跑不起来。** 先看[安装与第一个程序](getting-started.md)的“卡住时，按现象检查”，再看[工具链](toolchain.md)的“出问题时”。
- **看得懂例子，自己写就错。** 先记录期望结果和实际结果，逐步打印数据，看最早在哪一步不同；参考[采购项目排查](beginner/shopping.md)。涉及导入或对象时再查[模块与包](language/modules.md)、[类与对象](language/classes.md)。
- **不确定某个写法现在能不能用。** 看[规范与实现边界](appendix/implementation-status.md)，那里说明教程里三种说法的区别。
- **不知道读哪页。** 零基础回到[短路线](beginner/index.md)找自己的下一步；已有经验时可用搜索或页脚的“随便翻一页”。

## 下一站

- [安装与第一个程序](getting-started.md)：从 00 站开始，先让程序跑起来。
- [语言总览](language/index.md)：想看整章结构时从这里进。
