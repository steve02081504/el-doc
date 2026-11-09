# 函数与闭包

函数在 EL 里是普通值：可以声明、简写、捕获周围绑定、作为实参传递。这一页讲清楚函数的各种写法和闭包语义，读完你能写出参数默认值、把 lambda 传给集合算法，也能读懂定向返回、借用来源与 `async` 块。

## `fn` 声明与 `=>` 简写

```el
fn add(a: Number, b: Number) {
	return a + b
}

fn double(value: Number) => value * 2

console.stdout.writeLine(add(1, 2))    // 3
console.stdout.writeLine(double(4))    // 8
```

- 声明用 `fn 名字(参数) 返回注解? 函数体`，返回注解可以省略。
- 块体不写 `return` 时，返回值是最后执行语句的值；写了 `return` 就提前返回。
- `=>` 简写等价于一个只有单条表达式的块体，两种写法在类型与调用语义上没有区别。
- 没有 `main` 函数，模块顶层的代码就是入口。

递归也一样写，不需要额外的声明关键字：

```el
fn factorial(n: Number): Number {
	if (n <= 1) return 1
	n * factorial(n - 1)
}

console.stdout.writeLine(factorial(5))   // 120
```

## 箭头 lambda 与匿名 `fn`

```el
let square = (value: Number) => value * value
let classify = fn(value: Number) {
	if (value < 0) return "negative"
	"non-negative"
}
let immediate = ((x: Number) => x + 1)(2)

console.stdout.writeLine(square(5))       // 25
console.stdout.writeLine(classify(-1))    // negative
console.stdout.writeLine(immediate)       // 3
```

- `(a, b) => 表达式` 与 `fn(a, b) { ... }` 都是匿名函数，区别只在写法。
- 箭头 lambda 也能写返回注解：`(value: Number): Number => value + 1`。
- 括号包住 lambda 之后可以继续普通后缀调用，例如 `((x) => x + 1)(2)`。

## 裸 `=>` 与 `it`

省略参数列表的裸箭头是动态参数模板：

```el
let negate = => -it
let doubled = @[1, 2, 3].map(=> it * 2)

console.stdout.writeLine(negate(3))   // -3
console.log.value(doubled)            // [2, 4, 6]
```

- 裸 `=> 表达式` 接受任意数量实参，`it` 默认指代第一实参；没有实参时 `it` 的值是 `void`。
- 裸箭头提供的 `it` 绑定优先于外层同名绑定；它不会捕获外层的 `it`。
- 显式写 `() => 表达式` 仍是空参数列表，其中的 `it` 按外层作用域解析。
- 无名变长参数 `fn f(...)` 的函数体里，`it` 指收到的参数集合本身。

`it` 不是关键字，只有在按普通名字解析不到绑定时才启用这条候选链；显式声明了名为 `it` 的绑定时以显式绑定为准。

## 默认参数

```el
fn greet(name: Text = "world") => `Hello, ${name}!`
fn area(width: Number, height: Number = width) => width * height
fn pick(value: any = 0) => value

console.stdout.writeLine(greet())        // Hello, world!
console.stdout.writeLine(greet(void))    // Hello, world!
console.stdout.writeLine(area(3))        // 9
console.stdout.writeLine(area(3, 4))     // 12
console.log.value(pick(nil))             // nil：默认值不触发
```

- 实参省略或实参为 `void` 时求默认表达式；`nil` 不触发默认值。
- 参数从左到右初始化；默认表达式可以引用前面已初始化的参数和函数可见的外部绑定，不能引用尚未初始化的后续参数。
- 默认表达式的副作用、异常、异步与族属性参与函数属性推断。
- 调用时可以用 `名: 值` 形式的关键字传参：`area(3, height: 4)`；位置实参在前，关键字实参在后。

## 函数类型

函数类型只描述参数与返回形状：

```el
let combine: (Number, Number) => Number = (a, b) => a + b
let reader: () => Text = () => "value"

console.stdout.writeLine(combine(2, 3))   // 5
console.stdout.writeLine(reader())        // value
```

- 多参数写 `(A, B) => C`；无参数写 `() => C`。
- 单参数值函数有简写 `A -> B`，它右结合：`A -> B -> C` 表示 `A -> (B -> C)`，不是三参数函数。
- 异常、异步、族、纯性等属性属于完整签名，由推断与声明共同约束，不写在普通函数类型里。

## 闭包捕获绑定

lambda 自动捕获它引用的外层绑定，捕获的是**绑定**，不是值快照：

```el
let x = 1
let read = () => x
x = 2
console.stdout.writeLine(read())   // 2

fn makeCounter(): () => Number {
	let count = 0
	return () => {
		count += 1
		count
	}
}

let counter = makeCounter()
console.stdout.writeLine(counter())   // 1
console.stdout.writeLine(counter())   // 2
```

- 对捕获绑定的后续赋值，闭包都能看到；即使赋值换了绑定类型，闭包观察到的也是新值。
- 多个 lambda 捕获同一个 `let` 时，它们看到的是同一个绑定，彼此能看到对方的写入。
- lambda 可以写回捕获的绑定；逃逸的闭包保持该绑定有效。
- 范围循环的元素变量作用域限于循环体，每轮迭代不跨轮保留状态；闭包捕获它时按该轮的元素绑定处理。

## 把 lambda 传给集合算法

数组的 `map`、`filter` 等接受普通可调用值，lambda、裸箭头、具名函数都可以：

```el
let numbers = @[1, 2, 3, 4]
let squared = numbers.map(value => value * value)
let evens = numbers.filter(value => value % 2 == 0)

console.stdout.writeLine(numbers.join(", "))   // 1, 2, 3, 4
console.log.value(squared)                     // [1, 4, 9, 16]
console.log.value(evens)                       // [2, 4]
console.log.value(numbers.map(square))         // 具名可调用值同样可以传
```

`map` 的参数是上一节声明的 `square`，传的是函数值本身，不是调用结果。集合算法如何迭代、返回什么类型，见[集合与文本](../stdlib/collections.md)。

## 定向返回：从外层具名函数返回

普通 `return` 只结束当前函数。写 `return 值 from 目标` 可以越过当前的 lambda、回调或局部函数，直接结束一个词法上在外围的具名函数。目标写成函数名，并且按词法作用域解析，不是运行时搜索最近的同名函数。

### 三种写法

```el
fn invoke(callback) {
	callback()
}

fn finish() {
	invoke(fn() {
		return from finish
	})
}

fn finishExplicitly() {
	invoke(fn() {
		return void from finishExplicitly
	})
}

fn findName(target: Text) {
	for (let name in @["Ada", "Grace", "Linus"]) {
		if (name == target) return name from findName
	}
	throw StateError("not found")
}
```

- `return value from func` 把一个值交给目标函数的调用者，并结束目标的那次调用。
- `return from func` 是无值形式，和普通无值 `return` 一样返回 `void`。
- `return void from func` 是显式写出返回 `void` 的版本，与前一种等价。

`from` 后面的名字不是被求值的实参，也不参与返回值表达式；它是 return 语句的目标分隔符。嵌套括号内部按普通表达式解析，不会把 `from` 当成返回值的一部分。

### 词法目标，不是运行时最近同名

目标在当前词法作用域里向外查找，可以是当前函数、外围具名函数、具名方法或局部具名函数；找到的声明就是目标。目标必须唯一：同一次查找只应命中一个声明，内层同名声明按遮蔽规则胜出。名字不存在、不是允许的函数目标、有歧义，或者返回值不满足目标的返回合同，都属于 ELC 的良构错误。

```el
fn outer() {
	fn middle() {
		fn inner() {
			return 7 from middle   // 只结束 middle，不会直接结束 outer
		}
		inner()
	}
	middle()
}
```

`inner` 里的定向返回结束 `middle`，`middle` 再把值交给 `outer`。如果目标写 `outer`，就结束 `outer`；写哪个名字只结束哪个具名函数。

同名遮蔽也按声明身份处理：

```el
fn shadow() {
	fn shadow() {
		invoke(fn() { return 8 from shadow })   // 目标是内层 shadow 的这次调用
		return 0
	}
	return shadow()
}
```

内层 `shadow` 遮蔽外层同名声明，回调里的目标因此绑定到内层的这次 activation。匿名函数没有名字，不能凭编译器内部名字成为目标；变量里保存的 lambda 也不是具名目标，能指名的只有具名函数声明、具名方法和局部具名函数。

### 返回类型与 `Never`

目标的返回类型推断包含所有 `return ... from 目标` 的返回值，不只包含目标函数体里的普通 `return`。所以 `findName` 即使唯一的正常返回写在循环体里，也能从 `name` 推断出返回 `Text`。

定向返回本身不产生可读取的值，它的类型是 `Never`。因此它可以放在表达式位置或分支里，不会给类型合流制造一个假的 `void` 或其它分支值：

```el
fn requireReady(ready: Bool) {
	if (!ready) return from requireReady
	performWork()
}
```

### 执行边界

每次函数调用建立独立的逻辑 activation；定向返回捕获的是那次调用的目标 token，而不是函数代码地址。递归、重入、内联和尾递归帧复用都不能把旧 token 指向另一次调用。

- 在同一条逻辑调用链上普通挂起不会结束目标：回调里先 `sleep` 或等待 I/O，恢复后仍然可以 `return ... from 外层`。
- 独立 `spawn` 出来的 task 不继承父目标的返回能力；`async {}` 建立的也是独立 task，里面的定向返回不能跨回启动它的函数。ELF 会按可调用效果检查这种调用，运行时不能依赖一个无效目标。
- 目标已经退出，或已经开始不可逆退出清理（Exiting），就不再接受新的返回。闭包捕获对象能保住闭包的值，但不能恢复已经退出的函数 activation。
- 没有有效目标属于运行时 UB。ELC 只检查目标的词法名字、类别、唯一性和返回类型这些良构条件；目标是否仍活着、是否在当前 task 的允许返回链上，由 ELF 在调用执行时证明，证明不了就报告 error，不会因此把良构程序判成 ELC 编译失败。

```el
import { sleep } from "el:concurrency/"

fn load(): Text {
	invoke(fn() {
		sleep(1)                    // 普通挂起后目标仍然有效
		return "ready" from load
	})
	throw StateError("unreachable")
}

fn capture(): () => Number {
	return fn() { return 5 from capture }
}

let expired = capture()
expired()   // 没有有效目标：capture 已经退出，不能借旧 token 复活
```

这段只用于说明边界：没有有效目标时行为没有可依赖的定义；ELF 对这类调用无法建立有效目标证明时就报告 error，不能把它当成恢复已退出帧的手段。

清理路径同样受约束：`finally` 里新起的普通 `return`、`break`、`continue` 或定向返回不能覆盖正在进行的跨层返回；局部循环的 `break`/`continue`，以及清理中新建的 helper 里只结束该 helper 的局部定向返回，不受影响。

## 生命周期与借用

EL 没有 Rust 式显式生命周期参数（`'a`）；对象何时析构、引用能用多久，由 `@assign`/`@destruct`、来源描述符与借用规则推断，而不是靠命名生命周期。

这一页只保留和函数写法直接相关的入口：

- `borrow`/`ref` 参数是借用，不接管所有权；`take` 接管，`rvalue` 限定实参为右值。
- 返回引用写 `borrow T from source` 或 `ref T from source`；`: forward` 按返回表达式推断类别与来源。
- `scope let` 与 `@destruct(mode: "scope")` 把对象至少保到名称作用域结束；`ptr<noescape>` 约束原生指针不被长期保存。

完整规则、析构时机例子和常见陷阱见[生命周期与析构](lifetimes.md)。

## 自动等待与 `async`/`await` 宏

函数是否异步由函数体自动推断，普通调用会自动等待实际挂起，调用者随之被推断为异步；不需要也不允许在函数签名上标记。

需要显式并发时才写 `async`。`async { ... }` 和 `await(p)` 不是关键字，而是标准库提供的 Expr 宏：`async { ... }` 把块内容解析成一个新的零参 callback，再立即 `spawn` 它，返回 `Promise`；`await(p)` 只对接收者生成一次 `.get()`。

```el
let work = async {
	let total = 0
	for (let n in @[1, 2, 3]) {
		total += n
	}
	total
}

console.stdout.writeLine(await(work))   // 6
```

- `async` 表达式执行时活动就已经启动，不会等到 `await` 才启动。
- `await(p)` 只生成一次 `p.get()`，接收者只求值一次；它不额外复制 `Promise`，不捕获错误，也不会递归展平结果本身仍是 `Promise` 的情况。
- `async` 里的普通 `return` 属于那个 callback，不是外围函数；独立 task 之间的定向返回仍受本页“执行边界”的约束。
- 默认标准库通过显式的惰性导出提供 `async` 与 `await`；关闭默认前导或写自定义模块时，从 `el:concurrency/` 普通导入。
- `spawn` 显式启动独立任务并返回 `Promise`；保存 `Promise` 不会等待，`get()` 才等待结果。

并发写法、`Promise` 组合与取消见[错误处理与异步](errors-async.md)。

## `@pure`

`@pure` 是显式的纯性求值合同，编译器信任这个标注：

```el
@pure fn cube(value: Number) => value * value * value

console.stdout.writeLine(cube(3))   // 27
```

输入在编译期能确定时，这类函数必须在编译期完成求值并物化结果；输入只能在运行期确定的，就像普通函数一样执行。纯性不表示函数不会抛错，异常始终可观察，也不会因标注而消失。

## 继续阅读

- [生命周期与析构](lifetimes.md)：对象何时析构、引用何时失效，以及 `scope let`、`take`、`borrow` 的完整规则。
- [类与对象](classes.md)：把方法、构造与析构写进类型里。
- [控制流](control-flow.md)：函数体里的分支、循环与隐式返回值。
- [错误处理与异步](errors-async.md)：异常、任务与并发集合。
