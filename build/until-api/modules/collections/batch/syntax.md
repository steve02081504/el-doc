# collections/batch/syntax.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## batch 局部语法 {#api-d8a8c1e22e896268a765}

源码：`src/stdlib/collections/batch/syntax.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/batch/syntax.el#L1)

提供数组按元素投影执行的 batch 块，以及在块内丢弃当前元素的 keep。

## keepElement {#api-c5174b75e0d42f4f9356}

源码：`src/stdlib/collections/batch/syntax.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/batch/syntax.el#L47)

batch 块中的局部语法 `keep(...)` 按条件保留当前元素；条件为假时丢弃该元素。

```el
syntax keepElement
```

**参数**：condition 当前元素上的布尔条件。

**返回值**：若条件为真，保留唯一变化来源对应的当前元素值。

### 示例：筛选正数

```el
import { batch } from "el:collections/batch/index.el"
fn positive(values) => batch { keep(values > 0) }
let selected = positive(@[-1, 2, 3])
console.stdout.writeLine(selected.join(", "))
```

## batch {#api-5c14c93c3afb46cd3f53}

源码：`src/stdlib/collections/batch/syntax.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/batch/syntax.el#L79)

将块内使用的变化数组绑定映射到对应元素，并收集逐元素求值结果。

```el
export syntax batch
```

### 示例：对数组逐元素筛选

```el
import { batch } from "el:collections/batch/index.el"
fn positive(values) => batch { keep(values > 0) }
let selected = positive(@[-1, 2, 3])
console.stdout.writeLine(selected.join(", "))
```
