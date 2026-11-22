# neural-networks/text/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 语言模型文本接口 {#api-7fd4ad34016e169a14da}

源码：`src/stdlib/neural-networks/text/index.el:8` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/index.el#L8)

汇总文本模型、分词器、检查点与生成接口，并提供显式宿主读取边界。

## generateText {#api-4cef645bf57c84498b12}

源码：`src/stdlib/neural-networks/text/index.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/index.el#L51)

对文本提示执行自回归生成，并使用 tokenizer 解码令牌。`readHost` 是显式的设备到主机边界，负责从当前模型输出中读取最后一个序列位置的词表 logits；缓存隔离、取消轮询和逐令牌通知遵循 `generateTokens` 的合同。

```el-signature
export fn generateText(model, tokenizer, prompt: Text, readHost, options: GenerationOptions = GenerationOptions(), cancelled = fn() { return f }, onToken = fn(token, snapshot) {})
```

**参数**：model 提供 prefill/decode 行为的因果语言模型实例。

**参数**：tokenizer 提供 `encode`、`decode`、`bosId` 和令牌元数据的 tokenizer。

**参数**：prompt 输入文本；若 tokenizer 有 BOS 令牌则在编码时添加。

**参数**：readHost 将当前 logits 转成扁平主机标量数组的显式回调。

**参数**：options 生成与采样选项。

**参数**：cancelled 在生成步骤边界查询是否取消。

**参数**：onToken 每提交一个令牌后接收令牌和隔离的生成快照。

**返回值**：生成结果及停止原因。

### 示例：生成需要宿主读取回调的模型上下文

```el
// @external model, tokenizer, readHost
// 调用上下文需提供 model、tokenizer，以及按模型存储布局读取末位置 logits 的 readHost 回调。
let result = generateText(model, tokenizer, "你好", readHost)
```
示例为调用上下文片段，不代表可独立运行；示例未运行验证。
