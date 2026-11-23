# database/table.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/database.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数据库表定义 {#api-18a38e20f506824673c0}

源码：`src/stdlib/database/table.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/table.el#L14)

以 EL 原生类型、列定义和主键描述数据库表。

## DbColumnDefinition {#api-4c3e6ac827cdd538a56e}

源码：`src/stdlib/database/table.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/table.el#L30)

描述表中的一列及其数据库类型和可空性。

```el-signature
export class DbColumnDefinition
```

**参数**：name 非空列名。

**参数**：type 原生数据库类型描述。

**参数**：nullable 是否允许缺失值。

**失败与异常**：列名为空或 type 不是 DbType 时抛出 TableDefinition 错误。

### 示例：定义非空文本列

```el
let column = DbColumnDefinition("name", dbTextType())
```

## DbTableDefinition {#api-0629134ecfbe648b9f02}

源码：`src/stdlib/database/table.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/table.el#L56)

描述由列集合和至少一个主键列组成的表。

```el-signature
export class DbTableDefinition
```

**参数**：name 非空表名。

**参数**：columns 非空的列定义数组。

**参数**：primary 至少包含一个已定义列名的主键列数组。

**失败与异常**：表名、列集合或主键不满足要求时抛出 TableDefinition 错误。

### 示例：定义带主键的表

```el
// @external column: DbColumnDefinition
let table = DbTableDefinition("people", @[column], @["name"])
```
