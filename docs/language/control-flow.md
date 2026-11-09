# 控制流

EL 的语句都有值，`if` 本身就是表达式。这一页讲条件、循环、`switch` 与跳转，读完你能用表达式风格写出分支和循环，而不是先声明变量再到处赋值。

## `if` 是表达式

```el
let score = 72
let grade = if (score >= 90) { "A" } else if (score >= 60) { "B" } else { "C" }

console.stdout.writeLine(grade)   // B
```

- 每个分支是一个块，块的值就是它最后执行语句的值；`if` 的值取被选中分支的值。
- 没有 `else` 且条件为假时，结果是 `void`：

```el
let bonus = if (score > 100) { "extra" }
console.log.value(bonus)   // void
```

- 条件不需要外层括号，圆括号只用于表达式分组：

```el
if score >= 60 {
	console.stdout.writeLine("pass")
}
```

- `else` 结合最近的、尚未匹配的 `if`，嵌套时按这个规则读，不要靠缩进猜。
- `if` 的值可以直接作为初始化器、实参或隐式返回值，不要求先赋给变量。

## `while` 与 `do while`

```el
let count = 0
while (count < 3) {
	console.stdout.writeLine(count)
	count += 1
}

let attempts = 0
do {
	attempts += 1
} while (attempts < 2)
```

- `while` 的条件同样可以省略外层括号；`do while` 的尾部条件要求括号。
- `do while` 先执行一次循环体再检查条件，所以循环体至少执行一次。
- 两个循环的值都按“最后执行语句的值”规则；零次迭代时值是 `void`。

## C 风格 `for`

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
- 零次执行时循环的值是 `void`，`break`/`continue` 保留此前最后产生的语句值。

## 范围循环

```el
let names = @["Ada", "Grace", "Linus"]

for (let name in names) {
	console.stdout.writeLine(name)
}

for (let i in 0..3) {
	console.stdout.writeLine(i)    // 0 1 2
}
for (let i in 0..|3) {
	console.stdout.writeLine(i)    // 0 1 2 3
}

for in 0..3 {
	console.stdout.writeLine(it)   // 省略变量：it 指代当前元素
}
```

- 带 `in` 的头部括号可省略；省略元素变量时写 `for in c` 或直接 `for c`，循环体用 `it` 指代元素。
- 同一个 `for` 内不能混写三段式与范围循环的片段；三段式必须带括号。
- 循环自动等待迭代结果、结束信号和清理，没有单独的 `for await` 语法。
- 元素按元素类型的复制/共享协议交给循环体：共享类型元素改字段会反映到容器；整体重绑元素变量不会写回容器槽位。

## `switch`

```el
let command = "start"

switch (command) {
	case "start" => console.stdout.writeLine("starting")
	case "stop" => console.stdout.writeLine("stopping")
	default => console.stdout.writeLine("unknown")
}
```

- selector 只求值一次；普通 `case` 按顺序用 `==` 比较，只求值实际检查到的表达式。
- 不贯穿：分支执行完直接离开 `switch`。`break` 不退出 `switch`，而是作用于外围循环；没有外围循环时报错。
- `case` 用 `=>` 分隔，不用冒号。
- 函数 case 写 `case predicate => ...`，会以 selector 为实参调用它，并沿用 `if` 的条件语义：

```el
let isReady = fn(state: Text) => state == "ready"

switch (command) {
	case isReady => console.stdout.writeLine("ready")
	default => console.stdout.writeLine("wait")
}
```

- `switch` 的值由展开后的 `if` 链决定，因此同样遵守分支取值规则。

## `break`、`continue` 与标签

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

- 标签只标循环，写法是 `name: for (...)`（`while`、`do while`、范围循环同样可用）。
- `break name` 结束目标循环，`continue name` 结束目标循环的当前轮。
- 标签有独立的控制目标命名空间，内层同名标签遮蔽外层；不能把标签指向非循环语句。
- 不带标签的 `break`/`continue` 作用于最近的适用循环。

## 所有语句都有值

函数没写 `return` 时，返回值就是最后执行语句的值：

```el
fn sumTo(limit: Number): Number {
	let total = 0
	for (let i in 1..|limit) {
		total += i
	}
	total
}

fn describe(value: Number): Text {
	if (value < 0) "negative"
	else if (value == 0) "zero"
	else "positive"
}

console.stdout.writeLine(sumTo(4))       // 10
console.stdout.writeLine(describe(-5))   // negative
```

- 循环零次执行时值是 `void`；`break`/`continue` 保留此前最后产生的语句值，没有则为 `void`。
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
fn fizzbuzz(n: Number): Text {
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

## 继续阅读

- [运算符与表达式](operators.md)：条件里用到的比较、逻辑与空值合并。
- [函数与闭包](functions.md)：把控制流封进函数，以及隐式返回值。
- [值与类型](values.md)：`Bool`、`t`/`nil`/`void` 的判定规则。
