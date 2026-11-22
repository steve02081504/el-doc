# collections/trees/euler-tour.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 树 Euler 游走 {#api-34a3bb7562411876fd28}

源码：`src/stdlib/collections/trees/euler-tour.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/euler-tour.el#L1)

在共享的迭代 DFS 事件骨架上记录首次到达和每次沿边回父。

## euler_tour {#api-347b8c5b0509471819bd}

源码：`src/stdlib/collections/trees/euler-tour.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/euler-tour.el#L99)

从根键和直接子键遍历构建 Euler 游走。

```el-signature
export fn euler_tour(nodeCount: Number, root: Number, childrenOf: fn(key: Number): Number[]): EulerTour
```

**返回类型**：[`EulerTour`](../../../types.md#api-cd53273398ddc932fa34)

**参数**：nodeCount 节点键上界；有效键是 [0, nodeCount) 内的整数。

**参数**：root 根键；nodeCount 为零时忽略。

**参数**：childrenOf 返回给定键的直接子节点键数组；不保留返回的数组。

**返回值**：可按位置查询节点和深度、按节点查询首次位置的游走。

**失败与异常**：节点数、根键或子键非法，或同一键从根被到达多次时抛出 SubtreeIntervalError。

### 示例：找到子节点首次出现的位置

```el
let children: Number[][] = @[@[1, 2], @[], @[]]
let tour = euler_tour(3, 0, (key: Number): Number[] => children[key])
console.stdout.writeLine(tour.first(2))
```
```text
3
```
