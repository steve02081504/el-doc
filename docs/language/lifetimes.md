# 生命周期与析构

EL 自动管理对象生命周期：你通常不需要手写释放，但需要知道对象在哪个点析构、引用在哪个点失效。读完这一页，你能按复制、共享与 unique 区分所有权，读懂 `@destruct` 的两档策略，并用 `scope let`、`take`、`borrow`、`ref` 控制对象的存活边界。

## 所有权：copy、shared 与 unique

每个具名类都必须声明赋值策略，常见写法是 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`；没有默认值。属性合同还允许 `@assign(mode: "unique")`，用于不可复制的独占拥有类。

| 策略 | 普通赋值与传参 | 析构 |
| --- | --- | --- |
| `copy` | 产生独立副本 | 每个副本各自析构 |
| `shared` | 共享同一个对象 | 最后一个持有者释放时析构一次 |
| `unique` | 不可复制，必须转移拥有权 | 最后的拥有者负责清理 |

复制深度由类型的复制构造定义，不承诺默认深拷贝。`Number`、`Bool`、`Text` 是复制值语义；数组与对象字面量默认是 shared。普通参数与返回值遵循同一类型策略，显式 `take` 则按接管协议处理。

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

`unique` 用拥有的方式表达“只能有一个所有者”：不能普通复制，拥有权只能通过已证明的最后使用、`rvalue(...)` 或 `take` 参数转移；转移之后源绑定是亡值，继续读取会被拒绝，异常也不会把源恢复成可用状态（规范第 20 章 §4.1.1、MOVE-2、MOVE-15）。

```el
@assign(mode: "unique")
class Buffer { let data = @[1, 2, 3] }

fn consume(take buffer: Buffer): Number => buffer.data.size

let buffer = Buffer()
console.stdout.writeLine(consume(rvalue(buffer)))   // 3
// console.stdout.writeLine(buffer.data.size)       // 拒绝：所有权已经转移
```

## 析构策略：aggressive 与 scope

`@destruct(mode: ...)` 写在类声明上，析构函数本身不带属性。默认档是 aggressive：对象在最后一次合法使用之后就可以析构；`scope` 至少等到所属名称作用域结束才析构。两档都以“所有使用者都不再需要对象”为前提，策略取实际具体类自己的声明，不沿继承链继承。

aggressive 的“最后使用”是按实际控制流保守分析的：某个分支里的读取、闭包捕获、借用或残留清理都可能延长它。不要把它理解成“声明之后马上析构”，也不要依赖它在后续语句中仍然存活；需要确定的词法边界时用 scope 或 `scope let`。

## 析构时机

下面的例子都用带输出的析构函数观察顺序。默认策略是 aggressive；要观察词法边界的确定性，需要显式声明 `@destruct(mode: "scope")`。

### 块结束与逆声明顺序

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

两个对象在同一个块出口都变成可析构，顺序按变量声明逆序：先 `second`、再 `first`，所以先输出 `2`、再输出 `1`。逆声明顺序只约束同一个析构点上已经可清理的对象；对默认 aggressive 策略，一个对象更早到达最后使用就可以先析构，再继续执行后面的语句（LIFE-6、LIFE-7）。

### 提前 return

```el
@assign(mode: "shared") @destruct(mode: "scope")
class Trace { destructor() { console.stdout.write("R") } }

fn pick(): Text {
	let trace = Trace()
	return "value"
}

console.stdout.writeLine(pick())   // Rvalue
```

`return` 先完成返回值的求值，再执行局部清理和 `finally`，最后才把结果交给调用者。所以析构在调用者的 `writeLine` 之前运行，输出 `Rvalue`，不是 `valueR`。

### 抛错与栈展开

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

抛出异常会离开当前作用域，局部对象按正常清理规则析构，之后才进入外层 `catch`。析构函数本身可以抛错或等待异步清理；一个析构失败不会取消其余清理，多个清理错误会带原错误与有序子错误聚合（DEST-1、DEST-3、DEST-8、DEST-10）。

### 临时值与完整语句

默认 aggressive 的无绑定临时值按最后使用析构；只有显式 scope 策略的类型，其无绑定临时才保留到所在完整语句结束，或在异常离开该语句时清理。EL 不采用“所有临时值都活到语句末”的默认。

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

`Trace()` 是 scope 类型的无绑定临时值，它在 `finish(Trace())` 这条完整语句结束时才析构；`finish` 已输出 `F`，随后临时值输出 `T`，再执行下一句输出 `|`。如果这里是 aggressive 类型，最后使用之后就可以析构，不能依赖它拖到语句末。

### 控制结构结束与池路径

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

分支体、循环体和普通显式块都是名称作用域；离开该体时按逆声明顺序清理它自己的局部绑定。`break`、`continue`、`return` 和 `throw` 离开时同样执行必要的清理，不会跳过作用域里的对象。

**清理与池路径：**析构函数允许抛错，也允许是异步的；清理期间不会被重复取消打断，进程退出前会等待必要的异步清理。析构触发与存储回收是两个事件：析构发生后，内存可以在之后回收，不能因为存储还没回收就认为析构还没发生（LIFE-9、DEST-4、MEM-10）。

上面的确定时机属于静态可析构路径。GC 开启且分析不到确定生命周期时，普通对象可能进入池路径，规范不保证它在某个具体语言点析构，顺序也不受逆声明顺序约束；资源关闭仍必须由类型提供明确的 `close()` 之类入口，不能依赖 GC 触发确定性释放（MEM-1、MEM-2、MEM-4、MEM-5）。

## 手动控制生存期

### `scope let`

普通 `let` 按最后使用析构。需要“至少活到名称作用域结束”的锁、事务或文件句柄，用 `scope let`：

```el
import { openFileReader } from "el:filesystem/"

fn readPrefix(path: Text): Number {
	scope let reader = openFileReader(path)
	let bytes = reader.read(4096)
	bytes.size
}
```

`reader` 在函数出口才析构并关闭文件，即使它已经不再被读取。`scope let` 是拥有绑定加上词法退出义务，不是另一套析构机制；它不允许再把绑定里的拥有权移走（不能对它写 `rvalue(...)`、用 `take` 捕获、存进拥有容器或作为拥有值返回），`forward` 也不能洗掉 scope 来源，但合法的只读借用和可写借用仍可使用。

### `take` 与 `rvalue`

`take` 参数表示接管所有权，`rvalue` 参数表示只接受右值表达式；`rvalue(...)` 则显式消费一个左值。它们都用于明确表达“这里发生了所有权转移”，不要靠普通参数悄悄完成。上面的 `consume(take buffer: Buffer)` 调用后，`buffer` 不能再使用；`const` 左值也不能匹配 `rvalue`。

### 借用与原生指针

`borrow` 参数只读借用，不复制、不接管；`ref` 参数借用可写槽位，函数里的赋值写回原槽位；`const ref T` 只读，`rvalue ref T` 仍借原槽位并允许运用移动语义。引用只在来源有效期内可用：借用不会延长来源寿命，`borrow` 和 `ref` 也不是“保存起来以后再用”的许可。

`ptr<noescape>` 是原生指针参数上的合同：被调方承诺不在调用返回后保存该地址。它不转移所有权，也不延长来源生命周期；需要原生方长期保留指针时，必须走 `@transfer`、`@retain` 或回调句柄协议，而不是把 `noescape` 当成万能通行证。

## 生命周期标注：写来源，不写 `'a`

EL 没有 Rust 那种显式生命周期参数，函数签名里不写 `'a`，也不给每个引用命名生命周期。引用的可用范围由实际来源、借用规则和结果描述符推断；签名只写结果的类别与来源合同。这不是“完全不标注”，而是把可验证的关系写成 `borrow T from source`、`ref T from source` 或 `: forward`。

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

- `borrow Item from box` 表示结果只读依赖 `box` 所指的实际存储，结果不能活得比来源更久；返回局部槽位的借用会被拒绝，不会自动延寿（LIFE-12、REF-7）。
- `ref Item from box` 表示结果仍借用原槽位，但保留可写能力；把引用结果交给 `ref` 参数就能写回原位置，别把它保存到来源失效之后。
- `: forward` 不是独立类型，而是按每个正常返回推断类型、类别（owned、borrow、ref）和来源的请求。`relay` 推断为来自 `box` 的借用；`forward` 不会偷偷把借用变成复制，也不会把引用变成拥有值。互斥分支得到不同类别时要显式决定，不能靠推断猜。
- `forward` 参数保存操作数的原类别，调用时在实参前写 `forward`；函数体最后使用这个参数不会自动拿走调用者的对象。需要真正接管时仍写 `take` 或 `rvalue(...)`。

## 常见陷阱

- 返回局部借用：函数返回 `ref`/`borrow` 时，来源必须能活到调用者使用结果的时候。返回局部槽位的引用，确定违规会被 ELF 拒绝；把局部引用捕获进长寿闭包也一样，不能靠“已经返回”延长局部寿命。
- 容器扩容：变长数组插入元素可能搬迁已有元素；之前从物理槽位借出的引用不能跨过扩容继续使用，按容器和索引重新访问才会定位新槽位。按值读出的元素内容不受影响（COLL-11、REF-11）。
- 闭包按绑定捕获：闭包捕获的是绑定，不是值快照。源变量之后重新赋值，闭包看到新值；逃逸闭包会保活该绑定，但不会让已经失效的局部引用复活。

```el
let value = 1
let read = () => value
value = 2
console.stdout.writeLine(read())   // 2
```

- 提前析构：默认 aggressive 的对象在上一次读取之后就可能析构，分支或循环体里的局部对象也一样；需要它在后续语句中仍然存活时，显式使用 scope 类型或 `scope let`，不要依赖未声明的最后使用规则。
- 借用不延寿：把 `borrow`/`ref` 结果存进字段、容器或闭包之前，先确认来源活得足够久；来源离开作用域后，保存下来的引用没有可依赖的定义。

!!! note "实现状态"
    `@assign`、`@destruct` 的模式检查、析构清理与清理错误聚合在 `src/stdlib/compiler/attributes.el`、`tests/cleanup-provider/` 等源码/用例中有对应实现。`scope let`、`borrow`/`ref`/`forward` 等标注按语言规范第 6 章与第 20 章说明；当前仓库 `src/stdlib/compiler/parser.el` 中未定位到 `scope` 语句前缀的解析实现，使用 `scope let` 时以实际 `elc` 的诊断为准。

## 继续阅读

- [函数与闭包](functions.md)：函数值、闭包捕获与定向返回。
- [类与对象](classes.md)：`@assign`、构造、析构与私有字段。
- [错误处理与异步](errors-async.md)：析构失败、取消与跨任务的清理。
