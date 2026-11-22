# collections/trees/subtree-intervals.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 树区间索引 {#api-1ee1d11e23264c68a37a}

源码：`src/stdlib/collections/trees/subtree-intervals.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/subtree-intervals.el#L1)

在共享 DFS 事件骨架上为稳定整数键的树建立子树区间。

## subtree_intervals {#api-37e0a96d3351f37024a3}

源码：`src/stdlib/collections/trees/subtree-intervals.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/subtree-intervals.el#L52)

从根键和直接子键遍历构建子树区间索引。

```el-signature
export fn subtree_intervals(count: Number, root: Number, childrenOf: fn(key: Number): Number[]): SubtreeIntervalIndex
```

**返回类型**：[`SubtreeIntervalIndex`](../../../types.md#api-1eb0061b759a5fb3e533)

**参数**：count 节点键上界；有效键是 [0, count) 内的整数。

**参数**：root 根键；count 为零时忽略。

**参数**：childrenOf 返回给定键的直接子节点键数组；不保留返回的数组。子节点顺序只影响区间编号，不影响祖先关系。

**返回值**：可按祖先关系查询的索引。

**失败与异常**：节点数、根键或子键非法，或同一键从根被到达多次时抛出 SubtreeIntervalError。

### 示例：查询树中的祖先关系

```el
let children: Number[][] = @[@[1, 2], @[], @[]]
let index = subtree_intervals(3, 0, (key: Number): Number[] => children[key])
console.stdout.writeLine(index.contains(0, 2))
```

## subtree_interval_bounds {#api-58102f2d42f76134f8dc}

源码：`src/stdlib/collections/trees/subtree-intervals.el:72` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/subtree-intervals.el#L72)

直接构建调用方拥有的稠密子树区间表，不经索引包装和数组复制。

```el-signature
export fn subtree_interval_bounds(count: Number, root: Number, childrenOf: fn(key: Number): Number[]): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：count 节点键上界；有效键是 [0, count) 内的整数。

**参数**：root 根键；count 为零时忽略。

**参数**：childrenOf 返回给定键的直接子节点键数组；不保留返回的数组。

**返回值**：每个节点两个端点；未索引键保持 [-1,-1)。

**失败与异常**：节点数、根键或子键非法，或同一键从根被到达多次时抛出 SubtreeIntervalError。

### 示例：读取根节点的半开区间

```el
let children: Number[][] = @[@[1], @[]]
let bounds = subtree_interval_bounds(2, 0, (key: Number): Number[] => children[key])
console.stdout.writeLine(bounds[0], ", ", bounds[1])
```
```text
0, 2
```
