# logic/table.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## logic/table {#api-23f2767ea466fa08b311}

源码：`src/stdlib/logic/table.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/table.el#L1)

在显式有限活动域上执行分层、范围受限的逻辑规则；规则不接收原生谓词作为全性或单调性证明。
典型用法是以 `TableRule` 描述事实/规则，再交给表格化求解接口执行。

## TableRule {#api-59ef583f88344d472ae5}

源码：`src/stdlib/logic/table.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/table.el#L25)

有限活动域上的规则，包含头部、正向条件和可选的否定条件。

```el-signature
export @assign(mode: "shared") class TableRule
```

**参数**：head 规则头部。

**参数**：body 正向条件。

**参数**：negative 否定条件，变量须由正向条件绑定。

### 示例：创建一条地面事实规则

```el
import { TableRule } from "el:logic/table.el"
let rule = TableRule(atom("ready"), @[])
```
