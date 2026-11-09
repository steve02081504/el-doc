<div class="el-hero" markdown>
<p class="el-hero__eyebrow">EviL LANGUAGE · EL 教学文档</p>
<h1>一份源码，既开窗口，也开网页。</h1>
<p class="el-hero__lead">EL 是一门面向整个应用的通用语言：脚本、原生程序、服务、标签式 GUI 与数据库查询共用一套语法、类型和运行时。同一套界面代码既能打开系统窗口，也能编译成单文件网页，双击就在浏览器里跑起来。这份教程从第一行输出开始，带你走到能独立写出程序。</p>
<div class="el-hero__actions">
<a class="md-button md-button--primary" href="getting-started/">从第一个程序开始</a>
<a class="md-button" href="tour/">15 分钟速览</a>
</div>
<div class="el-hero__code" markdown>
```el
fn greet(name: Text = "world") => "hello " + name

console.stdout.writeLine(greet())
console.info.value(@{ language: "EL" })
```
</div>
</div>

<div class="el-status" markdown>
<strong>文档状态</strong>
<div>EL 仍在开发中。规范描述的是目标合同，部分能力还没走完实现与验收；本教程会在对应位置用「实现状态」注明。代码示例按当前语言规范编写，不保证每个都能在现有发行版上直接运行。</div>
</div>

## 为什么是 EL

多数项目最终会变成几种语言加一层胶水：界面一种、服务一种、查询一种、底层又一种。数据在边界上被搬来搬去，类型和错误处理各写一遍。EL 想做的是让这些部分共享同一套语言设施。

- **一套语言覆盖应用与平台。** 脚本、原生程序、服务、GUI 和远程模块更新使用同一份源码；同一份 GUI 既开原生窗口，也出网页。原生目标覆盖 Windows、Linux、macOS、FreeBSD、iOS、Android，浏览器里则是单文件页面：wasm 模块内嵌在 HTML 中，界面仍由 EL 用 Canvas 自绘。
- **把工具该做的事交给工具。** 查询规划、编译优化、类型推断由编译器承担，代码里少写重复的样板。
- **数值不将就。** 日常的 `Number` 是精确有理数：`1/3` 可以精确保存，数值变大时按需扩展表示，不会仅因超过固定机器位宽就溢出。
- **资源规则是语言的一部分。** 对象明确选择复制还是共享，构造与析构有固定时机，需要时能直接指定存储位置与借用来源。
- **Debug 护具穿满，Release 跑得很快。** 两种模式共用一条优化流水线；安全检查可以关闭，但语言合同不会因此改变。

想先看它长什么样，读[语言速览](tour.md)；想直接动手，去[安装与第一个程序](getting-started.md)。

## 学习路径

<div class="el-grid" markdown>
<div class="el-card" markdown>
### 语言核心
[读语言之前](language/before-you-start.md)、[值](language/values.md)、[数值与位类型](language/numeric-types.md)、[运算符](language/operators.md)、[控制流](language/control-flow.md)、[函数](language/functions.md)、[生命周期与析构](language/lifetimes.md)、[类](language/classes.md)、[内存布局与 GC 钩子](language/memory-layout.md)、[模块](language/modules.md)、[Shell 语法](language/shell.md)、[错误与异步](language/errors-async.md)、[性能与底层优化](language/performance.md)、[外部接口与 ABI](language/foreign.md)。

从变量和表达式写到能拆模块、处理失败、并发执行；再往深处走到对象生命周期、自定义布局、shell 脚本、性能手段与原生 ABI。
</div>
<div class="el-card" markdown>
### 标准库
[Console](stdlib/console.md)、[集合与文本](stdlib/collections.md)、[文件与网络](stdlib/files-network.md)、[GUI](stdlib/gui.md)、[声音与音频](stdlib/audio.md)、[神经网络](stdlib/neural-networks.md)、[测试](stdlib/testing.md)。

学会用标准库输出、处理数据、读写外部世界，发出声音、训练小模型，并给代码补上测试。
</div>
<div class="el-card" markdown>
### 工具链
[安装](getting-started.md)、[`el` 与 `elc`](toolchain.md)、运行、构建、格式化、缓存。

把单文件脚本变成可交付的原生产物。
</div>
<div class="el-card" markdown>
### 动手
[命令行工具](practice/cli-tool.md)、[图形程序](practice/gui-app.md)、[从其他语言过来](appendix/coming-from.md)、[常见问题](appendix/faq.md)。

用两个完整项目把前面的知识串起来，再看[手写解析器](practice/json-parser.md)、[规则式机器人](practice/logic-game.md)、[定理证明](practice/proofs.md)与[矩阵脚本](practice/numerics.md)这四种不同写法。
</div>
</div>

## 怎么读

**有别的语言经验。** 先读[语言速览](tour.md)和[从其他语言过来](appendix/coming-from.md)，再按需要跳到具体章节。EL 的写法接近 JavaScript 与 C 的混合体，但语义上有几处关键差异：`async {}` 与 `await(p)` 是标准库宏而不是关键字、逻辑运算不是 `&&`/`||`、`^` 是乘方而不是异或、类必须声明复制还是共享。

**第一次学编程。** 按左侧导航从上往下读，每章的代码都自己敲一遍。先只关注能运行的部分，标了「实现状态」的能力可以等需要时再回来看。

**只想查写法。** [语言](language/values.md)部分按主题拆分，每页开头就是结论和最小例子；[工具链](toolchain.md)有完整的命令速查。

## 这份文档怎么来的

本教程按 EL 仓库里的语言规范、标准库源码和示例编写，尽量只教已经定下来的写法；规范与示例冲突时以规范为准。

发现错误或想补内容，欢迎在[仓库](https://github.com/steve02081504/el-doc)提 issue 或 PR。

## 继续阅读

- [安装与第一个程序](getting-started.md)
- [语言速览](tour.md)
- [规范与实现边界](appendix/implementation-status.md)
