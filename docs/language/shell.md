# Shell 语法

这一页讲 EL 的 shell 前端：怎么用 `.esh` 写批处理脚本、怎么在 `.el` 里用 `shell { ... }` 调用外部程序，以及命令、参数、管道和结果状态的实际写法。读完你能独立写出把外部命令和 EL 值接在一起的小脚本。

本页涉及外部命令的示例统一用 `git`：运行这些示例前，需要当前目录在 git 仓库中、`PATH` 上有 `git`；换成你环境里存在的程序时规则相同。

## 两种入口与两个语法域

EL 的 shell 是标准库的一部分，入口有两个名字：`esh` 与 `el shell`。`esh file.esh` 和 `el shell file.esh` 走同一套宿主、编译器和运行时，不维护第二套执行语义。

- `.esh` 文件顶层直接是 shell 语法域，不需要再包一层 `shell { ... }`；文件开头的 `import`（含 `lazy import`）与 `@module`、`@runtime` 声明仍是普通 EL，其余顶层内容进入 shell 块。
- `.el`、`.els` 和 `el repl` 是普通 EL 语法域。要在 `.el` 里写 shell，导入 `shell` 宏后用 `shell { ... }` 块。
- 普通 `fn` 的函数体在两个入口里都仍然是 EL；函数体里需要外部命令时，写显式的 `shell { ... }` 块。

`shell { ... }` 是普通库宏，不是关键字：只有导入后才可用。`.esh` 的包装由入口生成，脚本里不需要自己导入 `shell` 宏；完整例子见文末。

## 命令、参数与外部程序

命令头先查词法绑定：有同名变量、函数或导入就用该绑定，裸变量直接求值，不会启动同名程序；只有没有绑定的完整命令形状才建立外部程序引用。绑定存在时缺参、类型错误都是 EL 错误，不会失败后再去查 `PATH`。

`&` 是命令头的显式外部调用前缀，`&(expr)` 先求值得到一个路径或程序引用：

```sh
git status --short
& git status --short
& "./tool with spaces" --help
```

它和 EL 的二元 `&` 不冲突：`&` 只在 shell 命令头出现时才表示外部程序，普通表达式里的 `a & b` 仍是逻辑与；`&` 也不表示后台执行。

同名绑定存在时，普通写法用绑定，`&` 强制找外部程序：

```sh
let git = @{ name: "bound" }

git.name
& git status
```

shell 域里的 `f a b` 是一次 `f(a, b)`，不是普通 EL 的空格应用；完整 EL 调用 `f(a, b)` 仍然合法，复杂算式用完整括号调用。原生调用（被绑定的 EL 函数）还支持 shell 风格的具名参数：`-name value`、`-name:value`，`--` 终止参数标记解析。

| 写法 | 解释 |
| --- | --- |
| `f -count 3`、`f -force` | 具名参数；`-force` 只在形参声明为 `Switch` 时无值 |
| `a - b`、`a-b` | EL 减法 |
| `a -b` | 具名参数表面；不可调用时也不会回退成减法 |
| `f -1` | 参数列表尚未打开，是减法；要传负数写 `f(-1)` |
| `f -count -1`、`f x -1` | 参数列表已打开，`-1` 是参数值 |

`Switch` 是普通库类型，`-flag` 表示开启、不带值；需要显式值写 `-flag:Switch.off`。参数按源码顺序各求值一次，具名槽先占位，位置参数再按声明顺序填剩下的槽位。

外部程序的参数是另一套规则：不做分词、通配符展开、反引号执行或插值后的二次解析，未引用的词逐字作为 argv 项。

## 引号、变量与插值

shell 域里的引号就是 EL 字符串字面量，单引号双引号等价，转义规则与普通 EL 相同；`#` 在行首或空白之后起注释。

- 未引用的词是字面 argv 项，不是变量引用。
- `"..."` 或 `'...'` 包住整个词时，按 EL 字符串求值，一个字符串是一整项。
- `${expr}` 是 EL 表达式洞，求值后作为**一项** argv 插入。
- `...${expr}` 在独占词位时展开一个 `Text` 序列为多项参数。
- 洞和引号不能与字面文本拼成一项：写 `& git log "--grep=fix"`，不要写 `--grep="fix"`。
- argv 项必须是 `Text`；数字等值先显式转换，例如 `${Text(limit)}`。

```sh
let author = "Ada Lovelace"

& git log ${"--author=" + author} --oneline -n 3
```

```sh
let flags: Text[] = @["--oneline", "-n", "3"]

& git log ...${flags}
```

普通 EL 语句在 shell 块里照常写：`let`、`const`、`fn`、`if`、`for` 都不变，绑定的名字也可以作为命令头调用。

## 管道与重定向

最外层的 `|` 把前一阶段的产出接到后一阶段的主输入。原生值函数的管道把值注入后一个调用的第一个参数；完整分组里的 `|` 仍是 EL 逻辑或。

- `value | f a b` 与 `value | f(a, b)` 都把 `value` 作为 `f` 的第一个参数。
- 要把值放到其他参数位置，写 `value | (x => g(other, x))` 明确重排。
- 数组是一个值，不会自动拆成多个输出项。
- 连续的纯外部阶段之间走操作系统字节管道；外部阶段与 EL 阶段混用时，必须显式选 codec：`utf8Input(Text)` 与 `bytesInput(Buffer 或其序列)` 把 EL 值变成字节 stdin，`text` 把 shell 结果投影回 `Text`。

例如 `shell { 21 | double | label }` 先把 `21` 注入 `double`，再把结果注入 `label`。

没有 POSIX 重定向语法：`<`、`>`、`>>`、`2>`、`|&` 都不是 shell 语法，前三个在普通 EL 里是运算符。文件输出用文件 API，例如 `writeTextFile("status.txt", Text(result))`（来自 `el:filesystem/index.el`），不要写 `>`。

把文件内容接到外部命令的 stdin，同样要先读成 `Text`（如 `readTextFile`）交给 `utf8Input`，或读成字节再显式构造 `Buffer` 交给 `bytesInput`，然后通过管道交给外部阶段。

## 结果、退出码与状态

`shell { ... }` 本身就是输出与状态的收集边界，返回 `ShellResult`：

| 成员 | 含义 |
| --- | --- |
| `output` | `CapturedOutput`，保留通道、结构值、字节与消息 |
| `exitCode` | 汇总退出码 |
| `status` | `ShellStatus`：`Success`、`ProcessFailure`、`StartFailure`、`Exception`、`StreamFailure`、`Cancelled` |
| `stages` | `ShellStage[]`，每阶段保留 `command`、`status`、`exitCode`、`signal`、`error`、`handled` |
| `complete` | 输出是否完整 |
| `text(partial?)`、`Text(result)` | 受检文本投影：只取标准输出，按记录顺序拼接，不混 stderr 与日志 |

- 全部阶段成功时 `exitCode` 是 0；有未处理失败时取最右侧真实进程退出码；没有进程码的启动、EL 与流错误汇总为 1。
- signal 保留在对应 stage 的 `signal` 字段，不伪造跨平台退出码。
- 非零退出不会自动变成异常：块会正常返回结果，由你读 `exitCode` 和 `status` 决定下一步。
- 块内的 EL 异常也会被收进结果，默认停止块内后续语句后返回。
- 文本投影只在明确要求时发生。输出不完整时 `Text(result)` 默认拒绝；传 `t` 给 `result.text(t)` 时不再要求完整，只投影已保存的部分。

## 错误策略

失败与退出码策略注册在 `ShellSession` 上：

- `session.onFailure(callback)` 接收 `ShellFailure`，其中有 `stage` 与 `output`；返回 `ShellFailureAction.Default` 时交给后续 hook，`Continue` 表示这一阶段已处理、块内继续往下执行，`Exit` 请求结束会话。
- `session.onExitCode(callback)` 把汇总退出码映射为另一个整数；返回 `void_t` 表示不映射。
- 两者都返回 `ShellHookRegistration`，`remove()` 可以重复调用。
- 没有 hook 处理时，未处理失败默认让当前块停止；`.esh` 批处理入口最后把已收集输出展示一次，并以汇总退出码退出进程。

`session.run(work)` 在这个会话的逻辑目录与环境下执行 `work`，结束后恢复外层上下文；它返回 `work` 自己的结果。

## 会话与作业

`ShellSession` 保存逻辑工作目录、环境快照、失败 hook 和 Job 表。`replaceShellSession(session)` 切换当前会话，`cd(path)` 修改当前会话的逻辑目录。

后台任务用 `session.start(work)` 启动：`work` 是零参数回调，返回 `Job`。任务体在派生会话快照中运行，默认 stdin 为 EOF，不会抢父会话的交互输入。

- `job.wait()` 等待并返回 `ShellResult`；`job.completed` 是是否已完成。
- `job.snapshot()` 读取已经接纳的输出快照，不必等任务结束。
- `job.cancel()` 请求取消；`job.terminate()` 请求取消并等待。
- `session.jobs()` 查看保留的 Job；完成后的 Job 用 `session.forget(job)` 移除，或用 `session.closeJobs(ShellJobClose.Wait | Terminate)` 统一收束。

```el
import { ShellSession } from "el:shell/index.el"

let session = ShellSession()
let job = session.start(fn() { console.stdout.writeLine("background") })
let result = job.wait()

console.stdout.writeLine(Text(result))   // background
session.forget(job)
```

作者语法也可以直接把 shell 语句写成后台任务：单独导入 `start` 宏，写法是 `import /^start$/ as jobs from "el:shell/index.el"`，之后 `let job = jobs.start { git status }`。块里的 `return` 只结束这个后台回调，不影响外层函数；回调返回的非 `void` 值会进入 Job 的结果。

## 完整示例：`.esh` 脚本

保存为 `squares.esh`，用 `esh squares.esh` 或 `el shell squares.esh` 运行：

```sh
#!/usr/bin/env esh
# 计算一组数字的平方和，并通过一个值管道打印结果。

import { console } from "el:console/index.el"

fn square(value: Number): Number => value * value
fn describe(total: Number): Text => `sum of squares: ${Text(total)}`

let values = @[1, 2, 3, 4]
let total = 0
for (let value in values) {
	total += square(value)
}

let message = total | describe

console.stdout.writeLine(message)
```

```text
sum of squares: 30
```

- 第一行 shebang 与 `#` 开头的行在 shell 域里是注释。
- `import` 必须写在 shell 语句之前；`.esh` 会把其余内容放进同一个 shell 块。
- 顶层 `let`、`fn` 与 `.el` 写法一致，函数体是普通 EL。
- `total | describe` 把值注入 `describe` 的第一个参数。
- 脚本参数用 `command_arguments()` 读取，导入 `el:operating-system/arguments/index.el`；参数原样传入，不会被拼进脚本文本。
- 脚本结束统一展示一次捕获输出，并以汇总退出码作为进程退出码。

## 完整示例：在 `.el` 里调用 shell

```el
import { shell } from "el:shell/index.el"

let limit = 3
let branch = shell { git branch --show-current }
let recent = shell { git log --oneline -n ${Text(limit)} }

console.stdout.writeLine("branch: ", Text(branch))
console.stdout.writeLine(Text(recent))
```

- 需要当前目录位于 git 仓库中，`git` 在 `PATH` 上；换成别的程序时规则不变。
- 插值洞里的 `Text(limit)` 显式转换数字，argv 项必须是 `Text`。
- `Text(branch)` 只取标准输出；退出码与状态留在 `ShellResult` 里。
- 如果 `git` 失败，脚本不会抛异常，只是投影为空；要判断失败就读 `branch.status` 或 `branch.exitCode`。

## 实现状态

!!! note "实现状态"
    本页按 shell 模块的源码合同写：`.esh` 入口、`shell { ... }` 与 `start` 宏、ShellResult／ShellStatus／ShellStage、失败 hook、Job 与文本投影都在源码里有对应实现，本页示例未在教程环境实际运行验证。

    `.esh` 当前走批处理路径：入口把脚本内容包成 `shell { ... }` 并交给 `finishShellScript` 展示一次输出、以汇总退出码退出。交互提示符、长期增量 `EvalSession`、TTY/PTY 与默认 `fg` 作业选择、跨进程 cwd 与会话传递、受限输出历史预算、结构化 EOD 通道协商仍是目标合同，尚未接齐；默认 TTY 启动前会明确拒绝，而不是假装成功。

    规范把结果字段写作 `completeness`，列举完整、部分写入、截断等细分状态；当前 `ShellResult` 只暴露 `Bool` 的 `complete`，没有这些细分；以源码为准。输出不完整时仍可用 `result.text(t)` 显式取已保存部分。

## 继续阅读

- [模块与包](modules.md)：`.esh` 与 `.el` 里的 import 和模块身份。
- [错误处理与异步](errors-async.md)：任务、取消与异常处理的完整规则。
- [Console 与日志](../stdlib/console.md)：shell 之外的输出入口与路由。
- [命令行工具](../practice/cli-tool.md)：在一个真实 CLI 项目里接外部程序。
