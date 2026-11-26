# mathematics/notation/equality.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 相等记号 {#api-be69ab809a3672cf2859}

源码：`src/stdlib/mathematics/notation/equality.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/equality.el#L1)

命题相等。Eq 由导入记号包的模块提供。

## equalityNotation {#api-c0502b469cf6048b4813}

源码：`src/stdlib/mathematics/notation/equality.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/equality.el#L15)

用 `(a = b)` 或 `a == b` 写命题相等。使用模块提供 `Eq`。

```el-signature
export syntax equalityNotation
```

### 示例：在签名中写自然数等式

```el
import { Eq } from "el:language/proofs.el"
import { Nat } from "el:mathematics/arithmetic/natural.el"
import { equalityNotation } from "el:mathematics/notation/equality.el"
fn same(value: Nat): (value = value) => prove { refl }
```
