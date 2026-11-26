# mathematics/proof/logic.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 命题联结词 {#api-ed73e208afe484ff7cb1}

源码：`src/stdlib/mathematics/proof/logic.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/proof/logic.el#L1)

提供合取、析取、等价及其引入和消去规则。

## And {#api-9556cb62a74531299a24}

源码：`src/stdlib/mathematics/proof/logic.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/proof/logic.el#L18)

合取命题的证据包含左右两个命题各自的证据。

```el-signature
export data And<P: Prop, Q: Prop>: Prop
```

### 示例：使用 And

```el
import { And } from "el:mathematics/proof/logic.el"
import { Prop } from "el:language/proofs.el"
fn keep(P: Prop, Q: Prop, evidence: And(P, Q)): And(P, Q) => evidence
```
