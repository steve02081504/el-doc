# 类型

| 查询 | 规则 |
| --- | --- |
| 局部注解 | `let` 注解是值版本的上界 |
| 联合 | `T | U` 表示类型联合 |
| 普通隐式转换 | 每条路径最多一层用户隐式转换 |
| 缺失 | `nil` 与 `f` 不同，条件中缺失按假处理 |

## 类型表达式

类型注解写作 `name: Type`。类型语法包括函数类型、泛型实参、联合类型、元组与类型查询。泛型实参通常必须写出形参名；仅当实参列表恰有一个参数且声明的首个形参是类型参数时，允许省略名称，例如 `Array<ExamplePoint>`。

```el
// @external origin: ExamplePoint, ExamplePoint: type
let point: ExamplePoint = origin
let maybeText: Text | nil_t = nil
```

这里仅展示注解写法。类型位置的 `|` 表示联合类型；表达式中的同一符号按表达式上下文解释。

类型参数与值参数的声明、具名实参、单类型参数简写及 `@requires` 候选约束见[泛型与约束](generics.md)。

## 声明约束与当前位置的类型

每次初始化或写入都建立一个值版本。读取、`typeof` 和重载选择使用当前位置可到达的类型。显式注解规定绑定可以接收哪些值。省略注解的局部 `let` 可以在后续写入时换类型。分支合流需要容纳所有可达版本。

在 `let x: Base = Derived()` 中，能无歧义地适配到 `Base` 的派生值保留 `Derived` 类型。后续可给 `x` 写入其他满足 `Base` 的值。若初值不属于 `Base` 且 `Base` 指定具体类，初始化按显式 `Base(expr)` 处理，shared 类也适用。

### 数值范围如何随写入变化 { #numeric-range-updates }

```el
let a: Number = 3
let b = console.stdin.readAs(parsers.integer(min: 0, max: 60, epsilon: 0))
a = a + b
b = '3'
```

| 位置 | 当前值的类型 |
| --- | --- |
| `a` 初始化后 | `Number<min: 3, max: 3, epsilon: 0, integer: t>` |
| `b` 读入后 | `Number<min: 0, max: 60, epsilon: 0, integer: t>` |
| `a` 写入和之后 | `Number<min: 3, max: 63, epsilon: 0, integer: t>` |
| `b` 写入文本之后 | `Text<bitWidth: 8, size: 1>` |

读取时，解析器使用调用者提供的上下界、精度和整数要求校验输入。它的声明决定静态范围，因此输入恰好是 12 也仍按 `[0, 60]` 参与静态重载。加法把两个最小值相加、两个最大值相加。两个输入保证为整数，所以和也是整数。这里 `epsilon: 0` 表示精确。

数值实参可匹配覆盖其范围、误差和整数合同的形参。例如初始的 `a` 同时匹配 `[0, 60]` 和 `[0, 100]` 的精确整数形参时，先选 `[0, 60]`。直接调用也可以从当前位置的显式目标接收具名实参，例如把注解的 `epsilon` 交给初始化器中的 `sqrt`。

对声明了环绕策略的绑定，`a++` 和 `a += 1` 按声明更新目标。`a + 1` 单独计算一个新结果，函数返回值携带的策略也不会传给下一次运算。普通除法可以产生分数，例如 `Integer(7) / Integer(2)` 得到 `7/2`。

!!! note "实现状态"
    数值库会保留并计算值域。两套编译器的 `typeof`、范围重载和受约束更新仍待接通。上表描述语言合同。

### 容器的构造推断 { #container-construction-inference }

数组、Map 和 Set 的构造推断由容器库登记。函数内声明在同一函数内求解，模块声明在同一模块内求解，类声明在同一类内求解。证据不足或无法确定唯一类型时，在声明处报错。

空数组可由范围内的用法提供元素类型。`let xs = @[Derived()]` 也可由同一范围内需要 `Base[]` 的调用推断出更宽的元素类型。`let xs: Base[] = @[Derived()]` 则已给出约束，后续使用须满足它。

!!! note "实现状态"
    seed 支持部分函数局部数组推断。统一的容器登记及模块、类内推断仍待接通。

## 值集合与文本键签名

以下为设计中的类型工具。值域可以表达单点、区间、前缀以及它们的并、交、差。遍历 `"ab"` 追加 `'c'` 的结果时，元素域包含 `'a'`、`'b'`、`'c'`，因此只接受前两个字符的函数无法接收该迭代元素。数组 `@[0, 3]` 加入一个 `[2, 50]` 的整数后，元素域为 `{0} ∪ [2, 50]`。这个域排除 1，但仍包含 21 到 50。

索引运算符可以用文本键域描述读取签名。例如把 `On` 前缀域减去 `On_` 前缀域，再用该域作为 `operator[]` 的参数类型。这样 `handlers["OnClick"]` 可以按签名返回函数，`handlers["On_Click"]` 会在键检查时被拒绝。普通 `Text` 键可以先做受检窄化，再用于索引。

若同时声明接收 `On`、`On_` 两种前缀的重载，已知以 `On_` 开头的键选较窄的重载。静态类型只保证 `On` 的键选覆盖整个域的重载。需要按实际键分派时，先检查前缀再在分支中调用。运行时取得的前缀可用于匹配和分派，类型实参所需的域在编译期确定。

## 联合与动态类型

`any` 表示动态类型存储。`t_t`、`f_t`、`nil_t` 是标准环境提供的普通类型，不是编译器内建类。`f` 与 `nil` 是不同的值；缺失结果与假值不同，但条件中缺失按假值处理。

`Bool` 是 `t_t | f_t` 的类型别名，布尔值本来就是这两种类型之一，不需要再转换成该联合。不要把值名字 `t`、`f` 与类型名字混写成 `t | f`。`Bool(value)` 是同名的条件求值函数，按输入返回 `t` 或 `f`；相关例子见[条件转换](conversions.md#conditions)。

## 相关条目

- [左值、右值与亡值](value-categories.md)
- [赋值、复制与共享](assignment-semantics.md)
- [复制消除](copy-elision.md)

- [类型转换](conversions.md)
- [重载解析](overload-resolution.md)

- [声明与绑定](declarations.md)
- [表达式与运算符](expressions.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [核心语义](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [数值语义](https://github.com/steve02081504/el/blob/master/docs/spec/04-numbers.md)
