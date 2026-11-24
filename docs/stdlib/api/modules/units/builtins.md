# units/builtins.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 基础单位 {#api-c4fd1e5f0b840cf0678a}

源码：`src/stdlib/units/builtins.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L1)

长度、时间、质量和其他基础量的单位。

## metre {#api-b32408cdaf0a7e358c90}

源码：`src/stdlib/units/builtins.el:26` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L26)

长度的国际单位制基本单位，符号 m。

```el-signature
export let metre = Unit(Dimension.base(LengthDimension), 1, "m", "units.metre")
```

### 示例：使用示例

```el
import { metre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1metre
```

## centimetre {#api-3080aef0789598381951}

源码：`src/stdlib/units/builtins.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L35)

长度单位厘米，等于百分之一米。

```el-signature
export let centimetre = defineUnit("centimetre", metre, 1 / 100, "cm", "units.centimetre")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { centimetre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1centimetre
```

## kilometre {#api-5655325fb10d72db67cc}

源码：`src/stdlib/units/builtins.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L45)

长度单位千米，等于一千米。

```el-signature
export let kilometre = defineUnit("kilometre", metre, 1000, "km", "units.kilometre")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { kilometre } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilometre
```

## second {#api-230fcff883b7bd288a08}

源码：`src/stdlib/units/builtins.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L56)

时间的国际单位制基本单位，符号 s。

```el-signature
export let second = Unit(Dimension.base(DurationDimension), 1, "s", "units.second")
```

### 示例：使用示例

```el
import { second } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1second
```

## hour {#api-cfb3480341fa6cdcab1c}

源码：`src/stdlib/units/builtins.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L69)

时间单位小时，等于 3600 秒。

```el-signature
export let hour = defineUnit("hour", second, 3600, "h", "units.hour")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { hour } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1hour
```

## kilogram {#api-f2ac2d0de5ca0ce0dc2d}

源码：`src/stdlib/units/builtins.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L79)

质量的国际单位制基本单位，符号 kg。

```el-signature
export let kilogram = Unit(Dimension.base(MassDimension), 1, "kg", "units.kilogram")
```

### 示例：使用示例

```el
import { kilogram } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilogram
```

## ampere {#api-db3b9a4f750733941c6c}

源码：`src/stdlib/units/builtins.el:94` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/builtins.el#L94)

电流的国际单位制基本单位，符号 A。

```el-signature
export let ampere = Unit(Dimension.base(CurrentDimension), 1, "A", "units.ampere")
```

### 示例：使用示例

```el
import { ampere } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1ampere
```
