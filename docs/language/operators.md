# 运算符与表达式

这一页按优先级把 EL 的运算符过一遍，重点讲那些从别的语言带过来的习惯会踩坑的地方，以及怎么给自己的类型重载运算符。读完你能正确写出短路逻辑、乘方、范围、空值判断和复合赋值。

## 优先级速览

从低到高。级别序号只用于心算相对顺序，同级默认左结合，标了“右”的除外。

| 级 | 运算符 | 结合性 |
| --- | --- | --- |
| 1 | `=` `+=` `-=` `*=` `/=` `%=` `&=` <code>&#124;=</code> `^=` `<<=` `>>=` `??=` | 右 |
| 2 | <code>&#124;</code> | 左 |
| 3 | `??` | 左 |
| 4 | `&` | 左 |
| 5 | `==` `!=` `===` `!==` | 左 |
| 6 | `<` `>` `<=` `>=` `<=>` `is` `isnot` | 左 |
| 7 | `..` <code>..&#124;</code> | 不结合 |
| 8 | `<<` `>>` | 左 |
| 9 | `+` `-` | 左 |
| 10 | `*` `/` `%` `.*` `./` | 左 |
| 11 | 前缀 `-` `+` `!` | 右 |
| 12 | `^` `.^` | 右 |
| 13 | 前缀 `++` `--`、`new` | 右 |
| 14 | 空格应用 `f x` | 左 |
| 15 | 调用 `()`、下标 `[]`、成员 `.` `?.` `::`、后缀 `++` `--` | 左 |

记住三条就够用大部分场景：幂高于前缀负号，`&`/`|` 低于比较高于赋值，成员和调用最紧。

## 逻辑运算：`&` 与 `|`

`&` 是短路逻辑与，`|` 是短路逻辑或。它们返回**被选中操作数的原值**，不归一成 `Bool`：

```el
console.stdout.writeLine(7 & 8)    // 8：左侧真，取右值
console.stdout.writeLine(7 | 8)    // 7：左侧真，取左值
console.log.value(nil & 8)         // nil：左侧假，保留左值
console.log.value(nil | 8)         // 8：左侧假，取右值

let selected = 3 & 4
console.stdout.writeLine(selected)   // 4，结果不是 t
```

规则是：`L & R` 在 `L` 为真时求 `R` 并取它，否则取 `L`；`L | R` 在 `L` 为真时取 `L`，否则求 `R` 并取它。结果类型是各可能分支的合流类型。

这条规则带来两个结论：

- 不要假设 `a & b` 是 `Bool`。两个操作数都是 `Bool` 时结果恰好仍是 `Bool`，但当 `a`、`b` 是 Number 或 Text 时，结果保留它们的类型。
- 需要真值时，条件上下文会把结果按条件转换判定；不要手工去“归一”。

没有 `&&` 和 `||`：

```el
let ready = t
let healthy = nil

if (ready & healthy) {
	console.stdout.writeLine("start")
}
// if (ready && healthy) { }   // 词法错误：&& 不是 EL 的运算符
```

也没有三目运算符，条件取值统一用 `if` 表达式：

```el
let label = if (ready) { "on" } else { "off" }
console.stdout.writeLine(label)   // on
```

## 比较：`==`、`===`、`is`、`isnot`

`==`/`!=` 走类型的相等重载，`===`/`!==` 比较对象身份。复制类型赋值会产生另一个对象：

```el
let a = 1
let b = a

console.log.value(a == b)    // t：值相等
console.log.value(a === b)   // nil：两个对象身份不同
```

`is` 与 `isnot` 做类型判断，右侧只接一个类型原子；联合类型必须加括号：

```el
let value: Number | Text = 42

if (value is Number) {
	console.stdout.writeLine(value + 1)   // 43
}

console.log.value(value is (Number | Text))           // t
console.log.value(value isnot Number | value is Text) // nil：等价于 (value isnot Number) | (value is Text)
```

- `a isnot X | b` 里的 `|` 是逻辑或，不是类型联合；类型联合只能出现在括号里，或不含 `|` 的单个类型原子。
- 关系运算符不可链式：`a < b < c` 报错，要写 `a < b & b < c`。
- 标准 Text 与 Number 没有默认混合比较：`"2" == 2` 走异类后备得到假，而不是报错；顺序比较需要合法的重载，不要依赖字符编码。
- `<=>` 返回三路比较结果，不能直接使用时继续与 `0` 比较。

## 乘方 `^`

`^` 是普通二元重载，对 Number 表示乘方，对 BitSet 表示逐位异或。它右结合，并且高于前缀负号：

```el
console.stdout.writeLine(2 ^ 10)     // 1024
console.stdout.writeLine(2 ^ 3 ^ 2)  // 512，等于 2 ^ (3 ^ 2)
console.stdout.writeLine(-2 ^ 2)     // -4，等于 -(2 ^ 2)
console.stdout.writeLine(2 ^ -3)     // 0.125，右侧允许带符号
```

- 没有 `**` 和 `**=`：写 `x ** 2` 不能得到乘方。
- number 的位异或用标准库函数 `bit_xor(a, b)`，不用 `^`。
- `^=` 展开为 `target = target ^ rhs`，目标只定位一次、右侧求值一次。

## 范围 `..` 与 `..|`

`start..end` 是左闭右开范围，`start..|end` 是左闭右闭范围，都按整数步长 `+1` 前进：

```el
for (let i in 0..3) {
	console.stdout.writeLine(i)    // 0 1 2
}
for (let i in 0..|3) {
	console.stdout.writeLine(i)    // 0 1 2 3
}
```

- 边界各求值一次，创建范围后不随外部绑定变化；范围值可以保存、传递、重复迭代。
- 不自动倒序，也不会补上没被步进命中的端点：`0.5..|2` 只产生 `0.5` 和 `1.5`。
- 两个方向都不可连续结合，`0..2..4` 是语法错误，需要分别写括号。
- 数字范围也用作数组的轴切片，规则与迭代一致。

## 空值：`??`、`?.`、`??=`

三个运算符都只认 `void`，`nil` 是普通值、不触发：

```el
let maybe: Text | void_t = void
console.log.value(maybe ?? "fallback")   // "fallback"

let box: Text | void_t = void
console.log.value(box?.count)            // void：接收者缺失，整个后缀链短路

let name: Text | void_t = void
name ??= "anonymous"
console.log.value(name)                  // "anonymous"
```

- `a ?? b` 在 `a` 是 `void` 时求 `b`，否则取 `a`；右侧只在需要时求值。`nil ?? b` 得 `nil`。
- `a?.b` 在 `a` 是 `void` 时短路整个后缀链，结果为 `void`；不是 `void` 时与普通成员访问相同。
- 可选的 `?.[` 不提供，`a?.[i]` 是语法错误；可选调用写 `callback?.(x)`。
- `?.` 出现在赋值目标里是“补齐”而不是短路：`a?.b?.c = 1` 会为缺失的层建立空值再写。
- `??` 的优先级低于 `&`、高于 `|`；`??=` 是条件赋值，只在目标为 `void` 时写。

## 条件写回：`|=` 与 `&=`

`|=` 和 `&=` 对应逻辑 `|`/`&` 的短路写回：目标只读取一次，右侧只在真的要写的时候求值，写回值与表达式结果都取被选中操作数的原值。

```el
let flag = nil
flag |= "yes"     // 目标是假值 → 求右侧 "yes" 并写回，表达式值也是 "yes"
flag &= "again"   // 目标现在是真值 → 求右侧 "again" 并写回
```

如果目标的静态类型有显式的 `operator |/1`、`operator &/1` eager 值重载，或声明了对应的复合赋值重载，则 `|=`/`&=` 按普通复合运算求值，两侧都求值，不再走条件短路写回。

## 复合赋值与自增

复合赋值覆盖 `+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`、`??=`。左侧必须是可赋值目标，目标只定位一次，右侧求值一次。

```el
let n = 10
n += 5
n *= 2
console.stdout.writeLine(n)   // 30

let counter = 0
console.stdout.writeLine(++counter)   // 1：前缀取运算后的值
console.stdout.writeLine(counter++)   // 1：后缀取运算前的值
console.stdout.writeLine(counter)     // 2
```

`++`/`--` 是 `v = v + 1` / `v = v - 1` 的赋值糖，不是新的算术规则。目标必须是可赋值的绑定、可写类成员或可读写下标；`const` 目标报定位错误。

## 运算符重载 {#operator-overloading}

运算符是普通重载的一种：声明成成员时左侧是 `this`；声明成自由函数时左操作数就是第一个参数。候选从类内成员、调用处词法可见的类外声明，以及操作数类型定义模块导出的关联声明中收集，去重后按普通重载规则选择；并列报歧义，不按声明顺序或导入顺序偏袒（OP-3、OP-15）。

```el
@assign(mode: "copy")
class Vec2 {
	let x: Number = 0
	let y: Number = 0

	constructor(x: Number = 0, y: Number = 0) {
		init this
		this.x = x
		this.y = y
	}

	operator +(rhs: Vec2): Vec2 {
		return Vec2(this.x + rhs.x, this.y + rhs.y)
	}

	operator -(): Vec2 {
		return Vec2(-this.x, -this.y)
	}

	operator ==(rhs: Vec2): Bool {
		return (this.x == rhs.x) & (this.y == rhs.y)
	}
}

let sum = Vec2(1, 2) + Vec2(3, 4)
console.stdout.writeLine(sum.x)             // 4
console.log.value(-sum == Vec2(-4, -2))     // t
```

同名的类外声明把左操作数写成普通参数：

```el
operator +(lhs: Vec2, rhs: Number): Vec2 {
	return Vec2(lhs.x + rhs, lhs.y)
}
```

运算符的优先级和结合性由符号本身固定，重载不能改；能改的是求值方式和结果类型。

### 可以重载哪些

| 形式 | 声明写法 | 说明 |
| --- | --- | --- |
| 二元 | `operator +(rhs: T): T`；类外 `operator +(lhs: T, rhs: U)` | 用符号自己的优先级与结合性，二元运算符基本都能重载 |
| 一元 | `operator -()`、`operator !()` | 前缀 |
| 自增自减 | `operator++()`、`operator--()`（后置）；`++operator()`、`--operator()`（前置） | 返回值由声明决定，不强制返回自身 |
| 下标 | `operator[](index: Number): T` 读；`operator[]=(index: Number, value: T)` 写 | 接收者、下标、右侧各求值一次 |
| 调用 | `operator()(x: Number): T` | 让对象像函数一样被调用 |
| 赋值 | `operator =(rhs: T)` | 初始化不调用它，之后对已构造对象赋值才调用 |
| 转换 | `operator Text(): Text`（显式）、`implicit operator Text(): Text`（隐式） | 默认只允许源码明确请求 |
| 字面量 | `operator number(...)`、`operator""(...)`、`operator@[](...)` | 标准库字面量协议的入口 |

写入下标也可以写成双参数形式 `operator[](index, value)`。`??`、`??=`、`&=`、`|=` 同样可以重载，`&`/`|` 的规则见下一节。`===`/`!==` 的身份比较与 `is`/`isnot` 的类型判断不能被重载；`&&`、`||`、`~` 本来就不是 EL 运算符，也没有对应重载。

### 逻辑运算的位置

`&`/`|` 需要单独记：源码里的 `a & b`、`a | b` 默认是短路逻辑，不会调用你的重载；只有类型声明了显式的 `operator &`/`operator |` 值重载时，才按普通 eager 调用求值，两侧都求值（OP-7）。重载无法截获短路本身，也不存在“接收右侧延迟求值”的重载协议。

### 转换默认是显式的

`operator Text()` 这类转换只在你明确请求时使用，例如 `Text(value)`，或条件上下文需要转换时；要让它在普通参数、赋值和运算中自动参与，声明时加 `implicit`。隐式构造器同理：

```el
@assign(mode: "copy")
class Money {
	let cents: Number = 0

	implicit constructor(cents: Number) {
		init this
		this.cents = cents
	}

	operator Text(): Text {
		return "$" + Text(this.cents)
	}
}

fn describe(value: Money) {
	console.stdout.writeLine(value)
}

describe(350)                       // $350：Number 经 implicit 构造器转成 Money
console.stdout.writeLine(Money(5))  // $5：参数转换请求 operator Text
```

一条普通转换路径最多有一层用户转换；显式转换与隐式转换同时可用时按适用程度选择，并列就报歧义，不按库名或声明顺序猜（OP-10）。

### 在作用域里临时换掉符号

`let operator * = ...` 把某个二元值运算绑定成当前词法作用域里的普通可调用值，只影响该作用域中的值运算，退出作用域就恢复；它不改变身份比较、短路和赋值的语法含义：

```el
fn twice(value: Number): Number {
	let operator * = (left: Number, right: Number) => left * right * 2
	return value * 3        // 调用上面的绑定，得到 30
}

console.stdout.writeLine(twice(5))
```

### 重载的边界

- 运算符重载不授予数学性质：`+` 就是一次普通调用，不意味着交换律、结合律或纯性。
- 重载按声明签名选择；不要指望“左边是 `Text` 就自动把右边转成文本”（OP-2）。需要时显式写 `Text(value)`。
- `<=>` 的结果要能继续使用：Number 的 `<=>` 返回 Number，自定义类型返回 `Comparison`，按规范与 `0` 比较或取用三路结果（OP-8）。
- 显式 `operator =` 的返回值可以是 `this`、代理或 `void`；后续使用仍要满足普通的复制、借用与生命周期规则。

## 没有位运算运算符

`&`、`|`、`^` 在 EL 里都不是位运算。number 的按位运算使用标准库的普通函数：

```el
import { bit_and, bit_or, bit_xor, bit_not } from "el:number/bit-operations.el"

console.stdout.writeLine(bit_and(0b1100, 0b1010))   // 8
console.stdout.writeLine(bit_or(0b1100, 0b1010))    // 14
console.stdout.writeLine(bit_xor(0b1100, 0b1010))   // 6
console.stdout.writeLine(bit_not(0b1010))           // -11
```

- `~`、`&&`、`||` 及其重载声明都不是 EL 的运算符，出现即词法错误。
- `<<`、`>>` 是普通可重载二元运算符，但 Number 本身不提供移位；需要位宽语义时用标准库的 `BitInteger`、`BitSet` 等显式类型及其操作。
- 这些函数按无限二补码合同工作，不隐含机器位宽；需要固定宽度截断时显式声明布局。

## 常见易错点

| 想写 | 实际写法 |
| --- | --- |
| `a && b` | `a & b` |
| <code>a &#124;&#124; b</code> | <code>a &#124; b</code> |
| `cond ? x : y` | `if (cond) { x } else { y }` |
| `x ** 2` | `x ^ 2` |
| `~x` | `bit_not(x)` |
| `f -1` | `f(-1)` |
| `a < b < c` | `a < b & b < c` |
| `"2" + 1` | `"2" + Text(1)` |

空格应用也有坑：`f g x + 1` 是 `((f g) x) + 1`，`f x.foo` 是 `f(x.foo)`；以一元 `-`、`+`、`!` 开头的实参必须写括号。`.*`、`./`、`.^` 各自是单个记号，`a . * b` 与 `a.*b` 不是一回事。`a & b ^ c` 按幂优先分组为 `a & (b ^ c)`。

## 继续阅读

- [控制流](control-flow.md)：把条件与循环写成表达式。
- [值与类型](values.md)：这些运算符作用在哪些值上。
- [类与对象](classes.md)：为自己的类型重载运算符。
