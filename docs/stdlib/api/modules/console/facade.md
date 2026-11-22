# console/facade.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/console.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [ConsoleInputPort.isTTY](#api-ccb3fadaed7b080568fb)
- [ConsoleInputPort.supportsAnsi](#api-2ce95abce8884c0190ff)
- [ConsoleInputPort.readAs](#api-9e35bff3f1a3cb34dff2)
- [ConsoleInputPort.readAs~key](#api-f5d10a20aab0e4d0f5d6)
- [ConsoleInputPort.readAs~localized](#api-2be82159c61deced4686)
- [ConsoleInputPort.readLineAs](#api-00d315c84b632c0dbea0)
- [ConsoleInputPort.readLineAs~key](#api-0da505a7e456a47368b9)
- [ConsoleInputPort.readLineAs~localized](#api-40dacde7307346e1fb95)
- [ConsolePort.channel](#api-4b82c445007a4ad3eb60)
- [ConsolePort.isTTY](#api-8a808ef9be8eea53ac99)
- [ConsolePort.supportsAnsi](#api-1e14baa2ed802955a261)
- [ConsolePort.writeText](#api-fae6bc208bf9391a9866)
- [ConsolePort.write](#api-54304963a81ae8272c7a)
- [ConsolePort.writeLine](#api-e81005183e8ea76848da)
- [ConsolePort.writeBytes](#api-fe5fbcd5c1d1a9dfc277)
- [ConsolePort.emit](#api-74e095bfa3652f82157f)
- [ConsoleLevelPort.level](#api-2bc02e9669478eb95148)
- [ConsoleLevelPort.channel](#api-2a13aa2e4751d13d3f75)
- [ConsoleLevelPort.enabled](#api-f6892480137e18260442)
- [ConsoleLevelPort.operator](#api-975f263a222f7699e4e2)
- [ConsoleLevelPort.value~snapshot](#api-4f80af39229b7be2b8ea)
- [ConsoleLevelPort.value~value](#api-0cfa9b1274a2860fc25e)
- [ConsoleFacade.stdin](#api-f8dcccc707db3d761e8e)
- [ConsoleFacade.stdout](#api-d561aca3c282a561a29d)
- [ConsoleFacade.stderr](#api-65f237ddbf56eb1f2356)
- [ConsoleFacade.log](#api-92438e496693c0cffd45)
- [ConsoleFacade.info](#api-a2bee699cc550babdfbb)
- [ConsoleFacade.warning](#api-580597298bc5bf52b50c)
- [ConsoleFacade.error](#api-1e98a963c922a8010dcc)
- [ConsoleFacade.fatal](#api-ea2f5c4637892df4ad82)
- [ConsoleFacade.debug](#api-c49cfbb9a0f6d0235a35)
- [ConsoleFacade.trace](#api-d101bdd8b41f988731ea)
- [ConsoleFacade.enabled](#api-a56189a904459d7e2b3b)
- [ConsoleFacade.capture](#api-e6bf6c1b6908518cacea)

## 控制台输出与日志 {#api-625df3bb66413ba4ff2c}

源码：`src/stdlib/console/facade.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L1)

提供 stdout/stderr 文本与字节输出、分级消息、结构化值展示及捕获接口。

## ConsoleInputPort {#api-81b920eaf28d6a885747}

源码：`src/stdlib/console/facade.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L31)

控制台输入端口；通过当前目标查询能力并使用解析器读取输入。

```el-fragment
@assign(mode: "shared") class ConsoleInputPort
```

### 示例：使用示例

```el
let input = console.stdin
```

## ConsoleInputPort.isTTY {#api-ccb3fadaed7b080568fb}

源码：`src/stdlib/console/facade.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L40)

当前输入端是否为终端。

```el-fragment
get isTTY(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
let terminal = console.stdin.isTTY
```

## ConsoleInputPort.supportsAnsi {#api-2ce95abce8884c0190ff}

源码：`src/stdlib/console/facade.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L47)

当前输入端是否支持 ANSI。

```el-fragment
get supportsAnsi(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
let ansi = console.stdin.supportsAnsi
```

## ConsoleInputPort.readAs {#api-9e35bff3f1a3cb34dff2}

源码：`src/stdlib/console/facade.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L58)

使用解析器从当前目标的输入会话读取并返回解析结果。

```el-fragment
fn readAs(parser)
```

**参数**：parser 输入解析器。

**返回值**：解析器返回的值。

**失败与异常**：输入会话正在使用或读取、解析失败时传播异常。

### 示例：使用示例

```el
import { decimal } from "el:parsing/tokens.el"
let value = console.stdin.readAs(decimal(min: unbounded, max: unbounded, epsilon: 0))
```

## ConsoleInputPort.readAs~key {#api-f5d10a20aab0e4d0f5d6}

源码：`src/stdlib/console/facade.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L68)

使用当前 ConsoleFacade 的 i18n 服务显示提示并读取。同一终端上的积压输入会在显示前清理。

```el-fragment
fn readAs(parser, key: Text, parameters = @{})
```

**参数**：parser 输入解析器。

**参数**：key 提示消息的 i18n 键。

**参数**：parameters 提示消息的具名参数。

### 示例：用已注册的提示键读取

```el
let value = console.stdin.readAs(parsers.integer(), "app.enterNumber", parameters: @{label: "A"})
```

## ConsoleInputPort.readAs~localized {#api-2be82159c61deced4686}

源码：`src/stdlib/console/facade.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L77)

显示已选本地化内容并读取。

```el-fragment
fn readAs(parser, prompt: LocalizedMessage | LocalizedContent)
```

**参数**：parser 输入解析器。

**参数**：prompt 显示在标准输出的本地化消息或组合内容。

### 示例：使用已选择的本地化提示

```el
let value = console.stdin.readAs(parsers.integer(), prompt)
```

## ConsoleInputPort.readLineAs {#api-00d315c84b632c0dbea0}

源码：`src/stdlib/console/facade.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L86)

消费一行输入，再用解析器匹配整行。换行符不传给解析器。

```el-fragment
fn readLineAs(parser)
```

**参数**：parser 支持整段文本解析的解析器。

**失败与异常**：读取、输入结束或整行解析失败时传播异常。

### 示例：读取 80 到 560 的整数

```el
let value = console.stdin.readLineAs(parsers.integer(min: 80, max: 560))
```

## ConsoleInputPort.readLineAs~key {#api-0da505a7e456a47368b9}

源码：`src/stdlib/console/facade.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L96)

用 i18n 键显示提示，再读取并解析整行。

```el-fragment
fn readLineAs(parser, key: Text, parameters = @{})
```

**参数**：parser 支持整段文本解析的解析器。

**参数**：key 提示消息的 i18n 键。

**参数**：parameters 提示消息的具名参数。

### 示例：用已注册的提示键读取

```el
let value = console.stdin.readLineAs(parsers.integer(), "app.enterNumber", parameters: @{label: "A"})
```

## ConsoleInputPort.readLineAs~localized {#api-40dacde7307346e1fb95}

源码：`src/stdlib/console/facade.el:105` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L105)

显示已选本地化内容，再读取并解析整行。

```el-fragment
fn readLineAs(parser, prompt: LocalizedMessage | LocalizedContent)
```

**参数**：parser 支持整段文本解析的解析器。

**参数**：prompt 显示在标准输出的本地化消息或组合内容。

### 示例：使用已选择的本地化提示

```el
let value = console.stdin.readLineAs(parsers.integer(), prompt)
```

## ConsolePort {#api-1e5cdfe9e38e075d126d}

源码：`src/stdlib/console/facade.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L142)

控制台逻辑输出端口；每次操作解析当前目标。

```el-fragment
export @assign(mode: "shared") class ConsolePort
```

### 示例：使用示例

```el
let output = console.stdout
```

## ConsolePort.channel {#api-4b82c445007a4ad3eb60}

源码：`src/stdlib/console/facade.el:151` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L151)

此端口的逻辑通道。

```el-fragment
get channel(): ConsoleChannel
```

**返回类型**：[`ConsoleChannel`](../../types.md#api-014dddb6e6d5af8b8537)

### 示例：使用示例

```el
let channel = console.stdout.channel
```

## ConsolePort.isTTY {#api-8a808ef9be8eea53ac99}

源码：`src/stdlib/console/facade.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L158)

当前目标对应输出端是否为终端。

```el-fragment
get isTTY(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
let terminal = console.stdout.isTTY
```

## ConsolePort.supportsAnsi {#api-1e14baa2ed802955a261}

源码：`src/stdlib/console/facade.el:165` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L165)

当前目标对应输出端是否支持 ANSI。

```el-fragment
get supportsAnsi(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
let ansi = console.stdout.supportsAnsi
```

## ConsolePort.writeText {#api-fae6bc208bf9391a9866}

源码：`src/stdlib/console/facade.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L175)

将已确定的文本直接写到对应通道，不调用任意值的文本转换。

```el-fragment
@discardable fn writeText(text: Text): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：text 要输出的文本。

**返回值**：写入的 UTF-8 字节数。

### 示例：输出已有文本

```el
console.stdout.writeText("already text")
```

## ConsolePort.write {#api-54304963a81ae8272c7a}

源码：`src/stdlib/console/facade.el:188` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L188)

将参数依次转换为文本写到对应通道，不追加换行或分隔符。

```el-fragment
@discardable fn write(...values): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：values 要按顺序输出的值。

**返回值**：写入的 UTF-8 字节数。

### 示例：写出不换行文本

```el
console.stdout.write("ready")
```

## ConsolePort.writeLine {#api-e81005183e8ea76848da}

源码：`src/stdlib/console/facade.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L201)

将参数依次转换为文本并写到对应通道，最后追加一个 LF。

```el-fragment
@discardable fn writeLine(...values): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：values 要按顺序输出的值；参数之间不自动插入分隔符。

**返回值**：写入的 UTF-8 字节数，包含末尾 LF。

### 示例：输出计数

```el
console.stdout.writeLine("count: ", 3)
```

## ConsolePort.writeBytes {#api-fe5fbcd5c1d1a9dfc277}

源码：`src/stdlib/console/facade.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L216)

将字节缓冲原样写到对应通道，不进行文本编码。

```el-fragment
@discardable fn writeBytes(bytes: Buffer): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：bytes 要输出的字节缓冲。

**返回值**：写入的字节数。

### 示例：写出字节缓冲

```el
import { bufferFromBytes } from "el:formats/"
console.stdout.writeBytes(bufferFromBytes(@[72, 105]))
```

## ConsolePort.emit {#api-74e095bfa3652f82157f}

源码：`src/stdlib/console/facade.el:229` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L229)

将值作为数据记录发送到对应通道，不转换成文本或结构化展示记录。

```el-fragment
fn emit(value): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：value 要发送的数据值。

**返回值**：nil。

### 示例：发送数据记录

```el
console.stdout.emit(@{ status: "ready" })
```

## capture {#api-db1d137769d65c8ddae2}

源码：`src/stdlib/console/facade.el:267` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L267)

在临时控制台目标中执行回调，并返回回调结果与捕获的输出记录。

```el-fragment
export fn capture(work, latePolicy: ConsoleLatePolicy = ConsoleLatePolicy.Forward, maxRecords: Number | nil_t = nil)
```

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

## ConsoleLevelPort {#api-82d3368b956700e55610}

源码：`src/stdlib/console/facade.el:283` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L283)

可调用的等级端口，发送本地化消息或结构化展示记录。

```el-fragment
export @assign(mode: "shared") class ConsoleLevelPort
```

### 示例：使用示例

```el
console.info.value(@{ count: 3 })
```

## ConsoleLevelPort.level {#api-2bc02e9669478eb95148}

源码：`src/stdlib/console/facade.el:301` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L301)

此端口的日志等级。

```el-fragment
get level(): ConsoleLevel
```

**返回类型**：[`ConsoleLevel`](../../types.md#api-bcca0db28d7f511b4f1f)

### 示例：使用示例

```el
let level = console.info.level
```

## ConsoleLevelPort.channel {#api-2a13aa2e4751d13d3f75}

源码：`src/stdlib/console/facade.el:308` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L308)

此端口的默认通道。

```el-fragment
get channel(): ConsoleChannel
```

**返回类型**：[`ConsoleChannel`](../../types.md#api-014dddb6e6d5af8b8537)

### 示例：使用示例

```el
let channel = console.info.channel
```

## ConsoleLevelPort.enabled {#api-f6892480137e18260442}

源码：`src/stdlib/console/facade.el:316` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L316)

查询此端口的等级是否被当前筛选器和纯上下文规则允许。

```el-fragment
fn enabled(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：是否启用。

### 示例：使用示例

```el
let active = console.info.enabled()
```

## ConsoleLevelPort.operator {#api-975f263a222f7699e4e2}

源码：`src/stdlib/console/facade.el:326` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L326)

发送本地化消息 key 或已构造的本地化内容，并附带参数对象。

```el-fragment
operator()(message: Text | LocalizedMessage | LocalizedContent, parameters = @{}): nil_t
```

**参数**：message 消息 key、LocalizedMessage 或 LocalizedContent。

**参数**：parameters 用于本地化消息的字段值。

**返回值**：nil。

### 示例：发送带计数参数的消息

```el
console.info("task.done", @{ count: 3 })
```

<span id="api-16a5a6805cf2bf2d045d"></span>

## ConsoleLevelPort.value~snapshot {#api-4f80af39229b7be2b8ea}

源码：`src/stdlib/console/facade.el:341` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L341)

将已有安全快照作为指定等级的结构化展示记录发送。

```el-fragment
fn value(snapshot: ConsoleValueSnapshot, channel: ConsoleChannel = this.#channel): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：snapshot 已构造的展示快照。

**参数**：channel 输出通道，默认使用此等级端口的通道。

**返回值**：nil。

### 示例：输出结构化快照

```el
console.info.value(consoleSnapshot(@{ count: 3 }))
```

## ConsoleLevelPort.value~value {#api-0cfa9b1274a2860fc25e}

源码：`src/stdlib/console/facade.el:356` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L356)

获取值的安全快照并作为结构化展示记录发送，不调用 getter、转换或迭代器。

```el-fragment
fn value(borrow value, channel: ConsoleChannel = this.#channel): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：value 要展示的值。

**参数**：channel 输出通道，默认使用此等级端口的通道。

**返回值**：nil。

### 示例：展示结构化值

```el
console.info.value(@{ count: 3, names: @["Ada", "Grace"] })
```

## ConsoleFacade {#api-b279f598543f0f517e5b}

源码：`src/stdlib/console/facade.el:371` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L371)

控制台入口，提供输入、输出端口、等级端口和捕获操作。

```el-fragment
export @assign(mode: "shared") class ConsoleFacade
```

### 示例：使用示例

```el
console.stdout.writeLine("ready")
```

## ConsoleFacade.stdin {#api-f8dcccc707db3d761e8e}

源码：`src/stdlib/console/facade.el:379` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L379)

输入端口。

```el-fragment
get stdin(): ConsoleInputPort
```

**返回类型**：[`ConsoleInputPort`](facade.md#api-81b920eaf28d6a885747)

### 示例：使用示例

```el
let input = console.stdin
```

## ConsoleFacade.stdout {#api-d561aca3c282a561a29d}

源码：`src/stdlib/console/facade.el:412` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L412)

标准输出逻辑端口；每次操作使用当前控制台目标。

```el-fragment
get stdout(): ConsolePort
```

**返回类型**：[`ConsolePort`](facade.md#api-1e5cdfe9e38e075d126d)

### 示例：输出一行

```el
console.stdout.writeLine("ready")
```
```text
ready
```

## ConsoleFacade.stderr {#api-65f237ddbf56eb1f2356}

源码：`src/stdlib/console/facade.el:420` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L420)

标准错误逻辑端口；每次操作使用当前控制台目标。

```el-fragment
get stderr(): ConsolePort
```

**返回类型**：[`ConsolePort`](facade.md#api-1e5cdfe9e38e075d126d)

### 示例：输出一行错误信息

```el
console.stderr.writeLine("failed")
```
标准错误输出为 `failed`，后跟 LF。

## ConsoleFacade.log {#api-92438e496693c0cffd45}

源码：`src/stdlib/console/facade.el:427` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L427)

日志等级端口，用于本地化消息或结构化展示。

```el-fragment
get log(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送 log 等级消息

```el
console.log("cache.hit", @{ key: "index" })
```

## ConsoleFacade.info {#api-a2bee699cc550babdfbb}

源码：`src/stdlib/console/facade.el:434` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L434)

信息等级端口；直接调用时第一个参数是本地化消息 key。

```el-fragment
get info(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送信息消息

```el
console.info("task.done", @{ count: 3 })
```

## ConsoleFacade.warning {#api-580597298bc5bf52b50c}

源码：`src/stdlib/console/facade.el:441` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L441)

警告等级端口。

```el-fragment
get warning(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送警告消息

```el
console.warning("cache.stale", @{})
```

## ConsoleFacade.error {#api-1e98a963c922a8010dcc}

源码：`src/stdlib/console/facade.el:448` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L448)

错误等级端口。

```el-fragment
get error(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送错误消息

```el
console.error("http.failed", @{ status: 500 })
```

## ConsoleFacade.fatal {#api-ea2f5c4637892df4ad82}

源码：`src/stdlib/console/facade.el:455` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L455)

致命错误等级端口。

```el-fragment
get fatal(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送 fatal 等级消息

```el
console.fatal("app.unrecoverable", @{})
```

## ConsoleFacade.debug {#api-c49cfbb9a0f6d0235a35}

源码：`src/stdlib/console/facade.el:462` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L462)

调试等级端口。

```el-fragment
get debug(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送调试消息

```el
console.debug("cache.miss", @{ key: "index" })
```

## ConsoleFacade.trace {#api-d101bdd8b41f988731ea}

源码：`src/stdlib/console/facade.el:469` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L469)

跟踪等级端口。

```el-fragment
get trace(): ConsoleLevelPort
```

**返回类型**：[`ConsoleLevelPort`](facade.md#api-82d3368b956700e55610)

### 示例：发送跟踪消息

```el
console.trace("request.start", @{ path: "/" })
```

## ConsoleFacade.enabled {#api-a56189a904459d7e2b3b}

源码：`src/stdlib/console/facade.el:479` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L479)

查询指定等级是否被此 facade 的筛选器和纯上下文规则允许。

```el-fragment
fn enabled(level: ConsoleLevel): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：level 要查询的等级。

**返回值**：是否启用。

### 示例：使用示例

```el
import { ConsoleLevel } from "el:console/"
let active = console.enabled(ConsoleLevel.Info)
```

## ConsoleFacade.capture {#api-e6bf6c1b6908518cacea}

源码：`src/stdlib/console/facade.el:492` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L492)

在临时控制台目标中执行回调，返回结果和捕获的记录。

```el-fragment
fn capture(work, latePolicy: ConsoleLatePolicy = ConsoleLatePolicy.Forward, maxRecords: Number | nil_t = nil)
```

**参数**：work 无参回调。

**参数**：latePolicy 捕获结束后迟到记录的处理策略。

**参数**：maxRecords 可选的记录数量上限。

**返回值**：包含 result 和 output 的对象。

**失败与异常**：回调或捕获缓冲操作失败时传播异常。

### 示例：使用示例

```el
let captured = console.capture(() => console.stdout.writeLine("ready"))
console.stdout.write(captured.output.text())
```

## console {#api-b4ac6973d3d99a3bab2a}

源码：`src/stdlib/console/facade.el:507` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/facade.el#L507)

默认控制台对象，类型为 ConsoleFacade；标准库入口通过 prelude 提供此绑定。

```el-fragment
export const console = ConsoleFacade()
```

**类型**：[`ConsoleFacade`](facade.md#api-b279f598543f0f517e5b)

**注意**：也可从 el:console/ 显式导入；stdout 和 stderr 是 ConsolePort，等级成员是 ConsoleLevelPort。

### 示例：写入标准输出

```el
console.stdout.writeLine("hello")
```
```text
hello
```
