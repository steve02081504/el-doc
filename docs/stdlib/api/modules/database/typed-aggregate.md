# database/typed-aggregate.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/database.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数据聚合 {#api-edd2d37a0c8e9d7fafb3}

源码：`src/stdlib/database/typed-aggregate.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/typed-aggregate.el#L4)

对有限行集合执行计数、数值聚合和有序极值选择。

## count {#api-0280cb5fc9d8aaea0053}

源码：`src/stdlib/database/typed-aggregate.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/typed-aggregate.el#L20)

返回行集合中的行数，包括字段值为 nil 的行。

```el-signature
export fn count(rows: any): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：rows 支持 count 属性的有限行集合。

**返回值**：行集合的行数。

### 示例：统计记录数（rows 是已有的行集合）

```el
// @external rows
let total = count(rows)
```
