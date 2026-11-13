# collections/arrays/dynamic.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Array.count](#api-dc53f1b7c7bb205456fe)
- [Array.unshift](#api-0d49f10ce11561b6c3d4)
- [Array.push](#api-667c1e6be4c14a58cf83)
- [Array.pop](#api-b2d6f065ddc035962676)
- [Array.shift](#api-f5ecc5c0a1649295acd5)
- [Array.clear](#api-2f0dc66bf9a8acb8acc6)
- [Array.some](#api-62d8ef96ddac55a5e4be)
- [Array.all](#api-8981ea4aa2a88e2d41b5)
- [Array.filter](#api-e9c5cd664038d0ffd435)
- [Array.drop](#api-effa05c31b8b8f5e7352)
- [Array.take](#api-c5fa66ab34cdd427c5c8)
- [Array.indexOf](#api-ecbded967606961a0653)
- [Array.sort](#api-6329d5217c413e7c25f7)
- [Array.reverse](#api-87bcb7d8c6070a3515c9)
- [Array.reversed](#api-5dd9c5add2a8a84dbdd5)
- [Array.slice](#api-798006d6685ff5c33c0b)
- [Array.sliceDynamic](#api-bd2715c4bb37b48f50de)
- [Array.join](#api-2f72f73fba18bd804573)
- [Array.map](#api-1721eda4a7e77ea6fcdc)
- [Array.includes](#api-31fc5732d3781cb03718)

## 动态数组 {#api-ac2cbfeb62dc24b1405f}

源码：`src/stdlib/collections/arrays/dynamic.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L1)

提供可变长数组类型及映射、过滤、查找、切片、排序和拼接操作。

## Array.count {#api-dc53f1b7c7bb205456fe}

源码：`src/stdlib/collections/arrays/dynamic.el:46` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L46)

```el
virtual get count(): Integer
```

**返回类型**：`Integer`

返回数组中当前元素数量。

**返回值**：数组长度，以 NativeSignedInteger 表示。

### 示例：读取数组长度

```el
console.stdout.writeLine(@[10, 20, 30].count)
```

## Array.unshift {#api-0d49f10ce11561b6c3d4}

源码：`src/stdlib/collections/arrays/dynamic.el:70` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L70)

```el
@discardable virtual fn unshift(value: any): Array
```

**返回类型**：`Array`

将元素插入数组开头，并返回数组。

**参数**：value 要插入的元素。

**返回值**：当前数组。

### 示例：在开头插入元素

```el
let values = @[10, 20]
values.unshift(0)
console.stdout.writeLine(values[0])
```

## Array {#api-02f04934b15030edb96d}

源码：`src/stdlib/collections/arrays/dynamic.el:119` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L119)

```el
export fn Array(element: type): type
```

**返回类型**：`type`

创建带元素类型的可变长数组类型，实例支持索引读写、增删和常用遍历操作。

**参数**：element 数组元素类型。

**返回值**：可实例化的 Array 类型。

### 示例：创建并追加元素

```el
let values = @[1, 2]
values.push(3)
console.stdout.writeLine(values.count)
```

## Array.push {#api-667c1e6be4c14a58cf83}

源码：`src/stdlib/collections/arrays/dynamic.el:139` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L139)

```el
@discardable virtual fn push(value: element): Array
```

**返回类型**：`Array`

将一个元素追加到数组末尾，并返回数组以便继续链式操作。

**参数**：value 要追加的元素。

**返回值**：当前数组。

### 示例：追加元素

```el
let values = @[1]
values.push(2)
console.stdout.writeLine(values[1])
```

## Array.pop {#api-b2d6f065ddc035962676}

源码：`src/stdlib/collections/arrays/dynamic.el:150` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L150)

```el
@discardable virtual fn pop(): element
```

**返回类型**：`element`

移除并返回数组末尾元素。

**返回值**：原末尾元素。

**失败与异常**：DynamicArray 为空时抛出 RangeError。

### 示例：取走末尾元素

```el
let values = @[1, 2]
let last = values.pop()
console.stdout.writeLine(last)
```

## Array.shift {#api-f5ecc5c0a1649295acd5}

源码：`src/stdlib/collections/arrays/dynamic.el:162` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L162)

```el
@discardable virtual fn shift(): element
```

**返回类型**：`element`

移除并返回数组首元素。

**返回值**：原首元素。

**失败与异常**：DynamicArray 为空时抛出 RangeError。

### 示例：取走首元素

```el
let values = @[1, 2]
let first = values.shift()
console.stdout.writeLine(first)
```

## Array.clear {#api-2f0dc66bf9a8acb8acc6}

源码：`src/stdlib/collections/arrays/dynamic.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L175)

```el
virtual fn clear(): void_t
```

**返回类型**：`void_t`

原地移除全部元素；空数组调用后仍为空。

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

源码：`src/stdlib/collections/arrays/dynamic.el:187` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L187)

```el
fn some(predicate): Bool
```

**返回类型**：`Bool`

判断是否至少有一个元素满足谓词；找到首个匹配项后即停止遍历。

**参数**：predicate 接收元素并返回布尔值的函数。

**返回值**：存在匹配元素时为真。

### 示例：判断数组是否含大数

```el
console.stdout.writeLine(@[1, 30, 2].some(value => value > 20))
```

## Array.all {#api-8981ea4aa2a88e2d41b5}

源码：`src/stdlib/collections/arrays/dynamic.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L201)

```el
fn all(predicate): Bool
```

**返回类型**：`Bool`

判断所有元素是否都满足谓词；遇到首个不匹配项后即停止遍历。

**参数**：predicate 接收元素并返回布尔值的函数。

**返回值**：全部匹配时为真；空数组返回真。

### 示例：检查数值范围

```el
console.stdout.writeLine(@[1, 2, 3].all(value => value > 0))
```

## Array.filter {#api-e9c5cd664038d0ffd435}

源码：`src/stdlib/collections/arrays/dynamic.el:215` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L215)

```el
fn filter(predicate)
```

保留谓词返回真的元素，并按原有顺序组成新数组。

**参数**：predicate 接收一个元素并返回布尔值的函数。

**返回值**：满足谓词的元素数组。

### 示例：筛选较大的数

```el
let values = @[10, 30, 20]
let large = values.filter(value => value > 15)
console.stdout.writeLine(large.join(", "))
```

## Array.drop {#api-effa05c31b8b8f5e7352}

源码：`src/stdlib/collections/arrays/dynamic.el:226` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L226)

```el
@optimize(using: optimize_array, data: @{ stage: "drop", receiver: "member", prepare: normalize_count })
		fn drop(count)
```

返回跳过开头指定数量元素后的数组。

**参数**：count 要跳过的元素数。

**返回值**：新数组，不改变原数组。

### 示例：跳过首项

```el
console.stdout.writeLine(@[1, 2, 3].drop(1).join(", "))
```

## Array.take {#api-c5fa66ab34cdd427c5c8}

源码：`src/stdlib/collections/arrays/dynamic.el:236` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L236)

```el
@optimize(using: optimize_array, data: @{ stage: "take", receiver: "member", prepare: normalize_count })
		fn take(count)
```

返回开头指定数量的元素组成的新数组。

**参数**：count 要保留的元素数。

**返回值**：最多含 count 个元素的新数组。

### 示例：取前两项

```el
console.stdout.writeLine(@[1, 2, 3].take(2).join(", "))
```

## Array.indexOf {#api-ecbded967606961a0653}

源码：`src/stdlib/collections/arrays/dynamic.el:248` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L248)

```el
fn indexOf(value: element): Number
```

**返回类型**：`Number`

查找与给定值相等的第一个元素位置。

**参数**：value 要查找的元素。

**返回值**：首个匹配下标；未找到时返回 -1。

### 示例：查找数组元素

```el
console.stdout.writeLine(@[10, 20, 30].indexOf(20))
```

## Array.sort {#api-6329d5217c413e7c25f7}

源码：`src/stdlib/collections/arrays/dynamic.el:264` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L264)

```el
fn sort(less = (left, right) => left < right, strategy = stable_memory_sort)
```

按比较函数排序并返回新数组，保留原数组不变。

**参数**：less 当左值应排在右值之前时返回真的比较函数。

**参数**：strategy 排序策略，默认为稳定内存排序。

**返回值**：排序后的新数组。

### 示例：排序数值

```el
let sorted = @[3, 1, 2].sort()
console.stdout.writeLine(sorted.join(", "))
```

## Array.reverse {#api-87bcb7d8c6070a3515c9}

源码：`src/stdlib/collections/arrays/dynamic.el:274` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L274)

```el
@discardable fn reverse()
```

原地反转数组元素顺序，并返回当前数组。

**返回值**：已反转的当前数组。

### 示例：原地反转

```el
let values = @[1, 2, 3]
values.reverse()
console.stdout.writeLine(values.join(", "))
```

## Array.reversed {#api-5dd9c5add2a8a84dbdd5}

源码：`src/stdlib/collections/arrays/dynamic.el:283` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L283)

```el
fn reversed()
```

返回元素顺序相反的新数组，不改变原数组。

**返回值**：反转顺序的数组副本。

### 示例：保留原数组并取反序副本

```el
let values = @[1, 2, 3]
console.stdout.writeLine(values.reversed().join(", "))
```

## Array.slice {#api-798006d6685ff5c33c0b}

源码：`src/stdlib/collections/arrays/dynamic.el:294` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L294)

```el
fn slice(start: Number, end: Number): FixedArray<element: element, length: end - start>
```

**返回类型**：`FixedArray<element: element, length: end - start>`

返回指定左闭右开区间的定长切片。

**参数**：start 起始下标。

**参数**：end 结束下标，不包含该位置。

**返回值**：长度由 end - start 决定的定长数组。

### 示例：取中间两个元素

```el
let middle = @[10, 20, 30, 40].slice(1, 3)
console.stdout.writeLine(middle[0], middle[1])
```

## Array.sliceDynamic {#api-bd2715c4bb37b48f50de}

源码：`src/stdlib/collections/arrays/dynamic.el:305` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L305)

```el
fn sliceDynamic(start: Number, end: Number): Array<element: element>
```

**返回类型**：`Array<element: element>`

复制指定左闭右开区间，并返回变长数组。

**参数**：start 起始下标。

**参数**：end 结束下标，不包含该位置。

**返回值**：区间内容的变长数组副本。

### 示例：复制数组片段

```el
let copy = @[10, 20, 30].sliceDynamic(1, 3)
console.stdout.writeLine(copy.join(", "))
```

## Array.join {#api-2f72f73fba18bd804573}

源码：`src/stdlib/collections/arrays/dynamic.el:316` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L316)

```el
fn join(separator: Text = Text()): Text
```

**返回类型**：`Text`

将元素依次转换为文本并用分隔文本连接。

**参数**：separator 元素之间插入的文本，默认为空文本。

**返回值**：连接后的文本。

### 示例：用逗号连接单词

```el
let words = @["red", "blue"]
console.stdout.writeLine(words.join(", "))
```

## Array.map {#api-1721eda4a7e77ea6fcdc}

源码：`src/stdlib/collections/arrays/dynamic.el:328` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L328)

```el
fn map(transform)
```

按原顺序对每个元素调用转换函数，并返回转换结果数组。

**参数**：transform 接收一个元素并返回新值的函数。

**返回值**：转换后的数组。

### 示例：将数值加倍

```el
let doubled = @[1, 2, 3].map(value => value * 2)
console.stdout.writeLine(doubled.join(", "))
```

## Array.includes {#api-31fc5732d3781cb03718}

源码：`src/stdlib/collections/arrays/dynamic.el:341` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/dynamic.el#L341)

```el
fn includes(value: element): Bool
```

**返回类型**：`Bool`

判断数组是否含有与给定值相等的元素。

**参数**：value 要查找的元素。

**返回值**：找到相等元素时为真。

### 示例：查找目标值

```el
console.stdout.writeLine(@["red", "blue"].includes("blue"))
```
