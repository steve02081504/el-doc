# compiler/proof/work.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/compiler.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 证明核工作预算 {#api-ba6fa8e068b316a702d3}

源码：`src/stdlib/compiler/proof/work.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/work.el#L1)

提供证明检查的工作预算及取消控制。

## ProofBudget {#api-294098eebbd742684492}

源码：`src/stdlib/compiler/proof/work.el:32` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/work.el#L32)

证明核共享的工作预算，可选限制步数和取消令牌；耗尽或取消表示检查未决。

```el-signature
export @assign(mode: "shared") class ProofBudget
```

### 示例：创建无限步数预算

```el
import { ProofBudget } from "el:compiler/proof/work.el"
let budget = ProofBudget()
```
