# collections/maps/base.el

本页由源码注释生成；示例未运行验证。

## Map.count {#api-0c7a0f184281a95f6821}

源码：`src/stdlib/collections/maps/base.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L31)

```el
virtual get count(): Number
```

返回当前映射中的键值对数量。

**返回值**：当前条目数。

### 示例：检查映射大小

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.count)
```

## Map.remove {#api-86c98fb1130f62b84401}

源码：`src/stdlib/collections/maps/base.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L44)

```el
@discardable virtual fn remove(lookupKey: key): Bool
```

删除给定键对应的条目。

**参数**：lookupKey 要删除的键。

**返回值**：找到并删除条目时为真。

### 示例：删除用户分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.remove("ada")
```

## Map.clear {#api-7c378e1cc018ee51ecee}

源码：`src/stdlib/collections/maps/base.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L53)

```el
virtual fn clear()
```

删除映射中的全部条目。

### 示例：清空映射

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.clear()
```

## Map.entries {#api-37209e2cfdae04240843}

源码：`src/stdlib/collections/maps/base.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L63)

```el
virtual fn entries(): Entry[]
```

返回当前键值对组成的数组快照。

**返回值**：每项包含 key 与 value 的条目数组。

### 示例：遍历映射条目

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
for (let entry in scores) console.stdout.writeLine(entry.key, " = ", entry.value)
```

## Map.has {#api-d0a46e913af4f7a66ee6}

源码：`src/stdlib/collections/maps/base.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L77)

```el
fn has(lookupKey: key): Bool
```

判断映射是否含有给定键，不读取或修改对应值。

**参数**：lookupKey 要查询的键。

**返回值**：键存在时为真。

### 示例：检查用户记录

```el
let users = Map<key: Text, value: Number>()
users.set("ada", 1)
console.stdout.writeLine(users.has("ada"))
```

## Map.get {#api-52852aadc467c16e4d8a}

源码：`src/stdlib/collections/maps/base.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L87)

```el
fn get(lookupKey: key): value | void_t
```

查询键对应的值；键不存在时返回 void。

**参数**：lookupKey 要查询的键。

**返回值**：已存储的值或 void。

### 示例：读取可缺失的键

```el
let scores = Map<key: Text, value: Number>()
let score = scores.get("ada")
```

## Map.getOr {#api-9b5fac9ee67f5fe57436}

源码：`src/stdlib/collections/maps/base.el:103` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L103)

```el
fn getOr(lookupKey: key, fallback: value): value
```

查询映射中的键；键不存在时返回调用方提供的默认值。

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

源码：`src/stdlib/collections/maps/base.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L140)

```el
fn keys(): key[]
```

返回当前键组成的数组快照。

**返回值**：键数组。

### 示例：遍历键快照

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.keys().join(", "))
```

## Map.values {#api-10056afaf272a33d1f68}

源码：`src/stdlib/collections/maps/base.el:154` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/base.el#L154)

```el
fn values(): value[]
```

返回当前值组成的数组快照。

**返回值**：值数组。

### 示例：读取所有分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.values().join(", "))
```
