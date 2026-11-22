# database/source-syntax.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/database.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数据库查询语法 {#api-dba5b367fde6beac97a5}

源码：`src/stdlib/database/source-syntax.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/source-syntax.el#L1)

解析并检查依赖数据库行类型的查询，生成可准备和执行的查询模板。

## query {#api-703451589618b8e34ad1}

源码：`src/stdlib/database/source-syntax.el:1380` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/source-syntax.el#L1380)

用原生数据库源构造可执行的查询模板。查询至少有一个来源，可在投影前筛选、联接或分组。

```el-signature
export syntax query
```

### 示例：从调用方提供的数据库源投影标识符

```el
// @external source: NativeSource<row: QueryExampleRow>, QueryExampleRow: type
import { query } from "el:database/"
let identifiers = query { from person in $(source) select person.id }
```
