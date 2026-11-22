# compiler/proof/kernel.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/compiler.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 证明核环境 {#api-a776cf5d92997e67e2f5}

源码：`src/stdlib/compiler/proof/kernel.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/kernel.el#L1)

提供声明环境及证明项检查。

## KernelEnvironment {#api-8e328cd33d4187104a5b}

源码：`src/stdlib/compiler/proof/kernel.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/proof/kernel.el#L47)

保存证明声明并执行核心项类型检查的环境。

```el-signature
export @assign(mode: "shared") class KernelEnvironment
```

### 示例：创建环境

```el
import { KernelEnvironment } from "el:compiler/proof/kernel.el"
let kernel = KernelEnvironment()
```
