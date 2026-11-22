# foreign-functions/target-facts.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/foreign-functions.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 外部调用目标事实 {#api-e2842ef082719537843a}

源码：`src/stdlib/foreign-functions/target-facts.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/target-facts.el#L1)

外部调用目标事实相关接口。

## AbiTarget {#api-ad1bc7df9299595e64c8}

源码：`src/stdlib/foreign-functions/target-facts.el:12` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/target-facts.el#L12)

枚举外部调用 ABI 目标；Unsupported 表示没有受支持的目标。

```el-signature
export enum AbiTarget
```

### 示例：用法

```el
import { AbiTarget } from "el:foreign-functions/target-facts.el"
let target = AbiTarget.SysVAmd64
```

## TargetFacts {#api-eeac3c8c2e6e330ab31f}

源码：`src/stdlib/foreign-functions/target-facts.el:26` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/target-facts.el#L26)

描述 ABI 目标、寻址单元和指针宽度及字节序。构造时检查已支持的目标布局，目前要求小端和 8 位寻址单元。

```el-signature
@assign(mode: "shared")
export class TargetFacts
```

### 示例：用法

```el
import { AbiTarget, TargetFacts } from "el:foreign-functions/target-facts.el"
let facts = TargetFacts(AbiTarget.SysVAmd64, 8, 64)
```
