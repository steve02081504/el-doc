# mathematics/functions/constants.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 常用数学常量 {#api-e5d9653514d2e200f1bf}

源码：`src/stdlib/mathematics/functions/constants.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L1)

代数、几何、统计、声学和信息计算所用的可细化常量。

## eulerNumber {#api-393326230920c68244b1}

源码：`src/stdlib/mathematics/functions/constants.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L23)

自然指数的底 e = exp(1)。epsilon 是最大绝对误差。

```el-signature
export fn eulerNumber(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { eulerNumber } from "el:mathematics/"
let growthFactor = eulerNumber(1e-12)
```

## tau {#api-2e6656104ad4f45ef310}

源码：`src/stdlib/mathematics/functions/constants.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L35)

整周角的弧度数 τ = 2π。epsilon 是最大绝对误差。

```el-signature
export fn tau(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { tau } from "el:mathematics/"
let turnRadians = tau(1e-12)
```

## radiansPerDegree {#api-1a0ac9b333f870f5399e}

源码：`src/stdlib/mathematics/functions/constants.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L47)

每度的弧度数 π/180。epsilon 是以弧度计的最大绝对误差。

```el-signature
export fn radiansPerDegree(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { radiansPerDegree } from "el:mathematics/"
let oneDegree = radiansPerDegree(1e-12)
```

## radiansPerArcminute {#api-c9455ae5f1450d4258c9}

源码：`src/stdlib/mathematics/functions/constants.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L59)

每角分的弧度数 π/10800。epsilon 是以弧度计的最大绝对误差。

```el-signature
export fn radiansPerArcminute(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { radiansPerArcminute } from "el:mathematics/"
let oneArcminute = radiansPerArcminute(1e-12)
```

## radiansPerArcsecond {#api-c6b39c850c54e460a941}

源码：`src/stdlib/mathematics/functions/constants.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L71)

每角秒的弧度数 π/648000。epsilon 是以弧度计的最大绝对误差。

```el-signature
export fn radiansPerArcsecond(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { radiansPerArcsecond } from "el:mathematics/"
let oneArcsecond = radiansPerArcsecond(1e-12)
```

## sqrtTwo {#api-aa2fc7a432dff7c7706e}

源码：`src/stdlib/mathematics/functions/constants.el:83` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L83)

√2，单位正方形的对角线长度。epsilon 是最大绝对误差。

```el-signature
export fn sqrtTwo(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { sqrtTwo } from "el:mathematics/"
let squareDiagonal = sqrtTwo(1e-12)
```

## sqrtThree {#api-6d507fe7529d6f202774}

源码：`src/stdlib/mathematics/functions/constants.el:95` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L95)

√3，单位立方体的体对角线长度。epsilon 是最大绝对误差。

```el-signature
export fn sqrtThree(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { sqrtThree } from "el:mathematics/"
let cubeDiagonal = sqrtThree(1e-12)
```

## sqrtFive {#api-60fb0e6091b605c3b51e}

源码：`src/stdlib/mathematics/functions/constants.el:107` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L107)

√5，黄金比例公式中的正平方根。epsilon 是最大绝对误差。

```el-signature
export fn sqrtFive(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { sqrtFive } from "el:mathematics/"
let root = sqrtFive(1e-12)
```

## goldenRatio {#api-76a306061bc39f18ef2f}

源码：`src/stdlib/mathematics/functions/constants.el:119` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L119)

黄金比例 φ = (1 + √5)/2。epsilon 是最大绝对误差。

```el-signature
export fn goldenRatio(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { goldenRatio } from "el:mathematics/"
let ratio = goldenRatio(1e-12)
```

## lnTwo {#api-2dfddc0dc586b3506f22}

源码：`src/stdlib/mathematics/functions/constants.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L137)

2 的自然对数 ln(2)。epsilon 是最大绝对误差。

```el-signature
export fn lnTwo(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { lnTwo } from "el:mathematics/"
let doublingExponent = lnTwo(1e-12)
```

## lnTen {#api-6bc2664c89164e216bb6}

源码：`src/stdlib/mathematics/functions/constants.el:149` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L149)

10 的自然对数 ln(10)。epsilon 是最大绝对误差。

```el-signature
export fn lnTen(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { lnTen } from "el:mathematics/"
let decadeExponent = lnTen(1e-12)
```

## log2Ten {#api-2da14af068a4d2729e4d}

源码：`src/stdlib/mathematics/functions/constants.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L161)

以 2 为底的 10 的对数 log₂(10)，用于十进制数位与二进制数位的换算。epsilon 是最大绝对误差。

```el-signature
export fn log2Ten(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { log2Ten } from "el:mathematics/"
let bitsPerDecimalDigit = log2Ten(1e-12)
```

## standardNormalDensityAtZero {#api-9d94f4f9be64e5f825e5}

源码：`src/stdlib/mathematics/functions/constants.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L175)

标准正态分布在零处的概率密度 1/√(2π)。epsilon 是最大绝对误差。

```el-signature
export fn standardNormalDensityAtZero(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { standardNormalDensityAtZero } from "el:mathematics/"
let density = standardNormalDensityAtZero(1e-12)
```

## equalTemperedSemitoneRatio {#api-6b5cc334dcaae6038d13}

源码：`src/stdlib/mathematics/functions/constants.el:192` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/constants.el#L192)

十二平均律里相邻半音的频率比 2^(1/12)。epsilon 是最大绝对误差。

```el-signature
export fn equalTemperedSemitoneRatio(epsilon: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：epsilon 有限正最大绝对误差。

**返回值**：带有所请求误差上限的 Number 近似值。

**失败与异常**：epsilon 为零、负数或非有限数时抛出 PrecisionError。

### 示例：计算近似值

```el
import { equalTemperedSemitoneRatio } from "el:mathematics/"
let nextPitchHz = 440 * equalTemperedSemitoneRatio(1e-12)
```
