# number/dit-float.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标数位软件浮点 {#api-1db106c9d45fbfa4fea0}

源码：`src/stdlib/number/dit-float.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-float.el#L1)

按目标基数实现具有 IEEE 风格特殊值的浮点类型，包括有符号零、无穷、NaN、次正规数、舍入、平方根及编码投影。

## DitFloat {#api-3bf2f5b6b8ccdfc86851}

源码：`src/stdlib/number/dit-float.el:285` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/dit-float.el#L285)

用目标基数创建软件浮点类型，支持有符号零、无穷和 NaN。`sign_dits: 0` 是不带符号数位的无符号布局。

```el-fragment
export fn DitFloat(sign_dits = 1, fraction_dits = 0, exponent_dits = 0, exponent_bias = 0, min = nil, max = nil, overflow = "ub"): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：sign_dits 符号数位数，0 或 1。

**参数**：fraction_dits 尾数域数位数，至少 1；有效精度为它加首位。

**参数**：exponent_dits 指数域数位数，至少 2。

**参数**：exponent_bias 指数偏置，非负且小于保留的最大保留指数码。

**参数**：min 可选的有限值下界。

**参数**：max 可选的有限值上界。

**参数**：overflow 溢出策略：ub、error、nan 或 wrap。

**返回值**：按最近偶数舍入并支持次正规数的布局类型。

**失败与异常**：无效布局抛 RangeError；越界或策略拒绝走既有的致命诊断路径。

### 示例：计算能精确表示的平方根

```el
let Small = DitFloat<sign_dits: 1, fraction_dits: 3, exponent_dits: 3, exponent_bias: 3>
console.stdout.writeLine(Small(4).sqrt().toNumber())
```
```text
2
```
