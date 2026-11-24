# units/references.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 常用跨学科参考量 {#api-f9a21da1aa772842f290}

源码：`src/stdlib/units/references.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/references.el#L1)

音乐调音、声学和温标换算所用的约定量值。

## standardTuningA4 {#api-9ed01829be0562ce6be8}

源码：`src/stdlib/units/references.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/references.el#L15)

音乐会标准音 A4 的频率，精确等于 440 Hz。

```el-signature
export let standardTuningA4 = 440 * hertz
```

### 示例：用法

```el
import { standardTuningA4, hertz } from "el:units/"
let reference = standardTuningA4.valueIn(hertz, Number)
```

## airSoundPressureReference {#api-142aa44ec682e05b422a}

源码：`src/stdlib/units/references.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/references.el#L24)

空气声压级的参考均方根声压 20 µPa。

```el-signature
export let airSoundPressureReference = 2e-5 * pascal
```

### 示例：用法

```el
import { airSoundPressureReference, pascal } from "el:units/"
let reference = airSoundPressureReference.valueIn(pascal, Number)
```

## soundIntensityReference {#api-1fa3c816a13ffbd9292b}

源码：`src/stdlib/units/references.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/references.el#L34)

声强级的参考声强 1 pW/m²。

```el-signature
export let soundIntensityReference = 1e-12 * (watt / (metre ^ 2))
```

### 示例：用法

```el
import { soundIntensityReference, watt, metre } from "el:units/"
import /^operator / from "el:units/"
let reference = soundIntensityReference.valueIn(watt / (metre ^ 2), Number)
```

## celsiusZeroOffset {#api-b54ce17ee1430a075a01}

源码：`src/stdlib/units/references.el:43` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/references.el#L43)

摄氏温标零点到绝对零点之间的温差，精确等于 273.15 K。

```el-signature
export let celsiusZeroOffset = 273.15 * kelvinDifference
```

### 示例：用法

```el
import { celsiusZeroOffset, kelvinDifference } from "el:units/"
let reference = celsiusZeroOffset.valueIn(kelvinDifference, Number)
```
