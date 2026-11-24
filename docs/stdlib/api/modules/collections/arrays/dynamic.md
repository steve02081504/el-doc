# collections/arrays/dynamic.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Array.compact](#api-b5d526b100604be1a50c)
- [Array.count](#api-dc53f1b7c7bb205456fe)
- [Array.unshift](#api-0d49f10ce11561b6c3d4)
- [Array.push](#api-667c1e6be4c14a58cf83)
- [Array.pushIfAbsent](#api-a3adc0d64072d7e15531)
- [Array.pop](#api-b2d6f065ddc035962676)
- [Array.shift](#api-f5ecc5c0a1649295acd5)
- [Array.clear](#api-2f0dc66bf9a8acb8acc6)
- [Array.some](#api-62d8ef96ddac55a5e4be)
- [Array.all](#api-8981ea4aa2a88e2d41b5)
- [Array.filter](#api-e9c5cd664038d0ffd435)
- [Array.drop](#api-effa05c31b8b8f5e7352)
- [Array.take](#api-c5fa66ab34cdd427c5c8)
- [Array.indexOf](#api-ecbded967606961a0653)
- [Array.lastIndexOf](#api-cff140a5b29c28e662f2)
- [Array.findIndex](#api-632fabd9f6338d6ce759)
- [Array.findLastIndex](#api-c3ff93098165e551ff0a)
- [Array.findLast](#api-0c516e2b015251cfd317)
- [Array.sort](#api-6329d5217c413e7c25f7)
- [Array.reverse](#api-87bcb7d8c6070a3515c9)
- [Array.slice](#api-798006d6685ff5c33c0b)
- [Array.sliceClamped](#api-e0a3a8d0e4a021feebae)
- [Array.join](#api-2f72f73fba18bd804573)
- [Array.map](#api-1721eda4a7e77ea6fcdc)
- [Array.includes](#api-31fc5732d3781cb03718)

## 动态数组 {#api-ac2cbfeb62dc24b1405f}

源码：`src/stdlib/collections/arrays/dynamic.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L1)

提供可变长数组类型及映射、过滤、查找、切片、排序和拼接操作。

## Array.compact {#api-b5d526b100604be1a50c}

源码：`src/stdlib/collections/arrays/dynamic.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L56)

释放可回收的预留存储，保留元素及顺序；可能使物理元素引用失效。
计算数组、定长数组和借用视图没有可释放的预留容量。

```el-signature
virtual fn compact()
```

### 示例：回收数组预留容量

```el
let values = @[1, 2, 3]
values.compact()
```

## Array.count {#api-dc53f1b7c7bb205456fe}

源码：`src/stdlib/collections/arrays/dynamic.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L64)

返回数组中当前元素数量。

```el-signature
virtual get count(): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**返回值**：数组长度，以精确的非负 Number 表示。

### 示例：读取数组长度

```el
console.stdout.writeLine(@[10, 20, 30].count)
```

## Array.unshift {#api-0d49f10ce11561b6c3d4}

源码：`src/stdlib/collections/arrays/dynamic.el:91` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L91)

将元素插入数组开头，并返回数组。

```el-signature
@discardable virtual fn unshift(value: any): Array
```

**返回类型**：[`Array`](../../../types.md#api-02f04934b15030edb96d)

**参数**：value 要插入的元素。

**返回值**：当前数组。

### 示例：在开头插入元素

```el
let values = @[10, 20]
values.unshift(0)
console.stdout.writeLine(values[0])
```

## Array {#api-02f04934b15030edb96d}

源码：`src/stdlib/collections/arrays/dynamic.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L140)

创建带元素类型的可变长数组类型，实例支持索引读写、增删和常用遍历操作。

```el-signature
export fn Array(element: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：element 数组元素类型。

**返回值**：可实例化的 Array 类型。

### 示例：创建并追加元素

```el
let values = @[1, 2]
values.push(3)
console.stdout.writeLine(values.count)
```

## Array.push {#api-667c1e6be4c14a58cf83}

源码：`src/stdlib/collections/arrays/dynamic.el:184` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L184)

将一个元素追加到数组末尾，并返回数组以便继续链式操作。

```el-signature
@discardable virtual fn push(value: element): Array
```

**返回类型**：[`Array`](../../../types.md#api-02f04934b15030edb96d)

**参数**：value 要追加的元素。

**返回值**：当前数组。

### 示例：追加元素

```el
let values = @[1]
values.push(2)
console.stdout.writeLine(values[1])
```

## Array.pushIfAbsent {#api-a3adc0d64072d7e15531}

源码：`src/stdlib/collections/arrays/dynamic.el:195` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L195)

按 includes 检查元素，缺失时追加到末尾。

```el-signature
@discardable fn pushIfAbsent(value: element): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：value 要追加的元素。

**返回值**：已追加时为真，已存在时为假。

**失败与异常**：需要追加时会传播 push 的错误。

### 示例：追加缺失元素

```el
let values = @[1, 2]
values.pushIfAbsent(3)
```

## Array.pop {#api-b2d6f065ddc035962676}

源码：`src/stdlib/collections/arrays/dynamic.el:210` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L210)

移除并返回数组末尾元素。

```el-signature
@discardable virtual fn pop(): element
```

**返回类型**：[`element`](../../../types.md#api-5559abbccb9a177fbfdf)

**返回值**：原末尾元素。

**失败与异常**：DynamicArray 为空时抛出 RangeError。

### 示例：取走末尾元素

```el
let values = @[1, 2]
let last = values.pop()
console.stdout.writeLine(last)
```

## Array.shift {#api-f5ecc5c0a1649295acd5}

源码：`src/stdlib/collections/arrays/dynamic.el:222` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L222)

移除并返回数组首元素。

```el-signature
@discardable virtual fn shift(): element
```

**返回类型**：[`element`](../../../types.md#api-5559abbccb9a177fbfdf)

**返回值**：原首元素。

**失败与异常**：DynamicArray 为空时抛出 RangeError。

### 示例：取走首元素

```el
let values = @[1, 2]
let first = values.shift()
console.stdout.writeLine(first)
```

## Array.clear {#api-2f0dc66bf9a8acb8acc6}

源码：`src/stdlib/collections/arrays/dynamic.el:235` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L235)

原地移除全部元素；空数组调用后仍为空。

```el-signature
virtual fn clear(): nil_t
```

**返回类型**：[`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：清空数组

```el
let values = @[1, 2]
values.clear()
console.stdout.writeLine(values.count)
```
预期标准输出：
```text
0
```

## Array.some {#api-62d8ef96ddac55a5e4be}

源码：`src/stdlib/collections/arrays/dynamic.el:247` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L247)

判断是否至少有一个元素满足谓词；找到首个匹配项后即停止遍历。

```el-signature
fn some(predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：predicate 接收元素并返回布尔值的函数。

**返回值**：存在匹配元素时为真。

### 示例：判断数组是否含大数

```el
console.stdout.writeLine(@[1, 30, 2].some => it > 20)
```

## Array.all {#api-8981ea4aa2a88e2d41b5}

源码：`src/stdlib/collections/arrays/dynamic.el:261` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L261)

判断所有元素是否都满足谓词；遇到首个不匹配项后即停止遍历。

```el-signature
fn all(predicate): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：predicate 接收元素并返回布尔值的函数。

**返回值**：全部匹配时为真；空数组返回真。

### 示例：检查数值范围

```el
console.stdout.writeLine(@[1, 2, 3].all => it > 0)
```

## Array.filter {#api-e9c5cd664038d0ffd435}

源码：`src/stdlib/collections/arrays/dynamic.el:275` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L275)

保留谓词返回真的元素，并按原有顺序组成新数组。

```el-signature
fn filter(predicate)
```

**参数**：predicate 接收一个元素并返回布尔值的函数。

**返回值**：满足谓词的元素数组。

### 示例：筛选较大的数

```el
let values = @[10, 30, 20]
let large = values.filter => it > 15
console.stdout.writeLine(large.join(", "))
```

## Array.drop {#api-effa05c31b8b8f5e7352}

源码：`src/stdlib/collections/arrays/dynamic.el:286` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L286)

返回跳过开头指定数量元素后的数组。

```el-signature
@optimize(using: optimize_array, data: @{ stage: "drop", receiver: "member", prepare: normalize_count })
		fn drop(count)
```

**参数**：count 要跳过的元素数。

**返回值**：新数组，不改变原数组。

### 示例：跳过首项

```el
console.stdout.writeLine(@[1, 2, 3].drop(1).join(", "))
```

## Array.take {#api-c5fa66ab34cdd427c5c8}

源码：`src/stdlib/collections/arrays/dynamic.el:296` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L296)

返回开头指定数量的元素组成的新数组。

```el-signature
@optimize(using: optimize_array, data: @{ stage: "take", receiver: "member", prepare: normalize_count })
		fn take(count)
```

**参数**：count 要保留的元素数。

**返回值**：最多含 count 个元素的新数组。

### 示例：取前两项

```el
console.stdout.writeLine(@[1, 2, 3].take(2).join(", "))
```

## Array.indexOf {#api-ecbded967606961a0653}

源码：`src/stdlib/collections/arrays/dynamic.el:308` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L308)

查找与给定值相等的第一个元素位置。

```el-signature
fn indexOf(value: element): Number | nil_t
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

**参数**：value 要查找的元素。

**返回值**：首个匹配下标；未找到时返回 nil。

### 示例：查找数组元素

```el
console.stdout.writeLine(@[10, 20, 30].indexOf(20))
```

## Array.lastIndexOf {#api-cff140a5b29c28e662f2}

源码：`src/stdlib/collections/arrays/dynamic.el:317` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L317)

从数组末尾向前查找与给定值相等的元素。

```el-signature
fn lastIndexOf(value: element): Number | nil_t
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

**参数**：value 要查找的元素。

**返回值**：从零开始的末个匹配下标；未找到时返回 nil。

### 示例：查找重复元素的最后一次出现

```el
console.stdout.writeLine(@[10, 20, 10].lastIndexOf(10))
```

## Array.findIndex {#api-632fabd9f6338d6ce759}

源码：`src/stdlib/collections/arrays/dynamic.el:327` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L327)

从头查找满足谓词的元素，返回从零开始的下标或 nil。

```el-signature
fn findIndex(predicate): Number | nil_t
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：查找首个匹配下标

```el
@[1, 2, 3].findIndex => it > 1
```

## Array.findLastIndex {#api-c3ff93098165e551ff0a}

源码：`src/stdlib/collections/arrays/dynamic.el:334` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L334)

从尾查找满足谓词的元素，返回从零开始的下标或 nil。

```el-signature
fn findLastIndex(predicate): Number | nil_t
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：查找末个匹配下标

```el
@[1, 2, 3].findLastIndex => it > 1
```

## Array.findLast {#api-0c516e2b015251cfd317}

源码：`src/stdlib/collections/arrays/dynamic.el:341` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L341)

从尾查找满足谓词的元素，返回匹配值或 nil。

```el-signature
fn findLast(predicate)
```

### 示例：查找末个匹配值

```el
@[1, 2, 3].findLast => it > 1
```

## Array.sort {#api-6329d5217c413e7c25f7}

源码：`src/stdlib/collections/arrays/dynamic.el:354` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L354)

按比较函数排序并返回新数组，保留原数组不变。

```el-signature
fn sort(less = (left, right) => left < right, strategy = stable_memory_sort)
```

**参数**：less 当左值应排在右值之前时返回真的比较函数。

**参数**：strategy 排序策略，默认为稳定内存排序。

**返回值**：排序后的新数组。

### 示例：排序数值

```el
let sorted = @[3, 1, 2].sort()
console.stdout.writeLine(sorted.join(", "))
```

## Array.reverse {#api-87bcb7d8c6070a3515c9}

源码：`src/stdlib/collections/arrays/dynamic.el:363` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L363)

返回元素顺序相反的新数组，不改变原数组。

```el-signature
fn reverse()
```

**返回值**：反转顺序的数组副本。

### 示例：保留原数组并取反序副本

```el
let values = @[1, 2, 3]
console.stdout.writeLine(values.reverse().join(", "))
```

## Array.slice {#api-798006d6685ff5c33c0b}

源码：`src/stdlib/collections/arrays/dynamic.el:374` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L374)

严格复制指定的左闭右开区间。

```el-signature
fn slice(start: Number, end: Number)
```

**参数**：start 起始下标。

**参数**：end 结束下标，不包含该位置。

**返回值**：长度静态已知时返回定长数组，否则返回变长数组。

### 示例：取中间两个元素

```el
let middle = @[10, 20, 30, 40].slice(1, 3)
console.stdout.writeLine(middle[0], middle[1])
```

## Array.sliceClamped {#api-e0a3a8d0e4a021feebae}

源码：`src/stdlib/collections/arrays/dynamic.el:385` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L385)

将整数端点夹到有效下标范围，再复制左闭右开区间。反向区间返回空数组。

```el-signature
fn sliceClamped(start: Number, end: Number): Array<element: element>
```

**返回类型**：[`Array`](../../../types.md#api-02f04934b15030edb96d)<element: [`element`](../../../types.md#api-5559abbccb9a177fbfdf)>

**参数**：start 起始下标。

**参数**：end 结束下标，不包含该位置。

**返回值**：区间内容的变长数组副本。

### 示例：复制数组片段

```el
let copy = @[10, 20, 30].sliceClamped(1, 3)
console.stdout.writeLine(copy.join(", "))
```

## Array.join {#api-2f72f73fba18bd804573}

源码：`src/stdlib/collections/arrays/dynamic.el:396` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L396)

将元素依次转换为文本并用分隔文本连接。

```el-signature
fn join(separator: Text = Text()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：separator 元素之间插入的文本，默认为空文本。

**返回值**：连接后的文本。

### 示例：用逗号连接单词

```el
let words = @["red", "blue"]
console.stdout.writeLine(words.join(", "))
```

## Array.map {#api-1721eda4a7e77ea6fcdc}

源码：`src/stdlib/collections/arrays/dynamic.el:408` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L408)

按原顺序对每个元素调用转换函数，并返回转换结果数组。

```el-signature
fn map(transform)
```

**参数**：transform 接收一个元素并返回新值的函数。

**返回值**：转换后的数组。

### 示例：将数值加倍

```el
let doubled = @[1, 2, 3].map => it * 2
console.stdout.writeLine(doubled.join(", "))
```

## Array.includes {#api-31fc5732d3781cb03718}

源码：`src/stdlib/collections/arrays/dynamic.el:422` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L422)

判断数组是否含有与给定值相等的元素。

```el-signature
fn includes(value: element): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：value 要查找的元素。

**返回值**：找到相等元素时为真。

### 示例：查找目标值

```el
console.stdout.writeLine(@["red", "blue"].includes("blue"))
```
