# 常见问题

这一页收集新使用者最常卡住的写法问题，每条给出能直接照抄的入口和继续阅读的位置。

### 怎么输出一行文字？

用 `console.stdout.writeLine(...values)`：它接受多个参数，逐个转成文本后顺序写出，最后追加一个换行；`console.stdout.write(...values)` 不追加换行。参数之间不会自动加分隔符，要空格就自己写在字符串里。`console` 由默认导入提供，普通模块不需要再 `import`。

```el
console.stdout.writeLine("count: ", 3)
```

详见 [Console 与日志](../stdlib/console.md)。

### 怎么查看一个对象或数组的内容？

用等级对象的 `.value` 方法，例如 `console.log.value(object)`、`console.info.value(values)`。等级对象是普通可调用对象：直接调用发本地化消息，第一个参数是消息 key 而不是任意裸文本；`.value` 发该等级的结构化展示记录。两者默认都走 stderr，`.value` 可以用第二个参数显式指定 channel。

```el
console.log.value(@{lines: 12, words: 340})
```

详见 [Console 与日志](../stdlib/console.md)。

### 怎么把结构化记录写到标准输出？

给 `.value` 传 `stdoutChannel`：`console.log.value(value, stdoutChannel)`，`stdoutChannel` 来自 `el:console/index.el`。程序对外交付的数据优先用 `console.stdout.write`／`writeLine` 直接写文本，日志和诊断留在 stderr，管道与重定向才不会混入噪声。

```el
import { stdoutChannel } from "el:console/index.el"

console.log.value(@{result: 42}, stdoutChannel)
```

详见 [Console 与日志](../stdlib/console.md)。

### 怎么运行一个文件？

在入口文件所在目录执行 `el run main.el`：它编译入口、立即运行，退出后删掉临时产物。要留下可交付文件用 `el build main.el`，产物的运行方式见[命令行工具](../practice/cli-tool.md)。入口文件可以用 `.el` 或 `.els`，两者共享同一套顶层语句语义。

```text
el run src/main.el
```

详见 [工具链](../toolchain.md)。

### 为什么写 `&&` 会报错？

EL 没有 `&&` 和 `||`，逻辑运算是 `!`、`&`、`|`。`&` 与 `|` 都短路，并且返回被选中操作数的原值而不归一成布尔值：`7 & 8` 得 `8`，`nil & 8` 得 `nil`。需要按条件取值时用 `if` 表达式，没有三目运算符。

```el
let label = if (count > 0) "有" else "无"
```

详见 [运算符与表达式](../language/operators.md)。

### `^` 为什么不是异或？

`^` 是普通的二元运算符，按操作数类型选择重载：`Number` 上它是乘方，`2 ^ 10` 得 1024，且右结合、右侧允许带符号；位集合类型的 `^` 才是逐位异或。对普通数字做位异或用数值库的 `bit_xor`，不要靠 `^` 去凑位运算。

```el
console.stdout.writeLine(2 ^ 10)
```

详见 [运算符与表达式](../language/operators.md)。

### try/catch 怎么取值？

`try` 是表达式，值是正常完成的 try 块或实际处理了异常的 catch 块的末尾语句结果，空块得到 `void`。`catch (error)` 的括号绑定异常对象，也可以省略绑定只处理异常；`finally` 的结果被丢弃，但清理照常执行。

```el
import { readTextFile } from "el:filesystem/index.el"

let text = try { readTextFile("config.el") } catch { "" }
```

详见 [错误处理与异步](../language/errors-async.md)。

### 为什么类必须写 `@assign`？

具名用户类型必须显式选择赋值与传参语义：`@assign(mode: "copy")` 复制出独立对象，`@assign(mode: "shared")` 共享同一个对象。语言不替你猜该用值语义还是引用语义，所以漏写就是编译错误。字段默认值写在字段声明上，构造器用 `constructor(...)` 并以 `init this` 开始。

```el
@assign(mode: "shared")
class Counter {
	let value = 0
	fn advance(amount: Number): Number {
		this.value += amount
		return this.value
	}
}
```

详见 [类与对象](../language/classes.md)。

### 程序为什么没有 `main` 函数？

EL 没有 `main`：模块顶层代码就是入口，按书写顺序执行到最后一条语句，退出码由程序自己决定。入口文件可以叫 `main.el`，也可以叫别的名字；用 `el run` 或构建后的产物启动时都从顶层语句开始。需要返回非零退出码时调用 `exit(code)`，它不会返回。

详见 [语言速览](../tour.md)。

### GUI 是 HTML 吗？

不是。EL 的界面是 EL 自己的声明对象图：节点是普通对象，布局、命中、事件和绘制都由标准库完成，平台层只提供窗口与像素表面。描述字符串里的 `<column>`、`<button>` 只是构造对象的数据，不是 DOM，也不会被当成 EL 执行；没有 CSS 的选择器与级联模型。

详见 [图形界面](../stdlib/gui.md)。

### 怎么读文件？

用 `el:filesystem/index.el` 的 `readTextFile(path)`，返回解码后的 `Text`；可选第二个参数限制最大字节数，超限抛错而不是截断。文件不存在、无权限或不是合法 UTF-8 都会抛异常，用 `try`／`catch` 处理。写文件用同模块的 `writeTextFile(path, value)`。

```el
import { readTextFile, writeTextFile } from "el:filesystem/index.el"

let text = try { readTextFile("notes.txt") } catch { "" }
writeTextFile("copy.txt", text)
```

详见 [文件与网络](../stdlib/files-network.md)。

### 怎么请求网络？

用 `el:network/index.el` 的 `fetchAs(format, url)`，格式从同模块的 `formats` 取，例如 `formats.JSON`。普通调用自动等待结果，非成功状态与解析失败都抛异常，所以常见写法是 `try` 取结果、`catch` 给默认值。需要更多控制时用同模块的 `request`。

```el
import { fetchAs, formats } from "el:network/index.el"

let config = try { fetchAs(formats.JSON, url) } catch { Json.Null }
```

详见 [文件与网络](../stdlib/files-network.md)。

### 怎么测试？

最小检查用 `assert(condition, reason)`：条件为假时以第二参数为原因抛 `AssertionError`，为真时返回真值。项目级测试用 `el test`，它读取最近 `package.eol` 里的测试配置并默认增量运行，`--full` 强制重跑所有行为用例。测试文件与断言组织见[测试](../stdlib/testing.md)。

详见 [测试](../stdlib/testing.md) 与 [工具链](../toolchain.md)。

### 怎么构建 release？

`el build --release src/main.el`：默认是 debug，`--release` 与 `--debug` 互斥。release 关闭普通数组、文本与视图的索引和范围检查，但类型、借用、所有权、生命周期检查以及 API 合同规定的失败仍然保留。两种模式共用同一条优化流水线，构建失败返回非零，不把半成品当成功。

```text
el build --release src/main.el
```

详见 [工具链](../toolchain.md)。

### 支持哪些平台？

目标平台是 Windows、Linux、macOS、FreeBSD、iOS、Android 六个，平台能力必须分开声明，不能互相推断。当前检出的 GUI 后端覆盖 Windows、Linux/X11 与 macOS，移动端和 FreeBSD 还没有对应窗口后端；编译器、运行时与标准库在各自平台上分别验收。

详见 [规范与实现边界](implementation-status.md)。

### 为什么没有 Web 目标？

目标平台清单是上面六个原生系统，不含浏览器；图形界面的设计是 EL 自绘对象图与绘制流水线，不使用可见 DOM 或 CSS 布局。规范里的浏览器条款只说明一旦存在 wasm 目标，界面视觉仍由 Canvas 自绘、语义 DOM 仅作辅助；当前平台枚举与 GUI 后端里没有 wasm，所以没有“编译成网页用 DOM 排版”的目标。

详见 [图形界面](../stdlib/gui.md) 与 [规范与实现边界](implementation-status.md)。

### 项目还在开发吗？

是。规范描述的是目标合同，部分能力已实现、部分仍在实现与验收中；本教程会在对应位置用「实现状态」注明差距，代码示例按当前规范与源码导出编写。想知道某个功能是否可用，先看那一页的实现状态说明，再对照[规范与实现边界](implementation-status.md)。

## 继续阅读

- [从其他语言过来](coming-from.md)：把熟悉语言的写法逐项翻译成 EL。
- [图形界面](../stdlib/gui.md)：GUI 的对象图、事件与定时器。
- [命令行工具](../practice/cli-tool.md)：从空目录到可交付产物的完整流程。
