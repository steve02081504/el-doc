# mathematics/functions/discrete.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 离散数学函数 {#api-f2c13b25cd31a256e9f9}

源码：`src/stdlib/mathematics/functions/discrete.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L11)

提供整数、取整、数论与插值等常用离散数值操作。

## floor {#api-bd10102e4c50e2f82d0e}

源码：`src/stdlib/mathematics/functions/discrete.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L33)

```el
export fn floor(value)
```

返回不大于输入值的最大整数，并保留输入数值类型。

**参数**：value 有限 Number 数值。

**返回值**：向负无穷取整后的值。

### 示例：对负数向下取整

```el
import { floor } from "el:mathematics/"
let whole = floor(-1.25)
```
