# Shell 语法

> 一段要跑外部命令、读结果、再打印统计的脚本，可以整段写在 `.esh` 里，`let` 和 `git log` 落在同一层——EL 的 shell 不是另一门语言，只是 EL 的一层调用表面。

!!! abstract "🎯 读完这页，你能"
    - 用 `.esh` 写出把外部命令、EL 值和管道接在一起的脚本
    - 在 `.el` 里用 `shell { ... }` 调用外部程序，并从 `ShellResult` 里读出结果
    - 判断一次失败该看 `exitCode`、`status`，还是落到 EL 异常里

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[函数与闭包](functions.md)、[模块与包](modules.md)</span>

## 先跑一个脚本

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

脚本里 shebang 与 `#` 行是注释，`import`、`fn` 体是普通 EL，`total | describe` 是值管道。==`.esh` 不是另一门语言，只是把顶层内容放进 shell 语法域。==

- `import` 必须写在 shell 语句之前；脚本参数用 `command_arguments()` 读取（导入 `el:operating-system/arguments/index.el`），参数原样传入，不会被拼进脚本文本。
- 脚本结束统一展示一次捕获输出，并以汇总退出码作为进程退出码。

## `.esh` 还是 `shell { ... }`？

| 你在哪 | shell 语法怎么进来 |
| --- | --- |
| `.esh` 文件 | 顶层直接是 shell 语法域；`import`（含 `lazy import`）与 `@module`、`@runtime` 声明仍是普通 EL |
| `.el`、`.els`、`el repl` | 普通 EL 域；导入 `shell` 宏后写 `shell { ... }` 块 |
| 普通 `fn` 的函数体 | 仍是 EL；函数体里需要外部命令时，写显式的 `shell { ... }` 块 |

`esh` 与 `el shell` 是同一入口的两个名字，共用宿主、编译器和运行时。`shell { ... }` 是普通库宏，不是关键字：只有导入后才可用；`.esh` 的包装由入口生成，脚本里不需要自己导入它。

在 `.el` 里，这个宏把外部命令接回普通值：

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
- `git` 失败时脚本不会抛异常，只是投影为空；要判断失败就读 `branch.status` 或 `branch.exitCode`。

## 命令头先查绑定，再查 `PATH`

`git status` 里的 `git` 不是先去 `PATH` 找程序：命令头先查词法绑定。有同名变量、函数或导入就用该绑定，裸变量直接求值，不会启动同名程序；只有没有绑定的完整命令形状才建立外部程序引用。绑定存在时缺参、类型错误都是 EL 错误，不会失败后再去查 `PATH`。

??? question "先猜：先 `let git = @{ name: \"bound\" }`，再写 `git status`，会运行外部 git 吗？"
    不会。命令头先查词法绑定，`git` 求值成那个对象，`git status` 变成对它的调用；只有 `& git status` 才绕过绑定、强制找外部程序。

`&` 是命令头的显式外部调用前缀，`&(expr)` 先求值得到一个路径或程序引用：

```sh
git status --short
& git status --short
& "./tool with spaces" --help
```

它和 EL 的二元 `&` 不冲突：`&` 只在 shell 命令头表示外部程序，普通 `a & b` 仍是逻辑与，也不表示后台执行。

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

## 外部参数：每个词是一项 argv

外部程序的参数是另一套规则：不做分词、通配符展开、反引号执行或插值后的二次解析，未引用的词逐字作为 argv 项。

引号就是 EL 字符串字面量，单双引号等价，转义与普通 EL 相同；`#` 在行首或空白之后起注释。

- 未引用的词是字面 argv 项，不是变量引用。
- `"..."` 或 `'...'` 包住整个词时，按 EL 字符串求值，一个字符串是一整项。
- `${expr}` 是 EL 表达式洞，求值后作为一项 argv 插入。
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

## 管道与重定向：`|` 接值，文件走 API

最外层的 `|` 把前一阶段的产出接到后一阶段的主输入。原生值函数的管道把值注入后一个调用的第一个参数；完整分组里的 `|` 仍是 EL 逻辑或。

- `value | f a b` 与 `value | f(a, b)` 都把 `value` 作为 `f` 的第一个参数。
- 要把值放到其他参数位置，写 `value | (x => g(other, x))` 明确重排。
- 数组是一个值，不会自动拆成多个输出项。
- 连续的纯外部阶段之间走操作系统字节管道；外部阶段与 EL 阶段混用时，必须显式选 codec：`utf8Input(Text)` 与 `bytesInput(Buffer 或其序列)` 把 EL 值变成字节 stdin，`text` 把 shell 结果投影回 `Text`。

例如 `shell { 21 | double | label }` 先把 `21` 注入 `double`，再把结果注入 `label`。

没有 POSIX 重定向语法：`<`、`>`、`>>`、`2>`、`|&` 都不是 shell 语法，前三个在普通 EL 里是运算符。文件输出用文件 API，例如 `writeTextFile("status.txt", Text(result))`（来自 `el:filesystem/index.el`），不要写 `>`。

把文件内容接到外部命令的 stdin，同样要先读成 `Text`（如 `readTextFile`）交给 `utf8Input`，或读成字节再显式构造 `Buffer` 交给 `bytesInput`，然后通过管道交给外部阶段。

## `ShellResult`：退出码不是异常

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

!!! warning "常见坑：命令失败不会自己抛"
    运行 `shell { git log -n 1 }` 却得到空文本、程序也没报错——很可能是 `git` 退出码非零，输出被收进了 `ShellResult`。读 `result.status` 或 `result.exitCode`，不要等异常。另外，`>` 在 EL 里是运算符，写文件要用 `writeTextFile`。

需要接管失败策略、切换会话或启动后台作业时，再展开下面这一节。

??? note "可选 · 深入：失败策略、会话与后台作业"

    失败与退出码策略注册在 `ShellSession` 上：`session.onFailure(callback)` 收到带 `stage` 与 `output` 的 `ShellFailure`，返回 `ShellFailureAction.Default` 交给后续 hook、`Continue` 继续块内后续语句、`Exit` 结束会话；`session.onExitCode(callback)` 把汇总退出码映射为另一个整数，返回 `void_t` 表示不映射。两者都返回 `ShellHookRegistration`，`remove()` 可重复调用。没有 hook 时未处理失败默认停止当前块；`.esh` 入口最后展示一次已收集输出，并以汇总退出码退出进程。

    `session.run(work)` 在会话的逻辑目录与环境里执行 `work`，结束后恢复外层上下文并返回它的结果。会话保存逻辑工作目录、环境快照、失败 hook 和 Job 表；`replaceShellSession(session)` 切换当前会话，`cd(path)` 修改逻辑目录。

    后台任务用 `session.start(work)` 启动：`work` 是零参数回调，返回 `Job`，在派生会话快照中运行，默认 stdin 为 EOF，不抢父会话的交互输入。

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

## 实现状态

!!! note "实现状态"
    本页按 shell 模块的源码合同写；`.esh`、`shell`／`start` 宏、`ShellResult`、失败 hook、Job 与文本投影都有对应实现，示例未在教程环境实际运行验证。

    `.esh` 当前走批处理路径：入口把脚本包成 `shell { ... }` 交给 `finishShellScript` 展示一次输出、以汇总退出码退出。交互提示符、长期增量 `EvalSession`、TTY/PTY 与 `fg` 作业选择、跨进程 cwd 与会话传递、输出历史预算、结构化 EOD 通道协商仍未接齐；默认 TTY 启动前会明确拒绝。

    规范把结果字段写作 `completeness`，列举完整、部分写入、截断等细分状态；当前 `ShellResult` 只暴露 `Bool` 的 `complete`，以源码为准。

## 带走这三样

- `.esh` 顶层是 shell 语法域，`.el` 里则先导入 `shell` 宏再写块；`esh` 与 `el shell` 是同一入口。
- 命令头先查词法绑定，`&` 强制走外部程序；`${expr}` 每次插入一项 argv，数字先 `Text(...)`，没有 `>` 重定向。
- `shell { ... }` 返回 `ShellResult`；非零退出不是异常，用 `exitCode`、`status` 和 `Text(result)` 判断与投影。

## 下一站：[错误处理与异步](errors-async.md)

> 外部命令失败还能靠 `exitCode` 读出来；可 EL 自己的调用失败、后台任务失败，又该在哪里被接住？

- 主推进：[错误处理与异步](errors-async.md)：把 `throw`／`try` 和任务失败接进同一条控制流。
- 想先练手：[命令行工具](../practice/cli-tool.md)：在一个真实 CLI 项目里接外部程序。
