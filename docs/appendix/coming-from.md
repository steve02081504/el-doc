# 从其他语言过来

> 你会写 JavaScript、Python、C++ 或 Rust，现在打开一份 EL 代码——哪些写法能直接看懂，哪些看着一样、语义却已经换了？

!!! abstract "🎯 读完这页，你能"
    - 把一段熟悉语言的脚本按 EL 语法改写过来
    - 认出“看着一样、语义不同”的写法，不在第一遍就踩坑
    - 说清 `@assign`、`&`、`^` 这几处差异会在哪里咬人

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[语言速览](../tour.md)</span>

## 先查表：你从哪来，先看哪三条

| 你从哪来 | 先看这三条 | 一句话 |
| --- | --- | --- |
| JavaScript | 没有 `var` 和变量提升；`async`、`await` 是宏，普通调用自动等待；类必须写 `@assign` | 最接近，但异步与类的语义换了 |
| Python | 块由花括号界定；方法里显式写 `this`；类必须写 `@assign` | 缩进只管排版 |
| C++ | 类型注解是上界，`Number` 是精确有理数；失败用异常；`@assign` 取代深拷贝／传引用 | 类型还在，内存规则不同 |
| Rust | `let` 默认可重赋；`&` 是逻辑与；没有 `Result`、`Option` | 借用不是 `&` 前缀 |

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

写法看着一样，语义不同：

| JavaScript | EL | 差别在哪 |
| --- | --- | --- |
| `let` / `const` | `let` / `const` | 没有 `var`，也没有变量提升：绑定从声明处开始生效。`let` 不写类型注解时之后可以换类型；`const` 必须初始化且不能再赋值 |
| `function f() {}` / `x => …` | `fn f(…) => …` / `(x) => …` | `fn` 声明与箭头 lambda 是两种函数写法，后者与匿名 `fn` 等价 |
| `[]` / `{}` | `@[…]` / `@{…}` | 两者都带 `@` 前缀，避免和块、类型参数混淆 |
| `async` / `await` | `async { … }` / `await(p)` | 两者是标准库宏，不是关键字；普通调用仍自动等待结果。独立任务用 `async` 或 `spawn` 启动，`await`/`get` 等待 |
| `Promise` 拒绝 | 普通异常 | 错误不是被拒绝的 Promise，而是普通异常，`throw` 之后由 `try`/`catch` 处理 |
| `class` 字段默认值 | `let field = 值` | 类必须写 `@assign` 声明复制还是共享 |

!!! warning "常见坑：把 `async` 当成语法标签"
    现象：在 EL 里找 `async function`，或者以为不写 `await` 就拿不到结果。`async { ... }` 与 `await(p)` 都是标准库宏；普通调用本来就会等待结果，需要并发时才显式用 `async` 或 `spawn`。

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

看着一样，语义不同：

| Python | EL | 差别在哪 |
| --- | --- | --- |
| 缩进 | 花括号 | 块由花括号界定，缩进不参与语法判断，格式化器会统一缩进 |
| `self` | `this` | 方法里显式写 `this`，没有隐式的 `self` 参数；构造器写 `constructor(...)` 并以 `init this` 初始化自身 |
| 列表推导式 | `map`、`filter` 与普通 `for` | 写法换掉，逐元素处理的语义还在 |
| `yield` 生成器 | 库宏包装普通函数 | 不是独立的 `yield` 关键字 |
| `try` / `except` | `try` / `catch` | 写法接近：`try` 块可以取值，`catch (error)` 绑定异常对象，也可以写不带绑定的 `catch` |
| `__init__` / `__str__` | `constructor`／显式方法与运算符重载 | 类同样必须 `@assign`，没有双下划线协议 |

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

看着一样，语义不同：

| C++ | EL | 差别在哪 |
| --- | --- | --- |
| 类型注解 | 可选的上界 | 写了就是值必须满足的上界，不写由推断和实际值决定；类型不匹配是编译错误，不是隐式截断 |
| `int` / `double` | `Number` | 日常 `Number` 是精确有理数，不会因为超过 32 位或 64 位就溢出；需要固定宽度整数时用数值库的位宽类型 |
| 错误码 | 异常 | 失败用异常而不是错误码返回值约定：抛出的值可以是文本或对象，`catch` 按类型自上而下匹配 |
| `new` / `delete` | 构造、复制或共享模式与析构规则 | 日常代码不靠手动配对的分配与释放；需要指定存储位置或直接操作原生内存时用存储与内存库，不把裸指针当作默认做法 |
| `public` / `private` | `let value` / `let #value` | 可见性由声明本身决定，没有隐式的默认可见性；构造器用 `constructor` 加 `init this`，没有初始化列表 |
| 深拷贝还是传引用 | `@assign(mode: "copy" / "shared")` | 取代“深拷贝还是传引用”的约定，决定赋值与传参时发生什么 |

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

看着一样，语义不同：

| Rust | EL | 差别在哪 |
| --- | --- | --- |
| `let mut` | `let` | 绑定默认可重新赋值，没有 `mut` 修饰；要常量用 `const` |
| `&` 引用 | 逻辑与 | 借用不写成 Rust 那样的引用前缀；所有权与借用通过参数标记（`take`、`ref`、`rvalue`）和返回来源合同表达，规范第 6 章与第 20 章管这块 |
| `Result` | 异常 | 没有 `Result` 组合子，直接抛异常 |
| `Option<T>` + `match` | `T` 与 `void_t` 的联合类型 + `is void_t` | 可能缺失的值用 `void` 和联合类型，用 `is void_t` 判断 |
| 宏／模式匹配／trait | 普通库宏／`switch` 加 `data` 与 `match`／`interface` | 类还是普通 `class` 加 `@assign`；这些能力按规范分阶段实现，别把 Rust 的心智模型整套搬来 |

## 对象：赋值是复制还是共享，由类自己声明

```el
@assign(mode: "shared")
class Counter {
	let value = 0
	constructor(initial: Number = 0) { init this; this.value = initial }
	fn advance(amount: Number) {
		this.value += amount
		return this.value
	}
}

let counter = Counter(5)
console.stdout.writeLine(counter.advance(3))
```

??? question "先猜：把同一个 `Counter` 赋给两个变量，改一处另一处会变吗？"
    会。`@assign(mode: "shared")` 让赋值和传参共享同一个对象；换成 `@assign(mode: "copy")` 才会按字段复制出独立副本。具名用户类型必须显式选一个，编译器不会替你在引用语义和值语义之间猜。

`let value = 0` 是公开字段，`let #value = 0` 是私有字段，外部只能通过 getter 与方法访问。

## 所有语言通用：这些习惯必须换掉

- **`&&`、`||`、三目 `?:`。** EL 没有这些：逻辑运算是 `!`、`&`、`|`。`&` 与 `|` 短路，并返回被选中操作数的原值，`7 & 8` 得 `8`，不归一成布尔值；条件取值用 `if (...) ... else ...` 表达式。
- **把 `^` 当异或。** `^` 是乘方，`2 ^ 10` 得 1024，右侧允许带符号，`2 ^ -3` 合法。逐位异或用数值库的 `bit_xor`；只有操作的类型把 `^` 重载成异或时，它才是异或。
- **默认的 `double`、`int`。** EL 的 `Number` 是精确有理数，`1 / 3` 保留精确值；需要机器浮点或定宽整数要显式选类型。
- **`main()`。** 没有 `main`：模块顶层语句就是入口，按书写顺序执行；入口文件可以叫 `main.el`，也可以叫别的名字。
- **`import *` 或裸导入。** 必须写清楚要哪些名字：`import /.*/ from "来源"`、`import /.*/ as m`、`import { a, b as c }`；没有 `import *`，也没有只执行副作用的裸导入。
- **`print()`。** 没有全局输出函数：文字用 `console.stdout.write`／`writeLine`，结构化值用 `console.log.value(...)`。
- **直接写类。** 类必须写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，没写就是编译错误。
- **`{}` 对象字面量。** 对象字面量必须带 `@`，写 `@{ name: "x" }`；裸 `{}` 在语句位置是块。
- **`undefined` / `null`。** 没有 `undefined`：缺失是 `void`，假值是 `nil`，两者不混用；`0` 与空文本仍按假值处理。

!!! tip "迁移顺序"
    先把变量、函数、循环改成 EL 语法，再处理输出；这两步走通后，把类补上 `@assign`，最后处理错误与并发。GUI 不是 HTML，界面代码基本要重写，见[图形界面](../stdlib/gui.md)。

## 带走这三样

- 看着一样的 `let`、`fn`、`[]`、`{}`，在 EL 里都有固定写法：`@[...]`、`@{...}`、`fn ... => ...`。
- 语义差异集中在三处：`&`/`|` 返回原值、`^` 是乘方、类必须声明 `@assign`。
- 没有 `main`、没有 `import *`、没有 `undefined`；输出走 `console.stdout`。

## 下一站：[常见问题](faq.md)

> 翻译过来的代码报了错，怎么最快判断是哪一类问题？

- 主推进：[常见问题](faq.md)：按输出、语法、类型与类、运行与构建分组，直接查现象。
- 想复习运算符：[运算符与表达式](../language/operators.md)：`&`、`|`、`^` 与优先级的完整规则。
- 想看类的全貌：[类与对象](../language/classes.md)：`@assign`、构造、私有字段与析构。
