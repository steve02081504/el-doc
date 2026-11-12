# 控制流

> `if`、块、循环都产生值。认出这一点，很多“先声明一个变量、再到处赋值”的写法就没有必要了。

!!! abstract "🎯 读完这页，你能"
    - 把 `if` 的值直接当初始化器、实参或返回值用
    - 在 `while`、C 风格 `for`、范围循环之间选对那一个
    - 用 `switch` 和带标签的 `break`／`continue` 把嵌套拉平
    - 判断什么时候该用受限的 `goto`

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[运算符与表达式](operators.md)</span>

## 一句话结论

==EL 没有“语句不产生值”这回事：分支、循环、块都产生值，函数的返回值就是最后执行那条语句的值。==

## `if` 是表达式，值从被选中的分支来

给借阅记录生成状态文字，方便打印提醒。读完时标为“可以还书”，否则标为“继续阅读”。

```el
let pagesRead = 72
let totalPages = 100
let status = if (pagesRead >= totalPages) { "可以还书" } else { "继续阅读" }

console.stdout.writeLine(status)   // 继续阅读
```

- 每个分支是一个块，块的值就是它最后执行语句的值；`if` 的值取被选中分支的值。
- 没有 `else` 且条件为假时，结果是 `void`：

```el
let reminder = if (pagesRead >= totalPages) { "请在周五前归还" }
console.log.value(reminder)   // void：尚未读完，这次没有生成归还提醒
```

- 条件不需要外层括号，圆括号只用于表达式分组：

```el
if pagesRead >= totalPages {
	console.stdout.writeLine("请带上这本书")
}
```

- `else` 结合最近的、尚未匹配的 `if`，嵌套时按这个规则读，不要靠缩进猜。
- `if` 的值可以直接作为初始化器、实参或隐式返回值，不要求先赋给变量。

!!! example "动手 30 秒"
    把 `pagesRead` 改成 `100` 再跑，第一个输出变成“可以还书”。改成 `99`，应仍为“继续阅读”。先预测，后核对。

## 循环也返回最后那条语句的值

```el
let saved = 0
while (saved < 30) {
	saved += 10
	console.stdout.writeLine("已攒：", saved, " 元")
}

let attempts = 0
do {
	attempts += 1
} while (attempts < 2)
```

第一段依次显示已攒 10、20、30 元：每轮存入 10 元，到达目标后停止。下面的 `do while` 片段用来对比执行顺序，最终 `attempts` 是 `2`。

- `while` 的条件同样可以省略外层括号；`do while` 的尾部条件要求括号。
- `do while` 先执行一次循环体再检查条件，所以循环体至少执行一次。
- 两个循环的值都按“最后执行语句的值”规则；零次迭代时值是 `void`。

## 需要计数器时：C 风格 `for`

```el
for (let i = 0; i < 3; i += 1) {
	console.stdout.writeLine(i)   // 0 1 2
}

let sum = 0
for (let i = 1; i <= 10; i += 1) {
	sum += i
}
console.stdout.writeLine(sum)   // 55
```

- 三段式必须带括号，形式是 `for (init; cond; step) statement`。
- `init` 里声明的 `let` 只在循环内可见；省略 `cond` 视为 `t`。
- `continue` 先执行 `step` 再判断条件；`break` 跳过 `step`。
- 零次执行时循环的值是 `void`，`break`／`continue` 保留此前最后产生的语句值。

!!! warning "常见坑：`in` 形式能省括号，三段式不能"
    **现象。** 写惯了 `for (let name in names)`，改成 `for let i = 0; i < 3; i += 1` 就报语法错误。**原因。** 只有带 `in` 的头部可以省略括号。**改法。** 三段式一律写 `for (...)`，别跟 `in` 形式混。

## 迭代用范围循环

```el
let reminders = @["带水杯", "还图书", "整理书包"]

for (let reminder in reminders) {
	console.stdout.writeLine("明日提醒：", reminder)
}

for (let day in 1..4) {
	console.stdout.writeLine("第 ", day, " 天读 10 页") // 第 1、2、3 天
}
for (let day in 1..|4) {
	console.stdout.writeLine("第 ", day, " 天读 10 页") // 第 1、2、3、4 天
}

for in reminders {
	console.stdout.writeLine("明日提醒：", it) // 省略变量：it 指代当前提醒
}
```

- 带 `in` 的头部括号可省略；省略元素变量时写 `for in c` 或直接 `for c`，循环体用 `it` 指代元素。
- 同一个 `for` 内不能混写三段式与范围循环的片段；三段式必须带括号。
- 循环自动等待迭代结果、结束信号和清理，没有单独的 `for await` 语法。
- 元素按元素类型的复制／共享协议交给循环体：共享类型元素改字段会反映到容器；整体重绑元素变量不会写回容器槽位。

## `switch` 不贯穿，`case` 用 `=>` 分隔

```el
let command = "start"

switch (command) {
	case "start" => console.stdout.writeLine("starting")
	case "stop" => console.stdout.writeLine("stopping")
	default => console.stdout.writeLine("unknown")
}
```

??? question "先猜：在 `switch` 的某个 `case` 里写 `break`，会跳出 `switch` 吗？"
    不会。`switch` 分支执行完直接离开，不需要 `break`；写在这里的 `break` 作用于外围循环，没有外围循环时直接报错。这是从 C 系语言带过来的最贵的一个习惯。

- selector 只求值一次；普通 `case` 按顺序用 `==` 比较，只求值实际检查到的表达式。
- 不贯穿：分支执行完直接离开 `switch`。
- `case` 用 `=>` 分隔，不用冒号。
- `switch` 的值由展开后的 `if` 链决定，因此同样遵守分支取值规则。

函数 case 写 `case predicate => ...`，会以 selector 为实参调用它，并沿用 `if` 的条件语义：

```el
let isReady = fn(state: Text) => state == "ready"

switch (command) {
	case isReady => console.stdout.writeLine("ready")
	default => console.stdout.writeLine("wait")
}
```

## 带标签的 `break`／`continue`：少一层嵌套

```el
outer: for (let i in 0..3) {
	for (let j in 0..3) {
		if (j == 1) continue outer
		if (i == 2) break outer
		console.stdout.writeLine(i, "-", j)
	}
}
```

输出是 `0-0` 与 `1-0`，第三轮在 `j == 0` 时被 `break outer` 结束。

- 标签写作 `name: statement`，可以标在循环上，也可以标在显式块上；标在普通语句上时只提供一个跳转入口。
- `break name` 结束目标循环或目标块，`continue name` 只对循环成立，结束目标循环的当前轮。
- 标签有独立的控制目标命名空间，内层同名标签遮蔽外层；同一块内不能重名。
- 不带标签的 `break`／`continue` 作用于最近的适用循环。

## 受限制的 `goto`：重试一段区域，或一次跳出多层

多数情况用 `break` 和 `continue` 就够了，`goto` 留给两类场景：重试一段已经建好的区域，以及从多层嵌套里一次跳到收尾。它是结构化的、受检查的跳转，不是可以指向任意地址的汇编跳转。

标签写作 `name: statement`；空的落点写 `done: ;`。标在显式块上的标签同时提供入口与 `break` 出口，标在循环上的标签还多一个 `continue` 继续边。`goto` 只能选中入口，不能当 `continue` 用。

```el
let attempts = 0
retry: {
	attempts += 1
	if (attempts < 3) goto retry
	console.stdout.writeLine("ready after ", attempts)
}
```

`goto retry` 跳到块入口：离开当前区域时先执行该区域的 `finally`、局部变量与临时值清理，清理成功后才落到入口。块被重新建立，`attempts` 声明在块外，所以状态保留，第三次进入时才打印 `ready after 3`。

向前跳同样合法，常用来跳出多层嵌套：

```el
let words = @["alpha", "", "beta"]
let found = ""
scan: for (let word in words) {
	if (word == "") break scan
	if (word == "beta") goto done
	found = word
}
done: ;
console.stdout.writeLine(found)
```

`done: ;` 是块内的空语句，只作为落点；`goto done` 先结束 `for` 的游标和本轮局部状态，再继续执行标签后面的语句，所以不会跳过 `found` 的声明或它的清理义务。

`goto` 的边界比普通跳转语言严格得多：

- 只能在同一函数、同一次 activation 内跳转，不能跨 lambda、任务、ABI 边界或续行。
- 不能从外部跳进嵌套块、`try`／`catch`／`finally` 或循环体内部，也不能跳过局部声明去使用尚未建立的变量。
- 跳到整个块或整个循环的入口是合法的，那会重新建立该区域；跳进循环体内部则不合法。
- 跳往循环标签会关闭旧游标并从入口重建循环，不执行 `continue` 的步进，也不保证旧 `for` 的 step 语义。
- 离开区域时先完成清理，清理失败会代替这次跳转；异步清理要等待完成。
- 标签本身不是值，不能保存、传递、比较或取地址。

可以跳到 `block` 或 `while` 这一级的入口，因为入口正是区域开始建立的地方；但不能越过入口直接落到循环体中间的某条语句，那里的局部状态还没有建立。这条规则和“所有语句都有值”是同一套清理模型的两面：跳转不能制造一个清理责任说不清的状态。

`goto` 也不替代 `continue`。需要“进入下一轮但保留循环状态”时写 `continue`；需要“把整个循环从初始化重新走一遍”时才写 `goto` 到循环标签。

`break name` 也可以提前结束一个带标签的块，这在参数校验里比多层 `if` 更平：

```el
let path = "src/main.el"
check: {
	if (path == "") break check
	if (!path.endsWith(".el")) break check
	console.stdout.writeLine("compiling ", path)
}
console.stdout.writeLine("done")
```

`break check` 只离开 `check` 块，不会影响外层循环；块结束后的语句照常执行。块本身没有“失败原因”载荷，需要区分成功与提前退出时，把状态写在块外的变量里。

## 函数不写 `return`，返回值就是最后一句

```el
fn sumTo(limit: Number) {
	let total = 0
	for (let i in 1..|limit) {
		total += i
	}
	total
}

fn describe(value: Number) {
	if (value < 0) "negative"
	else if (value == 0) "zero"
	else "positive"
}

console.stdout.writeLine(sumTo(4))       // 10
console.stdout.writeLine(describe(-5))   // negative
```

- 循环零次执行时值是 `void`；`break`／`continue` 保留此前最后产生的语句值，没有则为 `void`。
- 空函数体、空块的值是 `void`。显式写出无结果用 `return void`，显式返回假值用 `return nil`。
- `return`、`throw` 这类不继续的控制转移不产生可读取的占位值，分支类型合并时忽略它们。

```el
fn doNothing(): void_t {
	return void
}

console.log.value(doNothing())   // void
```

## 完整例子：FizzBuzz

```el
fn fizzbuzz(n: Number) {
	if (n % 15 == 0) "FizzBuzz"
	else if (n % 5 == 0) "Buzz"
	else if (n % 3 == 0) "Fizz"
	else Text(n)
}

for (let n in 1..|15) {
	console.stdout.writeLine(fizzbuzz(n))
}
```

```text
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

## 完整例子：查找

```el
let words = @["alpha", "beta", "gamma"]
let found: Text | void_t = void

for (let word in words) {
	if (word == "beta") {
		found = word
		break
	}
}

if (found is Text) {
	console.stdout.writeLine(found)       // beta
} else {
	console.stdout.writeLine("not found")
}
```

`found` 被声明为 `Text | void_t`，循环外仍然保留这个类型；`is` 判断让你在分支里安全使用它，不需要先塞一个假字符串当“没找到”。

## 带走这三样

- `if`、块、循环都产生值；函数不写 `return` 时返回最后执行语句的值。
- `switch` 不贯穿、`case` 用 `=>`；在里面写 `break` 是错误习惯，它管的是外围循环。
- 先用带标签的 `break`／`continue`，`goto` 只负责重试区域和一次跳出多层。

## 下一站：函数与闭包

> 既然返回值就是最后一句，`return 值 from 外层函数` 又是干什么的？

- 主推进：[函数与闭包](functions.md)：把控制流封进可复用的块，并读懂定向返回与闭包捕获。
- 想补条件里用到的运算符：[运算符与表达式](operators.md)。
