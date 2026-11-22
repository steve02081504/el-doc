# neural-networks/text/data.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 语言模型训练窗口 {#api-992698720854905284c2}

源码：`src/stdlib/neural-networks/text/data.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/data.el#L4)

将单文档令牌序列切分为带位置、目标与损失掩码的批次。

## LanguageModelWindows {#api-0a1a45f6971031715620}

源码：`src/stdlib/neural-networks/text/data.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/data.el#L49)

将单个文档的令牌序列按上下文长度切分为语言模型批次。构造时复制并校验令牌；不读取文件、不拼接文档，也不自动添加 BOS/EOS。默认步幅等于上下文长度，末尾不足的窗口会用 `padId` 填充并将对应 `lossMask` 置零。

```el-signature
export @assign(mode: "copy") class LanguageModelWindows
```

**参数**：ids 单个已分词文档的令牌 ID。

**参数**：context 每个窗口的输入长度，必须为正数。

**参数**：vocabularySize 有效令牌范围的词表大小。

**参数**：padId 尾部填充令牌，默认 0。

**参数**：stride 窗口起点间隔；零表示使用 `context`。

**参数**：dropTail 是否丢弃没有完整下一令牌目标的尾窗。

**参数**：maxTokens 与 `maxBatchElements` 分别限制保留令牌数和物化批元素数的资源预算。

### 示例：从一篇文档物化窗口

```el
import { LanguageModelWindows } from "el:neural-networks/index.el"
let windows = LanguageModelWindows(@[10, 11, 12, 13], context: 2, vocabularySize: 20)
let first = windows.batch(0, 1)
```
`batch` 的参数是窗口索引和批大小；示例未运行验证。
