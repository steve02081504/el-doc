# 值与类型

> `1 / 3` 存进 `Number`，是 `0.333…`，还是一对整数？如果它是精确的，那 `(1 / 3) * 3` 会不会正好等于 `1`？

!!! abstract "🎯 读完这页，你能"
    - 写出精确有理数、文本和布尔值的字面量，并解释 `(1 / 3) * 3` 为什么正好是 `1`
    - 区分 `t`、`nil`、`void` 三种“空”，知道什么时候该用哪个
    - 用类型注解、解构和三种字面量组装数据
    - 说出 `any` 为什么不是“自动适配一切”的捷径

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[读语言之前](before-you-start.md)</span>

## 先猜一个结果

```el
let ratio = 1 / 3
let scaled = ratio * 3

console.stdout.writeLine(scaled)
```

第二行输出什么：`0.9999999999999999`？`1`？还是别的？

??? question "看答案：为什么不是浮点误差"
    `1`。==在 EL 里，日常数字是精确有理数，不是固定位宽的机器浮点数==：`1 / 3` 用分子和分母保存，乘以 `3` 正好约回 `1`，中间没有舍入。

    这带来的区别贯穿整页：`Number` 的能力和限制，跟你在别的语言里熟悉的 `double`、`int` 都不一样。

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

- 整数、小数、指数与进制字面量都接受：`72`、`3.14`、`1e9`、`0xFF`、`0b1010`、`0o755`。
- `_` 可以分隔数字，例如 `1_000_000`，它不改变数值，只要求夹在同进制的两个数字之间。
- 需要精确保存时，`Number` 用分子与分母的有理数表示，所以 `1 / 3` 不会被舍入成二进制近似值；`(1 / 3) * 3` 得 `1`。
- 需要近似计算时，精度由 `Number` 的 `epsilon` 参数表达，而不是由底层机器格式决定。`epsilon` 是最大绝对误差的上限。
- `Number` 没有固定的 64 位宽度，也不会按机器字长环绕。需要明确位宽时使用标准库的 `BitInteger` 工厂（`bits` 与 `sign_bits` 参数），它是 `Number` 的派生类型，类型身份包含布局参数。

`Number` 的约束写在类型实参里，赋值时检查：

```el
let bounded: Number<min: 0, max: 100> = 72
let whole: Number<integer: t> = 7
let precise: Number<epsilon: 0.001> = 0.333
```

`integer: t` 是独立的整数约束，不能从 `epsilon` 推出来；`epsilon: 1` 不禁止 `1.5`。范围、精度与溢出的完整规则见语言规范第 4 章。

??? question "先猜：`Number<integer: t>` 能存 `1.5` 吗？"
    不能。整数约束一旦写上，小数就超出上界，赋值时被拒绝；它和 `epsilon` 是两件独立的事，`epsilon` 不会自动帮你把值取整。

!!! warning "常见坑：把 `Number` 当 64 位整数用"
    `Number` 不会在 2⁶³ 附近环绕，也不会悄悄截断。要位宽、要环绕、要位运算，用 `BitInteger`、`BitSet` 这类显式类型；把 `Number` 当 `long` 写，边界处的行为会和预期不同。

数值类型不止普通 `Number`。需要无界精确整数、固定位宽、固定布局浮点、目标机器浮点或位集合时，标准库分别提供 `Integer`/`UnsignedInteger`、`BitInteger`、`BitFloat`、`NativeFloat` 与 `BitSet<size:N>`；它们的构造、约束与取舍见[数值与位类型](numeric-types.md)。

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

??? question "先猜：`'你好'.count` 是 2 还是 6？"
    `2`。`count` 数的是 Unicode 标量，`'你好'` 有两个；按字节数才是 `6`。网络协议、文件偏移、缓冲区这类按字节算的场合，用 `byte_count`，不要用 `count`。

不要混淆 `Text` 与 `Char`：

- `'a'` 是只含一个标量的 `Text`，不是 `Char`。
- 索引文本、或用 `Char(...)` 构造，得到 `Char`；`Text` 按 Unicode 标量计数，而 `Char` 可以保存任意 N 位数据，`Char<bitWidth: 8>(170)` 合法，即使该值不是合法标量。
- 比较、相等与哈希按内容或标量值，不按位宽；拼接得到新的 `Text`。

??? quote "彩蛋：`Char` 不是“一个字符”"
    名字容易骗人：`Char` 存的是任意 N 位的数据单元，不保证是合法 Unicode 标量。`'a'` 反而是 `Text`。把两者当同义词，会在处理非 UTF-8 数据时出问题。

## t、nil、void：三种“空”

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

!!! warning "常见坑：默认值不认 `nil`"
    参数默认值和解构默认值只在**项缺失或值为 `void`** 时生效，`nil` 会原样传进去。写 `fn f(x: Number = 10)` 之后调用 `f(nil)`，进函数的是 `nil`，不是 `10`。

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
// label = 72             // 编译错误：72 超出 Text 上界

let amount: Number = 1
// amount = "one"         // 编译错误：Text 不在 Number 上界内
```

- 有注解的局部 `let` 允许在注解范围内细化或加宽实际值版本。例如 `let buffer: Text = '123'` 之后写入 `'鸡'`，实际值版本会加宽到能容纳该标量的位宽；显式写死的固定宽度上界不能靠运行期自动加宽越过。
- 无注解的 `let` 可以换类型，但换型仍按普通赋值规则选择重载；类型变化后，运算按当前值的可达类型解析。
- `const` 的只读是浅层的：重赋、复合赋值、步进或经别名写回都是违规；重赋和经别名写回属于未定义行为，确定违规由 `elf` 报错。

!!! warning "常见坑：`const` 只保护绑定本身"
    `const` 不让绑定换值，但不冻结它指向的对象。经别名写回、复合赋值、步进都可能绕过它，其中一部分属于**未定义行为**——程序可能照跑，只是结果不保证。为什么这件事要在读语言前先知道，见[读语言之前](before-you-start.md)。

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

## 数组、对象与矩阵：三种字面量

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

## any：显式放弃类型保证

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

!!! warning "常见坑：以为 `any` 会自动适配"
    `let x: any = 1` 之后写 `x + 1` 不一定合法：运算前得先缩窄。`any` 是“我放弃静态保证”的声明，不是“编译器帮我兜底”的开关。

## 带走这三样

- `Number` 是精确有理数，`(1 / 3) * 3` 正好是 `1`；需要位宽、浮点或位集合时换专门类型。
- `t`、`nil`、`void` 是三种不同的“空”：真值、标准假值、没有结果；默认值只认 `void`。
- 类型注解是上界；`any` 要显式缩窄，`const` 只保护绑定本身。

## 下一站：数值与位类型

> 既然 `Number` 是精确有理数，那“必须 64 位、溢出要环绕”的场合怎么办？

- 主推进：[数值与位类型](numeric-types.md)：`BitInteger`、`BitFloat`、`NativeFloat` 与 `BitSet` 各自负责什么。
- 想先练手：[15 分钟速览](../tour.md)：把这一页的字面量放进一个完整小程序里。
- 后面会用到：[集合与文本](../stdlib/collections.md)：数组和文本的常用方法。
