# Console 与日志

> 同一句 `"hello"`，写进 stdout 是数据，交给 `console.info` 是消息 key，包进 `.value` 是结构化展示。三者混淆时，你会盯着空白终端找一个根本没被打印的 bug。

!!! abstract "🎯 读完这页，你能"
    - 按“我要做什么”在两秒内选对 `console.stdout`、等级调用还是 `.value`
    - 写出不会被管道吞掉、也不会把日志当序列化的输出
    - 用 `console.capture` 在测试里检查程序到底写了什么
    - 判断一条记录去了 stdout 还是 stderr，以及重定向后日志为什么“不见了”

    <span class="el-chip">⏱ 约 8 分钟</span> <span class="el-chip">前置：[值与类型](../language/values.md)</span>

`console` 由预导入提供，不用 import。它只有三个出口，分别负责**数据**、**消息**和**结构化展示**。

## 我要做什么，就用哪个

| 我想…… | 用 | 默认去 |
| --- | --- | --- |
| 输出程序结果，给管道或重定向 | `console.stdout.writeLine(...)` | stdout |
| 输出一段已有文本，不换行 | `console.stdout.write(...)` | stdout |
| 记一条能筛选、能本地化的日志 | `console.info("消息 key", 参数对象)` | stderr |
| 打印一个对象、数组或错误 | `console.info.value(value)` | stderr |
| 输出明确不改结构的数据记录 | `console.stdout.emit(value)` | stdout |

最小入口就是第一行：

```el
console.stdout.writeLine("count: ", 3)
```

输出：

```text
count: 3
```

看到 `3` 前面有一个空格就说明对了：多个参数逐个转换后拼接，不自动加分隔符。

!!! example "动手 30 秒"
    把 `"count: "` 改成 `"count:"` 再跑一次。输出变成 `count:3`，说明空格来自字符串本身，不是 `writeLine` 加的。

## 文字输出：write 与 writeLine 只差一个 LF

`write` 和 `writeLine` 接受任意多个参数，按顺序逐个做普通的 `Text(value)` 转换，不加分隔符。

- `write` 不追加换行；`writeLine` 在所有参数写完后追加一个 LF。
- 两者都返回成功写入的 UTF-8 字节数；`writeLine` 的返回值包含最后的 LF。
- 零参 `write()` 不写任何东西并返回 0；零参 `writeLine()` 只写一个 LF。

```el
console.stdout.write("count: ", 3)
console.stdout.writeLine()
console.stdout.writeLine("done")
```

输出：

```text
count: 3
done
```

`write` 不是通用对象打印机。`console.stdout.write(obj)` 会按 `Text(value)` 的失败合同报错，不会自动调用同名方法或猜格式；要展示结构用 `.value(...)`，要保存或传输用 EOL/EOD。需要明确控制文本或字节时，用成对的显式入口：

```el
import { bufferFromBytes } from "el:formats/"

console.stdout.writeText("already text")
console.stdout.writeBytes(bufferFromBytes(@[72, 105]))
```

- `writeText(text)` 只接受已经确定的 `Text`，不做任意值转换。
- `writeBytes(bytes)` 接受字节缓冲，原样写出，不经过文本编码。

## 等级调用与 `.value`：一个发消息，一个展示值

七个等级 `log`、`info`、`warning`、`error`、`fatal`、`debug`、`trace` 都是普通对象，既能直接调用，也有 `.value(...)`。

直接调用的第一个参数是**消息 key**，第二个是参数对象：

```el
console.info("task.done", @{ count: 3 })
console.error("http.failed", @{ status: 500 })
```

`"task.done"` 不是要原样显示的文本，而是 i18n 资源里的 key，展示时才取当前语言，所以同一个 key 可以随语言设置显示成不同文字。`console.info("hello")` 不会打印 `hello`；只有一段不需要翻译的原文时，用 `console.stdout.writeLine`。

`.value(value)` 展示一个结构化值，并带上等级：

```el
console.log.value(@{ language: "EL", version: 1 })
console.info.value(@{ count: 3, names: @["Ada", "Grace"] })
console.error.value(error)
```

- `value` 可以是对象字面量、数组、错误值、类实例，展示时按字段和元素展开。
- 展示取发送时的安全快照：只读取可访问的数据成员，不执行 getter、转换或迭代器。日志不会因为展示一个对象而触发它的业务代码。
- `.value` 不参与本地化消息解析，它只是展示。
- `value(value, channel)` 可以明确选择通道；传 `stdoutChannel` 时记录保留原等级和 Display 类型，但写进 stdout：

```el
import { stdoutChannel } from "el:console/"

console.info.value(@{ count: 3 }, stdoutChannel)
```

`console.log.value` 和 `console.info.value` 的差别只在等级，不在“能不能展示对象”。选哪个等级取决于这条记录有多重要。

## 先猜：重定向 stdout 之后，日志去哪了？

??? question "先猜：`el run app.el > out.txt` 之后，`console.info("task.done", ...)` 去哪了？"
    不在 `out.txt` 里。等级调用和 `.value` 默认走 stderr，重定向只接走 stdout。这是设计：数据走 stdout，诊断走 stderr，管道只拿数据。要进 stdout 就用 `console.stdout.writeLine`，或给 `.value` 传 `stdoutChannel`。

路由规则就这几条：

- 等级表示严重性，默认不改变去向。`fatal` 只是等级，收到它不会终止进程；要退出就显式调用退出路径，或用 `die_with` 报告致命诊断。
- 宿主可以按等级筛选，筛选发生在记录生成之前：被筛掉的等级不会构造消息、模板或快照。所以用 `trace` / `debug` 承担业务输出不可靠，它们可能默认不启用。
- 给 `.value` 传 `stdoutChannel` 会跳过 stdout 文本的捕获投影，记录仍是 Display 类型。

```el
// 业务数据：进 stdout，能被管道和重定向拿到
console.stdout.writeLine("rows: ", rows.count)

// 诊断信息：进消息通道，可被等级筛选
console.debug("cache.miss", @{ key: key })
console.info.value(@{ elapsedMs: elapsed })
```

## 一张对照表：同一件事有四个入口

| 调用 | 内容 | 是否本地化 | 默认去向 |
| --- | --- | --- | --- |
| `console.stdout.writeLine(x)` | 文字 | 否 | stdout |
| `console.info("key", params)` | 消息 | 是 | stderr |
| `console.info.value(x)` | 结构化值 | 否 | stderr |
| `console.stdout.emit(x)` | 数据端口记录 | 否 | stdout |

==数据走 stdout，消息与展示走 stderr；等级只决定严重性，不决定去向。==

## 捕获输出：测试怎么看到你写了什么

`console.capture` 在当前执行链里临时替换输出目标，正常返回 `@{result, output}`：

```el
let { result, output } = console.capture(() => {
	console.stdout.writeLine("only captured")
	40 + 2
})

console.stdout.writeLine("result: ", result)
console.stdout.writeLine("captured: ", output.text())
```

- `result` 是回调返回值；`output` 是 `CapturedOutput`，`output.text()` 给 stdout 文本，`output.size` 是记录数。
- 只有 stdout 的数据记录能投影成文本。消息和 `.value` 的展示记录不会冒充业务文本；把它们算进 `text()` 会抛 `ConsoleProjectionError`，需要它们时读 `output.records`。
- 回调抛异常或任务被取消时，异常照常传播，外层路由仍会恢复。
- 嵌套捕获默认只写最内层；晚到的输出默认转交捕获创建时的外层路由。长期后台任务要持有控制台直到任务完成。

??? note "可选 · 深入：捕获失败时还能看到什么"
    `console.capture` 的成功路径很直接，边界都在失败侧：嵌套时只有最内层拿得到捕获内容；晚到的输出会转交捕获创建时的外层路由，所以后台任务要一直持有控制台到任务结束。失败后还想看部分输出，就先持有 `VirtualConsole` 再 run；异常会带着已经写入的部分输出一起抛给调用方。

## 原始流绕过捕获，GUI console 保留历史

`rawStdout` 和 `rawStderr` 提供同样的文字入口，但直接写操作系统字节，不经过逻辑 ConsolePort 的路由；它们不在预导入里：

```el
import { rawStdout } from "el:console/"

rawStdout.writeLine("bypasses logical capture")
```

只在输出必须绕过当前执行链的捕获时才用它，比如把子进程的原始字节转交出去。普通程序输出用 `console.stdout`，否则测试和 GUI console 都看不到你写的内容。

默认 GUI console 是普通 GUI 的客户端，复用布局、字体、主题和输入。程序正常结束但还有输出要保留时，窗口会继续显示历史，等待用户关闭；显式退出会关闭窗口并结束程序，`die_with` 尽力保留可用窗口和错误信息。历史容量默认为 `auto`，通常以约 20,000 条记录为目标，内存压力下可以缩减；它是展示历史的上限，不是业务数据的保留保证，也不会截断 shell 捕获或 EOD 消息。

!!! warning "常见坑：四件先别当 bug 报的事"
    - `console.info("hello")` 没显示原文：第一个参数是消息 key，裸文本用 `writeLine`。
    - `console.stdout.write(obj)` 报转换错误：`write` 不是通用对象打印机，用 `console.info.value(obj)` 或显式序列化。
    - 重定向 stdout 后看不到日志：消息默认走 stderr，这是设计而不是丢失。
    - 收到 `fatal` 但进程没退出：等级不等于终止，退出要显式做。

## 带走这三样

- 文字走 `console.stdout.write` / `writeLine`，等级调用发本地化消息，`.value` 展示结构化值，三者职责不重叠。
- 等级默认走 stderr，`fatal` 不会终止进程；要 stdout 的数据必须显式写。
- `console.capture` 只把 stdout 数据投影成文本，消息记录要读 `output.records`。

## 下一站：集合与文本

> 输出之前总得先有数据。EL 的数组、映射和文本各自提供哪些常用操作？

- 主推进：[集合与文本](collections.md)：数组、`Map`、`Set` 与 `Text` 的常用操作。
- 想先练手：[测试](testing.md)：用 `console.capture` 检查程序的输出。
- 后面会用到：[文件与网络](files-network.md)：把数据写进文件或发到网络，而不是日志。
