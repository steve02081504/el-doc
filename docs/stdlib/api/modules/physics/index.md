# physics/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/physics.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 物理计算 {#api-e59cca203873add0b061}

源码：`src/stdlib/physics/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L1)

使用带单位的量计算力学、流体静力学和电学结果。

## acceleration {#api-64f732cae3d9a028f029}

源码：`src/stdlib/physics/index.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L50)

根据力和质量计算加速度。

```el-signature
export fn acceleration(force, mass)
```

**参数**：force 可转换为牛顿的力，支持相应的量向量。

**参数**：mass 可转换为千克的有限正质量。

**返回值**：力除以质量得到的加速度。

**失败与异常**：质量非有限或非正、单位不兼容，或底层量运算失败时抛出异常。

### 示例：计算加速度

```el
import { kilogram, newton } from "el:units/"
import /^operator / from "el:units/"
import { acceleration } from "el:physics/"
let result = acceleration(10newton, 2kilogram)
```

<span id="api-9d8502b2d977f65ef7b6"></span>

## constantForceImpulse~timeDiff {#api-a300beb251e4b237a253}

源码：`src/stdlib/physics/index.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L75)

用时间差计算恒力产生的冲量。

```el-signature
export fn constantForceImpulse(force, duration: TimeDiff)
```

**参数**：force 可转换为牛顿的力，支持相应的量向量。

**参数**：duration 非负的时间差，以其总秒数计算。

**返回值**：力与持续时间的乘积。

**失败与异常**：时间差不能换算为总秒数、持续时间为负、单位不兼容，或底层量运算失败时抛出异常。

### 示例：使用时间差

```el
import { newton } from "el:units/"
import { TimeDiff } from "el:time/"
import /^operator / from "el:units/"
import { constantForceImpulse } from "el:physics/"
let result = constantForceImpulse(3newton, TimeDiff())
```

## constantForceImpulse~quantity {#api-19445f9734440c9f8b54}

源码：`src/stdlib/physics/index.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L89)

用时间量计算恒力产生的冲量。

```el-signature
export fn constantForceImpulse(force, duration)
```

**参数**：force 可转换为牛顿的力，支持相应的量向量。

**参数**：duration 可转换为秒的有限非负时间量。

**返回值**：力与持续时间的乘积。

**失败与异常**：持续时间非有限或为负、单位不兼容，或底层量运算失败时抛出异常。

### 示例：使用时间量

```el
import { newton, second } from "el:units/"
import /^operator / from "el:units/"
import { constantForceImpulse } from "el:physics/"
let result = constantForceImpulse(3newton, 2second)
```

## hydrostaticPressureIncrease {#api-488c5c38665ecaea60fd}

源码：`src/stdlib/physics/index.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L115)

计算均匀流体中深度造成的静水压力增量。

```el-signature
export fn hydrostaticPressureIncrease(density, gravityMagnitude, depth)
```

**参数**：density 可转换为千克每立方米的有限非负密度。

**参数**：gravityMagnitude 可转换为米每平方秒的有限非负重力加速度大小。

**参数**：depth 可转换为米的有限非负深度。

**返回值**：以帕斯卡表示的压力增量。

**失败与异常**：输入非有限、为负或单位不兼容时抛出异常。

### 示例：计算压力增量

```el
import { kilogram, metre, second } from "el:units/"
import /^operator / from "el:units/"
import { hydrostaticPressureIncrease } from "el:physics/"
let increase = hydrostaticPressureIncrease((1000kilogram / (metre ^ 3)), (9.81metre / (second ^ 2)), 2metre)
```

## hydrostaticAbsolutePressure {#api-5ffe2cac67dba8195e59}

源码：`src/stdlib/physics/index.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L137)

将表面压力与静水压力增量相加，计算绝对压力。

```el-signature
export fn hydrostaticAbsolutePressure(surfacePressure, density, gravityMagnitude, depth)
```

**参数**：surfacePressure 可转换为帕斯卡的有限非负表面压力。

**参数**：density 可转换为千克每立方米的有限非负密度。

**参数**：gravityMagnitude 可转换为米每平方秒的有限非负重力加速度大小。

**参数**：depth 可转换为米的有限非负深度。

**返回值**：以帕斯卡表示的绝对压力。

**失败与异常**：输入非有限、为负或单位不兼容时抛出异常。

### 示例：计算绝对压力

```el
import { kilogram, metre, pascal, second } from "el:units/"
import /^operator / from "el:units/"
import { hydrostaticAbsolutePressure } from "el:physics/"
let pressure = hydrostaticAbsolutePressure(100000pascal, (1000kilogram / (metre ^ 3)), (9.81metre / (second ^ 2)), 2metre)
```

## ohmicCurrent {#api-e32cf7aa5c64b770648f}

源码：`src/stdlib/physics/index.el:160` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/physics/index.el#L160)

根据电压和电阻计算欧姆电流。

```el-signature
export fn ohmicCurrent(voltage, resistance)
```

**参数**：voltage 可转换为伏特的有限电压，可为负。

**参数**：resistance 可转换为欧姆的有限正电阻。

**返回值**：以安培表示的电流，符号随电压变化。

**失败与异常**：电压或电阻非有限、电阻非正或单位不兼容时抛出异常。

### 示例：计算负电流

```el
import { ohm, volt } from "el:units/"
import /^operator / from "el:units/"
import { ohmicCurrent } from "el:physics/"
let current = ohmicCurrent(-12volt, 6ohm)
```
