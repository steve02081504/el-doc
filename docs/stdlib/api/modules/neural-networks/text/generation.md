# neural-networks/text/generation.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 令牌生成 {#api-de47978321759e4fea1e}

源码：`src/stdlib/neural-networks/text/generation.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/generation.el#L6)

定义生成选项、结果及带采样和缓存隔离合同的令牌解码循环。

## GenerationOptions {#api-2303e0907642e9bc866e}

源码：`src/stdlib/neural-networks/text/generation.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/generation.el#L36)

配置令牌生成长度、采样、重复惩罚和令牌过滤。温度为零使用贪心选择且不推进随机状态；`topK: 0` 关闭 top-k 截断，`topP: 1` 保留全部候选概率质量。令牌列表在构造时复制。

```el-signature
export @assign(mode: "copy") class GenerationOptions
```

**参数**：maxNewTokens 最多生成的令牌数，默认 32。

**参数**：contextLimit 提示与生成内容的总上下文上限，默认 2048。

**参数**：temperature 采样温度，零表示贪心解码。

**参数**：topK 保留的最高分候选数，零表示不限制。

**参数**：topP 核采样概率阈值，范围为 `(0, 1]`。

**参数**：repetitionPenalty 重复令牌的分数惩罚，必须为正数。

**参数**：eosTokens 遇到即停止的令牌 ID。

**参数**：forbiddenTokens 不参与采样的令牌 ID。

**参数**：randomState 可复现采样的初始随机状态。

### 示例：配置短的贪心生成

```el
import { GenerationOptions } from "el:neural-networks/index.el"
let options = GenerationOptions(maxNewTokens: 16, contextLimit: 256, temperature: 0)
```
生成时还会按 logits 词表检查令牌 ID；示例未运行验证。
