# units/core.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Quantity.valueIn](#api-9f5927927fcab644bfd3)
- [Quantity.inUnit](#api-2750ca6f68ab784c1945)
- [Quantity.standardText](#api-4ac6cde63fa13cc83ff3)

## 单位与量 {#api-706adb5f0c687980abce}

源码：`src/stdlib/units/core.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L1)

线性单位、携带单位的量及其转换。

## Unit {#api-59cfa52bcbc40973a040}

源码：`src/stdlib/units/core.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L22)

带量纲、比例和符号的线性单位。比例必须为有限正数。

```el-signature
export @assign(mode: "copy") @readonly(fields: t) class Unit
```

### 示例：使用示例

```el
import { metre } from "el:units/"
import /^operator / from "el:units/"
let length = 2metre
```

## Quantity {#api-e3b39160772294c021c5}

源码：`src/stdlib/units/core.el:70` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L70)

携带数值及其表示单位的量类型。同量纲单位之间可转换。

```el-signature
export fn Quantity(element: type): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

### 示例：使用示例

```el
import { centimetre } from "el:units/"
import /^operator / from "el:units/"
let length = 125centimetre
```

## Quantity.valueIn {#api-9f5927927fcab644bfd3}

源码：`src/stdlib/units/core.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L89)

将量转换为指定同量纲单位并返回数值。

```el-signature
fn valueIn(unit: Unit): element
```

**返回类型**：[`element`](../../types.md#api-7fa45cb4014a5ae01da4)

### 示例：使用示例

```el
import { Quantity, centimetre, metre } from "el:units/"
import /^operator / from "el:units/"
let length: Quantity<element: Number> = Number(125) * centimetre
let metres = length.valueIn(metre)
```

## Quantity.inUnit {#api-2750ca6f68ab784c1945}

源码：`src/stdlib/units/core.el:101` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L101)

返回以指定同量纲单位表示的量。

```el-signature
fn inUnit(unit: Unit): Value
```

**返回类型**：[`Value`](../../types.md#api-7cbc2372dc56c0003748)

### 示例：使用示例

```el
import { Quantity, centimetre, metre } from "el:units/"
import /^operator / from "el:units/"
let length: Quantity<element: Number> = Number(125) * centimetre
let converted = length.inUnit(metre)
```

## Quantity.standardText {#api-4ac6cde63fa13cc83ff3}

源码：`src/stdlib/units/core.el:123` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/core.el#L123)

以数值和单位符号组成文本。

```el-signature
fn standardText(): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

### 示例：使用示例

```el
import { Quantity, centimetre } from "el:units/"
import /^operator / from "el:units/"
let length: Quantity<element: Number> = Number(125) * centimetre
let text = length.standardText()
```
