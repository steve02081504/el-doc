# units/builtins.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 基础单位 {#api-c4fd1e5f0b840cf0678a}

源码：`src/stdlib/units/builtins.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L1)

长度、时间、质量和其他基础量的单位。

## one {#api-ce3dd1134717aa952f89}

源码：`src/stdlib/units/builtins.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L19)

无量纲单位一。

```el-signature
@quantityDimension()
export let one = Unit(Dimension(), 1, "1", "units.one")
```

### 示例：使用示例

```el
import { one } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * one
```

## metre {#api-b32408cdaf0a7e358c90}

源码：`src/stdlib/units/builtins.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L29)

长度的国际单位制基本单位，符号 m。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let metre = Unit(Dimension.base(LengthDimension), 1, "m", "units.metre")
```

### 示例：使用示例

```el
import { metre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1metre
```

## centimetre {#api-3080aef0789598381951}

源码：`src/stdlib/units/builtins.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L39)

长度单位厘米，等于百分之一米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let centimetre = defineUnit("centimetre", metre, 1 / 100, "cm", "units.centimetre")
```

### 示例：使用示例

```el
import { centimetre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1centimetre
```

## millimetre {#api-4b19c340cc1b67ebcadb}

源码：`src/stdlib/units/builtins.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L49)

长度单位毫米，等于千分之一米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let millimetre = defineUnit("millimetre", metre, 1 / 1000, "mm", "units.millimetre")
```

### 示例：使用示例

```el
import { millimetre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * millimetre
```

## kilometre {#api-5655325fb10d72db67cc}

源码：`src/stdlib/units/builtins.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L59)

长度单位千米，等于一千米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let kilometre = defineUnit("kilometre", metre, 1000, "km", "units.kilometre")
```

### 示例：使用示例

```el
import { kilometre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilometre
```

## inch {#api-8cc1487a3290a95a0fc6}

源码：`src/stdlib/units/builtins.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L69)

国际英寸，精确等于 0.0254 米。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let inch = defineUnit("inch", metre, 127 / 5000, "in", "units.inch")
```

### 示例：使用示例

```el
import { inch } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * inch
```

## foot {#api-00386fa0826510dcb30d}

源码：`src/stdlib/units/builtins.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L79)

国际英尺，精确等于 12 英寸。

```el-signature
@quantityDimension(numerator: @[LengthDimension])
export let foot = defineUnit("foot", metre, 381 / 1250, "ft", "units.foot")
```

### 示例：使用示例

```el
import { foot } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * foot
```

## second {#api-230fcff883b7bd288a08}

源码：`src/stdlib/units/builtins.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L89)

时间的国际单位制基本单位，符号 s。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let second = Unit(Dimension.base(DurationDimension), 1, "s", "units.second")
```

### 示例：使用示例

```el
import { second } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1second
```

## nanosecond {#api-df0c7cdcde04e6f397c6}

源码：`src/stdlib/units/builtins.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L99)

时间单位纳秒，等于十亿分之一秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let nanosecond = defineUnit("nanosecond", second, 1 / 1000000000, "ns", "units.nanosecond")
```

### 示例：使用示例

```el
import { nanosecond } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * nanosecond
```

## microsecond {#api-b78bdf085d79f1afe5e7}

源码：`src/stdlib/units/builtins.el:109` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L109)

时间单位微秒，等于百万分之一秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let microsecond = defineUnit("microsecond", second, 1 / 1000000, "us", "units.microsecond")
```

### 示例：使用示例

```el
import { microsecond } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * microsecond
```

## millisecond {#api-7692226990c917ffa974}

源码：`src/stdlib/units/builtins.el:119` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L119)

时间单位毫秒，等于千分之一秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let millisecond = defineUnit("millisecond", second, 1 / 1000, "ms", "units.millisecond")
```

### 示例：使用示例

```el
import { millisecond } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * millisecond
```

## minute {#api-4c969db3b42489227a34}

源码：`src/stdlib/units/builtins.el:129` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L129)

时间单位分，等于 60 秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let minute = defineUnit("minute", second, 60, "min", "units.minute")
```

### 示例：使用示例

```el
import { minute } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * minute
```

## hour {#api-cfb3480341fa6cdcab1c}

源码：`src/stdlib/units/builtins.el:139` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L139)

时间单位小时，等于 3600 秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let hour = defineUnit("hour", second, 3600, "h", "units.hour")
```

### 示例：使用示例

```el
import { hour } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1hour
```

## day {#api-b75d19dff7243069061d}

源码：`src/stdlib/units/builtins.el:149` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L149)

时间单位日，等于 86400 秒。

```el-signature
@quantityDimension(numerator: @[DurationDimension])
export let day = defineUnit("day", second, 86400, "d", "units.day")
```

### 示例：使用示例

```el
import { day } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * day
```

## kilogram {#api-f2ac2d0de5ca0ce0dc2d}

源码：`src/stdlib/units/builtins.el:159` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L159)

质量的国际单位制基本单位，符号 kg。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let kilogram = Unit(Dimension.base(MassDimension), 1, "kg", "units.kilogram")
```

### 示例：使用示例

```el
import { kilogram } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilogram
```

## gram {#api-0155cadf76b765a93fe9}

源码：`src/stdlib/units/builtins.el:169` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L169)

质量单位克，等于千分之一千克。

```el-signature
@quantityDimension(numerator: @[MassDimension])
export let gram = defineUnit("gram", kilogram, 1 / 1000, "g", "units.gram")
```

### 示例：使用示例

```el
import { gram } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * gram
```

## byte {#api-dac96bd726aa5b725ea0}

源码：`src/stdlib/units/builtins.el:179` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L179)

文件和协议使用的字节单位，表示固定的八位组。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let byte = Unit(Dimension.base(StorageDimension), 1, "B", "units.byte")
```

### 示例：使用示例

```el
import { byte } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * byte
```

## kibibyte {#api-3b63c493276fc8f4fabd}

源码：`src/stdlib/units/builtins.el:189` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L189)

二进制千字节，等于 1024 字节。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let kibibyte = defineUnit("kibibyte", byte, 1024, "KiB", "units.kibibyte")
```

### 示例：使用示例

```el
import { kibibyte } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * kibibyte
```

## mebibyte {#api-42314e3c67dace9f9fe3}

源码：`src/stdlib/units/builtins.el:199` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L199)

二进制兆字节，等于 1048576 字节。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let mebibyte = defineUnit("mebibyte", kibibyte, 1024, "MiB", "units.mebibyte")
```

### 示例：使用示例

```el
import { mebibyte } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * mebibyte
```

## gibibyte {#api-55d2ac2d34ab1f19964c}

源码：`src/stdlib/units/builtins.el:209` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L209)

二进制吉字节，等于 1073741824 字节。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let gibibyte = defineUnit("gibibyte", mebibyte, 1024, "GiB", "units.gibibyte")
```

### 示例：使用示例

```el
import { gibibyte } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * gibibyte
```

## tebibyte {#api-0a361fa152fec4d5c988}

源码：`src/stdlib/units/builtins.el:219` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L219)

二进制容量单位 TiB，精确等于 1024 GiB。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let tebibyte = defineUnit("tebibyte", gibibyte, 1024, "TiB")
```

### 示例：换算字节数

```el
import { tebibyte, byte } from "el:units/"
let bytes = tebibyte.ratioTo(byte)
```

## pebibyte {#api-a7969d82566c5f5d72af}

源码：`src/stdlib/units/builtins.el:229` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L229)

二进制容量单位 PiB，精确等于 1024 TiB。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let pebibyte = defineUnit("pebibyte", tebibyte, 1024, "PiB")
```

### 示例：换算字节数

```el
import { pebibyte, byte } from "el:units/"
let bytes = pebibyte.ratioTo(byte)
```

## exbibyte {#api-a3aced9bf128a31504bb}

源码：`src/stdlib/units/builtins.el:239` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L239)

二进制容量单位 EiB，精确等于 1024 PiB。

```el-signature
@quantityDimension(numerator: @[StorageDimension])
export let exbibyte = defineUnit("exbibyte", pebibyte, 1024, "EiB")
```

### 示例：换算字节数

```el
import { exbibyte, byte } from "el:units/"
let bytes = exbibyte.ratioTo(byte)
```

## kelvinDifference {#api-366de44f588e53ad7f13}

源码：`src/stdlib/units/builtins.el:249` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L249)

温差单位开尔文，不表示绝对温度坐标。

```el-signature
@quantityDimension(numerator: @[TemperatureDifferenceDimension])
export let kelvinDifference = Unit(Dimension.base(TemperatureDifferenceDimension), 1, "K", "units.kelvinDifference")
```

### 示例：使用示例

```el
import { kelvinDifference } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * kelvinDifference
```

## ampere {#api-db3b9a4f750733941c6c}

源码：`src/stdlib/units/builtins.el:259` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L259)

电流的国际单位制基本单位，符号 A。

```el-signature
@quantityDimension(numerator: @[CurrentDimension])
export let ampere = Unit(Dimension.base(CurrentDimension), 1, "A", "units.ampere")
```

### 示例：使用示例

```el
import { ampere } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1ampere
```

## mole {#api-8f71df0717e044ed6fc1}

源码：`src/stdlib/units/builtins.el:269` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L269)

物质的量的国际单位制基本单位摩尔。

```el-signature
@quantityDimension(numerator: @[AmountDimension])
export let mole = Unit(Dimension.base(AmountDimension), 1, "mol", "units.mole")
```

### 示例：使用示例

```el
import { mole } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * mole
```

## candela {#api-544922f57082602df48d}

源码：`src/stdlib/units/builtins.el:279` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L279)

发光强度的国际单位制基本单位坎德拉。

```el-signature
@quantityDimension(numerator: @[LuminosityDimension])
export let candela = Unit(Dimension.base(LuminosityDimension), 1, "cd", "units.candela")
```

### 示例：使用示例

```el
import { candela } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1 * candela
```
