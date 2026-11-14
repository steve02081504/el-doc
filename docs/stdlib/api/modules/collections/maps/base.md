# collections/maps/base.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Map.count](#api-0c7a0f184281a95f6821)
- [Map.remove](#api-86c98fb1130f62b84401)
- [Map.compact](#api-216207f74418a0afe4f3)
- [Map.clear](#api-7c378e1cc018ee51ecee)
- [Map.entries](#api-37209e2cfdae04240843)
- [Map.has](#api-d0a46e913af4f7a66ee6)
- [Map.get](#api-52852aadc467c16e4d8a)
- [Map.getOr](#api-9b5fac9ee67f5fe57436)
- [Map.keys](#api-bc2703a8337e9d87c267)
- [Map.values](#api-10056afaf272a33d1f68)

## Map.count {#api-0c7a0f184281a95f6821}

源码：`src/stdlib/collections/maps/base.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L31)

返回当前映射中的键值对数量。

```el
virtual get count(): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**返回值**：当前条目数。

### 示例：检查映射大小

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.count)
```

## Map.remove {#api-86c98fb1130f62b84401}

源码：`src/stdlib/collections/maps/base.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L44)

删除给定键对应的条目。

```el
@discardable virtual fn remove(lookupKey: key): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：lookupKey 要删除的键。

**返回值**：找到并删除条目时为真。

### 示例：删除用户分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.remove("ada")
```

## Map.compact {#api-216207f74418a0afe4f3}

源码：`src/stdlib/collections/maps/base.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L53)

释放预留容量及删除留下的空槽，保持现有键值及顺序合同。

```el
virtual fn compact()
```

### 示例：回收映射预留容量

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.compact()
```

## Map.clear {#api-7c378e1cc018ee51ecee}

源码：`src/stdlib/collections/maps/base.el:62` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L62)

删除映射中的全部条目。

```el
virtual fn clear()
```

### 示例：清空映射

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.clear()
```

## Map.entries {#api-37209e2cfdae04240843}

源码：`src/stdlib/collections/maps/base.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L75)

返回当前键值对组成的数组快照；直接遍历映射也使用此快照。
条目的 key 和 value 是只读属性；使用 set 更新映射，不会修改已有快照中的条目。
快照不保证深复制键或值。

```el
virtual fn entries(): Entry[]
```

**返回类型**：[`Entry`](../../../types.md#api-9ed70f0c228b3a6dd8a0)[]

**返回值**：每项包含 key 与 value 的条目数组。

### 示例：遍历映射条目

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
for (let {key, value} in scores) console.stdout.writeLine(key, " = ", value)
for (let {key: name, value: score} in scores) console.stdout.writeLine(name, " = ", score)
```

## Map.has {#api-d0a46e913af4f7a66ee6}

源码：`src/stdlib/collections/maps/base.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L89)

判断映射是否含有给定键，不读取或修改对应值。

```el
fn has(lookupKey: key): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：lookupKey 要查询的键。

**返回值**：键存在时为真。

### 示例：检查用户记录

```el
let users = Map<key: Text, value: Number>()
users.set("ada", 1)
console.stdout.writeLine(users.has("ada"))
```

## Map.get {#api-52852aadc467c16e4d8a}

源码：`src/stdlib/collections/maps/base.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L99)

查询键对应的值；键不存在时返回 void。

```el
fn get(lookupKey: key): value | void_t
```

**返回类型**：[`value`](../../../types.md#api-55134cc5930243ac905e) | [`void_t`](../../language/values.md#api-d7b419fab395eef3d142)

**参数**：lookupKey 要查询的键。

**返回值**：已存储的值或 void。

### 示例：读取可缺失的键

```el
let scores = Map<key: Text, value: Number>()
let score = scores.get("ada")
```

## Map.getOr {#api-9b5fac9ee67f5fe57436}

源码：`src/stdlib/collections/maps/base.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L115)

查询映射中的键；键不存在时返回调用方提供的默认值。

```el
fn getOr(lookupKey: key, fallback: value): value
```

**返回类型**：[`value`](../../../types.md#api-55134cc5930243ac905e)

**参数**：lookupKey 要查询的键。

**参数**：fallback 键缺失时返回的默认值。

**返回值**：已存储的值或默认值。

### 示例：使用默认值统计

```el
let counts = Map<key: Text, value: Number>()
counts.set("red", counts.getOr("red", 0) + 1)
console.stdout.writeLine(counts.getOr("red", 0))
```

## Map.keys {#api-bc2703a8337e9d87c267}

源码：`src/stdlib/collections/maps/base.el:152` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L152)

返回当前键组成的数组快照。

```el
fn keys(): key[]
```

**返回类型**：[`key`](../../../types.md#api-dcca461a039f57c7eab5)[]

**返回值**：键数组。

### 示例：遍历键快照

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.keys().join(", "))
```

## Map.values {#api-10056afaf272a33d1f68}

源码：`src/stdlib/collections/maps/base.el:166` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L166)

返回当前值组成的数组快照。

```el
fn values(): value[]
```

**返回类型**：[`value`](../../../types.md#api-55134cc5930243ac905e)[]

**返回值**：值数组。

### 示例：读取所有分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.values().join(", "))
```
