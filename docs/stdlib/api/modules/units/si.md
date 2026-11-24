# units/si.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 国际单位制导出单位 {#api-3ad30912ffea25b6ec16}

源码：`src/stdlib/units/si.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L1)

从基础单位组合的常用国际单位制单位。

## newton {#api-d8155e776258ac4fec54}

源码：`src/stdlib/units/si.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L17)

力的国际单位制导出单位牛顿。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let newton = defineUnit("newton", kilogram * metre / (second ^ 2), 1, "N")
```

### 示例：使用示例

```el
import { newton } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1newton
```

## pascal {#api-556e3c267d5dbc84a8eb}

源码：`src/stdlib/units/si.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L27)

压力的国际单位制导出单位帕斯卡。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let pascal = defineUnit("pascal", newton / (metre ^ 2), 1, "Pa")
```

### 示例：使用示例

```el
import { pascal } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1pascal
```

## kilopascal {#api-5ff14a69fb644a35172e}

源码：`src/stdlib/units/si.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L37)

压力单位千帕，等于 1000 帕。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let kilopascal = defineUnit("kilopascal", pascal, 1000, "kPa")
```

### 示例：使用示例

```el
import { kilopascal } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilopascal
```

## joule {#api-d837f33716e3c6b9b4a7}

源码：`src/stdlib/units/si.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L47)

能量和功的国际单位制导出单位焦耳。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let joule = defineUnit("joule", newton * metre, 1, "J")
```

### 示例：使用示例

```el
import { joule } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1joule
```

## watt {#api-12f5835f3505b137d572}

源码：`src/stdlib/units/si.el:57` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L57)

功率单位瓦特，等于焦耳每秒。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension, DurationDimension])
export let watt = defineUnit("watt", joule / second, 1, "W")
```

### 示例：使用示例

```el
import { watt } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * watt
```

## coulomb {#api-aa977ccbbd3f65c3324b}

源码：`src/stdlib/units/si.el:67` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L67)

电荷单位库仑，等于安培秒。

```el-signature
@quantityDimension(numerator: @[CurrentDimension, DurationDimension])
export let coulomb = defineUnit("coulomb", ampere * second, 1, "C")
```

### 示例：使用示例

```el
import { coulomb } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * coulomb
```

## volt {#api-b1380e56034af98e8ee5}

源码：`src/stdlib/units/si.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L77)

电压的国际单位制导出单位伏特。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension, DurationDimension, CurrentDimension])
export let volt = defineUnit("volt", watt / ampere, 1, "V")
```

### 示例：使用示例

```el
import { volt } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1volt
```

## ohm {#api-2bf8d67950303a33dd95}

源码：`src/stdlib/units/si.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L87)

电阻的国际单位制导出单位欧姆。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension, DurationDimension, CurrentDimension, CurrentDimension])
export let ohm = defineUnit("ohm", volt / ampere, 1, "Ω")
```

### 示例：使用示例

```el
import { ohm } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1ohm
```

## hertz {#api-b08b72205bde3ecfd609}

源码：`src/stdlib/units/si.el:97` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L97)

频率单位赫兹；每秒一个周期。

```el-signature
@quantityDimension(denominator: @[DurationDimension])
export let hertz = defineUnit("hertz", one / second, 1, "Hz")
```

### 示例：使用示例

```el
import { hertz } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * hertz
```

## farad {#api-0aa5e1f0a8408bf1f250}

源码：`src/stdlib/units/si.el:107` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L107)

电容单位法拉，等于库仑每伏特。

```el-signature
@quantityDimension(numerator: @[DurationDimension, DurationDimension, DurationDimension, DurationDimension, CurrentDimension, CurrentDimension], denominator: @[MassDimension, LengthDimension, LengthDimension])
export let farad = defineUnit("farad", coulomb / volt, 1, "F")
```

### 示例：使用示例

```el
import { farad } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * farad
```

## siemens {#api-f20e67d864ccaef4bafb}

源码：`src/stdlib/units/si.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L117)

电导单位西门子，等于安培每伏特。

```el-signature
@quantityDimension(numerator: @[DurationDimension, DurationDimension, DurationDimension, CurrentDimension, CurrentDimension], denominator: @[MassDimension, LengthDimension, LengthDimension])
export let siemens = defineUnit("siemens", ampere / volt, 1, "S")
```

### 示例：使用示例

```el
import { siemens } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * siemens
```

## weber {#api-1383248428c170652e5c}

源码：`src/stdlib/units/si.el:127` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L127)

磁通量单位韦伯，等于伏特秒。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension, CurrentDimension])
export let weber = defineUnit("weber", volt * second, 1, "Wb")
```

### 示例：使用示例

```el
import { weber } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * weber
```

## tesla {#api-5786456d60babbadf7bb}

源码：`src/stdlib/units/si.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L137)

磁通密度单位特斯拉，等于韦伯每平方米。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[DurationDimension, DurationDimension, CurrentDimension])
export let tesla = defineUnit("tesla", weber / (metre ^ 2), 1, "T")
```

### 示例：使用示例

```el
import { tesla } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * tesla
```

## henry {#api-363cf8870703e8c6159c}

源码：`src/stdlib/units/si.el:147` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L147)

电感单位亨利，等于韦伯每安培。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension, CurrentDimension, CurrentDimension])
export let henry = defineUnit("henry", weber / ampere, 1, "H")
```

### 示例：使用示例

```el
import { henry } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * henry
```

## lumen {#api-726d043a36b020bff67b}

源码：`src/stdlib/units/si.el:157` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L157)

光通量单位流明，等于坎德拉乘球面度；球面度为无量纲单位。

```el-signature
@quantityDimension(numerator: @[LuminosityDimension])
export let lumen = defineUnit("lumen", candela, 1, "lm")
```

### 示例：使用示例

```el
import { lumen } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * lumen
```

## lux {#api-ff78834e68949177ea57}

源码：`src/stdlib/units/si.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L167)

照度单位勒克斯，等于流明每平方米。

```el-signature
@quantityDimension(numerator: @[LuminosityDimension], denominator: @[LengthDimension, LengthDimension])
export let lux = defineUnit("lux", lumen / (metre ^ 2), 1, "lx")
```

### 示例：使用示例

```el
import { lux } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * lux
```

## becquerel {#api-df062a73f0418228c72f}

源码：`src/stdlib/units/si.el:177` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L177)

放射性活度单位贝可勒尔；每秒一次衰变。

```el-signature
@quantityDimension(denominator: @[DurationDimension])
export let becquerel = defineUnit("becquerel", one / second, 1, "Bq")
```

### 示例：使用示例

```el
import { becquerel } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * becquerel
```

## gray {#api-1ce9668377003f1e5a31}

源码：`src/stdlib/units/si.el:187` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L187)

吸收剂量单位戈瑞，等于焦耳每千克。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let gray = defineUnit("gray", joule / kilogram, 1, "Gy")
```

### 示例：使用示例

```el
import { gray } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * gray
```

## sievert {#api-4a8702855cc4841ba69d}

源码：`src/stdlib/units/si.el:197` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L197)

当量剂量或有效剂量单位希沃特，等于焦耳每千克。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let sievert = defineUnit("sievert", joule / kilogram, 1, "Sv")
```

### 示例：使用示例

```el
import { sievert } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * sievert
```

## katal {#api-017cceea4c8bf790234f}

源码：`src/stdlib/units/si.el:207` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L207)

催化活性单位开特，等于摩尔每秒。

```el-signature
@quantityDimension(numerator: @[AmountDimension], denominator: @[DurationDimension])
export let katal = defineUnit("katal", mole / second, 1, "kat")
```

### 示例：使用示例

```el
import { katal } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * katal
```
