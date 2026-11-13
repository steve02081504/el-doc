# time/units.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间单位与格式化 {#api-73959705e96e3f6d20c9}

源码：`src/stdlib/time/units.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L1)

提供秒、日和纳秒的换算常量及时间数字格式化函数。

## whole {#api-8e669783c5c018bc539e}

源码：`src/stdlib/time/units.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L21)

```el
export fn whole(value: Number): Number
```

要求数值为有限整数并返回该值。

**参数**：value 待检查的数值。

**失败与异常**：非有限值或非整数值时抛 RangeError。

### 示例：检查整数输入

```el
import { whole } from "el:time/units.el"
whole(12)
```
预期结果：12。

**返回值**：经检查的原数值。

## floorDivide {#api-a45599efdbefd59dc9cf}

源码：`src/stdlib/time/units.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L39)

```el
export fn floorDivide(value: Number, divisor: Number): Number
```

当 divisor 为正数时，计算向负无穷取整的商。

**参数**：value 被除数。

**参数**：divisor 除数。

**注意**：divisor 必须为正数；本函数不显式检查除数或数值范围。

### 示例：对正除数作向下取整

```el
import { floorDivide } from "el:time/units.el"
floorDivide(-7, 3)
```
预期结果：-3。

**返回值**：向负无穷取整的商。

## positiveRemainder {#api-5e84633337d1771b191b}

源码：`src/stdlib/time/units.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L58)

```el
export fn positiveRemainder(value: Number, divisor: Number): Number
```

使用向下取整商计算余数；当 divisor 为正时，结果为非负余数。

**参数**：value 被除数。

**参数**：divisor 除数。

**注意**：divisor 必须为正数；本函数不显式检查除数或数值范围。

### 示例：计算正除数的非负余数

```el
import { positiveRemainder } from "el:time/units.el"
positiveRemainder(-7, 3)
```
预期结果：2。

**返回值**：非负余数，满足 0 ≤ result < divisor。

## decimalDigits {#api-5eb68fec95e1642e33bd}

源码：`src/stdlib/time/units.el:73` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L73)

```el
export fn decimalDigits(value: Number, width: Number): Text
```

把数值转为文本，并在左侧补零至至少指定宽度。

**参数**：value 待格式化数值。

**参数**：width 最小字符数。

### 示例：补足十进制位数

```el
import { decimalDigits } from "el:time/units.el"
decimalDigits(7, 3)
```
预期结果：007。

**返回值**：左侧补零后的文本。

## fractionalSecond {#api-1cba6f923c3983128204}

源码：`src/stdlib/time/units.el:90` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L90)

```el
export fn fractionalSecond(nanoseconds: Number): Text
```

将纳秒小数部分格式化为可选的小数点后缀，并去掉末尾零。

**参数**：nanoseconds 秒内的纳秒部分。

**注意**：调用者应传入 0 到 999999999 的整数；本函数不校验范围。

### 示例：格式化秒的小数部分

```el
import { fractionalSecond } from "el:time/units.el"
fractionalSecond(120000000)
```
预期结果：.12。

**返回值**：小数秒文本；输入为零时为空文本。

## secondsText {#api-53debbf5972f3bb0cee0}

源码：`src/stdlib/time/units.el:108` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L108)

```el
export fn secondsText(nanoseconds: Number): Text
```

将纳秒数格式化为秒文本，保留负号并省略无意义的末尾小数零。

**参数**：nanoseconds 有符号的纳秒数。

**注意**：调用者应传入整数纳秒；本函数不校验有限性或整数性。

### 示例：把纳秒转换为秒文本

```el
import { secondsText } from "el:time/units.el"
secondsText(1250000000)
```
预期结果：1.25。

**返回值**：秒数文本。
