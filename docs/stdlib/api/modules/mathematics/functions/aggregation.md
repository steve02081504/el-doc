# mathematics/functions/aggregation.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 标量聚合 {#api-69c62fe0b3acc5c17a3b}

源码：`src/stdlib/mathematics/functions/aggregation.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/aggregation.el#L1)

按实参顺序执行普通加法；不改变数组或张量模块中 sum 的归约合同。

## sum {#api-6e9b4c8195eebb551a52}

源码：`src/stdlib/mathematics/functions/aggregation.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/aggregation.el#L15)

从左到右累加所有输入；单个输入原样返回，零输入返回 Number 的零。

```el
export fn sum(...values)
```

**参数**：values 支持相邻累加的普通值；非空输入不额外与 Number 的零相加。

**返回值**：普通加法的结果，遵循输入类型的精度、溢出与效果合同。

**失败与异常**：加法抛出的异常原样传播，后续加法不执行。

**复杂度**：n 个非空输入执行 n-1 次加法。

### 示例：累加多个数

```el
let total = sum(1, 2, 3, 4)
// 预期 total 为 10。
```
