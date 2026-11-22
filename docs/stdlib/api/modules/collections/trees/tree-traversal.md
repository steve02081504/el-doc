# collections/trees/tree-traversal.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 树 DFS 事件 {#api-108a986f533e2a4ab6b0}

源码：`src/stdlib/collections/trees/tree-traversal.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/tree-traversal.el#L1)

用非递归事件栈遍历稳定整数键的根可达树。

## SubtreeIntervalError {#api-cb7126c5c995ac3f2f87}

源码：`src/stdlib/collections/trees/tree-traversal.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/tree-traversal.el#L15)

树索引遍历的输入契约失败；子树区间与 Euler 游走共享此错误。

```el-fragment
@assign(mode: "copy")
export class SubtreeIntervalError extends Error
```

### 示例：构造一个树索引错误

```el
let error = SubtreeIntervalError("node key out of range")
throw error
```

## tree_node_count {#api-a1b0b41129f878566799}

源码：`src/stdlib/collections/trees/tree-traversal.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/tree-traversal.el#L39)

校验并返回树索引的节点键上界。

```el-fragment
export fn tree_node_count(count: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**失败与异常**：不是非负有限整数时抛出 SubtreeIntervalError。

### 示例：校验三个节点

```el
console.stdout.writeLine(tree_node_count(3))
```
```text
3
```

## tree_node_key {#api-448ba0c99e25940c7132}

源码：`src/stdlib/collections/trees/tree-traversal.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/tree-traversal.el#L51)

校验并返回 [0, count) 内的稳定整数节点键。

```el-fragment
export fn tree_node_key(key: Number, count: Number): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**失败与异常**：键非法时抛出 SubtreeIntervalError。

### 示例：校验最后一个有效键

```el
console.stdout.writeLine(tree_node_key(2, 3))
```
```text
2
```

## tree_dfs_events {#api-1e880ea408abc13e01b7}

源码：`src/stdlib/collections/trees/tree-traversal.el:76` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/trees/tree-traversal.el#L76)

用迭代事件栈遍历根可达的稳定整数键树；进入和退出各报告一次。
事件顺序保证先报告父节点的进入、再报告其子节点事件，最后报告父节点的退出。

```el-fragment
export fn tree_dfs_events(count: Number, root: Number, childrenOf: fn(key: Number): Number[], visit: fn(key: Number, parent: Number, entering: Bool): nil_t): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：count 节点键上界；有效键是 [0, count) 内的整数。

**参数**：root 根键；count 为零时不调用回调，也不检查根键。

**参数**：childrenOf 返回给定键的直接子节点键数组；不保留返回的数组。

**参数**：visit 接收 (key, parent, entering)；根节点的 parent 是 -1。

**返回值**：根可达节点数。

**失败与异常**：节点数、根键或子键非法，或同一键从根被到达多次时抛出 SubtreeIntervalError。

### 示例：按访问顺序打印进入事件

```el
let children: Number[][] = @[@[1], @[]]
let count = tree_dfs_events(2, 0, (key: Number): Number[] => children[key], (key: Number, parent: Number, entering: Bool): nil_t => {
	if (entering) console.stdout.writeLine(key)
	return nil
})
console.stdout.writeLine(count)
```
```text
0
1
2
```
