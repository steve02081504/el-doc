# 从其他语言过来

这一页把熟悉的写法逐项对照：同一件事在 JavaScript、Python、C++、Rust 里怎么写，在 EL 里怎么写，以及哪些习惯必须换掉。读完你能把手上的一段脚本翻译成 EL，并知道第一遍会踩到哪里。

## JavaScript：最接近的邻居

```javascript
let count = 0;
const name = "EL";
function square(x) { return x * x; }
const twice = (x) => x * 2;
const values = [3, 1, 2];
const point = { x: 1, y: 2 };
console.log(square(count), twice(count), values[0], point.x);
```

```el
let count = 0
const name = "EL"
fn square(x) => x * x
let twice = (x) => x * 2
let values = @[3, 1, 2]
let point = @{x: 1, y: 2}
console.stdout.writeLine(square(count), " ", twice(count), " ", values[0], " ", point.x)
```

没有 `var`，也没有变量提升：绑定从声明处开始生效。`let` 不写类型注解时之后可以换类型，`const` 必须初始化且不能再赋值；`fn` 声明与箭头 lambda 是两种函数写法，后者与匿名 `fn` 等价。数组字面量是 `@[...]`，对象字面量是 `@{...}`，两者都带 `@` 前缀，避免和块、类型参数混淆。

异步写法差异最大：没有 `async`/`await`，普通调用自动等待结果，并发用 `spawn` 启动任务、`get` 取结果。错误不是被拒绝的 Promise，而是普通异常，`throw` 之后由 `try`/`catch` 处理。类必须写 `@assign` 声明复制还是共享，ES 的 class 字段默认值写法在这里对应 `let field = 值`。

## Python：缩进只是排版

```python
count = 0
def square(x):
    return x * x
values = [3, 1, 2]
point = {"x": 1, "y": 2}
```

```el
let count = 0
fn square(x) => x * x
let values = @[3, 1, 2]
let point = @{x: 1, y: 2}
```

花括号界定块，缩进不参与语法判断，格式化器会统一缩进。方法里显式写 `this`，没有隐式的 `self` 参数；构造器写 `constructor(...)` 并以 `init this` 初始化自身。列表推导式对应 `map`、`filter` 与普通 `for`；生成器由库宏包装普通函数，不是独立的 `yield` 关键字。异常写法接近：`try` 块可以取值，`catch (error)` 绑定异常对象，也可以写不带绑定的 `catch`。类同样必须 `@assign`，没有 `__init__`、`__str__` 这类双下划线协议，转换和拼接由显式方法与运算符重载承担。

## C++：类型依然在，内存规则不同

```cpp
int count = 0;
int square(int x) { return x * x; }
std::vector<int> values{3, 1, 2};
```

```el
let count: Number = 0
fn square(x: Number): Number => x * x
let values = @[3, 1, 2]
```

类型注解是可选的：写了就是值必须满足的上界，不写则由推断和实际值决定；类型不匹配是编译错误，不是隐式截断。日常 `Number` 是精确有理数，不会因为超过 32 位或 64 位就溢出，需要固定宽度整数时用数值库的位宽类型。失败用异常而不是错误码返回值约定：抛出的值可以是文本或对象，`catch` 按类型自上而下匹配。对象生命周期由构造、复制或共享模式与析构规则管理，日常代码不靠手动配对的分配与释放；需要指定存储位置或直接操作原生内存时用存储与内存库，不把裸指针当作默认做法。

类的写法更接近 C++，但可见性由声明本身决定：`let value = 0` 是公开字段，`let #value = 0` 是私有字段，没有隐式的默认可见性；构造器用 `constructor` 加 `init this`，没有初始化列表。`@assign(mode: "copy")` 与 `@assign(mode: "shared")` 取代“深拷贝还是传引用”的约定，决定赋值与传参时发生什么。

## Rust：不必到处标注生命周期

```rust
let mut count = 0;
fn square(x: i64) -> i64 { x * x }
let values = vec![3, 1, 2];
```

```el
let count = 0
fn square(x: Number): Number => x * x
let values = @[3, 1, 2]
```

`let` 绑定默认可重新赋值，没有 `mut` 修饰；要常量用 `const`。借用不写成 Rust 那样的引用前缀（EL 里的 `&` 是逻辑与），所有权与借用通过参数标记（`take`、`ref`、`rvalue`）和返回来源合同表达，规范第 6 章与第 20 章管这块。错误处理没有 `Result` 组合子，直接抛异常；可能缺失的值用 `void` 和联合类型（`T | void_t`），用 `is void_t` 判断，而不是 `Option` 加 `match`。

宏、模式匹配与 trait 对应分别是普通库宏、`switch`/`data` 加 `match`、接口（`interface`）；类还是普通 `class` 加 `@assign`。这些能力按规范分阶段实现，别把 Rust 的心智模型整套搬来。

## 对象：复制还是共享

```el
@assign(mode: "shared")
class Counter {
	let value = 0
	constructor(initial: Number = 0) { init this; this.value = initial }
	fn advance(amount: Number): Number {
		this.value += amount
		return this.value
	}
}

let counter = Counter(5)
console.stdout.writeLine(counter.advance(3))
```

`@assign(mode: "shared")` 让赋值和传参共享同一个对象，`@assign(mode: "copy")` 让它们得到按字段复制的独立副本。具名用户类型必须显式选一个，编译器不会替你在引用语义和值语义之间猜。`let value = 0` 是公开字段，`let #value = 0` 是私有字段，外部只能通过 getter 与方法访问。

## 必须换掉的习惯

- 没有 `&&`、`||`、三目 `?:`：逻辑运算写 `&`、`|`，条件取值写 `if (...)` 表达式。`&` 与 `|` 短路，并返回被选中操作数的原值，`7 & 8` 得 `8`，不归一成布尔值。
- `^` 是乘方，`2 ^ 10` 是 1024；右侧允许带符号，`2 ^ -3` 合法。逐位异或用数值库的 `bit_xor`，`^` 只在操作的类型把它重载成异或时才是异或。
- `Number` 是精确有理数，`1 / 3` 保留精确值，不会退化成近似浮点；需要机器浮点或定宽整数要显式选类型。
- 没有 `main` 函数：模块顶层语句就是入口，按书写顺序执行，入口文件可以叫 `main.el`，也可以叫别的名字。
- `import` 必须写清楚要哪些名字，没有 `import *`，也没有只执行副作用的裸导入。全量导入写 `import /.*/ from "来源"`。
- 没有全局输出函数：文字用 `console.stdout.write`／`writeLine`，结构化值用 `console.log.value(...)` 这类等级对象。
- 类必须写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，没写就是编译错误。
- 对象字面量必须带 `@`，写 `@{ name: "x" }`；裸 `{}` 在语句位置是块。
- 没有 `undefined`：缺失是 `void`，假值是 `nil`，两者不混用，`0` 与空文本仍按假值处理。

!!! tip "迁移顺序"
    先把变量、函数、循环改成 EL 语法，再处理输出；这两步走通后，把类补上 `@assign`，最后处理错误与并发。GUI 不是 HTML，界面代码基本要重写，见[图形界面](../stdlib/gui.md)。

## 继续阅读

- [运算符与表达式](../language/operators.md)：`&`、`|`、`^` 与优先级的完整规则。
- [类与对象](../language/classes.md)：`@assign`、构造、私有字段与析构。
- [常见问题](faq.md)：报错信息与常见写法卡点。
