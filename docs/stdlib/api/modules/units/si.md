# units/si.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 国际单位制导出单位 {#api-3ad30912ffea25b6ec16}

源码：`src/stdlib/units/si.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L1)

从基础单位组合的常用国际单位制单位。

## newton {#api-d8155e776258ac4fec54}

源码：`src/stdlib/units/si.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L15)

力的国际单位制导出单位牛顿。

```el-signature
export let newton = defineUnit("newton", kilogram * metre / (second ^ 2), 1, "N")
```

### 示例：使用示例

```el
import { newton } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1newton
```

## pascal {#api-556e3c267d5dbc84a8eb}

源码：`src/stdlib/units/si.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L24)

压力的国际单位制导出单位帕斯卡。

```el-signature
export let pascal = defineUnit("pascal", newton / (metre ^ 2), 1, "Pa")
```

### 示例：使用示例

```el
import { pascal } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1pascal
```

## kilopascal {#api-5ff14a69fb644a35172e}

源码：`src/stdlib/units/si.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L33)

压力单位千帕，等于 1000 帕。

```el-signature
export let kilopascal = defineUnit("kilopascal", pascal, 1000, "kPa")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { kilopascal } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1kilopascal
```

## joule {#api-d837f33716e3c6b9b4a7}

源码：`src/stdlib/units/si.el:42` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L42)

能量和功的国际单位制导出单位焦耳。

```el-signature
export let joule = defineUnit("joule", newton * metre, 1, "J")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { joule } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1joule
```

## volt {#api-b1380e56034af98e8ee5}

源码：`src/stdlib/units/si.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L53)

电压的国际单位制导出单位伏特。

```el-signature
export let volt = defineUnit("volt", watt / ampere, 1, "V")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { volt } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1volt
```

## ohm {#api-2bf8d67950303a33dd95}

源码：`src/stdlib/units/si.el:62` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/si.el#L62)

电阻的国际单位制导出单位欧姆。

```el-signature
export let ohm = defineUnit("ohm", volt / ampere, 1, "Ω")
```

**类型**：`defineUnit`

未解析：`defineUnit`

### 示例：使用示例

```el
import { ohm } from "el:units/"
import /^operator / from "el:units/"
let quantity = 1ohm
```
