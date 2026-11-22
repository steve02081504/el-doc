# number/dit-operations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标数位运算 {#api-ec66250386693d4a789b}

源码：`src/stdlib/number/dit-operations.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-operations.el#L1)

提供逐目标数码独立执行的模加、模减、最小值和最大值运算；这些操作不传播进位或借位，并对不受支持的操作数形状报告错误。

## dit_add_mod {#api-d0505a59ece12ababdb0}

源码：`src/stdlib/number/dit-operations.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-operations.el#L66)

每个目标数码独立进行模加，不把进位传给高位。

```el-signature
export fn dit_add_mod(left: Number, right: Number): Number
```

**返回类型**：[`Number`](number.md#api-3cc24d3ef702e8652fb4)

**参数**：left 有限整数。

**参数**：right 有限整数。

**返回值**：精确的普通 Number。

### 示例：对最低位运算

```el
console.stdout.writeLine(dit_add_mod(0, 1))
```
```text
1
```

## dit_sub_mod {#api-463e78a922d32514490c}

源码：`src/stdlib/number/dit-operations.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-operations.el#L79)

每个目标数码独立进行模减，不向高位借位。

```el-signature
export fn dit_sub_mod(left: Number, right: Number): Number
```

**返回类型**：[`Number`](number.md#api-3cc24d3ef702e8652fb4)

**参数**：left 有限整数。

**参数**：right 有限整数。

**返回值**：精确的普通 Number。

### 示例：对最低位运算

```el
console.stdout.writeLine(dit_sub_mod(1, 1))
```
```text
0
```

## dit_min {#api-adba7312cea79def5989}

源码：`src/stdlib/number/dit-operations.el:95` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-operations.el#L95)

逐位取两个整数目标数码的较小值。

```el-signature
export fn dit_min(left: Number, right: Number): Number
```

**返回类型**：[`Number`](number.md#api-3cc24d3ef702e8652fb4)

**参数**：left 有限整数。

**参数**：right 有限整数。

**返回值**：精确的普通 Number。

### 示例：对最低位运算

```el
console.stdout.writeLine(dit_min(0, 1))
```
```text
0
```

## dit_max {#api-ef7ccd1de40f01781213}

源码：`src/stdlib/number/dit-operations.el:108` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-operations.el#L108)

逐位取两个整数目标数码的较大值。

```el-signature
export fn dit_max(left: Number, right: Number): Number
```

**返回类型**：[`Number`](number.md#api-3cc24d3ef702e8652fb4)

**参数**：left 有限整数。

**参数**：right 有限整数。

**返回值**：精确的普通 Number。

### 示例：对最低位运算

```el
console.stdout.writeLine(dit_max(0, 1))
```
```text
1
```
