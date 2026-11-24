# collections/sorting/insertion.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 插入排序 {#api-a6afb207bc0444bd7299}

源码：`src/stdlib/collections/sorting/insertion.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/insertion.el#L1)

提供接受比较函数的排序操作。

## insertion_sort {#api-8c708d47f0f161a2d6f5}

源码：`src/stdlib/collections/sorting/insertion.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/insertion.el#L17)

使用相邻交换执行稳定插入排序。

```el-signature
@discardable
export fn insertion_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { insertion_sort } from "el:collections/sorting/insertion.el"
let values = @[3, 1, 2]
insertion_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。
