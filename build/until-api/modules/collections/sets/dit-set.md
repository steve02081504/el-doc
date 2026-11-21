# collections/sets/dit-set.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [DitSet.toNumber](#api-282ea6306ccd98aa7377)
- [DitSet.rotateLeft](#api-4cc991b5ddecd4c72186)
- [DitSet.rotateRight](#api-5e7bb9d8fb8dbd3d8cfa)

## 固定宽度目标数位序列 {#api-f17ee09973544862e226}

源码：`src/stdlib/collections/sets/dit-set.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/dit-set.el#L1)

提供按目标基数解释的定宽数位序列及逐位模加、模减。

## DitSet {#api-6b020efe38e03cdb8638}

源码：`src/stdlib/collections/sets/dit-set.el:72` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/dit-set.el#L72)

创建 N 位目标基数数位序列；每个数位是 `0..R-1` 的精确整数，R 由目标事实给出。

```el
export fn DitSet(size: Number): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：size 固定数位数，可为零。

**返回值**：可实例化的数位序列类型。

**失败与异常**：构造值为负数、非整数、非有限数或超出 N 位数位容量时抛出 RangeError。

### 示例：创建八位状态

```el
let flags = DitSet<size: 8>(5)
console.stdout.writeLine(flags.toNumber())
```

## DitSet.toNumber {#api-282ea6306ccd98aa7377}

源码：`src/stdlib/collections/sets/dit-set.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/dit-set.el#L99)

将数位序列按目标基数解释为精确数值。

```el
fn toNumber(): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**返回值**：数位序列对应的非负整数。

### 示例：读取数位序列数值

```el
let flags = DitSet<size: 8>(5)
console.stdout.writeLine(flags.toNumber())
```

## DitSet.rotateLeft {#api-4cc991b5ddecd4c72186}

源码：`src/stdlib/collections/sets/dit-set.el:141` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/dit-set.el#L141)

将数位序列循环左移指定位数；移出的高位绕回低位。

```el
fn rotateLeft(count: Number): DitSet<size: size>
```

**返回类型**：[`DitSet`](dit-set.md#api-6b020efe38e03cdb8638)<size: [`size`](../../../types.md#api-c0d15bc265145c1818ee)>

**参数**：count 非负整数移位数。

**返回值**：同位宽的新数位序列。

### 示例：循环左移

```el
let flags = DitSet<size: 8>(129)
console.stdout.writeLine(flags.rotateLeft(1).toNumber())
```

## DitSet.rotateRight {#api-5e7bb9d8fb8dbd3d8cfa}

源码：`src/stdlib/collections/sets/dit-set.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/dit-set.el#L158)

将数位序列循环右移指定位数；移出的低位绕回高位。

```el
fn rotateRight(count: Number): DitSet<size: size>
```

**返回类型**：[`DitSet`](dit-set.md#api-6b020efe38e03cdb8638)<size: [`size`](../../../types.md#api-c0d15bc265145c1818ee)>

**参数**：count 非负整数移位数。

**返回值**：同位宽的新数位序列。

### 示例：循环右移

```el
let flags = DitSet<size: 8>(129)
console.stdout.writeLine(flags.rotateRight(1).toNumber())
```
