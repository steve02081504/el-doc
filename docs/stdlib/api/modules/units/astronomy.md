# units/astronomy.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 天文与大地测量常量 {#api-ac64169817b332891cf8}

源码：`src/stdlib/units/astronomy.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L1)

精确天文单位、太阳和行星的名义换算值、地球参考椭球参数。

## astronomicalUnit {#api-ecf65166a6a640d3ade9}

源码：`src/stdlib/units/astronomy.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L23)

天文单位 au，精确等于 149597870700 米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let astronomicalUnit = defineUnit("astronomicalUnit", metre, 149597870700, "au")
```

### 示例：用法

```el
import { astronomicalUnit, metre } from "el:units/"
import /^operator / from "el:units/"
let metresPerAu = (1 * astronomicalUnit).valueIn(metre, Number)
```

## julianYear {#api-c7391f3d722372356bd8}

源码：`src/stdlib/units/astronomy.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L34)

儒略年 a，精确等于 365.25 天，适用于天文历时。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let julianYear = defineUnit("julianYear", day, 365.25, "a")
```

### 示例：用法

```el
import { julianYear, second } from "el:units/"
import /^operator / from "el:units/"
let secondsPerJulianYear = (1 * julianYear).valueIn(second, Number)
```

## julianCentury {#api-31b2c7797d04945cfc8d}

源码：`src/stdlib/units/astronomy.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L45)

儒略世纪，精确等于 100 儒略年。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let julianCentury = defineUnit("julianCentury", julianYear, 100, "cy")
```

### 示例：用法

```el
import { julianCentury, day } from "el:units/"
import /^operator / from "el:units/"
let daysPerCentury = (1 * julianCentury).valueIn(day, Number)
```

## lightYear {#api-9bfaf34f4ad32d610d08}

源码：`src/stdlib/units/astronomy.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L56)

光年 ly，是真空中的光在一个儒略年内走过的精确距离。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let lightYear = defineUnit("lightYear", metre, speedOfLight.exactMagnitude() * julianYear.scale, "ly")
```

### 示例：用法

```el
import { lightYear, kilometre } from "el:units/"
import /^operator / from "el:units/"
let kilometresPerLightYear = (1 * lightYear).valueIn(kilometre, Number)
```

## parsec {#api-81dd97c7f76adbbe8704}

源码：`src/stdlib/units/astronomy.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L66)

计算 1 秒差距 (648000/π) au。epsilon 是以米计的有限正最大绝对误差。

```el-signature
export fn parsec(epsilon: Number)
```

### 示例：将 1 秒差距换算为米

```el
import { parsec, metre } from "el:units/"
let metresPerParsec = parsec(0.001).valueIn(metre, Number)
```

## nominalSolarRadius {#api-5b3a589d24b1f173956b}

源码：`src/stdlib/units/astronomy.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L86)

太阳名义半径 R☉ᴺ。

```el-signature
export let nominalSolarRadius = 695700000 * metre
```

### 示例：用法

```el
import { nominalSolarRadius, metre } from "el:units/"
let reference = nominalSolarRadius.valueIn(metre, Number)
```

## nominalSolarIrradiance {#api-3dc912d23570e7b1f48e}

源码：`src/stdlib/units/astronomy.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L96)

在 1 au 处的太阳名义总辐照度。

```el-signature
export let nominalSolarIrradiance = 1361 * (watt / (metre ^ 2))
```

### 示例：用法

```el
import { nominalSolarIrradiance, watt, metre } from "el:units/"
import /^operator / from "el:units/"
let reference = nominalSolarIrradiance.valueIn(watt / (metre ^ 2), Number)
```

## nominalSolarLuminosity {#api-20356bc4ea5dfcb9288b}

源码：`src/stdlib/units/astronomy.el:105` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L105)

太阳名义光度 L☉ᴺ。

```el-signature
export let nominalSolarLuminosity = 3.828e26 * watt
```

### 示例：用法

```el
import { nominalSolarLuminosity, watt } from "el:units/"
let reference = nominalSolarLuminosity.valueIn(watt, Number)
```

## nominalSolarEffectiveTemperature {#api-905f3d5fbb7d96414f20}

源码：`src/stdlib/units/astronomy.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L114)

太阳名义有效温度，坐标从绝对零度起算。

```el-signature
export let nominalSolarEffectiveTemperature = 5772 * kelvinDifference
```

### 示例：用法

```el
import { nominalSolarEffectiveTemperature, kelvinDifference } from "el:units/"
let reference = nominalSolarEffectiveTemperature.valueIn(kelvinDifference, Number)
```

## nominalSolarMassParameter {#api-a36cd1e8d01d8af948c3}

源码：`src/stdlib/units/astronomy.el:124` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L124)

太阳名义引力参数 (GM)☉ᴺ。

```el-signature
export let nominalSolarMassParameter = 1.3271244e20 * gravityParameterUnit
```

### 示例：用法

```el
import { nominalSolarMassParameter, metre, second } from "el:units/"
import /^operator / from "el:units/"
let reference = nominalSolarMassParameter.valueIn((metre ^ 3) / (second ^ 2), Number)
```

## nominalEarthEquatorialRadius {#api-189649c915219452bf75}

源码：`src/stdlib/units/astronomy.el:133` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L133)

地球名义赤道半径，用于天文换算。

```el-signature
export let nominalEarthEquatorialRadius = 6378100 * metre
```

### 示例：用法

```el
import { nominalEarthEquatorialRadius, metre } from "el:units/"
let reference = nominalEarthEquatorialRadius.valueIn(metre, Number)
```

## nominalEarthPolarRadius {#api-2932367a5907a98ddff9}

源码：`src/stdlib/units/astronomy.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L142)

地球名义极半径，用于天文换算。

```el-signature
export let nominalEarthPolarRadius = 6356800 * metre
```

### 示例：用法

```el
import { nominalEarthPolarRadius, metre } from "el:units/"
let reference = nominalEarthPolarRadius.valueIn(metre, Number)
```

## nominalEarthMassParameter {#api-2b34bf54d377b8a4c754}

源码：`src/stdlib/units/astronomy.el:152` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L152)

地球名义引力参数 (GM)⊕ᴺ。

```el-signature
export let nominalEarthMassParameter = 3.986004e14 * gravityParameterUnit
```

### 示例：用法

```el
import { nominalEarthMassParameter, metre, second } from "el:units/"
import /^operator / from "el:units/"
let reference = nominalEarthMassParameter.valueIn((metre ^ 3) / (second ^ 2), Number)
```

## nominalJupiterEquatorialRadius {#api-4bef0f8978efd7cba2ec}

源码：`src/stdlib/units/astronomy.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L161)

木星名义赤道半径。

```el-signature
export let nominalJupiterEquatorialRadius = 71492000 * metre
```

### 示例：用法

```el
import { nominalJupiterEquatorialRadius, metre } from "el:units/"
let reference = nominalJupiterEquatorialRadius.valueIn(metre, Number)
```

## nominalJupiterPolarRadius {#api-e4b5a3042d6296cfaec8}

源码：`src/stdlib/units/astronomy.el:170` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L170)

木星名义极半径。

```el-signature
export let nominalJupiterPolarRadius = 66854000 * metre
```

### 示例：用法

```el
import { nominalJupiterPolarRadius, metre } from "el:units/"
let reference = nominalJupiterPolarRadius.valueIn(metre, Number)
```

## nominalJupiterMassParameter {#api-699977f62b0496a4baab}

源码：`src/stdlib/units/astronomy.el:180` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L180)

木星名义引力参数 (GM)♃ᴺ。

```el-signature
export let nominalJupiterMassParameter = 1.2668653e17 * gravityParameterUnit
```

### 示例：用法

```el
import { nominalJupiterMassParameter, metre, second } from "el:units/"
import /^operator / from "el:units/"
let reference = nominalJupiterMassParameter.valueIn((metre ^ 3) / (second ^ 2), Number)
```

## wgs84InverseFlattening {#api-3cefda7b18326ac9f493}

源码：`src/stdlib/units/astronomy.el:189` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L189)

WGS 84 参考椭球的逆扁率 1/f，精确等于 298.257223563。

```el-signature
export let wgs84InverseFlattening = 298.257223563
```

### 示例：用法

```el
import { wgs84InverseFlattening } from "el:units/"
let flattening = 1 / wgs84InverseFlattening
```

## wgs84Flattening {#api-db3e67a2b4e09e6c4bce}

源码：`src/stdlib/units/astronomy.el:198` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L198)

WGS 84 参考椭球的扁率 f = (a − b)/a。

```el-signature
export let wgs84Flattening = 1 / wgs84InverseFlattening
```

### 示例：用法

```el
import { wgs84Flattening } from "el:units/"
let axisRatio = 1 - wgs84Flattening
```

## wgs84SemiMajorAxis {#api-3bb7bb6ab6977046e204}

源码：`src/stdlib/units/astronomy.el:207` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L207)

WGS 84 参考椭球的长半轴，也即赤道半径。

```el-signature
export let wgs84SemiMajorAxis = 6378137 * metre
```

### 示例：用法

```el
import { wgs84SemiMajorAxis, metre } from "el:units/"
let reference = wgs84SemiMajorAxis.valueIn(metre, Number)
```

## wgs84SemiMinorAxis {#api-7ab9071d414471d91370}

源码：`src/stdlib/units/astronomy.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L216)

由长半轴和扁率推导的 WGS 84 参考椭球短半轴。

```el-signature
export let wgs84SemiMinorAxis = (wgs84SemiMajorAxis.exactMagnitude() * (1 - wgs84Flattening)) * metre
```

### 示例：用法

```el
import { wgs84SemiMinorAxis, metre } from "el:units/"
let reference = wgs84SemiMinorAxis.valueIn(metre, Number)
```

## wgs84AngularVelocity {#api-b918e48eba0a5bc2f969}

源码：`src/stdlib/units/astronomy.el:226` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L226)

WGS 84 规定的地球名义平均角速度，以弧度每秒计。

```el-signature
export let wgs84AngularVelocity = 7.292115e-5 * (one / second)
```

### 示例：用法

```el
import { wgs84AngularVelocity, one, second } from "el:units/"
import /^operator / from "el:units/"
let reference = wgs84AngularVelocity.valueIn(one / second, Number)
```

## wgs84MassParameter {#api-2b11fd986f89f1344e63}

源码：`src/stdlib/units/astronomy.el:236` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/astronomy.el#L236)

WGS 84 定义的地球引力参数，包含大气的质量贡献。

```el-signature
export let wgs84MassParameter = 3.986004418e14 * gravityParameterUnit
```

### 示例：用法

```el
import { wgs84MassParameter, metre, second } from "el:units/"
import /^operator / from "el:units/"
let reference = wgs84MassParameter.valueIn((metre ^ 3) / (second ^ 2), Number)
```
