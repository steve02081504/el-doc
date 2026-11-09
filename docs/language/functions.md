# 函数与闭包

函数在 EL 里是普通值：可以声明、简写、捕获周围绑定、作为实参传递。这一页讲清楚函数的各种写法和闭包语义，读完你能写出参数默认值、把 lambda 传给集合算法，并知道 `take`/`ref`/`rvalue` 大致在管什么。

## `fn` 声明与 `=>` 简写

```el
fn add(a: Number, b: Number): Number {
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

## 参数标记：`take`、`ref`、`rvalue`

参数前可以写三种标记，它们描述实参如何与形参交接：

```el
fn bump(ref value: Number) {
	value += 1
}

let n = 1
bump(n)
console.stdout.writeLine(n)   // 2
```

- `ref` 是可写槽位借用：函数内读参数读原槽位，给参数赋值写回原槽位；实参必须是可写左值。
- `take` 表示接管实参的所有权，调用后调用者那边的源不再可用。
- `rvalue` 限定实参必须是右值表达式；不会把左值复制一份来凑匹配。
- 三种标记不能叠加；`ref` 与 `rvalue` 不支持默认值或变长参数。借用、移动与所有权的完整规则见语言规范第 6 章。

## 没有 `async` 与 `await`

函数是否异步由函数体自动推断，调用处也自动等待，不需要也不存在 `async`/`await` 关键字：

```el
let work = spawn(fn() {
	let total = 0
	for (let n in @[1, 2, 3]) {
		total += n
	}
	total
})

console.stdout.writeLine(work.get())   // 6
```

- 普通调用会自动等待异步结果，调用者随之被推断为异步。
- `spawn` 显式启动一个独立任务并返回 `Promise`；保存 `Promise` 不会等待，`get()` 才等待结果。
- 不提供 `for await` 这类专门语法，迭代协议本身走普通自动等待。

## `@pure`

`@pure` 是显式的纯性求值合同，编译器信任这个标注：

```el
@pure fn cube(value: Number): Number => value * value * value

console.stdout.writeLine(cube(3))   // 27
```

输入在编译期能确定时，这类函数必须在编译期完成求值并物化结果；输入只能在运行期确定的，就像普通函数一样执行。纯性不表示函数不会抛错，异常始终可观察，也不会因标注而消失。

## 继续阅读

- [类与对象](classes.md)：把方法、构造与析构写进类型里。
- [控制流](control-flow.md)：函数体里的分支、循环与隐式返回值。
- [错误处理与异步](errors-async.md)：异常、任务与并发集合。
