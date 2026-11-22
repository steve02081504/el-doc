# text/byte-array.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/text.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文本字节数组 {#api-6e6efb93901c56bf0de3}

源码：`src/stdlib/text/byte-array.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/byte-array.el#L1)

文本字节数组相关接口。

## text_bytes {#api-17daf00360d0a4c676a9}

源码：`src/stdlib/text/byte-array.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/byte-array.el#L14)

复制文本的编码字节到新数组。

```el-signature
export fn text_bytes(text: Text): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：使用示例

```el
import { text_bytes } from "el:text/byte-array"
let bytes = text_bytes("hello")
```
