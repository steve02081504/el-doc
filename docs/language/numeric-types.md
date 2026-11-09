# 数值与位类型

普通数字是精确的 `Number`，它没有固定位宽，也不按机器字长溢出。写普通计算时不需要别的数值类型。

但固定位宽、机器布局、ABI、目标默认浮点与位集合是另外的需求。标准库为此提供了 `Integer`、`UnsignedInteger` 这些整数绑定与 `BitInteger`、`BitFloat` 这些位布局工厂，以及目标机器浮点声明 `NativeFloat` 和位集合 `BitSet<size:N>`；这一页说明每个类型表示什么、构造时受哪些约束，以及什么时候该换用哪一种。

`F64`、`U128` 这类名字不是语言内建类型。它们是标准库或用户源码里的普通绑定，通常写成某个工厂结果的透明别名；类型身份来自工厂参数，不来自拼写。

## 普通 Number：精确值加约束

`Number` 的参考值是精确有理数：需要时用分子与分母保存，`1 / 3` 不会被舍入成二进制近似值，整数运算也不按机器字长环绕。近似计算由 `epsilon` 表达误差上限，而不是由底层机器格式决定。

约束写在类型实参里，赋值与运算结果都要满足：

```el
let bounded: Number<min: 0, max: 100> = 42
let whole: Number<integer: t> = 7
let approximate: Number<epsilon: 0.001> = 1 / 3

let wrapped = Number<min: 0, max: 5, integer: t, overflow: "wrap">(4) + 3
```

`min` 与 `max` 构成闭区间，约束在构造与赋值时检查：`bounded` 写 42 合法，换成 101 会抛 `RangeError`。

`integer: t` 是独立的整数约束，不能由 `epsilon` 推出来；`whole` 拒绝 1.5，而 `epsilon: 1` 本身不禁止小数。

`epsilon` 是该类型运算结果允许的最大绝对误差。`epsilon: 0` 表示要求精确，`sqrt` 一类可能产生无理数的入口会拒绝零误差目标。

`overflow` 决定运算结果越界时怎么处理；省略时是 `"ub"`，构造时的初始值越界总是抛 `RangeError`。`"wrap"` 只适用于整数约束与有限区间：

| 策略 | 越界结果 |
| --- | --- |
| `"error"` | 抛 `RangeError` |
| `"nan"` | 把结果变成无序 NaN |
| `"wrap"` | 在区间内按周期环绕 |
| `"ub"` | 不提供可依赖的恢复行为 |

上面 `4 + 3` 在 `[0, 5]` 上环绕为 1。约束参数与布局参数一样参与类型身份，`Number<integer: t>` 与省略 `integer` 的 `Number` 不是同一个类型。

## Integer 与 UnsignedInteger：无界精确整数

`Integer` 是 `Number<epsilon: 0, integer: t, overflow: "error">` 的透明绑定，`UnsignedInteger` 另外加上 `min: 0`。两者都是无界精确整数，不表示机器字，也不承诺原生整数 ABI。

```el
import { Integer, UnsignedInteger } from "el:number/index.el"

let quotient = Integer(8) / Integer(2)          // 4
let fraction = Number(Integer(7)) / Number(2)  // 7/2

let negative = UnsignedInteger(5) - UnsignedInteger(6)  // RangeError
```

`/` 仍是精确除法，不是隐式取整：`Integer(8) / Integer(2)` 整除，结果是 4；`Integer(7) / Integer(2)` 不能由整数接收者容纳，抛 `RangeError`。需要分数时先转成普通 `Number`，如第二行。

无符号类型把负结果视为越界：`UnsignedInteger(5)` 减 `6` 抛 `RangeError`。这两个类型不按机器位宽截断，也不会因为位宽不足而失败；除零与非整除等操作仍按各自运算合同报错。不要把它们当作机器整数或地址偏移来用。

显式转换也检查约束：`Integer(UnsignedInteger(5))` 精确保值，`UnsignedInteger(Integer(5))` 检查非负。非整数、NaN 输入抛 `RangeError`；转换到 `UnsignedInteger` 时负数也抛 `RangeError`。转换不截断小数、不取绝对值，也不按模数环绕。

## BitInteger：固定位宽的整数

`BitInteger(bits, sign_bits, min, max, overflow)` 把总位宽与符号位作为布局参数。整数性是布局的内在性质：`sign_bits` 为 0 时范围是 `[0, 2^bits - 1]`，为 1 时范围是 `[-2^(bits - sign_bits), 2^(bits - sign_bits) - 1]`。可选的 `min`、`max` 只能在这个推导区间内收窄。

```el
let U8 = BitInteger<bits: 8, sign_bits: 0, overflow: "error">
let value = U8(197)
let width = value.bitWidth()      // 8
let shifted = value >> 1          // 98

let Wrapped = BitInteger<bits: 8, sign_bits: 0, overflow: "wrap">
let next = Wrapped(255) + 1       // 0

let Narrow = BitInteger<bits: 8, sign_bits: 0, min: 7, max: 9, overflow: "error">
let within = Narrow(8)
```

`U8` 的合法范围是 0 到 255；`U8(197)` 合法，`U8(256)` 在构造时抛 `RangeError`，`U8(197) + 100` 也因 `overflow: "error"` 抛错。`Wrapped` 把 255 加 1 环绕回 0。`Narrow` 在 8 位布局上把范围收窄到 7 至 9，构造 8 合法，构造 6 或 10 越界。

`bits` 是包含符号位的总位宽：8 位无符号是 0 至 255，8 位有符号是 -128 至 127。左移、右移与旋转都保持位宽，位移量必须是有限非负整数。`U128` 可以是 `BitInteger<bits: 128, sign_bits: 0, overflow: "error">` 的普通类型绑定，128 位范围是布局算出来的，不是编译器内建能力。

## BitFloat：固定布局的浮点

`BitFloat(sign_bits, fraction_bits, exponent_bits, exponent_bias, min, max, overflow)` 用布局参数描述一个二进制浮点格式。这些参数是表示布局，不是 `epsilon` 那样的精度要求，也不能替代普通 `Number` 的精确语义。

```el
let F64 = BitFloat<sign_bits: 1, fraction_bits: 52, exponent_bits: 11, exponent_bias: 1023>
let rounded = F64(0.1) + F64(0.2)
let equal = rounded == F64(0.3)      // nil

let exact = 1 / 10 + 2 / 10
let exactEqual = exact == 3 / 10     // t
```

布局限制是 `sign_bits` 取 0 或 1、`fraction_bits` 取 1 至 52、`exponent_bits` 取 2 至 15，且总位数不超过 64。`sign_bits: 0` 的格式只表示非负数；需要负数就写 1。上面 `F64` 的布局对应 binary64；`F32` 的布局是 `sign_bits: 1, fraction_bits: 23, exponent_bits: 8, exponent_bias: 127`。

`F64(0.1)` 把精确有理数舍入到该格式，之后每一步都按格式的精度计算，所以 `0.1 + 0.2` 不再精确等于 `0.3`。普通 `Number` 的 `1 / 10 + 2 / 10` 仍然精确等于 `3 / 10`；要精确分数就用 `Number`，要固定布局与可复现的舍入就用 `BitFloat`。

## NativeFloat：目标默认机器浮点

`NativeFloat` 是显式导入的机器浮点声明，不是关键字，也不是 `BitFloat` 的别名。它默认省略位宽，格式由编译目标的默认原生浮点事实决定；内建托管目标默认是 binary32。

```el
import { NativeFloat } from "el:platform/machine/float.el"

let x = NativeFloat(0.1)
let annotated: NativeFloat = 0.1
let doubled = x * NativeFloat(2)
let infinity = NativeFloat(1) / NativeFloat(0)
```

`NativeFloat(0.1)` 把精确数字一次舍入到目标格式；`annotated` 演示单一原生浮点注解也能给普通数字字面量提供上下文。

运算遵循 IEEE：逐操作最近偶数舍入，保留有符号零、无穷与次正规数，算术得到的 NaN 规范为正安静 NaN。上面的 `1 / 0` 是 IEEE 无穷，而不是普通 `Number` 的除零异常。它也不会让普通 `Number` 自动降精度参与混合运算；需要机器浮点就写 `NativeFloat`，需要精确值就留在 `Number`。精度、有效数字与有限端点等格式事实用 `representation_digits`、`type_max` 一类目标查询读取。

`NativeFloat` 不承诺标量、SIMD、GPU 与矩阵加速共享同一最快格式，也不以类型声明证明后端零开销；具体执行成本仍要以目标与实测为准。

## BitSet：位集合

`BitSet<size:N>` 是普通标准库类型，内部是普通 Bool 数组，`N` 是编译期非负整数，索引 0 是最低位。允许 `N = 0`，此时唯一数值是零。二元 `&`、`|`、`^` 要求两侧同宽并返回独立的新位集合，`==` 也要求同宽并返回 `Bool`。

```el
let low = BitSet<size: 8>(0b1010_0101)
let high = BitSet<size: 8>(0b1111_0000)
let anded = low & high          // 0b1010_0000
let ored = low | high           // 0b1111_0101
let xored = low ^ high          // 0b0101_0101
let inverted = !low             // 0b0101_1010
let shifted = low << 1          // 0b0100_1010
let rotated = low.rotateRight(1)  // 0b1101_0010
let value = xored.toNumber()    // 85
```

构造只接受非负有限整数，并且必须能被请求的位宽完整表示：不截断、不补码、不饱和。不同宽度的位集合、以及与普通数值混合的二元运算都会被拒绝。

`^` 在 `BitSet` 上是逐位异或；普通 `Number` 的 `^` 是乘方，两个重载按接收者类型选择。`!` 只翻转恰好 `N` 位，不产生无限高位。左移、右移与旋转同样保持 `N` 位：位移量必须是有限非负整数，大于等于 `N` 的移位得到零，旋转按 `N` 取模。

`toNumber()` 用精确整数累积逐位还原数值，不经过舍入；`Number(bits)` 与它共享同一转换核心。位集合适合位掩码、协议字段和需要按位组合的配置，不适合普通算术。

## 怎么选

| 需求 | 选用的类型 | 关键点 |
| --- | --- | --- |
| 日常计算、精确分数与大整数 | `Number` | 精确有理数；约束写在类型实参里 |
| 数学整数、无界、非机器字 | `Integer`、`UnsignedInteger` | 精确整数；非整除除法与负的无符号结果抛 `RangeError` |
| 固定位宽整数、移位旋转、ABI | `BitInteger` | `bits` 与 `sign_bits` 决定范围；布局进入类型身份 |
| 固定 IEEE 浮点格式 | `BitFloat` | 布局参数决定舍入格式；不是 `epsilon` |
| 目标默认机器浮点、外部 ABI | `NativeFloat` | 显式导入；目标选择格式；IEEE 运算 |
| 位掩码、协议字段、位集合 | `BitSet<size:N>` | Bool 位数组；同宽按位与、或、异或 |

需要跨目标复现位级结果时，固定 `BitFloat` 布局比 `NativeFloat` 更直接；`NativeFloat` 的默认格式可能随目标变化。需要精确数学时不要为了性能提前换浮点，`Number` 的精确性本身就是默认合同。

## 继续阅读

- [值与类型](values.md)：类型注解、绑定与 `Number` 字面量的基础。
- [运算符与表达式](operators.md)：`^`、移位与复合赋值的解析规则。
- [集合与文本](../stdlib/collections.md)：数组、文本与位集合在集合库中的位置。
- [神经网络](../stdlib/neural-networks.md)：用 `Number`／`BitFloat` 张量搭建并训练小模型。
