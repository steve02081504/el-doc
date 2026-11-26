# mathematics/notation/natural-order.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 自然数序记号 {#api-b94dd129233fada23233}

源码：`src/stdlib/mathematics/notation/natural-order.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/natural-order.el#L1)

自然数的序、命题不等和算术证明。各关系和定律组由导入记号包的模块提供。

## naturalOrderNotation {#api-754f1339c1a9ffd0f872}

源码：`src/stdlib/mathematics/notation/natural-order.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/natural-order.el#L16)

用 ASCII 或数学符号写自然数的序与不等，并为裸 `arith` 选定自然数算术规则。

```el-signature
export syntax naturalOrderNotation
```

### 示例：抵消不等式两边的加一

```el
import { Nat, add, nat_one } from "el:mathematics/arithmetic/natural.el"
import { Le, nat_arithmetic_rules } from "el:mathematics/arithmetic/natural-order.el"
import { naturalNotation } from "el:mathematics/notation/natural.el"
import { naturalOrderNotation } from "el:mathematics/notation/natural-order.el"
fn cancelAddOne((a, b): Nat, h: a + 1 <= b + 1): a <= b => prove { arith }
```
