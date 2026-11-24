# units/constants.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 物理常量 {#api-b08488aa488b77cc2981}

源码：`src/stdlib/units/constants.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L1)

提供带 SI 单位的定义值、约定值、实验参考值与可细化的公式值。

## speedOfLight {#api-76f2c5e19bdde6e081ee}

源码：`src/stdlib/units/constants.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L20)

真空光速，SI 精确定义值。

```el-signature
export let speedOfLight = 299792458 * (metre / second)
```

### 示例：使用示例

```el
import { speedOfLight } from "el:units/"
let value = speedOfLight
```

## caesiumHyperfineFrequency {#api-a5a9d6237a3b3b1d0793}

源码：`src/stdlib/units/constants.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L28)

铯 133 超精细跃迁频率，SI 精确定义值。

```el-signature
export let caesiumHyperfineFrequency = 9192631770 * (one / second)
```

### 示例：使用示例

```el
import { caesiumHyperfineFrequency } from "el:units/"
let value = caesiumHyperfineFrequency
```

## planckConstant {#api-939796812e96ce99913b}

源码：`src/stdlib/units/constants.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L36)

普朗克常量，SI 精确定义值。

```el-signature
export let planckConstant = 6.62607015e-34 * (joule * second)
```

### 示例：使用示例

```el
import { planckConstant } from "el:units/"
let value = planckConstant
```

## elementaryCharge {#api-30fee31dce69ed3e9ce8}

源码：`src/stdlib/units/constants.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L44)

元电荷，SI 精确定义值。

```el-signature
export let elementaryCharge = 1.602176634e-19 * coulomb
```

### 示例：使用示例

```el
import { elementaryCharge } from "el:units/"
let value = elementaryCharge
```

## boltzmannConstant {#api-321378b0e34b16b1b8e1}

源码：`src/stdlib/units/constants.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L52)

玻尔兹曼常量，SI 精确定义值。

```el-signature
export let boltzmannConstant = 1.380649e-23 * (joule / kelvinDifference)
```

### 示例：使用示例

```el
import { boltzmannConstant } from "el:units/"
let value = boltzmannConstant
```

## avogadroConstant {#api-b45b6024ed33858d45cc}

源码：`src/stdlib/units/constants.el:60` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L60)

阿伏伽德罗常量，SI 精确定义值。

```el-signature
export let avogadroConstant = 6.02214076e23 * (one / mole)
```

### 示例：使用示例

```el
import { avogadroConstant } from "el:units/"
let value = avogadroConstant
```

## luminousEfficacyConstant {#api-c0549c6afafeb0f304f2}

源码：`src/stdlib/units/constants.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L69)

540 THz 单色辐射的发光效能定义值。

```el-signature
export let luminousEfficacyConstant = 683 * (candela / watt)
```

### 示例：使用示例

```el
import { luminousEfficacyConstant } from "el:units/"
let value = luminousEfficacyConstant
```

## standardGravity {#api-c3844b3c010ca0981645}

源码：`src/stdlib/units/constants.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L78)

标准重力加速度，约定值。

```el-signature
export let standardGravity = 9.80665 * (metre / (second ^ 2))
```

### 示例：使用示例

```el
import { standardGravity } from "el:units/"
let value = standardGravity
```

## standardAtmosphericPressure {#api-4199324f103c007e8960}

源码：`src/stdlib/units/constants.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L86)

标准大气压，约定值。

```el-signature
export let standardAtmosphericPressure = 101325 * pascal
```

### 示例：使用示例

```el
import { standardAtmosphericPressure } from "el:units/"
let value = standardAtmosphericPressure
```

## standardStatePressure {#api-41d18e7b15eac5bf2f2a}

源码：`src/stdlib/units/constants.el:94` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L94)

标准态压力，约定值。

```el-signature
export let standardStatePressure = 100000 * pascal
```

### 示例：使用示例

```el
import { standardStatePressure } from "el:units/"
let value = standardStatePressure
```

## molarGasConstant {#api-030bb23bbb4fb15123d1}

源码：`src/stdlib/units/constants.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L102)

摩尔气体常量，SI 定义值的精确乘积。

```el-signature
export let molarGasConstant = avogadroConstant * boltzmannConstant
```

### 示例：使用示例

```el
import { molarGasConstant } from "el:units/"
let value = molarGasConstant
```

## faradayConstant {#api-9d25c2ba30884cc53df7}

源码：`src/stdlib/units/constants.el:110` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L110)

法拉第常量，SI 定义值的精确乘积。

```el-signature
export let faradayConstant = avogadroConstant * elementaryCharge
```

### 示例：使用示例

```el
import { faradayConstant } from "el:units/"
let value = faradayConstant
```

## idealGasMolarVolumeAtSTP {#api-cce28fb5b88ae1ff3757}

源码：`src/stdlib/units/constants.el:119` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L119)

273.15 K、100 kPa 下理想气体的摩尔体积。

```el-signature
export let idealGasMolarVolumeAtSTP = molarGasConstant * (273.15 * kelvinDifference) / standardStatePressure
```

### 示例：使用示例

```el
import { idealGasMolarVolumeAtSTP } from "el:units/"
let value = idealGasMolarVolumeAtSTP
```

## gravitationalConstant {#api-8b8a1c84c0269fae6965}

源码：`src/stdlib/units/constants.el:129` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L129)

牛顿引力常量的 中心参考值。

```el-signature
export let gravitationalConstant = 6.67430e-11 * gravitationUnit
```

### 示例：使用示例

```el
import { gravitationalConstant } from "el:units/"
let value = gravitationalConstant
```

## gravitationalConstantStandardUncertainty {#api-2b71bd006bb4d8f48075}

源码：`src/stdlib/units/constants.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L138)

引力常量的 标准不确定度，以一个标准差表示。

```el-signature
export let gravitationalConstantStandardUncertainty = 1.5e-15 * gravitationUnit
```

### 示例：使用示例

```el
import { gravitationalConstantStandardUncertainty } from "el:units/"
let value = gravitationalConstantStandardUncertainty
```

## reducedPlanckConstant {#api-81bcf4845d0d99b9f976}

源码：`src/stdlib/units/constants.el:157` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L157)

计算 ħ = h/(2π)。epsilon 是以 J·s 计的有限正最大绝对计算误差。

```el-signature
export fn reducedPlanckConstant(epsilon: Number)
```

### 示例：使用示例

```el
import { reducedPlanckConstant } from "el:units/"
let value = reducedPlanckConstant(1e-40)
```

## planckLength {#api-cc47984375d67cecd3ff}

源码：`src/stdlib/units/constants.el:191` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L191)

计算 ℓₚ = √(ħG/c³)。epsilon 以米计，误差相对于 G 的参考值。

```el-signature
export fn planckLength(epsilon: Number)
```

### 示例：使用示例

```el
import { planckLength } from "el:units/"
let value = planckLength(1e-40)
```

## planckTime {#api-dc703507e5e70e944646}

源码：`src/stdlib/units/constants.el:205` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L205)

计算 tₚ = √(ħG/c⁵)。epsilon 以秒计，误差相对于 G 的参考值。

```el-signature
export fn planckTime(epsilon: Number)
```

### 示例：使用示例

```el
import { planckTime } from "el:units/"
let value = planckTime(1e-40)
```

## planckMass {#api-7239dff84a0c4aa3b25d}

源码：`src/stdlib/units/constants.el:219` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L219)

计算 mₚ = √(ħc/G)。epsilon 以千克计，误差相对于 G 的参考值。

```el-signature
export fn planckMass(epsilon: Number)
```

### 示例：使用示例

```el
import { planckMass } from "el:units/"
let value = planckMass(1e-40)
```

## planckTemperature {#api-47ccbecdda2cd207bf67}

源码：`src/stdlib/units/constants.el:233` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/constants.el#L233)

计算 Tₚ = √(ħc⁵/(Gk²))。epsilon 以开尔文计，误差相对于 G 的参考值。

```el-signature
export fn planckTemperature(epsilon: Number)
```

### 示例：使用示例

```el
import { planckTemperature } from "el:units/"
let value = planckTemperature(1e-40)
```
