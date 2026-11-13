# collections/sequences/demand.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Sequence.consume](#api-45dc347b6a31d11d535a)
- [Sequence.drop](#api-20db4321c06f72ac55a5)
- [Sequence.take](#api-b415cd6c8b485fb55cfc)
- [Sequence.slice](#api-1a13690071622bccebd0)
- [Sequence.map](#api-a9dd3fbd45fbdbc235ae)
- [Sequence.filter](#api-779750da0080921fdd71)
- [Sequence.collect](#api-12bd7b94b2871a2ffb6c)
- [Sequence.sum](#api-f18006015ef6f920209d)

## 惰性序列 {#api-7a16f7a075763e8cea09}

源码：`src/stdlib/collections/sequences/demand.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L1)

提供按需迭代、变换、筛选、切片及物化消费的序列接口。

## Sequence {#api-f1b57111a81f88477e0f}

源码：`src/stdlib/collections/sequences/demand.el:76` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L76)

表示可重新打开迭代器的惰性元素序列；每次迭代按需计算元素。

```el
export @assign(mode: "shared") class Sequence
```

### 示例：映射并筛选惰性值

```el
let numbers = lazy @[1, 2, 3, 4]
let result = numbers.map(value => value * 2).filter(value => value > 4).collect()
console.stdout.writeLine(result.join(", "))
```

## Sequence.consume {#api-45dc347b6a31d11d535a}

源码：`src/stdlib/collections/sequences/demand.el:92` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L92)

完整迭代并丢弃所有元素，以触发序列中的按需计算与清理。

```el
fn consume()
```

### 示例：消费全部序列

```el
let numbers = lazy @[1, 2, 3]
numbers.consume()
```

## Sequence.drop {#api-20db4321c06f72ac55a5}

源码：`src/stdlib/collections/sequences/demand.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L102)

返回跳过前 count 个元素后的惰性序列。

```el
fn drop(count: Number): Sequence
```

**返回类型**：[`Sequence`](demand.md#api-f1b57111a81f88477e0f)

**参数**：count 要跳过的非负整数个数。

**返回值**：延迟读取后续元素的序列。

### 示例：跳过首两项

```el
console.stdout.writeLine(lazy @[1, 2, 3].drop(2).collect().join(", "))
```

## Sequence.take {#api-b415cd6c8b485fb55cfc}

源码：`src/stdlib/collections/sequences/demand.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L117)

返回最多取前 count 个元素的惰性序列；后续元素不会被求值。

```el
fn take(count: Number): Sequence
```

**返回类型**：[`Sequence`](demand.md#api-f1b57111a81f88477e0f)

**参数**：count 要取的非负整数个数。

**返回值**：最多含 count 个元素的序列。

### 示例：只取前两项

```el
console.stdout.writeLine(lazy @[1, 2, 3].take(2).collect().join(", "))
```

## Sequence.slice {#api-1a13690071622bccebd0}

源码：`src/stdlib/collections/sequences/demand.el:133` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L133)

返回指定区间的惰性序列；省略 end 时延伸到序列末尾。

```el
fn slice(start: Number, end: Number | void_t = void): Sequence
```

**返回类型**：[`Sequence`](demand.md#api-f1b57111a81f88477e0f)

**参数**：start 起始非负整数下标。

**参数**：end 可选的结束下标，不包含该位置。

**返回值**：区间对应的惰性序列。

### 示例：取中间两项

```el
console.stdout.writeLine(lazy @[1, 2, 3, 4].slice(1, 3).collect().join(", "))
```

## Sequence.map {#api-a9dd3fbd45fbdbc235ae}

源码：`src/stdlib/collections/sequences/demand.el:156` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L156)

按需对每个元素应用转换函数，返回新的惰性序列。

```el
fn map(transform): Sequence
```

**返回类型**：[`Sequence`](demand.md#api-f1b57111a81f88477e0f)

**参数**：transform 将元素转换为新值的函数。

**返回值**：惰性变换序列。

### 示例：延迟加倍元素

```el
console.stdout.writeLine(lazy @[1, 2].map(value => value * 2).collect().join(", "))
```

## Sequence.filter {#api-779750da0080921fdd71}

源码：`src/stdlib/collections/sequences/demand.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L167)

按需保留谓词为真的元素。

```el
fn filter(predicate): Sequence
```

**返回类型**：[`Sequence`](demand.md#api-f1b57111a81f88477e0f)

**参数**：predicate 接收元素并返回布尔值的函数。

**返回值**：惰性筛选序列。

### 示例：延迟筛选正数

```el
console.stdout.writeLine(lazy @[-1, 2, 3].filter(value => value > 0).collect().join(", "))
```

## Sequence.collect {#api-12bd7b94b2871a2ffb6c}

源码：`src/stdlib/collections/sequences/demand.el:178` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L178)

迭代至序列结束，并将产生的元素收集到数组。

```el
fn collect(): any[]
```

**返回类型**：[`any`](../../../../../reference/language/types.md)[]

**返回值**：按迭代顺序排列的数组。

### 示例：物化序列

```el
let values = lazy @[1, 2, 3].collect()
console.stdout.writeLine(values.count)
```

## Sequence.sum {#api-f18006015ef6f920209d}

源码：`src/stdlib/collections/sequences/demand.el:187` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/demand.el#L187)

按序累加所有元素，初始累加值由调用方指定。

```el
fn sum(initial)
```

**参数**：initial 累加初值。

**返回值**：最终累加值。

### 示例：对惰性数列求和

```el
console.stdout.writeLine(lazy @[1, 2, 3].sum(0))
```
