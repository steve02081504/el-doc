# queries/source-syntax.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/queries.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 查询源码语法 {#api-c840849616548d863be6}

源码：`src/stdlib/queries/source-syntax.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/queries/source-syntax.el#L17)

将 query 表达式解析为经过类型检查的有限查询执行计划。

## query {#api-284dc65ab75a83659889}

源码：`src/stdlib/queries/source-syntax.el:432` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/queries/source-syntax.el#L432)

使用声明式子句定义有类型的有限查询。
查询输入仅接受受支持的数组或强类型 Source；过滤和排序表达式须符合对应类型合同。

```el-signature
export syntax query
```

### 示例：查询偶数项并映射字段

```el
// @external values: Number[]
let result = query() {
	from value in values
	where value % 2 == 0
	select value
}
```
