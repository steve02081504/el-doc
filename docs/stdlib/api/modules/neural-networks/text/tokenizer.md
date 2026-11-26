# neural-networks/text/tokenizer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 字节级 BPE 分词器 {#api-9ca94a2fabf1fb68b980}

源码：`src/stdlib/neural-networks/text/tokenizer.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/tokenizer.el#L17)

提供受资源预算约束的字节对编码训练、编解码与持久化接口。

## trainBytePairTokenizer {#api-408a7f0e6aa9d7ecfdf8}

源码：`src/stdlib/neural-networks/text/tokenizer.el:353` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/tokenizer.el#L353)

使用提供的全部文档训练字节级 BPE 分词器。文档分别编码，不会跨文档合并；词频相同时按令牌对的数值字典序选择。`vocabularySize` 是上限，若没有重复令牌对可合并，实际词表会更小。

```el-signature
export fn trainBytePairTokenizer(texts: Text[], vocabularySize: Number, limits: TextTokenLimits = TextTokenLimits()): BytePairTokenizer
```

**返回类型**：[`BytePairTokenizer`](../../../types.md#api-acac142151ea6ed42b61)

**参数**：texts 用于训练的完整文本语料。

**参数**：vocabularySize 目标词表上限，至少为 259。

**参数**：limits 对输入字节、词表、训练工作量和文档数等资源设置可选预算；超预算会抛出 `InvalidTextTokens`，不会静默截断语料。

**返回值**：训练得到的 `BytePairTokenizer`。

### 示例：训练并编码一个短语料

```el
import { trainBytePairTokenizer } from "el:neural-networks/index.el"
let tokenizer = trainBytePairTokenizer(@["abab", "abab"], 261)
let ids = tokenizer.encode("abab")
```
训练结果取决于完整输入语料和预算；示例未运行验证。
