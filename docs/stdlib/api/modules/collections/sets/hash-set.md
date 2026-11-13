# collections/sets/hash-set.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 哈希集合 {#api-3c2602063f2b32fe6910}

源码：`src/stdlib/collections/sets/hash-set.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L1)

提供去重集合及集合代数操作。

## Set {#api-d0e70967a499a59ddcdc}

源码：`src/stdlib/collections/sets/hash-set.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L18)

```el
export fn Set(element: type): type
```

创建按元素去重的哈希集合类型。

**参数**：element 集合元素类型，须满足键相等与哈希合同。

**返回值**：可实例化的 Set 类型。

### 示例：添加与检查元素

```el
let tags = Set<element: Text>()
tags.add("el")
console.stdout.writeLine(tags.has("el"))
```

## Set.count {#api-7dcae9213eb8c6bddb8d}

源码：`src/stdlib/collections/sets/hash-set.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L36)

```el
get count(): Number
```

返回集合中不同元素的数量。

**返回值**：不重复元素数。

### 示例：查看去重结果数量

```el
let tags = Set<element: Text>()
tags.add("el")
tags.add("el")
console.stdout.writeLine(tags.count)
```

## Set.has {#api-8c4967d005886141d35a}

源码：`src/stdlib/collections/sets/hash-set.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L49)

```el
fn has(value: element): Bool
```

判断集合中是否已有给定元素。

**参数**：value 要检查的元素。

**返回值**：元素存在时为真。

### 示例：检查标签

```el
let tags = Set<element: Text>()
tags.add("el")
console.stdout.writeLine(tags.has("el"))
```

## Set.add {#api-19526eaad9f7ef5a50cf}

源码：`src/stdlib/collections/sets/hash-set.el:62` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L62)

```el
@discardable fn add(value: element): Bool
```

将元素加入集合；集合已有该元素时不产生重复项。

**参数**：value 要加入的元素。

**返回值**：元素原先不存在并成功加入时为真。

### 示例：添加去重标签

```el
let tags = Set<element: Text>()
tags.add("el")
tags.add("el")
console.stdout.writeLine(tags.count)
```

## Set.remove {#api-cec6fa071bc6bf0b9a95}

源码：`src/stdlib/collections/sets/hash-set.el:73` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L73)

```el
@discardable fn remove(value: element): Bool
```

从集合中删除给定元素（如果存在）。

**参数**：value 要删除的元素。

**返回值**：找到并删除时为真。

### 示例：删除标签

```el
let tags = Set<element: Text>()
tags.add("el")
tags.remove("el")
```

## Set.values {#api-08e9c0e43ab2da7101aa}

源码：`src/stdlib/collections/sets/hash-set.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L85)

```el
fn values(): element[]
```

返回集合中元素组成的数组快照。

**返回值**：含当前集合元素的数组。

### 示例：将集合内容写出

```el
let tags = Set<element: Text>()
tags.add("el")
console.stdout.writeLine(tags.values().join(", "))
```

## Set.union {#api-6fc99da40e2de7ac073d}

源码：`src/stdlib/collections/sets/hash-set.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L102)

```el
fn union(other): Set<element: element>
```

返回包含当前集合和另一个集合全部元素的新集合。

**参数**：other 参与并集的集合。

**返回值**：两个集合的并集，不修改操作数。

### 示例：合并标签

```el
let allTags = Set<element: Text>()
allTags.add("el")
let more = Set<element: Text>()
more.add("doc")
console.stdout.writeLine(allTags.union(more).count)
```

## Set.intersection {#api-b7027b62e6689eb23a7f}

源码：`src/stdlib/collections/sets/hash-set.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L114)

```el
fn intersection(other): Set<element: element>
```

返回仅包含同时存在于两个集合中的元素的新集合。

**参数**：other 参与交集的集合。

**返回值**：两集合交集，不修改操作数。

### 示例：求共同标签

```el
import { Set } from "el:collections/sets/"
let first = Set<element: Text>(); first.add("el")
let second = Set<element: Text>(); second.add("el")
let common = first.intersection(second)
```

## Set.difference {#api-374a5786f13d6e5ba4d3}

源码：`src/stdlib/collections/sets/hash-set.el:126` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L126)

```el
fn difference(other): Set<element: element>
```

返回存在于当前集合但不在另一个集合中的元素。

**参数**：other 用于排除元素的集合。

**返回值**：当前集合减去 other 后的新集合。

### 示例：排除已处理项目

```el
import { Set } from "el:collections/sets/"
let all = Set<element: Text>(); all.add("el")
let done = Set<element: Text>()
let remaining = all.difference(done)
```

## Set.symmetricDifference {#api-84114d3fe59c80193055}

源码：`src/stdlib/collections/sets/hash-set.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L138)

```el
fn symmetricDifference(other): Set<element: element>
```

返回只出现在其中一个集合中的元素。

**参数**：other 参与对称差运算的集合。

**返回值**：两集合对称差的新集合。

### 示例：查找集合不同项

```el
import { Set } from "el:collections/sets/"
let before = Set<element: Text>(); before.add("el")
let after = Set<element: Text>(); after.add("doc")
let changed = before.symmetricDifference(after)
```

## Set.isSubsetOf {#api-5dd01f2e69fa12046ef8}

源码：`src/stdlib/collections/sets/hash-set.el:150` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L150)

```el
fn isSubsetOf(other): Bool
```

判断当前集合是否为另一个集合的子集。

**参数**：other 候选超集。

**返回值**：当前集合每个元素都存在于 other 时为真。

### 示例：检查权限子集

```el
import { Set } from "el:collections/sets/"
let required = Set<element: Text>(); required.add("read")
let granted = Set<element: Text>(); granted.add("read")
console.stdout.writeLine(required.isSubsetOf(granted))
```

## Set.isSupersetOf {#api-01377dfbc1aa88307fa5}

源码：`src/stdlib/collections/sets/hash-set.el:162` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L162)

```el
fn isSupersetOf(other): Bool
```

判断当前集合是否包含另一个集合的全部元素。

**参数**：other 候选子集。

**返回值**：other 是当前集合子集时为真。

### 示例：检查已授予权限

```el
import { Set } from "el:collections/sets/"
let required = Set<element: Text>(); required.add("read")
let granted = Set<element: Text>(); granted.add("read")
console.stdout.writeLine(granted.isSupersetOf(required))
```

## Set.isDisjointFrom {#api-dcb2b454234c09158e47}

源码：`src/stdlib/collections/sets/hash-set.el:174` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/hash-set.el#L174)

```el
fn isDisjointFrom(other): Bool
```

判断两个集合是否没有共同元素。

**参数**：other 参与判断的集合。

**返回值**：两集合交集为空时为真。

### 示例：检查标签是否冲突

```el
import { Set } from "el:collections/sets/"
let first = Set<element: Text>(); first.add("el")
let second = Set<element: Text>(); second.add("doc")
console.stdout.writeLine(first.isDisjointFrom(second))
```
