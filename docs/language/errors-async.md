# 错误处理与异步

错误和异步是同一件事的两面：一个调用可能失败，也可能要等待。EL 把两者都放进普通表达式的类型与执行模型里；普通调用自动等待，显式并发用标准库宏 `async { ... }` 与 `await(p)`，它们不是关键字。这一页讲清 `throw`、`try`、`catch`、`finally` 的写法，标准库的错误类型，以及 `spawn`、`get`、`async` 与 `await` 的用法。

## throw：把错误交出去

`throw` 把任意值作为错误抛出，惯例是抛一个错误类的实例。抛出后当前表达式的正常求值立即结束，控制权交给最近的 `catch`。

```el
fn requirePort(value: Number) {
	if (!(value >= 1 & value <= 65535)) throw RangeError()
	return value
}
```

`throw` 不产生可读取的结果（内部是 never 流），所以它常出现在分支或提前返回的位置。需要按条件抛错时，用 `if` 把控制流写清楚：

```el
let config = if (candidate is void_t) {
	throw StateError("missing config")
} else {
	candidate
}
```

## try 是表达式

`try { ... }` 的值是 try 块最后执行语句的值；某个 `catch` 接住异常时，值就是那个 catch 块最后执行语句的值。`finally` 一定会执行，但它的普通结果会被丢弃。没有 `catch` 接住的异常继续向外传播。

```el
let port = try { requirePort(0) } catch (error: RangeError) { 8080 }
```

## catch 的写法

`catch` 有三种形式：

| 写法 | 含义 |
| --- | --- |
| `catch (e)` | 捕获全部异常，并把错误值绑到 `e` |
| `catch` | 捕获全部异常，不绑定错误值 |
| `catch (e: 类型)` | 只捕获该类型的异常，并把错误值绑到 `e` |

多个 `catch` 按从上到下的顺序匹配，第一个匹配的处理，后面的不再执行。带类型的 `catch` 要写在前面，不带类型（或类型为 `any`）的 `catch` 必须是最后一个。类型匹配走子类关系：`catch (e: Error)` 会接住 `Error` 本身及其子类。

```el
try {
	load()
} catch (error: StateError) {
	console.error.value(error)
} catch {
	console.stdout.writeLine("load failed")
}
```

## 标准库错误类型

下面这些类型都可以从 prelude 直接使用，不需要写 `import`。

| 类型 | 关键字段 | 说明 |
| --- | --- | --- |
| `Error` | `name`、`message`、位置字段、`cause`、`errors`、`stack` | 错误基类，构造时捕获调用栈 |
| `StateError` | `message`、`cause` | 继承 `Error`，对当前状态不合法的操作 |
| `RangeError` | 无字段 | 越界、范围不合法 |
| `AllocationError` | 无字段 | 分配失败 |
| `EncodingError` | `message` | 文本无法编码成目标编码 |
| `MatchError` | 无字段 | 模式匹配没有命中 |
| `CompileError` | `message` | 编译期错误 |
| `AssertionError` | `reason` | `assert` 失败时抛出 |
| `CleanupError` | `cause`、`errors` | 清理阶段聚合的多个错误 |
| `NetworkError` | `operation`、`detail`、`code` | 网络操作失败，来自 `el:network/` |
| `FileSystemError` | `operation`、`location`、`reason` | 逻辑文件系统失败，来自 `el:filesystem/` |
| `ParseError` | `offset`、`expected`、`contexts` | 文本解析失败，来自 `el:text/patterns` |

语言规范第 7 章的目标清单比上面更长（`TypeError`、`TimeoutError`、`AggregateError` 等），源码里还没有这些类；各库会定义并导出自己的错误类型，写代码时以对应模块的导出为准。

## assert

`assert(condition, reason)` 是 prelude 提供的普通函数，条件为假时抛 `AssertionError`，原因就是第二个参数；条件为真时返回真值。它同时为后续代码建立缩窄。

```el
let port = requirePort(8080)
assert(port > 0, "端口必须为正")
```

## 清理与资源关闭

`finally` 用于保证清理一定执行，无论 try 块是正常完成、抛错还是提前 return。

```el
import { openFileReader } from "el:filesystem/"

let reader = openFileReader("file:./data.txt")
try {
	let bytes = reader.read(4096)
	console.stdout.writeLine("read ", bytes.size)
} finally {
	reader.close()
}
```

清理期间抛出的错误不会淹没原始错误：原始错误保留在 `cause`，后续清理错误按启动顺序收进 `errors`（`CleanupError` 就是这种聚合）。资源类型提供幂等的 `close()` 和只读的 `closed`，作用域式管理用普通函数 `withResource(resource, body)`，它在 finally 里调 `close`。

## die_with

`die_with(text)` 是普通标准库函数，用于报告致命诊断并终止进程；它不是可恢复的 `throw`，调用者不应该指望它进入普通 catch。

## 异步：普通调用自动等待

普通调用一个可能挂起的函数时会自动等待结果，调用者随之被推断为异步；是否异步由实际调用与函数体共同决定，不需要也不允许在函数签名上标记。

```el
fn readBoth(first: Text, second: Text) {
	let a = readTextFile(first)
	let b = readTextFile(second)
	return a + b
}
```

这个函数里没有任何异步语法，但如果它调用的读取需要等待，整次调用就会等待。`@sync` 可以声明“这个接口不挂起”的要求，但它不会把异步实现变成同步实现。

## spawn 与 get

要显式并发，用 `spawn` 启动独立任务；下一节的 `async { ... }` 宏在建立 callback 后调用它：

```el
fn readPair() {
	let first = spawn(() => readTextFile("file:./a.txt"))
	let second = spawn(() => readTextFile("file:./b.txt"))
	return first.get() + second.get()
}
```

`spawn(work)` 立即返回一个 Promise；`work` 在独立任务里运行，`spawn` 本身不等待，因此只调用 `spawn` 不会让调用者变成异步。`p.get()` 等待该 Promise 完成：成功时返回结果，失败时抛出保存的错误。Promise 可以作为普通值保存、传参和返回，只有调用 `get` 才等待。

多个任务的结果可以用 `all`、`any`、`race` 组合，它们返回新的 Promise：

```el
let first = spawn(() => readTextFile("file:./a.txt"))
let second = spawn(() => readTextFile("file:./b.txt"))
let pages = all(@[first, second]).get()
console.stdout.writeLine("loaded ", pages.count, " files")
```

## `async` 块与 `await` 宏

`async { ... }` 与 `await(p)` 是标准库提供的 Expr 宏，不是关键字。`async { ... }` 把块内容解析成一个新的零参 callback，再立即 `spawn` 它：表达式执行时活动就已经发布，返回 `Promise`，不等 callback 完成。`await(p)` 只生成一次 `p.get()`：接收者只求值一次，保留真实的成员选择、返回类型与类别、异常、挂起效果和来源生命周期，不额外复制 `Promise`，也不捕获错误。

默认标准库通过显式的惰性导出提供这两个名字；关闭默认 prelude 或写自定义模块时，照常导入：

```el
import { async, await } from "el:concurrency/"
```

单个任务：

```el
let load = async {
	return readTextFile("file:./data.txt")
}

let text = await(load)
console.stdout.writeLine(text.count)
```

要并发，先把活动都启动，再等待。`await` 写在第几行不改变启动时机：

```el
let first = async {
	return readTextFile("file:./a.txt")
}
let second = async {
	return readTextFile("file:./b.txt")
}

let a = await(first)
let b = await(second)
console.stdout.writeLine(a + b)
```

- `async` 里的普通 `return` 属于那个 callback，不结束外围函数；需要跨出去时用[函数与闭包](functions.md)里的 `return ... from 外围函数`。
- `async` 建立的是独立 task。独立 task 不继承启动者的返回链，所以 callback 里对启动函数写 `return ... from` 没有有效目标；ELF 会检查这一点，运行时不能依赖它。
- 宏只生成普通的 `spawn` 与 `.get()` 调用，不改变 Promise、活动所有权、线程亲和、GC 根、取消或关闭语义，也不新增命名的 async 函数。
- `await(p)` 不捕获错误：`p` 失败时仍从 `await(p)` 或 `get()` 抛出保存的错误，照常由 `try`/`catch` 处理。结果本身还是 `Promise` 时要再等待一次。
- 普通调用仍然自动等待，因此不需要给每层函数加标记；`async` 只用于显式启动独立活动。

## 取消

取消是协作式的：在自动等待的挂起点或显式检查点，运行时会抛出 `Cancelled` 错误，程序仍然执行 `finally` 和必要的析构。没有等待或检查点的计算循环可能长时间不响应取消，所以不要把它当成随时可以中断的线程终止。

## 完整例子：解析失败回退

`parseJSON` 失败时抛 `ParseError`；`try` 表达式可以直接把“解析失败就退回空对象”写成一个值。

```el
fn settingsFrom(source: Text) {
	return try {
		parseJSON(source)
	} catch {
		Json.Object(@[])
	}
}

fn nameFrom(source: Text) {
	let config = settingsFrom(source)
	let value = try { jsonField(config, "name") } catch { return "anonymous" }
	match value {
		Json.String(text) => { return text }
		_ => { return "anonymous" }
	}
}
```

`settingsFrom` 的返回值是 `Json`，`catch` 块的最后一条语句是回退值。`nameFrom` 里的 `jsonField` 在成员缺失时抛 `ParseError`，`catch` 直接 `return`，于是整个函数提前结束，不再执行后面的 `match`。

## 继续阅读

- [函数与闭包](functions.md)：定向返回、生命周期标注、参数交接与 `async` 块的函数视角。
- [模块与包](modules.md)：错误类可以作为模块导出，跨模块共享同一套错误类型。
- [集合与文本](../stdlib/collections.md)：集合写入失败、解析结果都通过这里讲的异常交付。
- [测试](../stdlib/testing.md)：`check.throws` 用来断言一段代码抛出了预期类型的错误。
