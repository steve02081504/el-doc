# neural-networks/text/decoder.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 因果语言模型解码器 {#api-558a0ca8faf38193f7a7}

源码：`src/stdlib/neural-networks/text/decoder.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/decoder.el#L17)

提供按配置构造的自回归 Transformer 模型类型。

## CausalLanguageModel {#api-f1bfef9fe7b41a7e212c}

源码：`src/stdlib/neural-networks/text/decoder.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/decoder.el#L37)

创建因果语言模型类工厂。元素类型、权重存储类型和参数库类型由调用方提供；返回的模型以 `DecoderConfig` 定义结构，并通过调用方传入的上传回调初始化或载入参数。

```el-signature
export fn CausalLanguageModel(element: type, storage: type = Tensor<element: element>, parameterBank: type = ParameterModel<element: element, storage: storage>): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：element 模型运算使用的标量类型。

**参数**：storage 参数所用的存储类型，默认是 `Tensor<element: element>`。

**参数**：parameterBank 参数库类型，默认由 `element` 和 `storage` 构造。

**返回值**：可用 `DecoderConfig` 构造实例的模型类型。

### 示例：选择模型的元素类型

```el
import { CausalLanguageModel } from "el:neural-networks/index.el"
import { Tensor } from "el:numerical-computing/tensor.el"
let Model = CausalLanguageModel<element: Number, storage: Tensor<element: Number>>
```
该示例只展示工厂类型选择，不分配权重或执行推理。
