# collections/maps/hash-map.el

本页由源码注释生成；示例未运行验证。

## 哈希映射 {#api-e6d15a4109b1ed7292c3}

源码：`src/stdlib/collections/maps/hash-map.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L1)

提供按键查找的映射类型，键类型需满足相等与哈希合同。

## Map {#api-4f70fe0b29e63a840346}

源码：`src/stdlib/collections/maps/hash-map.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L34)

```el
export fn Map(key: type, value: type): type
```

创建以键和值类型参数化的哈希映射类型。

**参数**：key 键类型，须满足映射的键相等与哈希合同。

**参数**：value 映射值类型。

**返回值**：可实例化的 Map 类型。

### 示例：创建映射并写入

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
console.stdout.writeLine(scores.getOr("ada", 0))
```

## Map.set {#api-2237aab881f7dd69a3e3}

源码：`src/stdlib/collections/maps/hash-map.el:156` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/maps/hash-map.el#L156)

```el
@discardable override fn set(lookupKey: key, newValue: value): Bool
```

写入键值；若键已存在则替换原值。

**参数**：lookupKey 要写入的键。

**参数**：newValue 要关联的值。

**返回值**：新增键时为真，替换既有键时为假。

### 示例：保存分数

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
```
