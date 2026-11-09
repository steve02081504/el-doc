# 生命周期与析构

> 函数返回 `"value"`，析构函数却先打印 `R`，输出成了 `Rvalue`。谁改了顺序？

!!! abstract "🎯 读完这页，你能"
    - 用 `copy`／`shared`／`unique` 判断一次赋值是复制、共享还是转移
    - 预测局部对象在块结束、提前 `return` 与抛错时的析构顺序
    - 用 `scope` 类型、`scope let`、`take`、`borrow`、`ref` 控制对象活到哪一行

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[函数与闭包](functions.md)</span>

## 一句话结论

==析构点由静态分析决定：默认在最后一次合法使用之后，只有 `@destruct(mode: "scope")` 会等到名称作用域结束。==

## 赋值先决定对象有几个

每个具名类都必须写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，没有默认值；属性合同还允许 `@assign(mode: "unique")`，用于不可复制的独占拥有类。

| 策略 | 普通赋值与传参 | 析构 |
| --- | --- | --- |
| `copy` | 产生独立副本 | 每个副本各自析构 |
| `shared` | 共享同一个对象 | 最后一个持有者释放时析构一次 |
| `unique` | 不可复制，必须转移拥有权 | 最后的拥有者负责清理 |

```el
@assign(mode: "copy") class Ticket { let seat = 0 }
@assign(mode: "shared") class Counter { let value = 0 }

let first = Ticket()
let second = first
second.seat = 7

let left = Counter()
let right = left
right.value = 1

console.stdout.writeLine(first.seat, " ", second.seat)   // 0 7
console.stdout.writeLine(left.value, " ", right.value)   // 1 1
```

`copy` 类型里改 `second.seat` 不影响 `first`，输出 `0 7`；`shared` 的两个名字指向同一对象，输出 `1 1`。复制深度由该类型的复制构造定义，不承诺默认深拷贝：`Number`、`Bool`、`Text` 是复制值语义，数组与对象字面量默认共享。参数与返回值遵循同一套策略，显式 `take` 按接管协议处理。

`unique` 不能普通复制，拥有权只能通过已证明的最后使用、`rvalue(...)` 或 `take` 参数转移；转移后源绑定是亡值，继续读取会被拒绝，异常也不会把源恢复成可用状态（语言规范第 20 章 §4.1.1，MOVE-2、MOVE-15）。

```el
@assign(mode: "unique")
class Buffer { let data = @[1, 2, 3] }

fn consume(take buffer: Buffer): Number => buffer.data.size

let buffer = Buffer()
console.stdout.writeLine(consume(rvalue(buffer)))   // 3
// console.stdout.writeLine(buffer.data.size)       // 拒绝：所有权已经转移
```

!!! example "动手 30 秒"
    把 `Ticket` 的 `@assign(mode: "copy")` 改成 `"shared"`，再跑一次。看到 `7 7` 而不是 `0 7`，就说明赋值策略直接改变了两个名字之间的关系。

## 析构发生在哪一行

`@destruct(mode: ...)` 写在类声明上，析构函数本身不带属性。默认 aggressive 在最后一次合法使用之后析构；`scope` 至少等到所属名称作用域结束。两档都以所有使用者不再需要对象为前提，策略取实际具体类自己的声明，不沿继承链继承。

aggressive 的“最后使用”按实际控制流保守分析：分支读取、闭包捕获、借用或残留清理都可能延长它。别把它理解成“声明之后马上析构”；需要确定的词法边界时用 `scope` 或 `scope let`。

### 同一个析构点：逆声明顺序

??? question "先猜：同一个块里的两个对象，谁先析构？"
    后声明的先析构。同一析构点上可析构的多个变量按变量声明逆序执行，所以输出顺序是 `2`、`1`，而不是 `1`、`2`。

```el
@assign(mode: "shared") @destruct(mode: "scope")
class First { destructor() { console.stdout.write("1") } }

@assign(mode: "shared") @destruct(mode: "scope")
class Second { destructor() { console.stdout.write("2") } }

fn run() {
	{
		let first = First()
		let second = Second()
	}
	console.stdout.write("|")
}

run()
console.stdout.writeLine("")   // 21|
```

两个对象在块出口都变成可析构，按声明逆序先 `second`、再 `first`，输出 `21|`。逆序只约束同一析构点上已经可清理的对象；更早到达最后使用的 aggressive 对象可以先析构（LIFE-6、LIFE-7）。

### 提前 return：先算返回值，再清理

```el
@assign(mode: "shared") @destruct(mode: "scope")
class Trace { destructor() { console.stdout.write("R") } }

fn pick(): Text {
	let trace = Trace()
	return "value"
}

console.stdout.writeLine(pick())   // Rvalue
```

`return` 先完成返回值的求值，再执行局部清理和 `finally`，最后把结果交给调用者，所以析构在调用者的 `writeLine` 之前运行，输出 `Rvalue`。

### 抛错：先清理，再进 catch

```el
@assign(mode: "shared") @destruct(mode: "scope")
class Trace { destructor() { console.stdout.write("X") } }

fn fail() {
	let trace = Trace()
	throw "boom"
}

try {
	fail()
} catch (error) {
	console.stdout.write("caught")
}
console.stdout.writeLine("")   // Xcaught
```

异常离开作用域时，局部对象按正常规则析构，之后才进入外层 `catch`。析构可以抛错或等待异步清理；一个失败不取消其余清理，多个错误带原错误与有序子错误聚合（DEST-1、DEST-3、DEST-8、DEST-10）。

### 临时值：aggressive 用完就死，scope 活到语句末

默认 aggressive 的无绑定临时值按最后使用析构；只有显式 scope 策略的类型，其无绑定临时才保留到完整语句结束，或在异常离开该语句时清理。EL 不默认“所有临时值活到语句末”。

```el
@assign(mode: "shared") @destruct(mode: "scope")
class Trace { destructor() { console.stdout.write("T") } }

fn finish(value: Trace) { console.stdout.write("F") }

fn run() {
	finish(Trace())
	console.stdout.write("|")
}

run()
console.stdout.writeLine("")   // FT|
```

`Trace()` 是 scope 类型的临时值，在 `finish(Trace())` 整句结束时才析构：`finish` 先输出 `F`，临时值随后输出 `T`，再输出 `|`。aggressive 临时值最后使用之后就可以析构，不能依赖它拖到语句末。

### 控制结构结束也清理

```el
@assign(mode: "shared") @destruct(mode: "scope")
class Trace { destructor() { console.stdout.write("I") } }

fn run() {
	if (t) {
		let trace = Trace()
		console.stdout.write("B")
	}
	console.stdout.write("|")
}

run()
console.stdout.writeLine("")   // BI|
```

分支体、循环体和普通显式块都是名称作用域，离开时按逆声明顺序清理自己的局部绑定；`break`、`continue`、`return` 和 `throw` 都不会跳过这些清理。

### 析构不等于立刻回收内存

析构触发与存储回收是两个事件：析构发生后，内存可以在之后回收，不能因为存储还没回收就认为析构还没发生（LIFE-9、DEST-4、MEM-10）。

上面的确定时机属于静态可析构路径。GC 开启且分析不到确定生命周期时，普通对象可能进入池路径，规范不保证它在某个具体语言点析构，顺序也不受逆声明顺序约束；资源关闭仍必须由类型提供明确的 `close()` 入口，不能依赖 GC（MEM-1、MEM-2、MEM-4、MEM-5）。

## 手动指定存活边界

### `scope let`：至少活到作用域出口

普通 `let` 按最后使用析构。锁、事务、文件句柄这类需要“至少活到名称作用域结束”的绑定，用 `scope let`：

```el
import { openFileReader } from "el:filesystem/"

fn readPrefix(path: Text): Number {
	scope let reader = openFileReader(path)
	let bytes = reader.read(4096)
	bytes.size
}
```

`reader` 在函数出口才析构并关闭文件，即使已经不再被读取。`scope let` 是拥有绑定加词法退出义务，不是另一套析构机制；它不允许再移走拥有权（不能写 `rvalue(...)`、用 `take` 捕获、存进拥有容器或作为拥有值返回），`forward` 也洗不掉 scope 来源，但合法的只读和可写借用仍可使用。

!!! note "实现状态"
    `@assign`、`@destruct` 的模式检查、析构清理与清理错误聚合在 `src/stdlib/compiler/attributes.el`、`tests/cleanup-provider/` 等源码与用例中有对应实现。`scope let`、`borrow`／`ref`／`forward` 等标注按语言规范第 6 章与第 20 章说明；当前仓库 `src/stdlib/compiler/parser.el` 中未定位到 `scope` 语句前缀的解析实现，使用 `scope let` 时以实际 `elc` 的诊断为准。

### `take`、`rvalue` 与借用参数

- `take` 参数接管所有权，`rvalue` 参数只接受右值表达式，`rvalue(...)` 显式消费一个左值。它们都表明“这里发生了所有权转移”；`consume(take buffer: Buffer)` 调用后，`buffer` 不能再使用，`const` 左值也不能匹配 `rvalue`。
- `borrow` 参数只读借用，不复制、不接管；`ref` 参数借用可写槽位，函数里的赋值写回原槽位；`const ref T` 只读，`rvalue ref T` 仍借原槽位并允许运用移动语义。引用只在来源有效期内可用，借用不延寿，也不是“保存起来以后再用”的许可。
- `ptr<noescape>` 是原生指针参数上的合同：被调方承诺不在调用返回后保存该地址。它不转移所有权，也不延长来源生命周期；需要原生方长期保留指针时，必须走 `@transfer`、`@retain` 或回调句柄协议。

## 签名里不写 `'a`，写来源

EL 没有 Rust 那种显式生命周期参数：签名不写 `'a`，引用范围由来源、借用规则和结果描述符推断，只写结果类别与来源合同。

```el
@assign(mode: "shared") class Item { let value = 0 }
@assign(mode: "shared") class Box {
	let item: Item
	constructor(item: Item) { init this; this.item = item }
}

fn get(borrow box: Box): borrow Item from box => box.item
fn edit(ref box: Box): ref Item from box => box.item
fn relay(borrow box: Box): forward => get(box)

fn setValue(ref target: Item, value: Number) { target.value = value }

let box = Box(Item())
console.stdout.writeLine(relay(box).value)   // 0
setValue(edit(box), 7)
console.stdout.writeLine(box.item.value)     // 7
```

- `borrow Item from box` 表示结果只读依赖 `box` 的实际存储，不能活得比来源更久；返回局部槽位的借用会被拒绝，不会自动延寿（LIFE-12、REF-7）。
- `ref Item from box` 表示结果仍借用原槽位但保留可写能力；交给 `ref` 参数就能写回原位置，别保存到来源失效之后。
- `: forward` 不是独立类型，而是按每个正常返回推断类型、类别（owned、borrow、ref）和来源的请求。`relay` 推断为来自 `box` 的借用；它不会把借用变成复制，也不会把引用变成拥有值。互斥分支类别不同时要显式决定。
- `forward` 参数保存操作数的原类别，调用时在实参前写 `forward`；最后使用它不会自动拿走调用者的对象，真正接管仍写 `take` 或 `rvalue(...)`。

!!! warning "常见坑：四个最常看错的生命周期陷阱"
    - **返回局部借用。** 函数返回 `ref`／`borrow` 时，来源必须能活到调用者使用结果的时候；返回局部槽位的引用，确定违规会被 ELF 拒绝，把局部引用捕获进长寿闭包也一样。
    - **容器扩容。** 变长数组插入元素可能搬迁已有元素；从物理槽位借出的引用不能跨过扩容继续使用，按容器和索引重新访问才会定位新槽位，按值读出的内容不受影响（COLL-11、REF-11）。
    - **提前析构。** 默认 aggressive 的对象在上一次读取之后就可能析构，分支或循环体里的局部对象也一样；需要它活到后续语句时，显式使用 scope 类型或 `scope let`。
    - **借用不延寿。** 借用结果存进字段、容器或闭包前先确认来源活得够久；来源离开作用域后，保存的引用没有可依赖的定义。

### 闭包捕获绑定，不是快照

```el
let value = 1
let read = () => value
value = 2
console.stdout.writeLine(read())   // 2
```

闭包捕获的是绑定，不是值快照：源变量之后重新赋值，闭包看到新值；逃逸闭包会保活该绑定，但不会让已经失效的局部引用复活。

??? note "可选 · 深入：`unique` 的自动转移与清理失败"
    自动最后使用转移只在拥有型位置触发：普通赋值或声明初始化、拥有结果 `return`、已选定的 `take` 参数；来源还必须是当前函数局部绑定或值参数，未被闭包捕获、没有活跃借用、不是 `scope` 来源，读取位于直线代码。证明不了时绑定保持原状，需要显式写 `rvalue(...)`；借用、`ref`、`forward` 边界不触发自动消费（语言规范第 20 章 §4.1.1）。

    清理允许抛错与异步：期间不会被重复取消打断，进程退出前会等待异步清理。若异常 X 引发退出、清理又产生 Y 和 Z，保留 X 为原始原因并附带 Y、Z（DEST-3）。析构先标记 `closing`，逐资源摘除所有权，完成后 `closed`，重入不重复释放（DEST-10）；进池不放宽借用、析构与 `close` 保证（LIFE-12、MEM-1、MEM-2）。

## 带走这三样

- 赋值策略决定对象有几个：`copy` 复制、`shared` 共享、`unique` 只能转移。
- 默认 aggressive 在上次使用后析构，`scope` 才活到作用域结束；逆声明顺序只在同一个析构点生效。
- 借用不延寿；需要确定边界时用 `scope` 类型或 `scope let`，签名用 `borrow … from …` 写出来源。

## 下一站：类与对象

> 知道对象什么时候死，接下来看它怎么被定义出来：字段、构造器、私有成员和虚方法，怎样组成一个类型？

- 主推进：[类与对象](classes.md)：写带字段、构造器、私有成员和虚方法的类型。
- 想先练手：[命令行工具](../practice/cli-tool.md)：把它们串成小程序。
