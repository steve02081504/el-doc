# collections/trees/lca.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 静态树 LCA {#api-35b6e0345531ccea5e77}

源码：`src/stdlib/collections/trees/lca.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/lca.el#L1)

用 Euler 游走和可替换的区间 argmin 后端回答最近公共祖先。

## build {#api-d7bd504f7ed5fa93a3f8}

源码：`src/stdlib/collections/trees/lca.el:70` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/lca.el#L70)

从稳定整数键树建立 LCA 索引；默认使用 ±1 RMQ。

```el-fragment
export fn build(nodeCount: Number, root: Number, childrenOf: fn(key: Number): Number[], rmq: (fn(values: Number[]): fn(lo: Number, hi: Number): Number) | nil_t = nil): TreeLca
```

**返回类型**：[`TreeLca`](../../../types.md#api-e28f9d138e7f53b2d548)

**参数**：nodeCount 节点键上界；有效键是 [0, nodeCount) 内的整数。

**参数**：root 根键；nodeCount 为零时忽略。

**参数**：childrenOf 返回给定键的直接子节点键数组；不保留返回的数组。

**参数**：rmq 可选后端构造器：接收 Euler 深度快照，返回 [lo, hi) 内最小深度的最左下标；nil 使用 ±1 RMQ。

**返回值**：支持 lca、first、depth 等查询的索引。

**失败与异常**：节点数、根键或子键非法，或同一键从根被到达多次时抛出 SubtreeIntervalError。

### 示例：查询最近公共祖先

```el
let children: Number[][] = @[@[1, 2], @[], @[]]
let tree = build(3, 0, (key: Number): Number[] => children[key])
console.stdout.writeLine(tree.lca(1, 2))
```
