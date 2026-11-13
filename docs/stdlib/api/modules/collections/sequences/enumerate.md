# collections/sequences/enumerate.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 带下标的迭代 {#api-c5b0a34a6ca22a3202fa}

源码：`src/stdlib/collections/sequences/enumerate.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/enumerate.el#L1)

为迭代元素附加从零开始的下标。

## enumerate {#api-b0470098b0916d891bc1}

源码：`src/stdlib/collections/sequences/enumerate.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/enumerate.el#L71)

```el
export fn enumerate(source)
```

惰性包装迭代源，为每个产出元素配上从零开始的下标。

**参数**：source 可迭代值；每次创建迭代器时从下标零开始。

### 示例：示例

```el
import { enumerate } from "el:collections/sequences/enumerate.el"
let entries = enumerate(@["a", "b"])
for (let {index, value} in entries) { let pair = @[index, value] }
```
预期结果：依次输出 0 和 1。
