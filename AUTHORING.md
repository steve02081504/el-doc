# 写作须知

本文件给参与编写本教程的人或 agent 看，不进入网站导航。

## 目标

写一份面向**新使用者**的 EL 教学文档，按 GitHub Pages 静态站点发布。读者假设已经能下载到 `el`、`elc` 等发行内容，不需要在文档里解释怎么获得它们。

教程要让人能独立写出小程序，而不是复述规范。规范负责准确，教程负责可读、可跟做。

## 事实来源与优先级

1. EL 仓库 `docs/spec/` 下的规范。`02-lexical-and-syntax.md` 与 `12-syntax.md` 管写法，`03` 到 `11` 及专题规范管语义。
2. `src/stdlib/` 下的真实源码。公开模块路径、函数名、参数、返回类型以源码导出为准。
3. `examples/` 下的示例。示例可能滞后于规范，只当参考，不当权威。
4. `README.md`。它是项目门面，可能滞后于规范，例子不能直接照抄。

冲突时按上面的顺序取舍，并在给 Lead 的简报里说明冲突位置。

**不要发明 API。** 不确定某个方法、字段、模块路径是否存在时，先用 `grep`/`glob` 查源码；查不到就不写进代码示例，改为文字说明；文字也拿不准就列进简报，不要猜。本教程不依赖运行验证，所以每个示例都要按规范逐行核对。

已确认的语言事实：

- `async { ... }` 与 `await(p)` 是标准库宏，不是关键字；`async` 立即启动任务并返回 Promise，`await` 生成一次 `.get()`，普通调用仍自动等待。`spawn` 启动并发任务并返回 Promise，`.get()` 等待结果。
- 没有 `main`；模块顶层代码就是入口。
- 没有 `import * as m`、没有副作用导入；全量导入写 `import /.*/ from "..."`，命名空间写 `import /.*/ as m from "..."`，具名写 `import { a, b as c } from "..."`。
- `&&`、`||`、`**`、三目 `?:` 不是 EL 语法；逻辑运算是 `!`、`&`、`|`，乘方是 `^`。
- `let`、`const`、`fn`、`class`、`import`/`export`、`if`/`while`/`for`/`switch` 等写法见规范 12。
- 矩阵字面量 `@(1, 2; 3, 4)`，数组 `@[1, 2]`，对象 `@{ name: "x" }`。
- 类声明必须写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`；`@destruct` 可选，默认 aggressive。
- 文字输出用 `console.stdout.write(...values)`（不换行）与 `console.stdout.writeLine(...values)`（追加 LF）；`console.stdout.writeText(text)` 和 `console.stdout.writeBytes(bytes)` 是显式的文本／字节入口。
- `console.log`、`console.info`、`console.warning`、`console.error`、`console.fatal`、`console.debug`、`console.trace` 是普通可调用对象，同时提供 `.value(value, channel?)`。直接调用发本地化消息（`console.info("task.done", @{count: 3})`），`.value` 发该等级的结构化展示记录。
- 等级调用与同等级 `.value` 默认走 stderr；要写 stdout 数据用 `console.stdout.write`，或给 `.value` 明确传 `stdoutChannel`。`fatal` 只是等级，不自动终止进程。

代码示例统一风格：

```el
console.stdout.writeLine("count: ", 3)
console.info("task.done", @{count: 3})
console.info.value(@{count: 3})
console.error.value(error)
```

## 文章风格

- 中文正文；标识符、关键字、API 名、命令、路径、诊断原文保留英文。
- **一段话一行**，不按列宽折行。标题、表格、代码块不受限制。
- 中文用全角标点；中英文之间留一个半角空格；中文标点前后不加空格。
- 直接、技术化、少修辞。不写“本轮/此前/调研过程/已作废”这类过程叙述，也不写空泛的“众所周知”。
- 术语沿用 EL 中文文档的现成译法：contract=合同、borrow=借用、owner=所有者、lowering=降级、runtime=运行期/运行时、lifetime=生命周期、trap=陷阱、cleanup=清理、pipeline=流水线。
- 面向读者解释“为什么”，不要只罗列规则。每节至少有一个能独立运行的小例子或可观察结果。
- 不确定或尚未实现的能力，用 `!!! note "实现状态"` 说明，不要假装已经可用。
- 需要出处时写“语言规范第 N 章”这样的文字，不引用外部仓库链接。
- 页面之间用相对链接，例如 `[控制流](control-flow.md)`、`[Console](../stdlib/console.md)`。

## 页面模板

```markdown
# 页面标题

一句话说明这一页解决什么问题，读者读完能做什么。

## 小节

正文。

```el
// 可运行或可独立理解的例子
```

!!! tip "给有别的语言经验的读者"
    对照说明，可选。

## 继续阅读

- [下一页](next.md)
```

## 站点约定

- MkDocs Material；`el` 代码块有自定义高亮，`eol` 用于项目文件与数据字面量，`repl` 用于 `el repl` 会话记录（`>` 起头的行按 EL 高亮，其余按输出显示）。
- 可用 `!!! note`、`!!! tip`、`!!! warning`、`!!! danger`、`!!! example` 等 admonition。
- 可用 `=== "标签"` 做 tab（pymdownx.tabbed），少用。
- 不加外链图片、不引外部脚本；自包含。
- 页尾「随便翻一页」按钮由 `hooks/random_pages.py` 生成页面清单、`docs/assets/random-page.js` 渲染；新增页面只要进导航，就会自动进入随机池。
- 每页 H1 只出现一次，且与导航名一致或接近。
- 内部链接用相对路径，确保 `mkdocs build --strict` 通过。

## 分工与写作用途

每位写作者只改自己名下的文件，不碰 `mkdocs.yml`、`docs/index.md`、`docs/stylesheets/`、`hooks/`、`.github/` 和别人的页面。

文件写完后给 Lead 发消息，内容包括：完成文件列表、每页大致字数、你核对过的规范章节、仍不确定的事实（带路径和行号）、以及有意留空的实现状态说明。
