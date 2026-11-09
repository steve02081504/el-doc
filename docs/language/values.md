# 值与类型

这一页解决“EL 里的一个值是什么类型、怎么写、怎么声明绑定”。读完你能读懂类型注解、写出 Number 与 Text 字面量、区分 `t`/`nil`/`void`，并用解构和字面量组装数据。

## Number：精确有理数

日常数字是标准库 `Number`，不是固定位宽的机器整数。字面量写出来之后，原始文本会和类型约束一起交给标准库的数值协议，不会先被截成机器浮点数再解析。

```el
let total = 1_000_000
let ratio = 1 / 3
let scaled = ratio * 3

console.stdout.writeLine(total)        // 1000000
console.stdout.writeLine(scaled)       // 1
console.stdout.writeLine(0xFF + 0b1)   // 256
```

- 整数、小数、指数与进制字面量都接受：`42`、`3.14`、`1e9`、`0xFF`、`0b1010`、`0o755`。
- `_` 可以分隔数字，例如 `1_000_000`，它不改变数值，只要求夹在同进制的两个数字之间。
- 需要精确保存时，`Number` 用分子与分母的有理数表示，所以 `1 / 3` 不会被舍入成二进制近似值；`(1 / 3) * 3` 得 `1`。
- 需要近似计算时，精度由 `Number` 的 `epsilon` 参数表达，而不是由底层机器格式决定。`epsilon` 是最大绝对误差的上限。
- `Number` 没有固定的 64 位宽度，也不会按机器字长环绕。需要明确位宽时使用标准库的 `BitInteger` 工厂（`bits` 与 `sign_bits` 参数），它是 `Number` 的派生类型，类型身份包含布局参数。

`Number` 的约束写在类型实参里，赋值时检查：

```el
let bounded: Number<min: 0, max: 100> = 42
let whole: Number<integer: t> = 7
let precise: Number<epsilon: 0.001> = 0.333
```

`integer: t` 是独立的整数约束，不能从 `epsilon` 推出来；`epsilon: 1` 不禁止 `1.5`。范围、精度与溢出的完整规则见语言规范第 4 章。

## Text 与 Char

单引号和双引号等价，都是 `Text` 字面量；转义与插值写法统一。

```el
let single = 'hello'
let double = "hello"
let name = "Ada"
let message = `Hello, ${name}!`

console.log.value(single == double)          // t
console.stdout.writeLine(message)            // Hello, Ada!
```

反引号字符串支持 `${表达式}` 插值，可跨行；每次执行时从左到右求值插值表达式。插值只生成本次文本，不是 GUI 的持续绑定。

`Text` 的长度、索引与切片按 Unicode 标量计，不按字节：

```el
let greeting = '你好'

console.stdout.writeLine(greeting.count)          // 2，两个 Unicode 标量
console.stdout.writeLine(greeting.byte_count)     // 6，UTF-8 字节数
console.stdout.writeLine(greeting.slice(0, 1))    // 你
```

不要混淆 `Text` 与 `Char`：

- `'a'` 是只含一个标量的 `Text`，不是 `Char`。
- 索引文本、或用 `Char(...)` 构造，得到 `Char`；`Text` 按 Unicode 标量计数，而 `Char` 可以保存任意 N 位数据，`Char<bitWidth: 8>(170)` 合法，即使该值不是合法标量。
- 比较、相等与哈希按内容或标量值，不按位宽；拼接得到新的 `Text`。

## Bool 与 t/nil/void

`t`、`nil`、`void` 不是关键字，而是预导入提供的普通值绑定，类型分别是 `t_t`、`nil_t`、`void_t`。它们在名字解析上与普通绑定没有区别，可以被同名的局部绑定遮蔽。

- `t` 是真值，带 xata 条件属性。
- `nil` 是标准假值，带 netra 条件属性。
- `void` 表示没有结果，带 lohk 条件属性；`void` 只表示缺失，不表示假值，但在条件和逻辑判定中按假值处理。
- `Bool` 是 `t_t | nil_t` 的类型别名，`Bool(value)` 按标准库的条件转换给出 `t` 或 `nil`。

```el
let yes: Bool = t
let no: Bool = nil
let nothing = void

console.log.value(yes)                // t
console.log.value(no)                 // nil
console.log.value(nothing)            // void
console.log.value(nothing is void_t)  // t
console.log.value(Bool(0))            // nil
console.log.value(Bool(1))            // t
```

`nil` 与 `void` 是两种状态：`nil` 是普通值，可以保存、比较、当假值；`void` 表示这个位置没有值。需要可选值时写联合类型 `T | void_t`，缺失时存 `void`。普通读取动态对象上不存在的字段会报错，而不是自动得到 `void`。

```el
fn logLine(message: Text): void_t {
	console.stdout.writeLine(message)
	return void
}

logLine("done")
```

## let、const 与类型注解

`let` 声明可写绑定；`const` 声明只读绑定，必须带初值。同一作用域重复声明同名绑定是编译错误，内层可以遮蔽外层。

```el
let counter = 0
counter = counter + 1

const limit: Number = 10

let flexible = 1
flexible = "one"          // 无注解绑定可以换类型版本
```

类型注解是值的**上界**，不是“只能取这个类型”的封闭集合：

```el
let label: Text = "draft"
// label = 42             // 编译错误：42 超出 Text 上界

let amount: Number = 1
// amount = "one"         // 编译错误：Text 不在 Number 上界内
```

- 有注解的局部 `let` 允许在注解范围内细化或加宽实际值版本。例如 `let buffer: Text = '123'` 之后写入 `'鸡'`，实际值版本会加宽到能容纳该标量的位宽；显式写死的固定宽度上界不能靠运行期自动加宽越过。
- 无注解的 `let` 可以换类型，但换型仍按普通赋值规则选择重载；类型变化后，运算按当前值的可达类型解析。
- `const` 的只读是浅层的：重赋、复合赋值、步进或经别名写回都是违规；确定违规由 `elf` 报错。

## 解构

对象与数组模式支持重命名、默认值、嵌套、跳项与 rest。源表达式只求值一次，绑定从左到右初始化。

```el
let { name: userName, age = 0, ...other } = @{ name: "Ada", age: 36, city: "London" }
let [first, , third = 3, ...tail] = @[1, 2, 3, 4]

console.stdout.writeLine(userName)   // Ada
console.stdout.writeLine(age)        // 36
console.log.value(other)             // 剩余公开字段组成的 shared 动态对象
console.stdout.writeLine(first)      // 1
console.stdout.writeLine(third)      // 3
console.log.value(tail)              // [4]
```

- `name: userName` 是重命名，`age = 0` 是默认值。
- 默认值只在项缺失或值为 `void` 时求值，`nil` 不触发默认值；默认表达式可以引用前面已初始化的绑定。
- rest 必须放在最后且不能带默认值；数组 rest 是结构独立的新变长数组，对象 rest 是新的 shared 动态对象，只含来源自己的公开数据字段。
- 无默认值的必需项若静态可判定缺失，编译期拒绝；运行期才发现时抛异常。

## 数组、对象与矩阵

三种字面量各有固定写法：

```el
let numbers = @[1, 2, 3]
let mixed = @[1, "one"]                 // 元素类型是 Number | Text
let empty: Number[] = @[]               // 空数组由注解或后续用法提供元素类型
let point = @{ name: "origin", x: 0 }
let short = @{ numbers }                // 裸标识符缩写：numbers: numbers
let identity = @(1, 0; 0, 1)            // 逗号分列，分号分行

console.stdout.writeLine(numbers[0])    // 1
console.log.value(point)
console.log.value(identity)
```

- 数组是 `shared`：赋值复制引用而不是复制元素；需要独立内容时显式遍历复制。
- `@[1, "one"]` 的元素类型按元素集合推断成联合类型，后续赋值限制在该集合内。
- `@{}` 对象字面量定义匿名、封闭、共享的类并创建实例：有身份，声明字段可写，字段集合固定，不能新增或删除字段，也没有方法。需要开放字段或行为时用 `class`。
- 矩阵字面量 `@(1, 2; 3, 4)` 用逗号分列、分号分行；每行从左到右各求值一次，各行必须等长。

## any

`any` 是显式的任意类型，运行时可以换任意类型。它不是“自动适配一切”的捷径：对 `any` 做成员访问或运算之前，必须显式缩窄到确定支持该操作的类型或接口。

```el
let value: any = 41
value = "one"

if (value is Number) {
	console.stdout.writeLine(value + 1)   // 只有缩窄成立才允许按 Number 运算
}
console.log.value(value)                  // "one"
```

`any` 可以保存 `nil` 和 `void`：排除缺失只证明非 `void`，不能凭此获得任意对象成员的能力。显式 `any` 的运算默认不纯、可能抛出任意异常，动态返回也是 `any`；已知的返回类型声明仍然保留。

## 继续阅读

- [运算符与表达式](operators.md)：`&`/`|`、`^`、取值范围和空值合并怎么写。
- [函数与闭包](functions.md)：把上面的值交给函数、lambda 与默认参数。
- [集合与文本](../stdlib/collections.md)：数组和文本的常用方法。
