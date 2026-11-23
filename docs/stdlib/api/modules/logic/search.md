# logic/search.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [GroundCursor.next](#api-9a2563bdfb8e857f0b0f)
- [SearchCursor.next](#api-d6a4b9be8fcbef392bec)

## 逻辑搜索计划与游标 {#api-9d1814bb150c9a4284a6}

源码：`src/stdlib/logic/search.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L19)

将规则快照和查询准备为可复用搜索计划，并通过游标逐项获取答案或完整地面项。

## PreparedSearch {#api-903be40199787b3f4b1f}

源码：`src/stdlib/logic/search.el:568` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L568)

持有已准备的不可变规则快照及查询，可创建答案游标或地面答案游标。

```el-signature
export @assign(mode: "shared") class PreparedSearch
```

### 示例：创建地面答案游标

```el
// @external plan: PreparedSearch
let cursor = plan.ground().iterator()
let step = cursor.next()
```

## GroundSearch {#api-7a238a9cc648b83300d3}

源码：`src/stdlib/logic/search.el:841` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L841)

将 PreparedSearch 的答案按需转换为必须无逻辑变量的地面 Term。

```el-signature
export @assign(mode: "shared") class GroundSearch
```

### 示例：枚举地面结果

```el
// @external plan: PreparedSearch
let cursor = plan.ground().iterator()
let step = cursor.next()
```

## GroundCursor {#api-5942ab836ae0713bf70d}

源码：`src/stdlib/logic/search.el:860` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L860)

按需返回 GroundSearch 的地面项结果；完成时返回 done 标记。

```el-signature
export @assign(mode: "shared") class GroundCursor
```

### 示例：逐个读取地面结果

```el
// @external plan: PreparedSearch, consume: fn(value: Term): nil_t
let cursor = plan.ground().iterator()
let step = cursor.next()
if (!step.done) consume(step.value)
```

## GroundCursor.next {#api-9a2563bdfb8e857f0b0f}

源码：`src/stdlib/logic/search.el:886` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L886)

继续搜索并返回下一项地面 Term；耗尽时返回 done 步骤。

```el-signature
fn next(): IterationStep<element: Term>
```

**返回类型**：[`IterationStep`](../../types.md#api-e4b3e3cc13c7cec14564)<element: [`Term`](term.md#api-7560e808aaee9c6517d2)>

**返回值**：包含地面 Term 的迭代步骤，或表示结束的步骤。

**失败与异常**：搜索中断或答案含未绑定逻辑变量时抛出错误。

### 示例：迭代一个结果（使用类示例中的 cursor）

```el
// @external consume: fn(value: Term): nil_t
let step = cursor.next()
if (!step.done) consume(step.value)
```

## SearchCursor {#api-09b5771e54c5c1923052}

源码：`src/stdlib/logic/search.el:903` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L903)

逐项推进逻辑搜索的游标。提前停止读取时，可用 `close()` 释放搜索会话。

```el-signature
export @assign(mode: "shared") class SearchCursor
```

### 示例：从搜索计划打开游标

```el
// @external plan: PreparedSearch
let cursor = plan.iterator()
```

## SearchCursor.next {#api-d6a4b9be8fcbef392bec}

源码：`src/stdlib/logic/search.el:966` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/search.el#L966)

推进搜索并返回下一项结果。没有下一项时返回 `done`。推进期间发生的搜索中断会向调用者传播。

```el-signature
fn next(): IterationStep<element: Answer>
```

**返回类型**：[`IterationStep`](../../types.md#api-e4b3e3cc13c7cec14564)<element: [`Answer`](../../types.md#api-4e552bfbd023969638c0)>

### 示例：读取一个搜索结果

```el
// @external searchCursor: SearchCursor
let step = searchCursor.next()
```
