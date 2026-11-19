# collections/arrays/plus-minus-rmq.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## ±1 RMQ {#api-bea0228e96b076a20662}

源码：`src/stdlib/collections/arrays/plus-minus-rmq.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/plus-minus-rmq.el#L1)

在相邻差严格为 ±1 的数值序列上做 O(1) 区间最小值原下标查询。

## plus_minus_rmq {#api-a9b09a48c1e38238e73b}

源码：`src/stdlib/collections/arrays/plus-minus-rmq.el:170` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/plus-minus-rmq.el#L170)

从相邻差严格为 ±1 的数值数组建立区间 argmin 索引。

```el
export fn plus_minus_rmq(values: Number[]): PlusMinusRmq
```

**返回类型**：[`PlusMinusRmq`](../../../types.md#api-46e6fe6afedea524a4b7)

**参数**：values 数值数组；构造时复制并检验相邻差。

**返回值**：统一 [lo, hi)、并列取最左原下标的 ±1 RMQ。

**失败与异常**：存在非有限值或相邻差不是 1 或 -1 时抛出 PlusMinusRmqError。

### 示例：找区间内最左的最低点

```el
let index = plus_minus_rmq(@[2, 1, 0, 1, 0])
console.stdout.writeLine(index.argmin(0, 5))
```
```text
2
```
