# 函数与闭包

> 函数在 EL 里是普通值：能声明、能简写、能被捕获、能当实参传。难的不是写法，是搞清闭包到底捕获了什么。

!!! abstract "🎯 读完这页，你能"
    - 用 `fn`、箭头 lambda、裸 `=>` 三种写法，按场景挑
    - 写出默认参数、函数类型注解与关键字传参
    - 判断闭包捕获的是值还是绑定
    - 用定向返回从回调里结束外层函数，知道它的边界

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[控制流](control-flow.md)</span>

## 一句话结论

==函数是值；闭包捕获的是**绑定**而不是快照；普通调用自动等待，不需要标记。==

## 三种写法，同一种东西

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
- `=>` 简写等价于单表达式块体，两种写法在类型与调用语义上没有区别。
- 没有 `main` 函数，模块顶层的代码就是入口。

递归同样写：

```el
fn factorial(n: Number): Number {
	if (n <= 1) return 1
	n * factorial(n - 1)
}

console.stdout.writeLine(factorial(5))   // 120
```

`fn` 和 `let` 声明都能自指；用 `let` 绑定匿名函数也能写递归：

```el
let factorialValue = (n: Number): Number => if (n <= 1) { 1 } else { n * factorialValue(n - 1) }

console.stdout.writeLine(factorialValue(5))   // 120
```

这里创建闭包时捕获自身绑定，调用时绑定已经初始化；这不意味着可以在初始化完成前读取自身的值。

匿名函数也能写：

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

- `(a, b) => 表达式` 与 `fn(a, b) { ... }` 都是匿名函数，区别只在写法；箭头 lambda 也能写返回注解 `(value: Number): Number => value + 1`。
- 括号包住 lambda 之后可以继续普通后缀调用，例如 `((x) => x + 1)(2)`。

## 裸 `=>` 与 `it`：参数可以省略

```el
let negate = => -it
let doubled = @[1, 2, 3].map(=> it * 2)

console.stdout.writeLine(negate(3))   // -3
console.log.value(doubled)            // [2, 4, 6]
```

- 裸 `=> 表达式` 接受任意数量实参，`it` 默认指第一实参，没有实参时是 `void`；它优先于外层同名绑定，不捕获外层的 `it`。
- 显式写 `() => 表达式` 仍是空参数列表，其中的 `it` 按外层解析；无名变长参数 `fn f(...)` 的函数体里，`it` 指收到的参数集合本身。

`it` 不是关键字：按普通名字解析不到时这条候选链才启用，显式声明了名为 `it` 的绑定就听显式的。

!!! example "动手 30 秒"
    把 `=> -it` 改成 `=> it * 10`，`negate(3)` 就从 `-3` 变成 `30`。`it` 收的就是那一个实参。

## 默认参数：省略或传 `void` 才触发

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

- 实参省略或为 `void` 时求默认表达式，`nil` 不触发。
- 参数从左到右初始化；默认表达式可以引用前面已初始化的参数和外部绑定，不能引用尚未初始化的后续参数。
- 默认表达式的副作用、异常、异步与族属性参与函数属性推断；关键字传参写 `area(3, height: 4)`，位置实参在前。

## 函数类型只描述形状

```el
let combine: (Number, Number) => Number = (a, b) => a + b
let reader: () => Text = () => "value"

console.stdout.writeLine(combine(2, 3))   // 5
console.stdout.writeLine(reader())        // value
```

- 多参数写 `(A, B) => C`；无参数写 `() => C`。
- 单参数值函数有简写 `A -> B`，右结合：`A -> B -> C` 是 `A -> (B -> C)`，不是三参数函数。
- 异常、异步、族、纯性等属性属于完整签名，由推断与声明共同约束，不写在普通函数类型里。

## 闭包捕获的是绑定，不是快照

??? question "先猜：`let read = () => x` 捕获的是 `x` 的值，还是 `x` 这个绑定？"
    绑定。所以下面 `x = 2` 之后 `read()` 返回 `2`；如果捕获的是快照，你会看到 `1`。

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

- 对捕获绑定的后续赋值闭包都能看到（换了类型也一样）；多个 lambda 捕获同一个 `let` 时看的是同一个绑定，互相能看到写入。
- lambda 可以写回捕获的绑定；逃逸的闭包保持该绑定有效。
- 范围循环的元素变量作用域限于循环体，每轮不跨轮保留状态；闭包捕获它时按该轮的元素绑定处理。

## 把 lambda 传给集合算法

```el
let numbers = @[1, 2, 3, 4]
let squared = numbers.map(value => value * value)
let evens = numbers.filter(value => value % 2 == 0)

console.stdout.writeLine(numbers.join(", "))   // 1, 2, 3, 4
console.log.value(squared)                     // [1, 4, 9, 16]
console.log.value(evens)                       // [2, 4]
console.log.value(numbers.map(square))         // 具名可调用值同样可以传
```

`map` 收到的是 `square` 这个函数值本身，不是调用结果；集合算法如何迭代、返回什么类型，见[集合与文本](../stdlib/collections.md)。

## 定向返回：从回调里结束外层函数

普通 `return` 只结束当前函数；`return 值 from 目标` 能越过当前 lambda、回调或局部函数，结束一个词法上在外围的具名函数。目标按词法作用域解析，不是运行时搜索最近的同名函数。

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

- `return value from func`：把值交给目标函数的调用者，并结束目标那次调用。
- `return from func` 是无值形式，返回 `void`；`return void from func` 显式写出同一件事。

`from` 后的名字不是被求值的实参，也不参与返回值表达式，只是目标分隔符；括号内部按普通表达式解析。

### 目标是词法声明，不是运行时最近同名

目标在当前词法作用域里向外找：可以是当前函数、外围具名函数、具名方法或局部具名函数，必须唯一，内层同名声明按遮蔽规则胜出。名字不存在、不是允许的函数目标、有歧义，或返回值不满足目标的返回合同，都是 ELC 的良构错误。

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

`inner` 里的定向返回结束 `middle`，`middle` 再把值交给 `outer`；目标写 `outer` 就结束 `outer`。同名遮蔽按声明身份处理：

```el
fn shadow() {
	fn shadow() {
		invoke(fn() { return 8 from shadow })   // 目标是内层 shadow 的这次调用
		return 0
	}
	return shadow()
}
```

内层 `shadow` 遮蔽外层同名声明，回调里的目标因此绑定到内层这次 activation。匿名函数没有名字，变量里保存的 lambda 也不是具名目标；能指名的只有具名函数声明、具名方法和局部具名函数。

### 返回类型包含定向返回，`Never` 不污染合流

返回类型推断包含所有 `return ... from 目标` 的返回值，不只是普通 `return`；`findName` 因此能从 `name` 推断出返回 `Text`。定向返回本身不产生可读取的值，类型是 `Never`，能放在表达式位置或分支里，不会给类型合流制造假的 `void` 分支：

```el
fn requireReady(ready: Bool) {
	if (!ready) return from requireReady
	performWork()
}
```

### 执行边界

每次调用建立独立的逻辑 activation；定向返回捕获的是那次调用的目标 token，不是代码地址。递归、重入、内联和尾递归帧复用都不能把旧 token 指向另一次调用。

- 同一逻辑调用链上普通挂起不会结束目标：回调里先 `sleep` 或等 I/O，恢复后仍可 `return ... from 外层`。
- 独立 `spawn` 的 task 不继承父目标的返回能力；`async {}` 建立的也是独立 task，里面的定向返回跨不回启动它的函数。ELF 按可调用效果检查这种调用。
- 目标已退出或已开始不可逆退出清理（Exiting）就不再接受新的返回；闭包能保住值，不能恢复已退出的 activation。
- 没有有效目标属于运行时 UB。ELC 只检查词法名字、类别、唯一性与返回类型；目标是否还活着、是否在允许返回链上，由 ELF 执行时证明，证明不了就报 error，而不是把良构程序判成编译失败。

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

没有有效目标时行为没有可依赖的定义；ELF 建立不了有效目标证明就报告 error。清理路径同样受约束：`finally` 里新起的 `return`、`break`、`continue` 或定向返回不能覆盖正在进行的跨层返回；局部循环的 `break`／`continue` 与 helper 内只结束自己的局部定向返回不受影响。

## 生命周期与借用只在这里露个头

EL 没有 Rust 式显式生命周期参数（`'a`）；析构时机与引用寿命由 `@assign`／`@destruct`、来源描述符与借用规则推断。

- `borrow`／`ref` 参数是借用，不接管所有权；`take` 接管，`rvalue` 限定实参为右值。
- 返回引用写 `borrow T from source` 或 `ref T from source`；`: forward` 按返回表达式推断类别与来源。
- `scope let` 与 `@destruct(mode: "scope")` 把对象至少保到名称作用域结束；`ptr<noescape>` 约束原生指针不被长期保存。

完整规则、析构时机与陷阱见[生命周期与析构](lifetimes.md)。

## 自动等待，以及 `async`／`await` 宏

函数是否异步由函数体自动推断：普通调用自动等待挂起，调用者随之被推断为异步，不需要也不允许在签名上标记。需要显式并发时才写 `async`。`async { ... }` 和 `await(p)` 不是关键字，是标准库的 Expr 宏：`async { ... }` 把块内容解析成零参 callback 并立即 `spawn`，返回 `Promise`；`await(p)` 只对接收者生成一次 `.get()`。

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

- `async` 表达式执行时活动已启动，不会等到 `await`。
- `await(p)` 只生成一次 `p.get()`，接收者只求值一次；不复制 `Promise`，不捕获错误，也不递归展平结果仍是 `Promise` 的情况。
- `async` 里的普通 `return` 属于那个 callback，不是外围函数；独立 task 之间的定向返回仍受“执行边界”约束。
- 关闭默认前导或写自定义模块时，从 `el:concurrency/` 普通导入 `async` 与 `await`；默认标准库用惰性导出提供它们。
- `spawn` 显式启动独立任务并返回 `Promise`；保存 `Promise` 不会等待，`get()` 才等待结果。

并发写法、`Promise` 组合与取消见[错误处理与异步](errors-async.md)。

## `@pure`：显式要求编译期求值

```el
@pure fn cube(value: Number) => value * value * value

console.stdout.writeLine(cube(3))   // 27
```

`@pure` 是显式的纯性求值合同，编译器信任这个标注：输入在编译期能确定时必须在编译期求值并物化结果，否则就像普通函数一样在运行期执行。纯性不表示不会抛错，异常始终可观察，不会因标注消失。

## 带走这三样

- 函数是值；`=>` 与 `fn` 只是写法差异，没有 `main`，模块顶层就是入口。
- 闭包捕获绑定而不是快照，所以后赋值、互相写入、逃逸后继续用都成立。
- 普通调用自动等待；`async`／`await` 是宏，`async` 一执行就启动。

## 下一站：生命周期与析构

> 闭包逃逸之后，它捕获的那个绑定还能活多久？

- 主推进：[生命周期与析构](lifetimes.md)：对象何时复制、共享、析构，以及怎么标注借用。
- 想补类与析构写法：[类与对象](classes.md)。
