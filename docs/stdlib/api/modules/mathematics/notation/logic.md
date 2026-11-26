# mathematics/notation/logic.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 命题联结词记号 {#api-f3c35b5ef921afbaea41}

源码：`src/stdlib/mathematics/notation/logic.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/logic.el#L1)

命题联结词。Not、And、Or 和 Iff 由导入记号包的模块提供。

## logicNotation {#api-ff31d9bda8feca8e307d}

源码：`src/stdlib/mathematics/notation/logic.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/logic.el#L16)

用 `&`、`!`、`∧`、`¬`、`∨` 和 `↔` 写命题。使用模块提供所用的联结词。

```el-signature
export syntax logicNotation
```

### 示例：从一个合取中取出左侧证据

```el
import { Prop } from "el:language/proofs.el"
import { And } from "el:mathematics/proof/logic.el"
import { Not } from "el:mathematics/proof/propositions.el"
import { logicNotation } from "el:mathematics/notation/logic.el"
fn first((P, Q): Prop, evidence: P & !Q): P => evidence.left
```
