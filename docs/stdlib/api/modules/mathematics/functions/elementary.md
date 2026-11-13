# mathematics/functions/elementary.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数学初等函数 {#api-7d8af95145ca6c477bdb}

源码：`src/stdlib/mathematics/functions/elementary.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L14)

提供常用初等函数与圆周率近似，精度遵循输入 Number 类型的数值合同。

## sqrt {#api-fb173a899ba66d1e403d}

源码：`src/stdlib/mathematics/functions/elementary.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L27)

计算非负输入的平方根近似值。

```el
@pure
export fn sqrt(value)
```

**参数**：value 非负数值。

**返回值**：与输入数值语义相容的平方根近似值。

**失败与异常**：DomainError 当输入不在平方根定义域时抛出。

### 示例：计算平方根

```el
let root = sqrt(9)
```
示例展示接口用法；未运行验证。

## exp {#api-0eb3fa03c258f8a9125a}

源码：`src/stdlib/mathematics/functions/elementary.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L38)

计算自然指数函数的近似值。

```el
@pure
export fn exp(value)
```

**参数**：value 指数输入。

**返回值**：e 的 value 次幂近似值。

### 示例：计算自然指数

```el
let growth = exp(1)
```

## log {#api-1c0e614a110e84422686}

源码：`src/stdlib/mathematics/functions/elementary.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L50)

计算自然对数近似值。

```el
@pure
export fn log(value)
```

**参数**：value 正数输入。

**返回值**：value 的自然对数近似值。

**失败与异常**：DomainError 当输入不为正数时抛出。

### 示例：计算自然对数

```el
let logarithm = log(2)
```

## sin {#api-b86d1300e2b18347e166}

源码：`src/stdlib/mathematics/functions/elementary.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L66)

计算以弧度表示的正弦近似值。

```el
@pure
@optimize(data: @{ operation: "sin" })
export fn sin(value)
```

**参数**：value 有限弧度输入。

**返回值**：正弦函数近似值。

### 示例：计算单位圆上的正弦值

```el
import { sin } from "el:mathematics/"
let sample = sin(1.5707963267948966)
```
示例展示接口用法；未运行验证。

## pi {#api-ef44ff89f90725f1110c}

源码：`src/stdlib/mathematics/functions/elementary.el:124` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L124)

按指定 Number 类型的精度合同构造圆周率近似值。

```el
@pure
@optimize(data: @{ operation: "pi" })
export fn pi(Result: type)
```

**参数**：Result 输出 Number 类型。

**返回值**：Result 类型中的圆周率近似值。

**失败与异常**：PrecisionError 当输出类型要求不受支持的精度时抛出。

### 示例：请求指定精度的圆周率

```el
let Scalar = Number<min: unbounded, max: unbounded, epsilon: 0.001>
let circle = pi(Scalar)
```

## pow {#api-fa68c880d86864b1595c}

源码：`src/stdlib/mathematics/functions/elementary.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/elementary.el#L145)

计算底数的实数幂；省略 exponent 时计算平方。

```el
export fn pow(base, exponent = Number(2))
```

**参数**：base 底数。

**参数**：exponent 指数，默认 2。

**返回值**：幂运算的近似结果。

### 示例：计算三次方

```el
let cube = pow(2, 3)
```
