# collections/arrays/operations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数组操作 {#api-0bf83efb11c5d50a2109}

源码：`src/stdlib/collections/arrays/operations.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L1)

对可迭代序列执行查询、变换和排序。

## some {#api-98910e1916d786943aa8}

源码：`src/stdlib/collections/arrays/operations.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L30)

按迭代顺序检查元素，存在满足谓词的元素时立即返回真。

```el
@optimize(using: optimize_array, data: @{ stage: "some", receiver: "argument" })
export fn some(values, predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 被检查的可迭代值。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：检查是否存在偶数

```el
import { some } from "el:collections/arrays/operations.el"
some(@[1, 3, 4], value => value % 2 == 0)
```
预期结果：真。

**返回值**：Bool。

## any {#api-1fff05563d7e913b33e0}

源码：`src/stdlib/collections/arrays/operations.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L47)

判断序列中是否有元素满足谓词。

```el
@optimize(using: optimize_array, data: @{ stage: "some", receiver: "argument" })
export fn any(values, predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 被检查的可迭代值。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：检查是否存在正数

```el
import { any } from "el:collections/arrays/operations.el"
any(@[-2, 0, 5], value => value > 0)
```
预期结果：真。

**返回值**：Bool。

## none {#api-1e145e1a1577e85ae421}

源码：`src/stdlib/collections/arrays/operations.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L63)

判断序列中没有元素满足谓词。

```el
@optimize(using: optimize_array, data: @{ stage: "none", receiver: "argument" })
export fn none(values, predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 被检查的可迭代值。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：检查是否没有负数

```el
import { none } from "el:collections/arrays/operations.el"
none(@[1, 2, 3], value => value < 0)
```
预期结果：真。

**返回值**：Bool。

## all {#api-aac2646339bc62f9f5a9}

源码：`src/stdlib/collections/arrays/operations.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L79)

判断所有元素是否满足谓词；遇到首个不满足项时停止。

```el
@optimize(using: optimize_array, data: @{ stage: "all", receiver: "argument" })
export fn all(values, predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 被检查的可迭代值。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：检查序列中的每个值

```el
import { all } from "el:collections/arrays/operations.el"
all(@[1, 2, 3], value => value > 0)
```
预期结果：真。

**返回值**：Bool。

## every {#api-61e90cb749f6c5e91800}

源码：`src/stdlib/collections/arrays/operations.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L96)

判断序列中的每个元素是否满足谓词，与 all 使用相同规则。

```el
@optimize(using: optimize_array, data: @{ stage: "all", receiver: "argument" })
export fn every(values, predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 被检查的可迭代值。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：检查每个字符串长度

```el
import { every } from "el:collections/arrays/operations.el"
every(@["oak", "elm"], word => word.count == 3)
```
预期结果：真。

**返回值**：Bool。

## concat {#api-719bd5f02346e2576f74}

源码：`src/stdlib/collections/arrays/operations.el:112` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L112)

依次把两个序列的元素复制到新数组。

```el
export fn concat(left, right)
```

**参数**：left 结果前段的序列。

**参数**：right 接在前段之后的序列。

### 示例：拼接两个数组

```el
import { concat } from "el:collections/arrays/operations.el"
concat(@[1, 2], @[3])
```
预期结果：[1, 2, 3]。

**返回值**：新数组。

## includes {#api-a5804828a53f177aa6da}

源码：`src/stdlib/collections/arrays/operations.el:128` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L128)

判断序列是否包含与给定值相等的元素。

```el
export fn includes(values, value): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：values 提供元素比较操作的序列。

**参数**：value 要查找的值。

### 示例：检查数组是否包含元素

```el
import { includes } from "el:collections/arrays/operations.el"
includes(@["red", "blue"], "blue")
```
预期结果：真。

**返回值**：Bool。

<span id="api-3e781a07fe2531eed17f"></span>

## map~transform {#api-aabb1564064c8bd3cf0f}

源码：`src/stdlib/collections/arrays/operations.el:144` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L144)

将变换函数应用于每个元素，并按原顺序收集结果。

```el
@optimize(using: optimize_array, data: @{ stage: "map", receiver: "argument" })
export fn map(values, transform)
```

**参数**：values 输入序列。

**参数**：transform 接收一个元素并产生对应结果的函数。

### 示例：将数组元素加一

```el
import { map } from "el:collections/arrays/operations.el"
map(@[1, 2], value => value + 1)
```
预期结果：[2, 3]。

**返回值**：保存变换结果的新数组。

## filter {#api-b8bf1cd68b49358dbdef}

源码：`src/stdlib/collections/arrays/operations.el:166` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L166)

保留满足谓词的元素，并保持其相对顺序。

```el
@optimize(using: optimize_array, data: @{ stage: "filter", receiver: "argument" })
export fn filter(values, predicate)
```

**参数**：values 输入序列。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：筛选奇数

```el
import { filter } from "el:collections/arrays/operations.el"
filter(@[1, 2, 3], value => value % 2 == 1)
```
预期结果：[1, 3]。

**返回值**：保存符合谓词元素的新数组。

## drop {#api-6f4f6cc4e32930aa04c8}

源码：`src/stdlib/collections/arrays/operations.el:184` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L184)

跳过指定数量的前置元素并复制剩余元素。

```el
@optimize(using: optimize_array, data: @{ stage: "drop", receiver: "argument", prepare: normalize_count })
export fn drop(values, count)
```

**参数**：values 输入序列。

**参数**：count 调用方应提供非负有限整数；debug_mode 开启时，不合格值抛出字符串 ArrayCountRequiresNonnegativeInteger。

### 示例：跳过第一个元素

```el
import { drop } from "el:collections/arrays/operations.el"
drop(@[1, 2, 3], 1)
```
预期结果：[2, 3]。

**返回值**：跳过指定前缀后的新数组。

## take {#api-9aad8a70644d002e329e}

源码：`src/stdlib/collections/arrays/operations.el:207` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L207)

复制序列开头至多指定数量的元素。

```el
@optimize(using: optimize_array, data: @{ stage: "take", receiver: "argument", prepare: normalize_count })
export fn take(values, count)
```

**参数**：values 输入序列。

**参数**：count 调用方应提供非负有限整数；debug_mode 开启时，不合格值抛出字符串 ArrayCountRequiresNonnegativeInteger。

### 示例：取得前两个元素

```el
import { take } from "el:collections/arrays/operations.el"
take(@[1, 2, 3], 2)
```
预期结果：[1, 2]。

**返回值**：输入前缀的新数组。

## each {#api-abd0044e05f4d936ba48}

源码：`src/stdlib/collections/arrays/operations.el:227` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L227)

按迭代顺序对每个元素调用回调。

```el
@optimize(using: optimize_array, data: @{ stage: "each", receiver: "argument" })
export fn each(values, callback): void_t
```

**返回类型**：[`void_t`](../../language/values.md#api-d7b419fab395eef3d142)

**参数**：values 输入序列。

**参数**：callback 接收一个元素的函数。

### 示例：按顺序访问元素

```el
import { each } from "el:collections/arrays/operations.el"
each(@[1, 2], value => value)
```
预期结果：回调依次接收 1 和 2。

**返回值**：void_t。

## index_of {#api-1d673464d0f4a1e9259f}

源码：`src/stdlib/collections/arrays/operations.el:243` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L243)

返回首个与目标值相等的元素下标；未找到时返回 -1。

```el
export fn index_of(values, wanted): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：values 输入序列。

**参数**：wanted 要查找的值。

### 示例：查找元素下标

```el
import { index_of } from "el:collections/arrays/operations.el"
index_of(@[4, 7, 9], 7)
```
预期结果：1。

**返回值**：整数下标；未找到时为 -1。

## find {#api-460916110d52e2afe0bc}

源码：`src/stdlib/collections/arrays/operations.el:263` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L263)

返回首个满足谓词的迭代步骤；没有匹配项时返回空步骤。

```el
@optimize(using: optimize_array, data: @{ stage: "find", receiver: "argument" })
export fn find(values, predicate)
```

**参数**：values 输入序列。

**参数**：predicate 接收元素并返回布尔值的函数。

### 示例：查找首个奇数

```el
import { find } from "el:collections/arrays/operations.el"
find(@[2, 4, 5], value => value % 2 == 1).value
```
预期结果：5。

**返回值**：迭代步骤；未匹配时为空步骤。

## find_or_add {#api-067148f9a59780a84648}

源码：`src/stdlib/collections/arrays/operations.el:283` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L283)

查找满足谓词的元素；若不存在则创建、追加并返回新元素。

```el
export fn find_or_add(values, predicate, create)
```

**参数**：values 支持 push 的可变序列。

**参数**：predicate 查找谓词。

**参数**：create 无参数的创建函数。

### 示例：找不到时追加新值

```el
import { find_or_add } from "el:collections/arrays/operations.el"
let values = @[1, 3]
find_or_add(values, value => value == 2, () => 2)
```
预期结果：2。

**返回值**：已存在的匹配值，或创建并追加的新值。

## sort {#api-ae02065b29d656bd9fa4}

源码：`src/stdlib/collections/arrays/operations.el:302` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L302)

对输入副本排序并返回排序结果，输入保持不变。

```el
@optimize(using: optimize_sort, data: @{ receiver: "argument", independent: t, copy: copy_sort_input, pass: insertion_pass, tail: insertion_tail, ascending: ascending, merge: merge_sort, adaptive: adaptive_number_sort, insertion: insertion_sort, bucket: bounded_number_sort })
export fn sort(values, less = (left, right) => left < right, strategy = stable_memory_sort)
```

**参数**：values 支持迭代且其副本可排序。

**参数**：less 当左值应排在右值之前时返回真。

**参数**：strategy 选择排序策略，默认 stable_memory_sort。

**返回值**：排序后的新序列；输入通过复制路径排序，不原地修改。

### 示例：排序数组副本

```el
import { sort } from "el:collections/arrays/operations.el"
sort(@[3, 1, 2])
```
预期结果：[1, 2, 3]。

## reverse {#api-e7e440001fd92e7e7aab}

源码：`src/stdlib/collections/arrays/operations.el:318` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L318)

原地反转可写序列，并返回该序列。

```el
@discardable
export fn reverse(values)
```

**参数**：values 支持按下标读写的可变序列。

### 示例：原地反转数组

```el
import { reverse } from "el:collections/arrays/operations.el"
let values = @[1, 2, 3]
reverse(values)
```
预期结果：[3, 2, 1]。

**返回值**：原序列（已原地反转）。

## reversed {#api-9fcbfa328be62b344c58}

源码：`src/stdlib/collections/arrays/operations.el:338` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/operations.el#L338)

按相反顺序复制序列元素到新数组。

```el
export fn reversed(values)
```

**参数**：values 输入序列。

### 示例：反向复制数组

```el
import { reversed } from "el:collections/arrays/operations.el"
reversed(@[1, 2, 3])
```
预期结果：[3, 2, 1]。

**返回值**：顺序反转的新数组。
