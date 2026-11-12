# 语言速览

> 十五分钟，六站。每一站先猜一个输出，再跑一次代码；最后一站你会用它们拼出一个能跑的小程序。

!!! abstract "🎯 读完这页，你能"
    - 认出 EL 程序的常见形状：没有 `main`、`if` 和 `try` 是表达式、类要声明 `@assign`
    - 写出函数、集合、类、错误处理和并发的最小例子
    - 说清三处最容易从别的语言带过来的错觉

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[安装与第一个程序](getting-started.md)</span>

这一页适合已经会编程、想快速比较写法的读者。第一次学编程时，先走[零基础路线](beginner/index.md)，不用在一页里同时掌握函数、类和并发。下面各段是独立片段，不需要依次拼进同一个文件。

## 第一站：值与输出

```el
let item = "笔记本"
let quantity = 3

console.stdout.writeLine(item, " ", quantity, " 本")
```

```text
笔记本 3 本
```

- `let` 声明可写绑定，不写类型注解时可以换类型。
- `quantity` 记录数量。EL 的日常数字是精确有理数，不是固定位宽整数。
- `writeLine` 接受多个参数，逐个做 `Text` 转换后写出，不自动加空格；上面的空格是显式写出来的。
- 没有 `main`，模块顶层代码就是入口。

??? question "先猜：物品与数量之间的空格是谁加的？"
    `writeLine` 不负责加空格，第二个参数就是 `" "`。去掉它，物品和数量就会连在一起显示。

## 第二站：函数与集合

```el
fn costForTwo(price: Number) => price * 2

let prices = @[4, 2, 3]
let costs = prices.map(costForTwo)

for (let cost in costs) {
	console.stdout.writeLine("买两件：", cost, " 元")
}
```

```text
买两件：8 元
买两件：4 元
买两件：6 元
```

`fn name(...) => expression` 是表达式体函数，不写 `return` 时返回最后一条语句的值。这里每种商品都买两件，`map` 对每个单价调用同一个总价函数，得到一份小计清单，再用循环输出。

## 第三站：控制流是表达式

```el
fn gradeOf(score: Number) {
	if (score >= 90) "A"
	else if (score >= 60) "B"
	else "C"
}

console.stdout.writeLine(gradeOf(72))
```

```text
B
```

`if` 不只是语句，它产生值；函数没写 `return` 时，返回值就是最后执行的 `if` 的结果。这省掉了大量“先声明变量、再在分支里赋值、最后 return”的样板。

循环也可以逐项累计开支：

```el
let total = 0
for (let cost in @[12, 10, 6]) {
	total += cost
}
console.stdout.writeLine("合计：", total, " 元") // 合计：28 元
```

!!! tip "回头看一眼"
    第二站的 `costForTwo` 用表达式直接返回两件商品的总价。调用它时拿到的是数字，所以还可以继续求和。

## 第四站：类与对象

```el
@assign(mode: "shared")
class Counter {
	let value: Number = 0

	constructor(start: Number = 0) {
		this.value = start
	}

	fn advance(step: Number = 1) {
		this.value += step
		return this.value
	}
}

let counter = Counter(5)
console.stdout.writeLine(counter.advance(3))
```

```text
8
```

- 类声明前必须写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，明确普通赋值是复制还是共享。没有默认值。
- 构造器用 `constructor`，实例用 `Counter(5)` 创建，不需要 `new`。
- 方法里可以省略 `this.` 读成员，但写清楚更好读。
- 对象字面量 `@{ name: "Ada" }` 是另一条路：匿名、共享、字段可写，没有方法和继承。需要行为时用 `class`。

??? question "先猜：漏写 `@assign` 会怎样？"
    编译错误。EL 不替你挑默认语义：普通赋值到底是复制整个对象还是共享同一份数据，必须由类自己声明，调用方才不用猜。

## 第五站：错误可以被当成值处理

```el
fn divide(a: Number, b: Number) {
	if (b == 0) throw Error("division by zero")
	a / b
}

let result = try {
	divide(10, 0)
} catch (error) {
	console.warning.value(error)
	0
}

console.stdout.writeLine("result: ", result)
```

```text
result: 0
```

`try` 在表达式位置产生值：正常完成取 try 块的结果，捕获到异常时取 catch 块的结果。`console.warning.value` 按 warning 等级展示错误对象，不把它转成文本。

!!! warning "常见坑：`try` 是值，不是语句"
    `try { ... } catch { ... }` 的结果可以直接赋给变量、直接 `return`。写成“先声明 result，再在 try 里赋值、catch 里再赋值”不是不行，只是多了一层样板，也更容易漏掉一条路径。

## 第六站：异步与并发

普通调用会自动等待异步结果。需要显式并发时，用标准库的 `async { ... }` 立即启动一个任务，再用 `await(p)` 等它：

```el
let first = async {
	return 40 + 2
}
let second = async {
	return 8
}

console.stdout.writeLine("sum: ", await(first) + await(second))
```

```text
sum: 50
```

`async { ... }` 和 `await(p)` 是标准库宏，不是关键字：`async` 建立真实 callback 并立刻 `spawn`，返回 `Promise`；`await` 只生成一次 `.get()`。也可以直接用 `spawn(fn() { ... })` 启动任务、用 `.get()` 等待。多个任务、取消和并发集合在[错误处理与异步](language/errors-async.md)里展开。

??? question "先猜：`async` 和 `await` 是关键字吗？"
    不是，它们是标准库宏。这也是为什么搜索语法高亮时找不到它们、为什么 `await` 只能包住一个 Promise 表达式——宏展开后就是一次 `.get()`。

!!! warning "常见坑：以为没写 `await` 就没有等待"
    普通调用自动等待异步结果，不会返回一个“还在跑”的东西给你。显式并发只发生在 `async` 或 `spawn` 启动任务的时候。

## 把它们拼起来：任务清单

下面是一个完整的小程序：任务清单。它用了类、数组、函数、错误处理和结构化日志。

```el
@assign(mode: "shared")
class Task {
	let title: Text
	let done: Bool = nil

	constructor(title: Text) {
		this.title = title
	}

	fn finish() {
		this.done = t
	}

	fn label() => (if (this.done) "[x] " else "[ ] ") + this.title
}

fn addTask(tasks: Task[], title: Text) {
	if (title.count == 0) throw Error("task title must not be empty")
	tasks.push(Task(title))
}

let tasks: Task[] = @[]
addTask(tasks, "read the tour")
addTask(tasks, "write a program")
tasks[0].finish()

for (let task in tasks) {
	console.stdout.writeLine(task.label())
}

let finished = tasks.filter((task) => task.done).count
console.info.value(@{ total: tasks.count, finished })
```

运行后终端大致是：

```text
[x] read the tour
[ ] write a program
```

此外，`console.info.value` 会展示任务总数和完成数的结构化记录，默认走 stderr，不属于上面两行 stdout。具体呈现由终端或 GUI console 决定。

!!! example "动手 5 分钟"
    在这个程序上加三样东西：先新增一条任务，运行后应多一行 `[ ]`。再完成第二条任务，应看到第二行变为 `[x]`。最后尝试添加空标题，确认它抛出错误而不会加入清单。每次只做一项，保留已经正确的结果。

## 你已经见过了什么

| 概念 | 写法 | 去哪补细节 |
| --- | --- | --- |
| 变量 | `let`、`const` | [值与类型](language/values.md) |
| 精确数字 | `Number`、`1/3` | [值与类型](language/values.md) |
| 函数 | `fn name(...) => ...` | [函数与闭包](language/functions.md) |
| 集合 | `@[...]`、`map`、`filter`、`join` | [集合与文本](stdlib/collections.md) |
| 控制流 | `if`、`for`、`while`、`switch` | [控制流](language/control-flow.md) |
| 类 | `@assign`、`constructor`、`fn` | [类与对象](language/classes.md) |
| 错误 | `throw`、`try`/`catch` | [错误处理与异步](language/errors-async.md) |
| 并发 | `async`、`await`、`spawn`、`.get()` | [错误处理与异步](language/errors-async.md) |
| 输出 | `console.stdout.writeLine`、`.value` | [Console 与日志](stdlib/console.md) |

## 带走这三样

- 没有 `main`，顶层代码就是入口；`if`、`try`、块都能产生值。
- `writeLine` 不自动加空格，输出格式要自己写清楚。
- `async`/`await` 是宏，普通调用自动等待；类必须声明 `@assign`。

!!! success "检查点"
    - [ ] 每一站的代码你都在 REPL 或文件里跑过至少一次
    - [ ] 你能说出三处和 JavaScript／Python 不一样的地方
    - [ ] 任务清单程序能加上你自己的功能并跑通

## 下一站：语言总览

> 速览里每站都只有几行，真正的规则和边界在哪？

- 主推进：[语言总览](language/index.md)：15 页怎么排、哪些必读、哪些可以跳。
- 想直接开写：[命令行工具](practice/cli-tool.md)：用一个完整项目练手。
- 想先补基础：[值与类型](language/values.md)：把 `let`、`Number`、`Text` 和集合讲清楚。
