# number/native-float.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## canRepresentExactly {#api-4ba6311e8edff7e59788}

源码：`src/stdlib/number/native-float.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/native-float.el#L75)

判断目标原生浮点类型能否无舍入地表达该有限有理数；目标没有可用的数值编解码器时报 NativeFloatCodecUnavailable。

```el
export fn canRepresentExactly<T: type>(value: NumericRatio): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

### 示例：在使用二进制浮点编解码器的目标上检查二分之一

```el
import { NativeFloatExponent5 } from "el:platform/machine/float-codec.el"
import { NumericRatio } from "el:number/arithmetic.el"
let exact = canRepresentExactly<NativeFloatExponent5>(NumericRatio(1, 2))
console.stdout.writeLine(if (exact) "exact" else "rounded")
```
```text
exact
```
