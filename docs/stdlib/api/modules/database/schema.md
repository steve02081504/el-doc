# database/schema.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/database.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数据库模式 {#api-53648b6c5d4f6ddcc7bd}

源码：`src/stdlib/database/schema.el:8` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/schema.el#L8)

定义原生类型、列、关系模式和带缺失状态的行。

## dbNumberType {#api-2ddbd4fee6a5c3f8f91c}

源码：`src/stdlib/database/schema.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/schema.el#L175)

返回表示 EL Number 的数据库类型描述。

```el-signature
export fn dbNumberType(): DbType
```

**返回类型**：[`DbType`](../../types.md#api-b97251923dea90ac3394)

### 示例：获取数值类型描述

```el
let type = dbNumberType()
```

## dbTextType {#api-b61dd21199ca754c2383}

源码：`src/stdlib/database/schema.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/schema.el#L183)

返回表示 EL Text 的数据库类型描述。

```el-signature
export fn dbTextType(): DbType
```

**返回类型**：[`DbType`](../../types.md#api-b97251923dea90ac3394)

### 示例：获取文本类型描述

```el
let type = dbTextType()
```

## DbRow {#api-d4334f2561d4d10dfa71}

源码：`src/stdlib/database/schema.el:432` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/schema.el#L432)

保存符合关系模式的行值及每个字段是否存在的信息。

```el-signature
export @assign(mode: "copy")
class DbRow
```

**参数**：schema 行对应的关系模式。

**参数**：values 按模式列顺序排列的值。

**参数**：present 可选的存在标记；缺失位置必须对应 nil 值。

**失败与异常**：值数量、存在标记数量或值类型与模式不符时抛出错误。

### 示例：由模式和两个值创建行（schema 是已有的行模式）

```el
// @external schema: DbRelationSchema
let row = DbRow(schema, @[1, "Ada"])
```
