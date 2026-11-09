<div class="el-hero" markdown>
<p class="el-hero__eyebrow">EviL LANGUAGE · EL 教学文档</p>
<h1>一份源码，<br>既开窗口，也开网页。</h1>
<p class="el-hero__lead">EL 是一门面向整个应用的通用语言：脚本、原生程序、服务、标签式 GUI 与数据库查询共用一套语法、类型和运行时。同一套界面代码既能打开系统窗口，也能编译成单文件网页，双击就在浏览器里跑起来。</p>
<div class="el-hero__actions">
<a class="md-button md-button--primary" href="getting-started/">3 分钟跑起来</a>
<a class="md-button" href="roadmap/">先看学习地图</a>
</div>
<div class="el-hero__code" markdown>
```el
fn greet(name: Text = "world") => "hello " + name

console.stdout.writeLine(greet())
console.info.value(@{ language: "EL" })
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

## EL 是什么味道

- **一套语言覆盖应用与平台。** 脚本、原生程序、服务、GUI 和远程模块更新使用同一份源码；原生目标覆盖 Windows、Linux、macOS、FreeBSD、iOS、Android，浏览器里则是单文件页面：wasm 模块内嵌在 HTML 中，界面仍由 EL 用 Canvas 自绘。
- **数值不将就。** 日常的 `Number` 是精确有理数：`1/3` 可以精确保存，数值变大时按需扩展表示，不会仅因超过固定机器位宽就溢出。
- **资源规则是语言的一部分。** 对象明确选择复制还是共享，构造与析构有固定时机，需要时能直接指定存储位置与借用来源。
- **Debug 护具穿满，Release 跑得快。** 两种模式共用一条优化流水线；安全检查可以关闭，但语言合同不会因此改变。

想先看它长什么样，读[15 分钟速览](tour.md)；想直接动手，去[安装与第一个程序](getting-started.md)。

## 学习地图：五站，一条主线

每一站都有明确的产出和自检清单，读完就走，卡住再回来。完整路线与时间估算见[学习地图](roadmap.md)。

<div class="el-grid" markdown>
<div class="el-card" markdown>
<span class="el-card__num">00</span>
### [起步](getting-started.md)
让第一行代码跑起来，用 REPL 改几个值。
<span class="el-card__meta">约 40 分钟 · 2 页</span>
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
生命周期、类、模块、错误与异步。深水区可以跳过。
<span class="el-card__meta">约 4–5 小时 · 8 页</span>
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

    按[学习地图](roadmap.md)从上往下读，每页的代码都自己敲一遍。看到“实现状态”的标注可以先跳过；看到“可选 · 深入”先跳过，等主线走完再回来。卡住时先查[常见问题](appendix/faq.md)。

=== "会别的语言，想快速上手"

    先读[15 分钟速览](tour.md)和[从其他语言过来](appendix/coming-from.md)，再按需要跳到具体章节。EL 的写法接近 JavaScript 与 C 的混合体，但有四处关键差异：`async {}` 与 `await(p)` 是标准库宏而不是关键字、逻辑运算不是 `&&`/`||`、`^` 是乘方而不是异或、类必须声明复制还是共享。

=== "只想查写法"

    [语言总览](language/index.md)按主题拆分，每页开头就是结论和最小例子；[工具链](toolchain.md)有完整的命令速查；[常见问题](appendix/faq.md)按主题分组。用右上角的搜索比翻目录快。

<div class="el-status" markdown>
<strong>文档状态</strong>
<div>EL 仍在开发中。规范描述的是目标合同，部分能力还没走完实现与验收；本教程会在对应位置用「实现状态」注明。代码示例按当前语言规范编写，不保证每个都能在现有发行版上直接运行。</div>
</div>

## 这份文档怎么来的

本教程按 EL 仓库里的语言规范、标准库源码和示例编写，尽量只教已经定下来的写法；规范与示例冲突时以规范为准。三种“能不能用”的说法见[规范与实现边界](appendix/implementation-status.md)。

发现错误或想补内容，欢迎在[仓库](https://github.com/steve02081504/el-doc)提 issue 或 PR。

## 开始的三扇门

- [3 分钟跑起来](getting-started.md)：不确定从哪开始时选这个。
- [15 分钟速览](tour.md)：想先看看这门语言长什么样。
- [学习地图](roadmap.md)：想知道整份教程有多少、要花多久。
