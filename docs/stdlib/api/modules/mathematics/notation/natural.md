# mathematics/notation/natural.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 自然数算术记号 {#api-7f3672822953ceeacf18}

源码：`src/stdlib/mathematics/notation/natural.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/natural.el#L1)

自然数算术。Nat、nat_one、add、mul 和 pow 由导入记号包的模块按需提供。

## naturalNotation {#api-04468304dfcfd127cef5}

源码：`src/stdlib/mathematics/notation/natural.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/notation/natural.el#L16)

在注解和证明中用自然数字面量、后继、加法、乘法和乘方记号。

```el-signature
export syntax naturalNotation
```

### 示例：在等式里写自然数加法

```el
import { Eq } from "el:language/proofs.el"
import { Nat, add } from "el:mathematics/arithmetic/natural.el"
import { equalityNotation } from "el:mathematics/notation/equality.el"
import { naturalNotation } from "el:mathematics/notation/natural.el"
fn zeroPlus(value: Nat): (0 + value = value) => prove { refl }
```
