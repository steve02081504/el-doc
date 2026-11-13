<div class="el-hero" markdown>
<p class="el-hero__eyebrow">EviL LANGUAGE · EL 语言参考</p>
<h1>一份源码，<br>既开窗口，也开网页。</h1>
<p class="el-hero__lead">EL 是一门面向整个应用的通用语言：脚本、原生程序、服务、标签式 GUI 与数据库查询共用一套语法、类型和运行时。同一套界面代码既能打开系统窗口，也能编译成单文件网页，双击就在浏览器里跑起来。</p>
<div class="el-hero__actions">
<a class="md-button md-button--primary" href="reference/language/">查语言参考</a>
<a class="md-button" href="getting-started/">3 分钟跑起来</a>
<a class="md-button" href="stdlib/api/">查标准库 API</a>
</div>
<div class="el-hero__code" markdown>
```el
fn greet(name: Text = "world") => "hello " + name

console.stdout.writeLine(greet())
console.info.value(@{ language: "EL" })
```
</div>
</div>

## EL 是什么味道

- **一套语言覆盖应用与平台。** 脚本、原生程序、服务、GUI 和远程模块更新使用同一份源码；原生目标覆盖 Windows、Linux、macOS、FreeBSD、iOS、Android，浏览器里则是单文件页面：wasm 模块内嵌在 HTML 中，界面仍由 EL 用 Canvas 自绘。
- **数值不将就。** 日常的 `Number` 是精确有理数：`1/3` 可以精确保存，数值变大时按需扩展表示，不会仅因超过固定机器位宽就溢出。
- **资源规则是语言的一部分。** 对象明确选择复制还是共享，构造与析构有固定时机，需要时能直接指定存储位置与借用来源。
- **Debug 护具穿满，Release 跑得快。** 两种模式共用一条优化流水线；安全检查可以关闭，但语言合同不会因此改变。

想先看它长什么样，读[15 分钟速览](tour.md)；想直接动手，去[安装与第一个程序](getting-started.md)。

## 参考目录

查阅 EL 的语法、语言合同和标准库接口。已知名字时使用搜索或符号索引；按领域浏览时从下列分类进入。

## 语言

| 基础 | 程序结构 | 执行与扩展 |
| --- | --- | --- |
| [词法与字面量](reference/language/lexical.md) | [声明与绑定](reference/language/declarations.md) | [控制流](reference/language/control-flow.md) |
| [类型](reference/language/types.md) | [函数与重载](reference/language/functions.md) | [异常与并发](reference/language/execution.md) |
| [表达式与运算符](reference/language/expressions.md) | [类与生命周期](reference/language/classes.md) | [宏与元编程](reference/language/metaprogramming.md) |
| [语言参考总览](reference/language/index.md) | [模块与导入](reference/language/modules.md) | [工具链与命令](toolchain.md) |
| [文件预处理](reference/language/preprocessing.md) | [外部接口与 ABI](reference/language/foreign.md) | [规范与实现边界](appendix/implementation-status.md) |

## 标准库

[库分类总览](stdlib/api/index.md) · [模块索引](stdlib/api/modules.md) · [符号索引](stdlib/api/symbols.md)

| 领域 | 参考 |
| --- | --- |
| 容器与函数组合 | [collections](stdlib/api/categories/collections.md) · [functions](stdlib/api/categories/functions.md) |
| 文本与格式 | [text](stdlib/api/categories/text.md) · [formats](stdlib/api/categories/formats.md) |
| 数学与数值计算 | [mathematics](stdlib/api/categories/mathematics.md) · [numerical-computing](stdlib/api/categories/numerical-computing.md) · [random](stdlib/api/categories/random.md) |
| 文件、网络与输出 | [filesystem](stdlib/api/categories/filesystem.md) · [streams](stdlib/api/categories/streams.md) · [network](stdlib/api/categories/network.md) · [console](stdlib/api/categories/console.md) |
| 时间与密码学 | [time](stdlib/api/categories/time.md) · [cryptography](stdlib/api/categories/cryptography.md) |
| 并发与错误 | [concurrency](stdlib/api/categories/concurrency.md) · [errors](stdlib/api/categories/errors.md) |
| 图形、界面与媒体 | [graphics](stdlib/api/categories/graphics.md) · [user-interface](stdlib/api/categories/user-interface.md) · [multimedia](stdlib/api/categories/multimedia.md) · [theme](stdlib/api/categories/theme.md) |
| 神经网络 | [neural-networks](stdlib/api/categories/neural-networks.md) |
| 语言扩展与工具 | [language](stdlib/api/categories/language.md) · [logic](stdlib/api/categories/logic.md) · [tools](stdlib/api/categories/tools.md) |

API 条目包含源码签名、参数、返回值、失败条件和示例，并链接到定义位置。当前索引只包含已补文档的接口；完整度以[生成页统计](stdlib/api/index.md)为准。

## 工具与状态

- [工具链](toolchain.md)：命令、项目、构建与产物。
- [规范与实现边界](appendix/implementation-status.md)：区分规范合同、源码实现与实际验收。
- [文档注释与生成](stdlib/documentation-comments.md)：维护接口说明、生成网页与结构化数据。

语言参考按规范解释合同，不表示所有合同均已完成实现；源码注释示例当前未运行验证。站点构建检查链接和排版，不能证明 EL 程序能编译或运行。

## 学习 EL

[教程与指南](tutorials/index.md)收录零基础课程、语言讲解、标准库入门和实战项目。第一次接触编程可从[第一个程序](getting-started.md)开始；有经验的读者可读[15 分钟速览](tour.md)。
