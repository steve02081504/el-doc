# Console 与日志

程序要让人看见结果，也要让日志能被筛选、捕获和搬去别处。EL 把这件事拆成三个入口：数据走 stdout 端口，消息带等级，结构化值走等级对象的 `.value(...)`。

`console` 由预导入（prelude）自动提供，不需要手写 import。

## 三种输出

| 你想做的事 | 入口 | 默认去向 |
| --- | --- | --- |
| 写程序数据、管道输出 | `console.stdout.write` / `writeLine` / `writeText` / `writeBytes` | stdout |
| 发一条可本地化的消息 | `console.info("消息 key", 参数对象)` 等等级调用 | 消息通道（默认 stderr） |
| 展示一个对象、数组或错误值 | `console.info.value(value)` 等等级对象的 `.value` | 与该等级消息相同 |
| 写明确不动结构的数据 | `console.stdout.emit(value)` | stdout 数据端口 |

三个入口的职责不重叠：`write` 做文字转换，等级调用做本地化消息，`.value` 做结构化展示。

## 文字输出

`write` 和 `writeLine` 接受任意多个参数，按顺序逐个执行普通的 `Text(value)` 转换，不加分隔符。

- `write` 不追加换行。
- `writeLine` 在所有参数写完后追加一个 LF。
- 两者都返回成功写入的 UTF-8 字节数；`writeLine` 的返回值包含最后那个 LF。
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

多个参数是逐个转换后拼接，不插入空格。上例的 `"count: "` 自己带了一个空格；`writeLine("count:", 3)` 会得到 `count:3`。

### write、writeText 与 writeBytes

日常输出优先用 `write` / `writeLine`。需要明确控制文本或字节时，用成对的显式入口：

```el
import { bufferFromBytes } from "el:formats/"

console.stdout.writeText("already text")
console.stdout.writeBytes(bufferFromBytes(@[72, 105]))
```

- `writeText(text)` 只接受已经确定的 `Text`，不做任意值转换。
- `writeBytes(bytes)` 接受字节缓冲，原样写出，不经过文本编码。
- `write` / `writeLine` 是便利入口，不等同于“所有对象都能转成文字”。没有可用 `Text` 转换的值会按 `Text(value)` 的失败合同报错，不会自动调用同名方法或猜测格式。要展示结构，用 `.value(...)`；要保存或传输数据，用 EOL/EOD，不要把日志当序列化。

## 日志等级

七个等级是 `log`、`info`、`warning`、`error`、`fatal`、`debug`、`trace`。每个等级都是一个普通对象，既能直接调用，也有 `.value(...)` 方法。

### 直接调用：本地化消息

直接调用发送一条消息，第一个参数是消息 key，第二个参数是参数对象：

```el
console.info("task.done", @{ count: 3 })
console.error("http.failed", @{ status: 500 })
```

`"task.done"` 不是要原样显示的文本，而是应用的 i18n 资源里的 key；参数对象用来填消息模板。消息在展示时才取当前语言，因此同一个 key 可以随语言设置显示成不同文字。

如果只有一段不需要翻译的原文，不要拿它当 key 传给 `console.info`，用 `console.stdout.writeLine` 写。

### `.value`：带等级的结构化值

`.value(value)` 展示一个结构化的值，并带上这个等级：

```el
console.log.value(@{ language: "EL", version: 1 })
console.info.value(@{ count: 3, names: @["Ada", "Grace"] })
console.error.value(error)
```

- `value` 可以是对象字面量、数组、错误值、类实例等；展示会按字段和元素展开。
- 展示取发送时的安全快照：只读取可访问的数据成员，不执行 getter、转换或迭代器。日志不应该因为展示一个对象而触发它的业务代码。
- `.value` 不参与本地化消息解析；它是展示，不是文本资源。
- `value(value, channel)` 可以明确选择通道；默认用该等级自己的 channel。给 `stdoutChannel` 时，记录仍保留原等级和 Display 类型，但写进 stdout。

```el
import { stdoutChannel } from "el:console/"

console.info.value(@{ count: 3 }, stdoutChannel)
```

`console.log.value` 和 `console.info.value` 的差别只在等级，不在“能不能展示对象”。选择哪个等级取决于这条记录有多重要。

### 路由与筛选

- 等级表示严重性，默认不改变去向。普通消息和 `.value` 默认走 stderr；`.value` 的第二个参数可以显式指定 channel。
- 要向 stdout 明确输出数据，写 `console.stdout.write` 或 `console.stdout.writeText`；也可以给 `.value` 传 `stdoutChannel`，但要清楚这会跳过 stdout 文本的捕获投影，仍是 Display 记录。
- `fatal` 只是等级，不会因为收到 fatal 记录就终止进程。要退出就显式调用退出路径，或使用 `die_with` 报告致命诊断。
- 宿主可以按等级筛选。筛选发生在记录生成之前：被筛掉的等级不会构造消息、模板或快照。用 `trace` / `debug` 承担业务输出是不可靠的，它们可能默认不启用。

```el
// 业务数据：进 stdout，能被管道和重定向拿到
console.stdout.writeLine("rows: ", rows.count)

// 诊断信息：进消息通道，可被等级筛选
console.debug("cache.miss", @{ key: key })
console.info.value(@{ elapsedMs: elapsed })
```

### 一张对照表

| 调用 | 内容 | 是否本地化 | 默认去向 |
| --- | --- | --- | --- |
| `console.stdout.writeLine(x)` | 文字 | 否 | stdout |
| `console.info("key", params)` | 消息 | 是 | stderr |
| `console.info.value(x)` | 结构化值 | 否 | stderr |
| `console.stdout.emit(x)` | 数据端口记录 | 否 | stdout |

## 捕获输出

测试、工具和嵌套执行经常需要“这段代码写了什么”。`console.capture` 在当前执行链里临时替换输出目标，正常返回 `@{result, output}`：

```el
let { result, output } = console.capture(() => {
	console.stdout.writeLine("only captured")
	40 + 2
})

console.stdout.writeLine("result: ", result)
console.stdout.writeLine("captured: ", output.text())
```

- `result` 是回调的返回值。
- `output` 是 `CapturedOutput`；`output.text()` 返回捕获到的 stdout 文本，`output.size` 是记录数。
- 只有 stdout 的数据记录能投影成文本。消息和 `.value` 的展示记录不会冒充业务文本；把它们算进 `text()` 会抛 `ConsoleProjectionError`，需要它们时读 `output.records`。
- 回调抛异常或任务被取消时，异常照常传播，外层路由仍会恢复。失败后还要看部分输出，就先持有 `VirtualConsole` 再 run。
- 嵌套捕获默认只写最内层；晚到的输出默认转交捕获创建时的外层路由。长期后台任务要持有控制台直到任务完成。

## 原始流

`rawStdout` 和 `rawStderr` 提供同样的文字入口，但直接写操作系统字节，不经过逻辑 ConsolePort 的路由。它们不在预导入里，需要显式导入：

```el
import { rawStdout } from "el:console/"

rawStdout.writeLine("bypasses logical capture")
```

只有当输出必须绕过当前执行链的捕获（例如把子进程的原始字节转交出去）时才用它。普通程序输出用 `console.stdout`，否则测试和 GUI console 都看不到你写的内容。

## GUI 里的 console

默认 GUI console 是普通 GUI 的客户端，复用布局、字体、主题和输入。程序正常结束但还有输出要保留时，窗口会继续显示历史，等待用户关闭；显式退出会关闭窗口并结束程序。`die_with` 尽力保留可用窗口和错误信息。

历史容量默认为 `auto`，通常以约 20,000 条记录为目标，内存压力下可以缩减；它是展示历史的上限，不是业务数据的保留保证，也不会截断 shell 捕获或 EOD 消息。

## 常见错误

!!! warning "把这些当成 bug 报之前先看一眼"
    - `console.info("hello")` 没有显示原文：第一个参数是消息 key，不是裸文本。
    - `console.stdout.write(obj)` 报转换错误：`write` 不是通用对象打印机，用 `console.info.value(obj)` 或显式序列化。
    - 重定向 stdout 后看不到日志：消息默认走 stderr，这是设计而不是丢失。
    - 收到 `fatal` 但进程没退出：等级不等于终止，退出要显式做。

## 继续阅读

- [集合与文本](collections.md)：把数据准备好再输出。
- [测试](testing.md)：用捕获检查程序输出。
- [文件与网络](files-network.md)：把数据写到文件或网络，而不是日志。
