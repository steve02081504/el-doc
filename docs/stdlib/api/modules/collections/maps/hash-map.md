# collections/maps/hash-map.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Map.reserve](#api-f7d59581f3f1cbc587a2)
- [Map.set](#api-2237aab881f7dd69a3e3)
- [Map.tryAdd](#api-e277e1770ee904b688d8)
- [Map.getOrInsert](#api-dbfec9db9a187199f071)
- [Map.update](#api-ecbb1ca6393ae8693785)

## 哈希映射 {#api-e6d15a4109b1ed7292c3}

源码：`src/stdlib/collections/maps/hash-map.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L1)

提供按键查找的映射类型，键类型需满足相等与哈希合同。

## Map {#api-4f70fe0b29e63a840346}

源码：`src/stdlib/collections/maps/hash-map.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L34)

创建以键和值类型参数化的哈希映射类型。

```el
export fn Map(key: type, value: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：key 键类型，须满足映射的键相等与哈希合同；相等的键须有相同哈希。

**参数**：value 映射值类型。

**返回值**：可实例化的 Map 类型。

### 示例：创建映射并写入

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.getOr("ada", 0))
```

## Map.reserve {#api-f7d59581f3f1cbc587a2}

源码：`src/stdlib/collections/maps/hash-map.el:125` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L125)

为至少指定数量的条目预留容量，不改变已有键值。

```el
fn reserve(expected: Number)
```

**参数**：expected 非负、有限的整数条目数；零不作操作。

**失败与异常**：数量不合法或超过容器限制时抛出 RangeError。

### 示例：预留空间

```el
let scores = Map<key: Text, value: Number>()
scores.reserve(20)
console.stdout.writeLine(scores.count)
```
预期标准输出：
```text
0
```

## Map.set {#api-2237aab881f7dd69a3e3}

源码：`src/stdlib/collections/maps/hash-map.el:176` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L176)

写入键值；若键已存在则保留原键并替换原值。

```el
@discardable override fn set(lookupKey: key, newValue: value): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：lookupKey 要写入的键。

**参数**：newValue 要关联的值。

**返回值**：新增键时为真，替换既有键时为假。

### 示例：保存分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
```

## Map.tryAdd {#api-e277e1770ee904b688d8}

源码：`src/stdlib/collections/maps/hash-map.el:202` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L202)

仅当键不存在时插入键值，已有值保持不变。

```el
@discardable override fn tryAdd(lookupKey: key, newValue: value): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：lookupKey 要插入的键。

**参数**：newValue 要关联的值。

**返回值**：插入时为真；键已存在时为假。

### 示例：重复插入不替换值

```el
let scores = Map<key: Text, value: Number>()
scores.tryAdd("ada", 98)
scores.tryAdd("ada", 10)
console.stdout.writeLine(scores.getOr("ada", 0))
```
预期标准输出：
```text
98
```

参见：[collections/maps/hash-map::Map.set](hash-map.md#api-2237aab881f7dd69a3e3)

## Map.getOrInsert {#api-dbfec9db9a187199f071}

源码：`src/stdlib/collections/maps/hash-map.el:227` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L227)

返回已有值；键缺失时调用 make 一次，将结果插入并返回。

```el
override fn getOrInsert(lookupKey: key, make): value
```

**返回类型**：[`value`](../../../types.md#api-e66d20f23d46dbcc3bf5)

**参数**：lookupKey 要查询或插入的键。

**参数**：make 无参数的值生成函数；键存在时不调用。

**返回值**：已有值或新插入的值。

**失败与异常**：make 失败时传播其异常，条目不会插入；回调不得重入修改同一映射。

### 示例：仅在缺失时初始化

```el
let counts = Map<key: Text, value: Number>()
console.stdout.writeLine(counts.getOrInsert("red", () => 3))
console.stdout.writeLine(counts.getOrInsert("red", () => 9))
```
预期标准输出：
```text
3
3
```

## Map.update {#api-ecbb1ca6393ae8693785}

源码：`src/stdlib/collections/maps/hash-map.el:254` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L254)

用回调计算并保存新值；键缺失时以 initial 为输入。

```el
@discardable override fn update(lookupKey: key, change, initial: value): value
```

**返回类型**：[`value`](../../../types.md#api-e66d20f23d46dbcc3bf5)

**参数**：lookupKey 要更新的键。

**参数**：change 接收原值或 initial 并返回新值的函数。

**参数**：initial 键缺失时传给回调的值。

**返回值**：保存的新值。

**失败与异常**：change 失败时传播其异常，不提交新条目或替换值；回调不得重入修改同一映射。

### 示例：累计出现次数

```el
let counts = Map<key: Text, value: Number>()
counts.update("red", value => value + 1, 0)
console.stdout.writeLine(counts.update("red", value => value + 1, 0))
```
预期标准输出：
```text
2
```
