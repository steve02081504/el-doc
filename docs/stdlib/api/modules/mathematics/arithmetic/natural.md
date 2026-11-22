# mathematics/arithmetic/natural.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 归纳自然数 {#api-35b6ca167bc5f3669d62}

源码：`src/stdlib/mathematics/arithmetic/natural.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L1)

定义零、后继和按构造子递归的算术，并给出相关等式证明。

## Nat {#api-458aaf661a17a47f63c0}

源码：`src/stdlib/mathematics/arithmetic/natural.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L15)

归纳自然数，构造子为零与后继。可以按构造子递归定义函数并证明性质。

```el-signature
export data Nat: Type(0)
```

### 示例：构造零与它的后继

```el
import { Nat } from "el:mathematics/arithmetic/natural.el"
let origin = Nat.zero()
let successor = Nat.succ(origin)
```
