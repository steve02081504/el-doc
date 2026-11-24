# collections/sorting/copy.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 排序副本与默认策略 {#api-ef17b94aa6d182653937}

源码：`src/stdlib/collections/sorting/copy.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/copy.el#L1)

复制输入并在独立工作区执行稳定排序。

## copy_sort_input {#api-fde91638467437de3749}

源码：`src/stdlib/collections/sorting/copy.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/copy.el#L20)

将输入复制到新的动态数组，供排序策略重排。

```el-signature
export fn copy_sort_input(values)
```

**参数**：values 可迭代的输入序列。

**返回值**：包含输入元素的独立数组。

### 示例：复制待排序数据

```el
import { copy_sort_input } from "el:collections/sorting/copy.el"
let working = copy_sort_input(@[3, 1, 2])
```

## stable_memory_sort {#api-6f4ecce0a38661923bae}

源码：`src/stdlib/collections/sorting/copy.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/copy.el#L37)

使用稳定插入排序或稳定归并排序重排工作区；小于 32 项时选择插入排序。

```el-signature
@discardable
export fn stable_memory_sort(values, less = (left, right) => left < right)
```

**参数**：values 可按下标读写的工作区，会被改写。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**返回值**：排序后的工作区。

**失败与异常**：比较等操作失败时传播异常，工作区可能已部分重排。

### 示例：稳定排序工作区

```el
import { stable_memory_sort } from "el:collections/sorting/copy.el"
let values = @[3, 1, 2]
stable_memory_sort(values)
```

## copy_sort {#api-9e69003749314c9d21ab}

源码：`src/stdlib/collections/sorting/copy.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sorting/copy.el#L58)

复制输入，在副本上调用一次稳定排序策略，并返回该副本。

```el-signature
export fn copy_sort(values, less = (left, right) => left < right, strategy = stable_memory_sort)
```

**参数**：values 可迭代的输入序列。

**参数**：less 严格弱序比较函数，左值应排在右值之前时返回真。

**参数**：strategy 接收可写工作区及比较函数的稳定排序策略；其返回值不替代工作区。

**返回值**：排序后的独立动态数组。

**失败与异常**：复制、比较或策略失败时传播异常；回调的外部副作用不回滚。

### 示例：返回排序后的副本

```el
import { copy_sort } from "el:collections/sorting/copy.el"
let ordered = copy_sort(@[3, 1, 2])
```
