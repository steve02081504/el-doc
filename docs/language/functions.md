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

## 生命周期标注：类别与来源，不是生命周期参数

EL 没有 Rust 那种显式生命周期参数，函数签名里不写 `'a`，也不需要给每个引用命名生命周期。引用能用多久由实际来源、借用规则和函数效果描述符推断；签名只写结果的类别与来源合同。下面这些标注才是实际可写的生命周期与所有权信息。

### 参数交接：`borrow`、`ref`、`take`、`rvalue`

先定义一个具体类型，后面的例子基于它：

```el
@assign(mode: "shared")
class Item {
	let value: Number = 0
}

@assign(mode: "shared")
class Box {
	let item: Item

	constructor(item: Item) {
		init this
		this.item = item
	}
}
```

参数前的标注决定实参怎样交给形参：

| 标注 | 管什么 | 调用之后 |
| --- | --- | --- |
| `borrow x: T` | 只读借用，不复制也不移动 | 源绑定仍然可用 |
| `ref x: T` | 可写槽位借用 | 函数里的写入落回原槽位 |
| `take x: T` | 接管所有权 | 调用者不能再使用源绑定 |
| `rvalue x: T` | 限定实参是右值 | 只接受临时值或显式消费的位置 |

```el
fn itemCount(borrow box: Box) => box.item.value
fn bump(ref value: Number) { value += 1 }
fn unwrap(take box: Box) => box.item
fn label(rvalue message: Text) => message

let box = Box(Item(1))
itemCount(box)              // 只读借用：box 之后仍然可用
bump(box.item.value)        // 写回 box.item.value
console.stdout.writeLine(box.item.value)   // 2

let owned = unwrap(box)     // 接管：box 之后不可再用
console.stdout.writeLine(owned.value)   // 2

console.stdout.writeLine(label("new"))   // 右值实参可以匹配

const fixed = "old"
// label(fixed)             // 编译错误：const 左值不匹配 rvalue
```

- `borrow` 只读观察，不会复制出一个新对象，也不会延长对象的寿命。
- `ref` 是可写槽位借用：函数内读参数读原槽位，给参数赋值写回原槽位；实参必须是可写左值。
- `take` 表示接管实参的所有权，调用后调用者那边的源不再可用；调用处必须确实拥有该值。
- `rvalue` 限定实参必须是右值表达式，不会把左值复制一份来凑匹配；接管仍由 `take` 表达，`rvalue` 只限定值类别。
- 每个参数只能选一种交接方式，不能叠加；`ref` 与 `rvalue` 不支持默认值或变长参数。借用、移动与所有权的完整规则见语言规范第 6 章与第 20 章。

### 返回位：来源写到签名里

返回引用时，签名写结果的类别和来源，而不是只写 `T`。仍然用上面的 `Box`：

```el
fn get(borrow x: Box): borrow Item from x => x.item
fn edit(ref x: Box): ref Item from x => x.item
fn selected(borrow x: Box): forward => get(x)
```

- `borrow Item from x` 表示结果是 `x.item` 所在存储的只读借用，来源是参数 `x`；结果的生命周期不能超过这个来源。返回局部槽位，或让借用活到来源失效之后，都会被拒绝。
- `ref Item from x` 表示结果仍借用同一槽位，但保留可写能力。把引用结果交给另一个 `ref` 参数，就能写回原位置：

```el
fn setValue(ref target: Item, value: Number) {
	target.value = value
}

let box = Box(Item(0))
setValue(edit(box), 42)
console.stdout.writeLine(box.item.value)   // 42
```

- `: forward` 不是独立类型，而是“按返回表达式推断结果”的请求：编译器从每个正常返回收集类型、类别（owned、borrow、ref）和来源。`selected` 的推断结果是“来自 `x.item` 的借用”；`forward` 不会偷偷把借用变成复制，也不会把引用变成拥有值。
- 来源可以写得更精确，例如 `from x.item`；接口也可以只写 `from x` 作为保守上界。互斥分支必须得到可合并的类别，借用和拥有值混在一起时要显式决定，不能靠推断猜。
- `ref T`、`const ref T`、`rvalue ref T` 本身就是类型，可以出现在返回类型和联合分支中；`const ref` 以只读左值消费，联合结果先判别分支，再按选中的引用分支取值。

`forward` 参数保存操作数的原类别，调用时在实参前写 `forward`，例如 `relay(forward value)`；函数体最后使用这个参数不会自动拿走调用者的对象。需要真正接管时仍写 `take` 或 `rvalue(...)`。

### 词法退出：`scope let` 与 `@destruct(mode: "scope")`

普通绑定按最后使用和析构策略结束；需要“至少活到名称作用域结束”时用 `scope let`：

```el
import { openFileReader } from "el:filesystem/"

fn readPrefix(path: Text) {
	scope let reader = openFileReader(path)
	let bytes = reader.read(4096)
	bytes.size
}   // 离开函数时 reader 才析构并关闭文件，即使它已经不再被读取
```

- `scope let` 在拥有绑定的基础上加词法退出义务：绑定在块出口执行原生析构，未读取也不提前结束。它是绑定上的要求，不是另一套析构机制，也不改变类型自己的构造、复制和关闭协议；类型自身标了 `@destruct(mode: "scope")` 时，即使写普通 `let`，对象也至少活到名称作用域结束。
- 这套标注不允许从 `scope` 绑定转移所有权：不能对它写 `rvalue(...)`、用 `take` 捕获、存进拥有容器或作为拥有值返回；合法的只读借用和可写借用仍可使用，`forward` 也不能洗掉 scope 来源。
- 类的析构策略标在类声明上：`@destruct(mode: "scope")` 让该类的对象至少活到名称作用域结束，默认的 `aggressive` 则可以在最后一次使用后析构。析构函数本身不写这个属性；策略取实际具体类自己的声明，不沿继承链继承。
- `scope` 保证的是“析构不因最后使用提前发生”，不保证业务方法不会主动关闭或解锁资源；关闭动作仍按类型的公开协议执行。

### 原生指针：`ptr<noescape>`

`ptr<noescape>` 是外部函数参数上的原生指针合同：被调方承诺不在调用返回后保存该地址，编译器才允许把借用指针交给它。它不转移所有权，也不延长来源的生命周期；需要被调方保留指针时，必须走显式的 `@owned`、`@retain` 或回调句柄协议，而不是把 `noescape` 当成万能通行证。

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

- [类与对象](classes.md)：把方法、构造与析构写进类型里。
- [控制流](control-flow.md)：函数体里的分支、循环与隐式返回值。
- [错误处理与异步](errors-async.md)：异常、任务与并发集合。
