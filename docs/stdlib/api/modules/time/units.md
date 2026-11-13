# time/units.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间单位与格式化 {#api-73959705e96e3f6d20c9}

源码：`src/stdlib/time/units.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L1)

提供秒、日和纳秒的换算常量及时间数字格式化函数。

## whole {#api-8e669783c5c018bc539e}

源码：`src/stdlib/time/units.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L20)

```el
export fn whole(value: Number): Number
```

要求数值为有限整数并返回该值。

**参数**：value 待检查的数值。

**失败与异常**：非有限值或非整数值时抛 RangeError。

### 示例：示例

```el
import { whole } from "el:time/units.el"
whole(12)
```
预期结果：12。

## floorDivide {#api-a45599efdbefd59dc9cf}

源码：`src/stdlib/time/units.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L37)

```el
export fn floorDivide(value: Number, divisor: Number): Number
```

计算向负无穷取整的商，处理负值时不同于向零截断。

**参数**：value 被除数。

**参数**：divisor 除数。

**注意**：divisor 必须非零；本函数不显式检查零除数或数值范围。

### 示例：示例

```el
import { floorDivide } from "el:time/units.el"
floorDivide(-7, 3)
```
预期结果：-3。

## positiveRemainder {#api-5e84633337d1771b191b}

源码：`src/stdlib/time/units.el:55` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L55)

```el
export fn positiveRemainder(value: Number, divisor: Number): Number
```

按向下取整商计算正向余数。

**参数**：value 被除数。

**参数**：divisor 除数。

**注意**：divisor 必须非零；本函数不显式检查零除数或数值范围。

### 示例：示例

```el
import { positiveRemainder } from "el:time/units.el"
positiveRemainder(-7, 3)
```
预期结果：2。

## decimalDigits {#api-5eb68fec95e1642e33bd}

源码：`src/stdlib/time/units.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L69)

```el
export fn decimalDigits(value: Number, width: Number): Text
```

把数值转为文本，并在左侧补零至至少指定宽度。

**参数**：value 待格式化数值。

**参数**：width 最小字符数。

### 示例：示例

```el
import { decimalDigits } from "el:time/units.el"
decimalDigits(7, 3)
```
预期结果：007。

## fractionalSecond {#api-1cba6f923c3983128204}

源码：`src/stdlib/time/units.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L85)

```el
export fn fractionalSecond(nanoseconds: Number): Text
```

将纳秒小数部分格式化为可选的小数点后缀，并去掉末尾零。

**参数**：nanoseconds 秒内的纳秒部分。

**注意**：调用者应传入 0 到 999999999 的整数；本函数不校验范围。

### 示例：示例

```el
import { fractionalSecond } from "el:time/units.el"
fractionalSecond(120000000)
```
预期结果：.12。

## secondsText {#api-53debbf5972f3bb0cee0}

源码：`src/stdlib/time/units.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/units.el#L102)

```el
export fn secondsText(nanoseconds: Number): Text
```

将纳秒数格式化为秒文本，保留负号并省略无意义的末尾小数零。

**参数**：nanoseconds 有符号的纳秒数。

**注意**：调用者应传入整数纳秒；本函数不校验有限性或整数性。

### 示例：示例

```el
import { secondsText } from "el:time/units.el"
secondsText(1250000000)
```
预期结果：1.25。
