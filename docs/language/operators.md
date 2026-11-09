# 运算符与表达式

这一页按优先级把 EL 的运算符过一遍，重点讲那些从别的语言带过来的习惯会踩坑的地方。读完你能正确写出短路逻辑、乘方、范围、空值判断和复合赋值。

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
