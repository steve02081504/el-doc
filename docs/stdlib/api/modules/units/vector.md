# units/vector.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [QuantityVector.dot](#api-f12d85b10b7543e8697c)

## 带单位向量 {#api-497526ed008e697bfdef}

源码：`src/stdlib/units/vector.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/vector.el#L1)

在指定坐标系和维数中表示带单位的向量。

## QuantityVector {#api-41d14bd1ae7596d5412d}

源码：`src/stdlib/units/vector.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/vector.el#L37)

创建指定坐标系和维数的带单位向量类型。分量必须有限且量纲相容。

```el-signature
export fn QuantityVector(frame: type, dimensions): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

### 示例：使用示例

```el
import { QuantityVector, metre } from "el:units/"
import /^operator / from "el:units/"
@assign(mode: "copy")
class World {}
let WorldPlane: type = QuantityVector<frame: World, dimensions: 2>
let displacement = WorldPlane(@[2metre, 0metre])
```

## QuantityVector.dot {#api-f12d85b10b7543e8697c}

源码：`src/stdlib/units/vector.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/vector.el#L96)

计算同坐标系、同维数向量的点积，结果单位为两个向量单位的乘积。

```el-signature
fn dot(right: Vector): Quantity<element: Number>
```

**返回类型**：[`Quantity`](core.md#api-e3b39160772294c021c5)<element: [`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)>

### 示例：使用示例

```el
import { QuantityVector, metre } from "el:units/"
import /^operator / from "el:units/"
@assign(mode: "copy")
class World {}
let WorldPlane: type = QuantityVector<frame: World, dimensions: 2>
let displacement: QuantityVector<frame: World, dimensions: 2> = WorldPlane(@[2metre, 0metre])
let squaredLength = displacement.dot(displacement)
```
