# numerical-computing/tensor-file.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数位张量文件 {#api-89ef68a7104cc90d43f0}

源码：`src/stdlib/numerical-computing/tensor-file.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor-file.el#L1)

保存稠密张量的形状及精确数值或目标浮点表示。

## TensorFileFormat {#api-4cd178cbcee51ab32c4a}

源码：`src/stdlib/numerical-computing/tensor-file.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor-file.el#L33)

构造可传给 readFileAs 和 writeFileAs 的稠密张量文件格式，默认使用目标数位基数。

```el-signature
export fn TensorFileFormat(element: type): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：element 张量的精确数值或 DitFloat 元素类型。

**返回值**：接受可选 radix 和 inputLimit 构造参数的格式类型。

### 示例：保存精确数值张量

```el
import { Tensor, TensorFileFormat } from "el:numerical-computing/"
let Dense = Tensor<element: Number>
let Format = TensorFileFormat<element: Number>
let data = Format().encode(Dense(@[2], @[1/3, 2/3]))
```
