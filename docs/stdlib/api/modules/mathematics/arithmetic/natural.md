# mathematics/arithmetic/natural.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 归纳自然数 {#api-35b6ca167bc5f3669d62}

源码：`src/stdlib/mathematics/arithmetic/natural.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L1)

定义零、后继和按构造子递归的算术，并给出相关等式证明。

## Nat {#api-458aaf661a17a47f63c0}

源码：`src/stdlib/mathematics/arithmetic/natural.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L18)

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

## nat_one {#api-ced70b0586538468598a}

源码：`src/stdlib/mathematics/arithmetic/natural.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L27)

返回归纳自然数一。启用 `naturalNotation` 时，注解里的 `1` 展开为此调用。

```el-signature
export fn nat_one(): Nat
```

**返回类型**：[`Nat`](natural.md#api-458aaf661a17a47f63c0)

### 示例：使用 nat_one

```el
import { nat_one } from "el:mathematics/arithmetic/natural.el"
let unit = nat_one()
```

## add {#api-214ecee2ae229fe3d934}

源码：`src/stdlib/mathematics/arithmetic/natural.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural.el#L36)

按左端的构造子递归求两个自然数的和。

```el-signature
export fn add(left: Nat, right: Nat): Nat
```

**返回类型**：[`Nat`](natural.md#api-458aaf661a17a47f63c0)

### 示例：使用 add

```el
import { Nat, add } from "el:mathematics/arithmetic/natural.el"
let sum = add(Nat.zero(), Nat.succ(Nat.zero()))
```
