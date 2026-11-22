# number/dit-int.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标数位整数 {#api-735cbf7ec4d6f03b78e9}

源码：`src/stdlib/number/dit-int.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-int.el#L1)

构造固定目标数位宽度的整数类型，提供有符号或无符号解释、数值域与溢出策略，并在该类型上实现整数转换和按位操作。

## DitInt {#api-f257d1fae552cc435b0b}

源码：`src/stdlib/number/dit-int.el:42` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-int.el#L42)

创建按目标基数解释的固定数位整数 Number 类型。
无符号域为 `[0, R^N-1]`；有符号域为 `[-floor(R^N/2), ceil(R^N/2)-1]`，负值以不小于 `ceil(R^N/2)` 的模余数保存。

```el-fragment
export fn DitInt(digits = 0, signed = f, min = nil, max = nil, overflow = "ub"): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：digits 固定目标数位数，可为零。

**参数**：signed 是否按目标基数补码解释负值。

**参数**：min 可选的闭区间下界，必须在表示域内。

**参数**：max 可选的闭区间上界，必须在表示域内。

**参数**：overflow 运算结果越界策略：ub、error、nan 或 wrap。

**返回值**：可实例化的固定数位整数类型。

### 示例：创建四位无符号目标数位整数

```el
let U4 = DitInt(digits: 4, overflow: "wrap")
console.stdout.writeLine(U4(15) + 1)
```
