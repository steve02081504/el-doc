# units/roots.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 量值的平方根 {#api-3d3e3df06055ce20e4e6}

源码：`src/stdlib/units/roots.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/roots.el#L1)

在开平方时同时处理标量精度与单位量纲。

## sqrt {#api-8adf5fd0a8ae84875eb2}

源码：`src/stdlib/units/roots.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/roots.el#L22)

计算量值的平方根，结果量纲的各指数为原指数的一半。

```el-signature
export fn sqrt<element: type>(value: Quantity<element: element>, epsilon = nil)
```

**参数**：value 各基本量纲指数均为偶数的量值。

**参数**：epsilon 可选的标量最大绝对误差，以结果采用的单位计量。

**返回值**：带有平方根单位的量值。单位比例不能精确开方时，在比例为一的单位中计算。

**失败与异常**：UnitError 当任一基本量纲指数为奇数时抛出。数值域和精度错误沿用标量平方根的合同。

### 示例：从平方米求出米

```el
import { metre } from "el:units/"
import /^operator / from "el:units/"
let side = sqrt(4metre^2)
console.stdout.writeLine(side.valueIn(metre))
```
