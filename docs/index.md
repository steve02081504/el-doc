<div class="el-hero" markdown>
<p class="el-hero__eyebrow">EviL LANGUAGE · EL 教学文档</p>
<h1>从一笔零花钱，<br>开始写自己的程序。</h1>
<p class="el-hero__lead">不需要先懂编程。先让电脑算出买文具还剩多少钱，再一步步做出采购小助手。每一步都有完整例子、预期结果和可以自己检查的小任务。</p>
<div class="el-hero__actions">
<a class="md-button md-button--primary" href="getting-started/">写第一个程序</a>
<a class="md-button" href="roadmap/">先看学习地图</a>
<a class="md-button" href="stdlib/api/">查标准库 API</a>
</div>
<div class="el-hero__code" markdown>
```el
let budget = 20
let cost = 4 * 3
console.stdout.writeLine("余额：", budget - cost, " 元")
```
</div>
</div>

<div class="el-progress" data-el-progress hidden>
<div class="el-progress__head">
<p class="el-progress__count"><span data-el-progress-count>0</span><small data-el-progress-total> / 0 页</small></p>
<p class="el-progress__label">读过的页面会记在这台设备上</p>
</div>
<div class="el-progress__track"><div class="el-progress__fill" data-el-progress-fill></div></div>
<p class="el-progress__resume" data-el-progress-resume hidden></p>
<button class="el-progress__reset" type="button" data-el-progress-reset>清空本机进度</button>
</div>

## 第一次写代码，从这里走

上面的程序会显示 `余额：8 元`。看不懂英文也没关系，[第一个程序](getting-started.md)会从保存文件、打开终端开始；[零基础路线](beginner/index.md)再带你逐步读懂、修改和独立写程序。

==先做成一件小事，再学它背后的规则。== 每次只改一处，先预测结果，再运行检查。页面访问记录只代表来过，不代表已经学会。

## EL 能用来做什么

- **从计算脚本到应用。** EL 是仍在开发中的通用语言，目标包括原生程序、服务和图形界面。浏览器与各平台的实际可用范围请看[规范与实现边界](appendix/implementation-status.md)，不要把设计目标当作已经验证的能力。
- **数值不将就。** 日常的 `Number` 是精确有理数：`1/3` 可以精确保存，数值变大时按需扩展表示，不会仅因超过固定机器位宽就溢出。
- **资源规则是语言的一部分。** 对象明确选择复制还是共享，构造与析构有固定时机，需要时能直接指定存储位置与借用来源。
- **构建模式有明确边界。** Debug 与 Release 共用一条优化流水线，部分标准库安全检查随模式选择，语言合同保持一致。

想先看它长什么样，读[15 分钟速览](tour.md)；想直接动手，去[安装与第一个程序](getting-started.md)。

## 做完第一个作品之后

零基础先走[采购小助手路线](beginner/index.md)。下面是更完整的章节地图，适合做完第一个作品后按需查阅；无需先读完才能动手。

<div class="el-grid" markdown>
<div class="el-card" markdown>
<span class="el-card__num">00</span>
### [起步](getting-started.md)
让第一行代码跑起来，再沿零基础路线完成采购小助手。
<span class="el-card__meta">分小节练习 · 可以随时停下</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">01</span>
### [语言基础](language/index.md)
值、类型、运算符、控制流、函数——日常写代码真正会用到的部分。
<span class="el-card__meta">约 3 小时 · 6 页</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">02</span>
### [语言进阶](language/lifetimes.md)
生命周期、类、模块、预处理、错误与异步。深水区可以跳过。
<span class="el-card__meta">约 4–5 小时 · 9 页</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">03</span>
### [标准库](stdlib/index.md)
输出、集合、文件与网络、GUI、声音、神经网络、测试。
<span class="el-card__meta">约 3 小时 · 7 页</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">04</span>
### [交付与实战](practice/cli-tool.md)
构建产物，再用两个完整项目把前面的知识串起来。
<span class="el-card__meta">约 30 分钟 + 每个项目 30–60 分钟</span>
</div>
<div class="el-card" markdown>
<span class="el-card__num">05</span>
### [多范式](practice/json-parser.md)
手写解析器、规则式机器人、定理证明、矩阵脚本。
<span class="el-card__meta">换脑子用的 · 4 页</span>
</div>
</div>

## 三条常见路线

=== "第一次学编程"

    从[第一个程序](getting-started.md)开始，再走[零基础路线](beginner/index.md)。先运行例子，再改一处，最后收起例子独立做。速览、内存、异步和底层章节留到需要时查。

=== "会别的语言，想快速上手"

    先读[15 分钟速览](tour.md)和[从其他语言过来](appendix/coming-from.md)，再按需要跳到具体章节。EL 的写法接近 JavaScript 与 C 的混合体，但有四处关键差异：`async {}` 与 `await(p)` 是标准库宏而不是关键字、逻辑运算不是 `&&`/`||`、`^` 是乘方而不是异或、类必须声明复制还是共享。

=== "只想查写法"

    [语言总览](language/index.md)按主题拆分，每页开头就是结论和最小例子；[标准库 API 参考](stdlib/api/index.md)可查函数签名、参数、异常与示例；[工具链](toolchain.md)有完整的命令速查；[常见问题](appendix/faq.md)按主题分组。用右上角的搜索比翻目录快。

<div class="el-status" markdown>
<strong>文档状态</strong>
<div>EL 仍在开发中。规范描述的是目标合同，部分能力还没走完实现与验收；本教程会在对应位置用「实现状态」注明。代码示例按当前语言规范编写，不保证每个都能在现有发行版上直接运行。</div>
</div>

## 这份文档怎么来的

本教程按 EL 仓库里的语言规范、标准库源码和示例编写，尽量只教已经定下来的写法；规范与示例冲突时以规范为准。三种“能不能用”的说法见[规范与实现边界](appendix/implementation-status.md)。

发现错误或想补内容，欢迎在[仓库](https://github.com/steve02081504/el-doc)提 issue 或 PR。

## 选择起点

- [第一个程序](getting-started.md)：从保存文件和运行命令开始。
- [零基础路线](beginner/index.md)：用生活里的小任务学写程序。
- [15 分钟速览](tour.md)：想先看看这门语言长什么样。
- [学习地图](roadmap.md)：想知道整份教程有多少、要花多久。
