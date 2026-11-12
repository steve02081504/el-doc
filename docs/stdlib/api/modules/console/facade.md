# console/facade.el

本页由源码注释生成；示例未运行验证。

## 控制台输出与日志 {#api-625df3bb66413ba4ff2c}

源码：`src/stdlib/console/facade.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L1)

提供 stdout/stderr 文本与字节输出、分级消息、结构化值展示及捕获接口。

## ConsolePort.writeText {#api-fae6bc208bf9391a9866}

源码：`src/stdlib/console/facade.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L29)

```el
@discardable fn writeText(text: Text): Number
```

将已确定的文本直接写到对应通道，不调用任意值的文本转换。

**参数**：text 要输出的文本。

**返回值**：写入的 UTF-8 字节数。

### 示例：输出已有文本

```el
console.stdout.writeText("already text")
```

## ConsolePort.write {#api-54304963a81ae8272c7a}

源码：`src/stdlib/console/facade.el:42` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L42)

```el
@discardable fn write(...values): Number
```

将参数依次转换为文本写到对应通道，不追加换行或分隔符。

**参数**：values 要按顺序输出的值。

**返回值**：写入的 UTF-8 字节数。

### 示例：写出不换行文本

```el
console.stdout.write("ready")
```

## ConsolePort.writeLine {#api-e81005183e8ea76848da}

源码：`src/stdlib/console/facade.el:55` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L55)

```el
@discardable fn writeLine(...values): Number
```

将参数依次转换为文本并写到对应通道，最后追加一个 LF。

**参数**：values 要按顺序输出的值；参数之间不自动插入分隔符。

**返回值**：写入的 UTF-8 字节数，包含末尾 LF。

### 示例：输出计数

```el
console.stdout.writeLine("count: ", 3)
```

## ConsolePort.writeBytes {#api-fe5fbcd5c1d1a9dfc277}

源码：`src/stdlib/console/facade.el:70` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L70)

```el
@discardable fn writeBytes(bytes: Buffer): Number
```

将字节缓冲原样写到对应通道，不进行文本编码。

**参数**：bytes 要输出的字节缓冲。

**返回值**：写入的字节数。

### 示例：写出字节缓冲

```el
import { bufferFromBytes } from "el:formats/"
console.stdout.writeBytes(bufferFromBytes(@[72, 105]))
```

## ConsolePort.emit {#api-74e095bfa3652f82157f}

源码：`src/stdlib/console/facade.el:83` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L83)

```el
fn emit(value): void_t
```

将值作为数据记录发送到对应通道，不转换成文本或结构化展示记录。

**参数**：value 要发送的数据值。

**返回值**：void。

### 示例：发送数据记录

```el
console.stdout.emit(@{ status: "ready" })
```

## capture {#api-db1d137769d65c8ddae2}

源码：`src/stdlib/console/facade.el:121` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L121)

```el
export fn capture(work, latePolicy: ConsoleLatePolicy = ConsoleLatePolicy.Forward, maxRecords: Number | void_t = void)
```

在临时控制台目标中执行回调，并返回回调结果与捕获的输出记录。

**参数**：work 要执行的无参回调。

**参数**：latePolicy 捕获结束后迟到记录的转发或拒绝策略。

**参数**：maxRecords 可选的记录数量上限；省略时不设置该上限。

**返回值**：包含回调结果与 CapturedOutput 的对象。

**失败与异常**：回调或捕获缓冲操作失败时传播原异常。

### 示例：捕获标准输出

```el
import { capture } from "el:console/"
let captured = capture(() => console.stdout.writeLine("ready"))
console.stdout.writeLine(captured.output.records.count)
```

## ConsoleLevelPort.operator {#api-975f263a222f7699e4e2}

源码：`src/stdlib/console/facade.el:155` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L155)

```el
operator()(message: Text | LocalizedMessage | LocalizedContent, parameters = @{}): void_t
```

发送本地化消息 key 或已构造的本地化内容，并附带参数对象。

**参数**：message 消息 key、LocalizedMessage 或 LocalizedContent。

**参数**：parameters 用于本地化消息的字段值。

**返回值**：void。

### 示例：发送带计数参数的消息

```el
console.info("task.done", @{ count: 3 })
```

## ConsoleLevelPort.value~snapshot {#api-4f80af39229b7be2b8ea}

源码：`src/stdlib/console/facade.el:170` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L170)

```el
fn value(snapshot: ConsoleValueSnapshot, channel: ConsoleChannel = this.#channel): void_t
```

将已有安全快照作为指定等级的结构化展示记录发送。

**参数**：snapshot 已构造的展示快照。

**参数**：channel 输出通道，默认使用此等级端口的通道。

**返回值**：void。

### 示例：输出结构化快照

```el
console.info.value(consoleSnapshot(@{ count: 3 }))
```

## ConsoleLevelPort.value~value {#api-0cfa9b1274a2860fc25e}

源码：`src/stdlib/console/facade.el:185` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L185)

```el
fn value(borrow value, channel: ConsoleChannel = this.#channel): void_t
```

获取值的安全快照并作为结构化展示记录发送，不调用 getter、转换或迭代器。

**参数**：value 要展示的值。

**参数**：channel 输出通道，默认使用此等级端口的通道。

**返回值**：void。

### 示例：展示结构化值

```el
console.info.value(@{ count: 3, names: @["Ada", "Grace"] })
```

## ConsoleFacade.log {#api-92438e496693c0cffd45}

源码：`src/stdlib/console/facade.el:225` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L225)

```el
get log(): ConsoleLevelPort
```

日志等级端口，用于本地化消息或结构化展示。

### 示例：发送 log 等级消息

```el
console.log("cache.hit", @{ key: "index" })
```

## ConsoleFacade.info {#api-a2bee699cc550babdfbb}

源码：`src/stdlib/console/facade.el:232` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L232)

```el
get info(): ConsoleLevelPort
```

信息等级端口；直接调用时第一个参数是本地化消息 key。

### 示例：发送信息消息

```el
console.info("task.done", @{ count: 3 })
```

## ConsoleFacade.warning {#api-580597298bc5bf52b50c}

源码：`src/stdlib/console/facade.el:239` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L239)

```el
get warning(): ConsoleLevelPort
```

警告等级端口。

### 示例：发送警告消息

```el
console.warning("cache.stale", @{})
```

## ConsoleFacade.error {#api-1e98a963c922a8010dcc}

源码：`src/stdlib/console/facade.el:246` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L246)

```el
get error(): ConsoleLevelPort
```

错误等级端口。

### 示例：发送错误消息

```el
console.error("http.failed", @{ status: 500 })
```

## ConsoleFacade.fatal {#api-ea2f5c4637892df4ad82}

源码：`src/stdlib/console/facade.el:253` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L253)

```el
get fatal(): ConsoleLevelPort
```

致命错误等级端口。

### 示例：发送 fatal 等级消息

```el
console.fatal("app.unrecoverable", @{})
```

## ConsoleFacade.debug {#api-c49cfbb9a0f6d0235a35}

源码：`src/stdlib/console/facade.el:260` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L260)

```el
get debug(): ConsoleLevelPort
```

调试等级端口。

### 示例：发送调试消息

```el
console.debug("cache.miss", @{ key: "index" })
```

## ConsoleFacade.trace {#api-d101bdd8b41f988731ea}

源码：`src/stdlib/console/facade.el:267` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L267)

```el
get trace(): ConsoleLevelPort
```

跟踪等级端口。

### 示例：发送跟踪消息

```el
console.trace("request.start", @{ path: "/" })
```
