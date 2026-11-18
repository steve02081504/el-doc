# logic/proof-conflict.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## checkProofConflict {#api-ec7f2befb75a09d9dd76}

源码：`src/stdlib/logic/proof-conflict.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/proof-conflict.el#L66)

对传入的正反证据做核检查并分别报告依赖。不自动搜索，也不把搜不到证据当成反证。

```el
export fn checkProofConflict(kernel: KernelEnvironment, proposition: ProofTerm, falseFamily: Text, support: ProofTerm, refutation: ProofTerm, context: ProofTerm[] = @[], universes: Text[] = @[], constraints: SortConstraint[] = @[], budget: ProofBudget = ProofBudget()): ProofConflictReport
```

**返回类型**：[`ProofConflictReport`](../../types.md#api-2cae3cbc98d8b1af88b9)

### 示例：检查显式声明的正反证据并读取各自的公理依赖

```el
import { ProofBudget, KernelEnvironment } from "el:compiler/proof/kernel.el"
import { proof_sort, proof_constant, proof_pi } from "el:compiler/proof/term.el"
import { checkProofConflict } from "el:logic/proof-conflict.el"
let kernel = KernelEnvironment()
let budget = ProofBudget()
kernel.declare_axiom("P", proof_sort(0), budget)
kernel.declare_inductive("Empty", proof_sort(0), 0, @[], budget)
let proposition = proof_constant("P")
kernel.declare_axiom("positive", proposition, budget)
kernel.declare_axiom("negative", proof_pi(proposition, proof_constant("Empty")), budget)
let report = checkProofConflict(kernel, proposition, "Empty", proof_constant("positive"), proof_constant("negative"), budget: budget)
console.stdout.writeLine(report.supportAxioms().includes("positive"))
console.stdout.writeLine(report.refutationAxioms().includes("negative"))
```
