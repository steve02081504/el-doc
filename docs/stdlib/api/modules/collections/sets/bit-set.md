# collections/sets/bit-set.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [BitSet.toNumber](#api-a461f9fa010d45dc6fa5)
- [BitSet.rotateLeft](#api-5e4f408fca127d781277)
- [BitSet.rotateRight](#api-4e27c28ecd1abebd4b77)

## 固定位宽集合 {#api-dfad88fa0fa6c0a8b573}

源码：`src/stdlib/collections/sets/bit-set.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/bit-set.el#L1)

提供非负整数的固定宽度位集合及按位运算。

## BitSet {#api-2fd205cada268bede56b}

源码：`src/stdlib/collections/sets/bit-set.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/bit-set.el#L63)

```el
export fn BitSet(size: Number): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

创建 N 位无符号位集合类型；构造值必须是能完整表示在该位宽中的非负整数。

**参数**：size 固定位宽，可为零。

**返回值**：可实例化的位集合类型。

**失败与异常**：构造值为负数、非整数、非有限数或超出位宽时抛出 RangeError。

### 示例：创建八位标记

```el
let flags = BitSet<size: 8>(5)
console.stdout.writeLine(flags.toNumber())
```

## BitSet.toNumber {#api-a461f9fa010d45dc6fa5}

源码：`src/stdlib/collections/sets/bit-set.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/bit-set.el#L89)

```el
fn toNumber(): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

将位集合按无符号整数解释为精确数值。

**返回值**：位集合对应的非负整数。

### 示例：读取位集合数值

```el
let flags = BitSet<size: 8>(5)
console.stdout.writeLine(flags.toNumber())
```

## BitSet.rotateLeft {#api-5e4f408fca127d781277}

源码：`src/stdlib/collections/sets/bit-set.el:126` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/bit-set.el#L126)

```el
fn rotateLeft(count: Number): BitSet<size: size>
```

**返回类型**：[`BitSet`](bit-set.md#api-2fd205cada268bede56b)<size: [`size`](../../../types.md#api-09fd2333fe50aa733d41)>

将位集合循环左移指定位数；移出的高位绕回低位。

**参数**：count 非负整数移位数。

**返回值**：同位宽的新位集合。

### 示例：循环左移标记

```el
let flags = BitSet<size: 8>(129)
console.stdout.writeLine(flags.rotateLeft(1).toNumber())
```

## BitSet.rotateRight {#api-4e27c28ecd1abebd4b77}

源码：`src/stdlib/collections/sets/bit-set.el:143` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sets/bit-set.el#L143)

```el
fn rotateRight(count: Number): BitSet<size: size>
```

**返回类型**：[`BitSet`](bit-set.md#api-2fd205cada268bede56b)<size: [`size`](../../../types.md#api-09fd2333fe50aa733d41)>

将位集合循环右移指定位数；移出的低位绕回高位。

**参数**：count 非负整数移位数。

**返回值**：同位宽的新位集合。

### 示例：循环右移标记

```el
let flags = BitSet<size: 8>(129)
console.stdout.writeLine(flags.rotateRight(1).toNumber())
```
