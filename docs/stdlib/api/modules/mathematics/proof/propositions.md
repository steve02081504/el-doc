# mathematics/proof/propositions.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 否定与命题判定 {#api-a631f3539a22c7b5d95a}

源码：`src/stdlib/mathematics/proof/propositions.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/proof/propositions.el#L1)

定义否定和带证据的可判定性，并给出相关推理规则。

## Not {#api-e16c408c9adec6467f0b}

源码：`src/stdlib/mathematics/proof/propositions.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/proof/propositions.el#L16)

把命题映射为从该命题的证据推出矛盾的函数类型。

```el-signature
export fn Not(P: Prop): Prop
```

**返回类型**：[`Prop`](../../language/proofs.md#api-a376131941dc82f3eb3f)

### 示例：使用 Not

```el
import { Not } from "el:mathematics/proof/propositions.el"
import { Prop } from "el:language/proofs.el"
fn keep(P: Prop, evidence: Not(P)): Not(P) => evidence
```
