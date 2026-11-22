# compiler/proof/term.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/compiler.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 证明核心项 {#api-13ad5d413a185aaf62bc}

源码：`src/stdlib/compiler/proof/term.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/term.el#L1)

提供证明核项的构造函数。

## proof_sort {#api-667d64d582cac9f0f2ce}

源码：`src/stdlib/compiler/proof/term.el:129` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/term.el#L129)

构造指定数字层级的 Sort 项；层级 0 表示 Prop。

```el-signature
export fn proof_sort(level: Number): ProofTerm
```

**返回类型**：[`ProofTerm`](../../../types.md#api-0bc5b5a33724ea9be521)

### 示例：构造 Prop

```el
import { proof_sort } from "el:compiler/proof/term.el"
let propositionSort = proof_sort(0)
```

## proof_constant {#api-cd0dce69eb7ed98f96cd}

源码：`src/stdlib/compiler/proof/term.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/term.el#L142)

构造按名称引用声明的常量项。

```el-signature
export fn proof_constant(name: Text): ProofTerm
```

**返回类型**：[`ProofTerm`](../../../types.md#api-0bc5b5a33724ea9be521)

### 示例：引用常量

```el
import { proof_constant } from "el:compiler/proof/term.el"
let proposition = proof_constant("P")
```

## proof_pi {#api-b37052d536b90ae3014d}

源码：`src/stdlib/compiler/proof/term.el:219` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/term.el#L219)

从参数类型与项体构造依赖函数类型项。

```el-signature
export fn proof_pi(domain: ProofTerm, body: ProofTerm): ProofTerm
```

**返回类型**：[`ProofTerm`](../../../types.md#api-0bc5b5a33724ea9be521)

### 示例：构造函数类型

```el
import { proof_pi, proof_constant } from "el:compiler/proof/term.el"
let functionType = proof_pi(proof_constant("P"), proof_constant("Q"))
```
