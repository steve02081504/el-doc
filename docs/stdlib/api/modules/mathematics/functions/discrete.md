# mathematics/functions/discrete.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 离散数学函数 {#api-f2c13b25cd31a256e9f9}

源码：`src/stdlib/mathematics/functions/discrete.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L11)

提供整数、取整、数论与插值等常用离散数值操作。

## min {#api-f3ff61e2646083d63650}

源码：`src/stdlib/mathematics/functions/discrete.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L24)

返回一个或多个可比较值中的最小值。

```el-signature
export fn min(...values)
```

**失败与异常**：没有输入值时抛出 DomainError。

### 示例：使用示例

```el
import { min } from "el:mathematics/"
let result = min(3, 1, 2)
```

## max {#api-041f3b472602a39a94ee}

源码：`src/stdlib/mathematics/functions/discrete.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L33)

返回一个或多个可比较值中的最大值。

```el-signature
export fn max(...values)
```

**失败与异常**：没有输入值时抛出 DomainError。

### 示例：使用示例

```el
import { max } from "el:mathematics/"
let result = max(3, 1, 2)
```

## floor {#api-bd10102e4c50e2f82d0e}

源码：`src/stdlib/mathematics/functions/discrete.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/discrete.el#L50)

返回不大于输入值的最大整数，并保留输入数值类型。

```el-signature
export fn floor(value)
```

**参数**：value 有限 Number 数值。

**返回值**：向负无穷取整后的值。

### 示例：对负数向下取整

```el
import { floor } from "el:mathematics/"
let whole = floor(-1.25)
```
