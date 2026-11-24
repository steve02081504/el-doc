# units/everyday.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 常用精确换算单位 {#api-d3e007ea235170d56173}

源码：`src/stdlib/units/everyday.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L1)

以有理数定义的日常单位及信息单位。

## litre {#api-94b4de3d559c7f2226b9}

源码：`src/stdlib/units/everyday.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L18)

容积单位升，精确等于千分之一立方米。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let litre = defineUnit("litre", metre ^ 3, 1 / 1000, "L")
```

### 示例：使用示例

```el
import { litre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * litre
```

## millilitre {#api-9cb0c240ac35063ce389}

源码：`src/stdlib/units/everyday.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L28)

容积单位毫升，精确等于千分之一升。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let millilitre = defineUnit("millilitre", litre, 1 / 1000, "mL")
```

### 示例：使用示例

```el
import { millilitre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * millilitre
```

## hectare {#api-0d77f9a0ab018c1d9bb0}

源码：`src/stdlib/units/everyday.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L38)

面积单位公顷，精确等于一万平方米。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension])
export let hectare = defineUnit("hectare", metre ^ 2, 10000, "ha")
```

### 示例：使用示例

```el
import { hectare } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * hectare
```

## tonne {#api-395a16a1d435905a2e50}

源码：`src/stdlib/units/everyday.el:48` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L48)

质量单位吨，精确等于一千千克。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let tonne = defineUnit("tonne", kilogram, 1000, "t")
```

### 示例：使用示例

```el
import { tonne } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * tonne
```

## nauticalMile {#api-2e24a8709ef89f1ff3eb}

源码：`src/stdlib/units/everyday.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L58)

国际海里，精确等于 1852 米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let nauticalMile = defineUnit("nauticalMile", metre, 1852, "nmi")
```

### 示例：使用示例

```el
import { nauticalMile } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * nauticalMile
```

## knot {#api-abe9115f4498e01773ab}

源码：`src/stdlib/units/everyday.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L68)

速度单位节，精确等于每小时一海里。

```el-signature
@quantityDimension(numerator: @[LengthDimension], denominator: @[DurationDimension])
export let knot = defineUnit("knot", nauticalMile / hour, 1, "kn")
```

### 示例：使用示例

```el
import { knot } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * knot
```

## yard {#api-ed27a65c20d5dc42a7fe}

源码：`src/stdlib/units/everyday.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L78)

国际码，精确等于 3 英尺。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let yard = defineUnit("yard", foot, 3, "yd")
```

### 示例：使用示例

```el
import { yard } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * yard
```

## mile {#api-eca8dc38ce19ba79e384}

源码：`src/stdlib/units/everyday.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L88)

国际英里，精确等于 1760 码。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let mile = defineUnit("mile", yard, 1760, "mi")
```

### 示例：使用示例

```el
import { mile } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * mile
```

## pound {#api-925b50d763f3a9fa0b71}

源码：`src/stdlib/units/everyday.el:98` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L98)

国际常衡磅，精确等于 0.45359237 千克。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let pound = defineUnit("pound", kilogram, 45359237 / 100000000, "lb")
```

### 示例：使用示例

```el
import { pound } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * pound
```

## ounce {#api-d790c31af11e19888cc0}

源码：`src/stdlib/units/everyday.el:108` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L108)

常衡盎司，精确等于十六分之一磅。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let ounce = defineUnit("ounce", pound, 1 / 16, "oz")
```

### 示例：使用示例

```el
import { ounce } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * ounce
```

## usLiquidGallon {#api-1f7108862329d38adf64}

源码：`src/stdlib/units/everyday.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L118)

美制液体加仑，精确等于 231 立方国际英寸。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let usLiquidGallon = defineUnit("usLiquidGallon", inch ^ 3, 231, "gal (US)")
```

### 示例：使用示例

```el
import { usLiquidGallon } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * usLiquidGallon
```

## usFluidOunce {#api-fa2da697bd1a596ef3b6}

源码：`src/stdlib/units/everyday.el:128` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L128)

美制液量盎司，精确等于 128 分之一美制液体加仑。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let usFluidOunce = defineUnit("usFluidOunce", usLiquidGallon, 1 / 128, "fl oz (US)")
```

### 示例：使用示例

```el
import { usFluidOunce } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * usFluidOunce
```

## thermochemicalKilocalorie {#api-58a2277daa9fd2386b77}

源码：`src/stdlib/units/everyday.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L138)

热化学千卡，精确等于 4184 焦耳。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let thermochemicalKilocalorie = defineUnit("thermochemicalKilocalorie", joule, 4184, "kcal(th)")
```

### 示例：使用示例

```el
import { thermochemicalKilocalorie } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * thermochemicalKilocalorie
```

## percent {#api-062b65f4244b4570d6bb}

源码：`src/stdlib/units/everyday.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L148)

无量纲百分比，等于百分之一。

```el-signature
@quantityDimension()
export let percent = defineUnit("percent", one, 1 / 100, "%")
```

### 示例：使用示例

```el
import { percent } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * percent
```

## perMille {#api-74597eb92c11583b2659}

源码：`src/stdlib/units/everyday.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L158)

无量纲千分比，等于千分之一。

```el-signature
@quantityDimension()
export let perMille = defineUnit("perMille", one, 1 / 1000, "‰")
```

### 示例：使用示例

```el
import { perMille } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * perMille
```

## ppm {#api-9e779bd2fcc62ace8e3d}

源码：`src/stdlib/units/everyday.el:168` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L168)

无量纲百万分比，等于百万分之一。

```el-signature
@quantityDimension()
export let ppm = defineUnit("ppm", one, 1 / 1000000, "ppm")
```

### 示例：使用示例

```el
import { ppm } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * ppm
```

## basisPoint {#api-e3bc803bf5ac79415119}

源码：`src/stdlib/units/everyday.el:178` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L178)

无量纲基点，等于万分之一。

```el-signature
@quantityDimension()
export let basisPoint = defineUnit("basisPoint", one, 1 / 10000, "bp")
```

### 示例：使用示例

```el
import { basisPoint } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * basisPoint
```

## micrometre {#api-d49f33a9990af85e2953}

源码：`src/stdlib/units/everyday.el:189` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L189)

长度单位微米，精确等于一百万分之一米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let micrometre = defineUnit("micrometre", metre, 1 / 1000000, "µm")
```

### 示例：构造量值

```el
import { micrometre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * micrometre
```

## nanometre {#api-784e203f2c37bf56db3d}

源码：`src/stdlib/units/everyday.el:200` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L200)

长度单位纳米，精确等于十亿分之一米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let nanometre = defineUnit("nanometre", metre, 1 / 1000000000, "nm")
```

### 示例：构造量值

```el
import { nanometre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * nanometre
```

## angstrom {#api-6ed4655d69eeb98112f8}

源码：`src/stdlib/units/everyday.el:211` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L211)

长度单位埃，精确等于 0.1 纳米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let angstrom = defineUnit("angstrom", nanometre, 1 / 10, "Å")
```

### 示例：构造量值

```el
import { angstrom } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * angstrom
```

## milligram {#api-8186f44f947e86248b0a}

源码：`src/stdlib/units/everyday.el:222` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L222)

质量单位毫克，精确等于千分之一克。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let milligram = defineUnit("milligram", gram, 1 / 1000, "mg")
```

### 示例：构造量值

```el
import { milligram } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * milligram
```

## microgram {#api-19a25337080602a7bd46}

源码：`src/stdlib/units/everyday.el:233` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L233)

质量单位微克，精确等于千分之一毫克。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let microgram = defineUnit("microgram", milligram, 1 / 1000, "µg")
```

### 示例：构造量值

```el
import { microgram } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * microgram
```

## decilitre {#api-0b445a3df08840e7be6f}

源码：`src/stdlib/units/everyday.el:244` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L244)

容积单位分升，精确等于十分之一升。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let decilitre = defineUnit("decilitre", litre, 1 / 10, "dL")
```

### 示例：构造量值

```el
import { decilitre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * decilitre
```

## imperialGallon {#api-5233f462623c9b144dcb}

源码：`src/stdlib/units/everyday.el:255` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L255)

英制加仑，精确等于 4.54609 升。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension, LengthDimension])
export let imperialGallon = defineUnit("imperialGallon", litre, 4.54609, "gal (imp)")
```

### 示例：构造量值

```el
import { imperialGallon } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * imperialGallon
```

## acre {#api-615258a2a73c66ae2c3d}

源码：`src/stdlib/units/everyday.el:266` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L266)

国际英亩，精确等于 43560 平方国际英尺。

```el-signature
@quantityDimension(numerator: @[LengthDimension, LengthDimension])
export let acre = defineUnit("acre", foot ^ 2, 43560, "ac")
```

### 示例：构造量值

```el
import { acre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * acre
```

## bar {#api-f40b8b292605276beb9d}

源码：`src/stdlib/units/everyday.el:277` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L277)

压力单位巴，精确等于 100000 帕。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let bar = defineUnit("bar", pascal, 100000, "bar")
```

### 示例：构造量值

```el
import { bar } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * bar
```

## millibar {#api-489e7cd826bf2c123d42}

源码：`src/stdlib/units/everyday.el:288` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L288)

压力单位毫巴，精确等于 100 帕。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let millibar = defineUnit("millibar", bar, 1 / 1000, "mbar")
```

### 示例：构造量值

```el
import { millibar } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * millibar
```

## atmosphere {#api-329750289233e413fbe3}

源码：`src/stdlib/units/everyday.el:299` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L299)

标准大气压单位，精确等于 101325 帕。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let atmosphere = defineUnit("atmosphere", pascal, 101325, "atm")
```

### 示例：构造量值

```el
import { atmosphere } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * atmosphere
```

## torr {#api-2fba6013b239d6909632}

源码：`src/stdlib/units/everyday.el:310` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L310)

压力单位托，精确等于标准大气压的 1/760。

```el-signature
@quantityDimension(numerator: @[MassDimension], denominator: @[LengthDimension, DurationDimension, DurationDimension])
export let torr = defineUnit("torr", atmosphere, 1 / 760, "Torr")
```

### 示例：构造量值

```el
import { torr } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * torr
```

## celsiusDifference {#api-8660e7feb9dc891736dd}

源码：`src/stdlib/units/everyday.el:321` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L321)

摄氏温差单位，每摄氏度的温差等于 1 K。

```el-signature
@quantityDimension(numerator: @[TemperatureDifferenceDimension])
export let celsiusDifference = defineUnit("celsiusDifference", kelvinDifference, 1, "Δ°C")
```

### 示例：构造量值

```el
import { celsiusDifference } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * celsiusDifference
```

## fahrenheitDifference {#api-97f03c47f48ea17b290a}

源码：`src/stdlib/units/everyday.el:332` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L332)

华氏温差单位，每华氏度的温差等于 5/9 K。

```el-signature
@quantityDimension(numerator: @[TemperatureDifferenceDimension])
export let fahrenheitDifference = defineUnit("fahrenheitDifference", kelvinDifference, 5 / 9, "Δ°F")
```

### 示例：构造量值

```el
import { fahrenheitDifference } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * fahrenheitDifference
```

## desktopPublishingPoint {#api-8f4637841c95efc65d15}

源码：`src/stdlib/units/everyday.el:343` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/everyday.el#L343)

桌面排版点，精确等于 1/72 国际英寸。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let desktopPublishingPoint = defineUnit("desktopPublishingPoint", inch, 1 / 72, "pt")
```

### 示例：构造量值

```el
import { desktopPublishingPoint } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * desktopPublishingPoint
```
