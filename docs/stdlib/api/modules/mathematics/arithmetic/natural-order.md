# mathematics/arithmetic/natural-order.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 归纳自然数的序 {#api-edc154ec5ecf4ad59056}

源码：`src/stdlib/mathematics/arithmetic/natural-order.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural-order.el#L1)

定义大小关系、序引理和线性算术证明所用的规则。

## Le {#api-67278193356d441cf5be}

源码：`src/stdlib/mathematics/arithmetic/natural-order.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural-order.el#L27)

表示左端加上某个自然数后等于右端。

```el-signature
export fn Le(left: Nat, right: Nat): Prop
```

**返回类型**：[`Prop`](../../language/proofs.md#api-a376131941dc82f3eb3f)

### 示例：使用 Le

```el
import { Le } from "el:mathematics/arithmetic/natural-order.el"
import { Nat } from "el:mathematics/arithmetic/natural.el"
fn keep(a: Nat, b: Nat, h: Le(a, b)): Le(a, b) => h
```

## nat_arithmetic_rules {#api-2448c87e5840d363d406}

源码：`src/stdlib/mathematics/arithmetic/natural-order.el:180` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/arithmetic/natural-order.el#L180)

提供自然数序的偏移抵消、提升、传递和加一规则。启用 `naturalOrderNotation` 后可在自然数目标上用裸 `arith`。

```el-signature
export fn nat_arithmetic_rules(): ((cancel_order_shift() & (lift_order_shift() & (weaken_order_bound() & compose_order_bounds()))) & add_unit_offset())
```

**返回类型**：((`cancel_order_shift`() & (`lift_order_shift`() & (`weaken_order_bound`() & `compose_order_bounds`()))) & `add_unit_offset`())

未解析：`cancel_order_shift`、`lift_order_shift`、`weaken_order_bound`、`compose_order_bounds`、`add_unit_offset`

### 示例：使用 nat_arithmetic_rules

```el
import { nat_arithmetic_rules } from "el:mathematics/arithmetic/natural-order.el"
let rules = nat_arithmetic_rules()
```
