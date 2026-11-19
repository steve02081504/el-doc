# collections/arrays/sparse-argmin.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 静态区间 argmin 稀疏表 {#api-57e7624820f56352f0cc}

源码：`src/stdlib/collections/arrays/sparse-argmin.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/sparse-argmin.el#L1)

对固定数值快照建立 [lo, hi) 区间最小值的原下标查询。

## range_argmin_sparse_table {#api-56cb02464b2fc4b3f421}

源码：`src/stdlib/collections/arrays/sparse-argmin.el:98` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/sparse-argmin.el#L98)

从固定数值数组建立区间 argmin 稀疏表。

```el
export fn range_argmin_sparse_table(values: Number[]): RangeArgminSparseTable
```

**返回类型**：[`RangeArgminSparseTable`](../../../types.md#api-c71fa8fe2f844daa33ce)

**参数**：values 有限数值数组；构造时复制。

**失败与异常**：输入包含非有限值时抛出 RangeError。

**返回值**：统一 [lo, hi)、并列取最左原下标的静态索引。

### 示例：查询区间最小值的下标

```el
let table = range_argmin_sparse_table(@[3, 1, 2])
console.stdout.writeLine(table.argmin(0, 3))
```
