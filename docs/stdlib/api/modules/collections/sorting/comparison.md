# collections/sorting/comparison.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 比较排序 {#api-767810902b3bcd16e56b}

源码：`src/stdlib/collections/sorting/comparison.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L1)

提供接受比较函数的排序操作。

## heap_sort {#api-e67876bf6dfecec00dc5}

源码：`src/stdlib/collections/sorting/comparison.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L47)

使用堆排序重排输入；不保证相等元素的原有顺序。

```el-signature
@discardable
export fn heap_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { heap_sort } from "el:collections/sorting/comparison.el"
let values = @[3, 1, 2]
heap_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。

## merge_sort {#api-e461cf7a9724a50ce3a7}

源码：`src/stdlib/collections/sorting/comparison.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L88)

使用缓冲区执行稳定归并排序。

```el-signature
@discardable
export fn merge_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { merge_sort } from "el:collections/sorting/comparison.el"
let values = @[3, 1, 2]
merge_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。

## in_place_merge_sort {#api-2def1356afd383db0a39}

源码：`src/stdlib/collections/sorting/comparison.el:156` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L156)

使用旋转归并执行稳定排序。

```el-signature
@discardable
export fn in_place_merge_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { in_place_merge_sort } from "el:collections/sorting/comparison.el"
let values = @[3, 1, 2]
in_place_merge_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。

## quick_sort {#api-d585d22a1fa3c4fed027}

源码：`src/stdlib/collections/sorting/comparison.el:190` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L190)

使用末元素作为枢轴的快速排序；不保证相等元素的原有顺序。

```el-signature
@discardable
export fn quick_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { quick_sort } from "el:collections/sorting/comparison.el"
let values = @[3, 1, 2]
quick_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。

## intro_sort {#api-25406c1973ccd1e25d1e}

源码：`src/stdlib/collections/sorting/comparison.el:228` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/comparison.el#L228)

结合快速排序、插入排序和堆排序重排输入；不保证相等元素的原有顺序。

```el-signature
@discardable
export fn intro_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读取和写入的序列；排序会改写它。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的输入序列。

**失败与异常**：比较函数等操作失败时传播异常；输入可能已经部分重排。

### 示例：排序数值

```el
import { intro_sort } from "el:collections/sorting/comparison.el"
let values = @[3, 1, 2]
intro_sort(values)
```
调用后 values 的顺序为 [1, 2, 3]。
