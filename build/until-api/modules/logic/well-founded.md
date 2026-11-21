# logic/well-founded.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## WellFoundedTable {#api-f64e03ca1939d841cce2}

源码：`src/stdlib/logic/well-founded.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/well-founded.el#L96)

在有限的 TableRule 程序上显式启用良基语义；不改变默认表的两值语义。

```el
export @assign(mode: "shared") class WellFoundedTable
```

### 示例：负自环是未知，不是假

```el
let p = atom("p")
let table = WellFoundedTable(@[], @[TableRule(p, @[], @[p])])
let result = table.truth(p) // WellFoundedTruth.Undefined
```
