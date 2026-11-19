# 数值与位类型

> 用精确数值算，`1 / 10 + 2 / 10 == 3 / 10` 是 `t`；在采用 binary64 布局的二进制目标上，`F64(0.1) + F64(0.2) == F64(0.3)` 却是 `f`。差别不在精度高低，在你选了哪一种数值类型。

!!! abstract "🎯 读完这页，你能"
    - 说出 `Number` 与 `DitFloat` 各自保证什么，什么时候必须换类型
    - 给 `Number` 加上范围、整数、精度与溢出约束，并知道越界时看到什么
    - 用 `DitInt`、`DitFloat`、`DitSet` 区分目标数位布局和固定外部编码
    - 判断什么时候该用精确数、目标数位和外部编码

    <span class="el-chip">⏱ 约 10 分钟</span> <span class="el-chip">前置：[值与类型](values.md)</span>

## 一句话结论

==日常计算一律用 `Number`；只有需要固定位宽、固定布局、目标机器浮点或位集合时，才换成别的类型。==

`Number` 的参考值是精确有理数：需要时用分子与分母保存，`1 / 3` 不会被舍入成二进制近似值，整数运算也不按机器字长环绕。近似计算由 `epsilon` 表达误差上限，而不是由底层机器格式决定。

`F64`、`U128` 这类名字不是语言内建类型，而是标准库或用户源码里的普通绑定，通常写成某个工厂结果的透明别名；类型身份来自工厂参数，不来自拼写。

??? note "可选 · 深入：类型身份看实参集合，不看书写顺序"
    类型身份按具名实参集合确定，省略的参数按工厂默认值补齐：`Number<integer: t>`、`Number<integer: t, overflow: "ub">` 与 `Number<overflow: "ub", integer: t>` 是同一个类型（NUM-45、NUM-46）。布局参数则不进入 `Number` 的约束表，含义也不与约束参数复用（NUM-49）。所以“看起来不一样”的两种写法可能同一个类型，“看起来一样”的两种参数却可能不同。

## 约束是类型的一部分：`Number<...>` 的五个参数

```el
let bounded: Number<min: 0, max: 100> = 72
let whole: Number<integer: t> = 7
let approximate: Number<epsilon: 0.001> = 1 / 3

let wrapped = Number<min: 0, max: 5, integer: t, overflow: "wrap">(4) + 3
```

约束写在类型实参里，赋值与每一次运算结果都要满足。`min` 与 `max` 构成闭区间，在构造与赋值时检查：`bounded` 写 72 合法，换成 101 会抛 `RangeError`。

`epsilon` 是该类型运算结果允许的最大绝对误差；`epsilon: 0` 表示要求精确，`sqrt` 一类可能产生无理数的入口会拒绝零误差目标。

??? question "先猜：写了 `Number<epsilon: 0.001>`，`1 / 3` 会被舍入成 `0.333` 吗？"
    不会。`epsilon` 是后续运算允许的误差上限，不是小数位数，也不是必须踩的数值网格；值本身仍按精确有理数保存（语言规范第 4 章 NUM-9、NUM-10）。想限制小数位数得自己舍入。

`integer: t` 是独立的整数约束，不能由 `epsilon` 推出来：`whole` 拒绝 1.5，而 `epsilon: 1` 本身不禁止小数。

`overflow` 决定运算结果越界时怎么处理；省略时是 `"ub"`，构造时的初始值越界总是抛 `RangeError`。`"wrap"` 只适用于整数约束与有限区间：

| 策略 | 越界结果 |
| --- | --- |
| `"error"` | 抛 `RangeError` |
| `"nan"` | 把结果变成无序 NaN |
| `"wrap"` | 在区间内按周期环绕 |
| `"ub"` | 不提供可依赖的恢复行为 |

上面 `4 + 3` 在 `[0, 5]` 上环绕为 1；约束参数同样参与类型身份，`Number<integer: t>` 与省略 `integer` 的 `Number` 不是同一个类型。

!!! example "动手 30 秒"
    把 `wrapped` 那行的 `overflow: "wrap"` 改成 `"error"` 再跑一次。这次不是打印 `1`，而是抛 `RangeError`——溢出策略确实参与每一次运算。

## 要纯整数，就别自己取整：`Integer` 与 `UnsignedInteger`

`Integer` 是 `Number<epsilon: 0, integer: t, overflow: "error">` 的透明绑定，`UnsignedInteger` 另外加上 `min: 0`。两者都是无界精确整数，不表示机器字，也不承诺原生整数 ABI。

```el
import { Integer, UnsignedInteger } from "el:number/index.el"

let quotient = Integer(8) / Integer(2)          // 4
let fraction = Number(Integer(7)) / Number(2)  // 7/2

let negative = UnsignedInteger(5) - UnsignedInteger(6)  // RangeError
```

`/` 仍是精确除法，不是隐式取整：`Integer(8) / Integer(2)` 整除，结果是 4；`Integer(7) / Integer(2)` 不能由整数接收者容纳，抛 `RangeError`。需要分数时先转成普通 `Number`，如第二行。

无符号类型把负结果视为越界：`UnsignedInteger(5)` 减 `6` 抛 `RangeError`。这两个类型不按机器位宽截断；除零与非整除等操作仍按各自运算合同报错。不要把它们当作机器整数或地址偏移来用。

显式转换同样检查约束：`Integer(UnsignedInteger(5))` 精确保值，`UnsignedInteger(Integer(5))` 检查非负。非整数、NaN 输入抛 `RangeError`；转换到 `UnsignedInteger` 时负数也抛 `RangeError`。转换不截断小数、不取绝对值，也不按模数环绕。

## 用 DitInt 固定目标数位宽度

“dit” 是目标表示中的一位。二进制的 dit 是 bit，三进制的一位能放 0、1、2。普通类型工厂不接受覆盖目标基数的参数。

`DitInt(digits, signed, min, max, overflow)` 的宽度按 dit 计，包含符号所需的容量。设 N 是宽度，R 是目标基数，M = R^N。无符号范围是 0 到 M−1，有符号范围是 −floor(M/2) 到 ceil(M/2)−1。`min` 和 `max` 只能收窄范围。移位与旋转也按目标数位，而不是固定二进制位。

```el
let Small = DitInt<digits: 8, signed: f, overflow: "error">
let value = Small(5)
console.stdout.writeLine(value.digitWidth())  // 8
```

这个类型在二进制目标容纳 0…255，在三进制目标容纳 0…6560。固定协议字节和真实 ABI 的布局要另外核对，不能从普通数值对象推断。

## 用 DitFloat 选择浮点布局

`DitFloat(sign_dits, fraction_dits, exponent_dits, exponent_bias, min, max, overflow)` 同样使用目标基数。`sign_dits` 为 0 或 1；`fraction_dits` 不含正规有效数的首位；`exponent_dits` 至少为 2；`exponent_bias` 是从指数编码中减去的偏置。`min`、`max` 与 `overflow` 约束值，不改变布局。

```el
let Small = DitFloat<sign_dits: 1, fraction_dits: 3, exponent_dits: 4, exponent_bias: 7>
console.stdout.writeLine(Small(4).sqrt().toNumber())  // 2
```

公开构造和同布局算术以最近偶数舍入，支持有符号零、渐进次正规数、无穷和 NaN。两种零数值相等，NaN 无序且不等于自身。有限值的 `toNumber()` 返回**实际存储值**的精确有理数，不保留负零；无穷和 NaN 不能转成有限有理数。布局参数不是精度约束 `epsilon`。要精确算金额或分数，默认用 `Number`。

在二进制目标，`sign_dits: 1, fraction_dits: 52, exponent_dits: 11, exponent_bias: 1023` 对应 binary64 的数值布局；这**不**把 `DitFloat` 对象变成 C ABI 值，也不保证其他基数上的编码相同。在确实读写固定协议时，用 `el:number/digit-float/codec.el` 的 `ExternalFloatFormat`／`ExternalFloatCodec` 指定外部字段。`ExternalFloatFormat.packNumber` 可把精确 `Number` 直接舍入到外部格式，避免先转成 `DitFloat` 再进行第二次舍入。

## 原生浮点是一项目标能力

原生浮点由显式 RIS 声明确定：`@builtin:vome:float:number(exponent: E)` 对应 EIR `float(E)`，不能省略 E。这里的指数是存储宽度层级，宽度为 R^E 个目标数位，不是数值的指数域，也不保证 IEEE 字段、舍入或浮点算术可用。只有具体目标声明支持的操作才成立，不能从“可以存储”推断“可以执行”。需要判断某个精确值能否被某原生类型表示，参见 [原生浮点合同](https://github.com/steve02081504/el/blob/master/docs/spec/native-float.md) 的 `canRepresentExactly`。

## 用 DitSet 保存固定数量的目标数位

`DitSet<size: N>` 保存 N 个目标数位，索引 0 最低。构造非负有限整数时必须精确放得下；当 N 为零时只接受零。移位补零，旋转按宽度回绕。同宽 `+` 和 `-` 分别逐位模加、模减，不进位、不借位；不会修改输入。

```el
let value = DitSet<size: 3>(1)
let combined = value + value
console.stdout.writeLine((combined - value).toNumber())  // 1
```

逐位最小和最大写 `dit_min`、`dit_max`。`DitSet` 不提供 `&`、`|`、`!` 或 `^` 的按位重载；`Number` 的 `^` 仍是乘方。普通集合的对称差是 `Set.symmetricDifference`，固定二进制协议使用自己的表示。详见[为什么 EL 没有异或](why-no-xor.md)。

## 怎么选

| 需求 | 选用的类型或接口 |
| --- | --- |
| 精确分数与大整数 | `Number` |
| 无界整数 | `Integer`、`UnsignedInteger` |
| 固定目标数位的整数 | `DitInt` |
| 固定目标数位布局的浮点与舍入 | `DitFloat` |
| 固定外部浮点编码 | `ExternalFloatFormat`／`ExternalFloatCodec` |
| 原生浮点存储与算术 | 显式 RIS 类型与目标能力 |
| 固定数量数位的独立组合 | `DitSet` |

## 带走这三样

- `Number` 默认精确；目标数位布局用 `DitInt`、`DitFloat` 或 `DitSet`。
- “二进制字节”“目标数位”和“原生 ABI”是不同的合同。
- 组合与撤销用 `dit_add_mod` 与 `dit_sub_mod`；两者只有在二进制中才总相同。

## 下一站：运算符与表达式

> `-2 ^ 2` 等于 `-4` 还是 `4`？为什么 `a & b` 不一定是 `Bool`？

- 主推进：[运算符与表达式](operators.md)：把类型和优先级一起用对，读懂 EL 和别的语言差别最集中的那块。
- 想补 `Number` 字面量与类型注解：[值与类型](values.md)。