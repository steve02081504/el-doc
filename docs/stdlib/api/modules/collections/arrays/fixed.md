# collections/arrays/fixed.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [StaticArray.sort](#api-041dd00e19af12a0ad8d)

## 定长数组 {#api-13100f17eb10c3eeca71}

源码：`src/stdlib/collections/arrays/fixed.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/fixed.el#L1)

提供长度固定的数组及其操作。

## StaticArray {#api-853605d9b03b0a6daa7e}

源码：`src/stdlib/collections/arrays/fixed.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/fixed.el#L79)

创建元素类型和长度固定的数组类型。

```el-signature
export fn StaticArray(element: type, length = 0): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：element 数组元素类型。

**参数**：length 固定元素数量。

**返回值**：对应的定长数组类型。

### 示例：声明定长数组

```el
import { StaticArray } from "el:collections/arrays/fixed.el"
let values: StaticArray<element: Number, length: 3> = @[3, 1, 2]
```

## StaticArray.sort {#api-041dd00e19af12a0ad8d}

源码：`src/stdlib/collections/arrays/fixed.el:162` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/fixed.el#L162)

返回按比较函数排序的独立副本，保留原数组的顺序和元素槽。

```el-signature
@optimize(using: optimize_sort, data: @{ receiver: "member", independent: t, copy: copy_sort_input, pass: insertion_pass, tail: insertion_tail, ascending: ascending, merge: merge_sort, adaptive: adaptive_number_sort, insertion: insertion_sort, bucket: bounded_number_sort })
		fn sort(less = (left, right) => left < right, strategy = stable_memory_sort)
```

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**参数**：strategy 对独立工作区执行稳定排序的策略，默认为 stable_memory_sort。

**返回值**：排序后的新数组。

**失败与异常**：复制、比较或策略失败时传播异常；回调的外部副作用不回滚。

### 示例：排序定长数组的副本

```el
import { StaticArray } from "el:collections/arrays/fixed.el"
let values: StaticArray<element: Number, length: 3> = @[3, 1, 2]
let ordered = values.sort()
```
