# neural-networks/text/config.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 因果语言模型配置 {#api-5d1f7793206913bb8deb}

源码：`src/stdlib/neural-networks/text/config.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/config.el#L4)

定义解码器结构、参数布局与配置编码校验。

## DecoderConfig {#api-421a6ec1d0a5c1f04046}

源码：`src/stdlib/neural-networks/text/config.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/config.el#L25)

描述因果解码器的词表、层宽、注意力、前馈网络、位置编码和参数布局选项。构造时检查尺寸、头数关系、支持的枚举值及数值参数；`keyValueHeads: 0` 表示使用与 `heads` 相同的头数。

```el-signature
export @assign(mode: "copy") class DecoderConfig
```

**参数**：vocabulary 词表大小，默认 259（特殊令牌与字节令牌所需的最小词表）。

**参数**：width 隐藏宽度。

**参数**：layers Transformer 层数。

**参数**：heads 查询注意力头数，必须整除 `width`。

**参数**：hidden 前馈网络宽度。

**参数**：context 最大上下文长度。

**参数**：keyValueHeads 键和值头数，必须整除查询头数。

### 示例：创建一个小型解码器配置

```el
import { DecoderConfig } from "el:neural-networks/index.el"
let config = DecoderConfig(vocabulary: 300, width: 32, layers: 2, heads: 4, hidden: 64, context: 128)
```
参数范围和组合由构造器校验；示例未运行验证。
