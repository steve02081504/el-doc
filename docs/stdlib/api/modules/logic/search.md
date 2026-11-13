# logic/search.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [GroundCursor.next](#api-9a2563bdfb8e857f0b0f)

## 逻辑搜索计划与游标 {#api-9d1814bb150c9a4284a6}

源码：`src/stdlib/logic/search.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L19)

将规则快照和查询准备为可复用搜索计划，并通过游标逐项获取答案或完整地面项。

## PreparedSearch {#api-903be40199787b3f4b1f}

源码：`src/stdlib/logic/search.el:567` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L567)

```el
export @assign(mode: "shared") class PreparedSearch
```

持有已准备的不可变规则快照及查询，可创建答案游标或地面答案游标。

### 示例：创建地面答案游标

```el
let cursor = plan.ground().iterator()
let step = cursor.next()
```

## GroundSearch {#api-7a238a9cc648b83300d3}

源码：`src/stdlib/logic/search.el:842` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L842)

```el
export @assign(mode: "shared") class GroundSearch
```

将 PreparedSearch 的答案按需转换为必须无逻辑变量的地面 Term。

### 示例：枚举地面结果

```el
let cursor = plan.ground().iterator()
let step = cursor.next()
```

## GroundCursor {#api-5942ab836ae0713bf70d}

源码：`src/stdlib/logic/search.el:859` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L859)

```el
export @assign(mode: "shared") class GroundCursor
```

按需返回 GroundSearch 的地面项结果；完成时返回 done 标记。

### 示例：逐个读取地面结果

```el
let step = cursor.next()
if (!step.done) consume(step.value)
```

## GroundCursor.next {#api-9a2563bdfb8e857f0b0f}

源码：`src/stdlib/logic/search.el:884` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L884)

```el
fn next(): IterationStep<element: Term>
```

**返回类型**：[`IterationStep`](../../types.md#api-e4b3e3cc13c7cec14564)<element: [`Term`](term.md#api-7560e808aaee9c6517d2)>

继续搜索并返回下一项地面 Term；耗尽时返回 done 步骤。

**返回值**：包含地面 Term 的迭代步骤，或表示结束的步骤。

**失败与异常**：搜索中断或答案含未绑定逻辑变量时抛出错误。

### 示例：迭代一个结果

```el
let step = cursor.next()
if (!step.done) consume(step.value)
```
