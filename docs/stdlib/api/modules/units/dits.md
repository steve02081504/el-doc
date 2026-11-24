# units/dits.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标原生数位容量 {#api-1c54ccbedadbeefe67c0}

源码：`src/stdlib/units/dits.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L1)

基本数位和按编译目标基数分组的容量单位。

## dit {#api-b774fbdde3efd95b452b}

源码：`src/stdlib/units/dits.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L18)

一个目标原生数位，其状态数由编译目标基数决定。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let dit = Unit(Dimension.base(DigitStorageDimension), 1, "dit")
```

### 示例：构造数位容量

```el
import { dit } from "el:units/"
import /^operator / from "el:units/"
let capacity = 8 * dit
```

## kd {#api-ff9201f88257e3dd5325}

源码：`src/stdlib/units/dits.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L28)

容量为编译目标基数的 10 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let kd = defineUnit("kd", dit, kdDits, "kd")
```

### 示例：换算为原生数位

```el
import { kd, dit } from "el:units/"
let digitCount = kd.ratioTo(dit)
```

## md {#api-4e9a9feca66c3c9aa552}

源码：`src/stdlib/units/dits.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L38)

容量为编译目标基数的 20 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let md = defineUnit("md", dit, mdDits, "md")
```

### 示例：换算为原生数位

```el
import { md, dit } from "el:units/"
let digitCount = md.ratioTo(dit)
```

## gd {#api-8b6ac4d36e9109a0c660}

源码：`src/stdlib/units/dits.el:48` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L48)

容量为编译目标基数的 30 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let gd = defineUnit("gd", dit, gdDits, "gd")
```

### 示例：换算为原生数位

```el
import { gd, dit } from "el:units/"
let digitCount = gd.ratioTo(dit)
```

## td {#api-bbfa5b4ec47a7481e183}

源码：`src/stdlib/units/dits.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L58)

容量为编译目标基数的 40 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let td = defineUnit("td", dit, tdDits, "td")
```

### 示例：换算为原生数位

```el
import { td, dit } from "el:units/"
let digitCount = td.ratioTo(dit)
```

## pd {#api-dbe42f8924c1c4e37ef0}

源码：`src/stdlib/units/dits.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L68)

容量为编译目标基数的 50 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let pd = defineUnit("pd", dit, pdDits, "pd")
```

### 示例：换算为原生数位

```el
import { pd, dit } from "el:units/"
let digitCount = pd.ratioTo(dit)
```

## ed {#api-7c7a8894505905efc006}

源码：`src/stdlib/units/dits.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/dits.el#L78)

容量为编译目标基数的 60 次方个 dit。

```el-signature
@quantityDimension(numerator: @[DigitStorageDimension])
export let ed = defineUnit("ed", dit, edDits, "ed")
```

### 示例：换算为原生数位

```el
import { ed, dit } from "el:units/"
let digitCount = ed.ratioTo(dit)
```
