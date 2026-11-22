# network/bytes.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/network.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 网络字节转换 {#api-5128f1370300914a14bf}

源码：`src/stdlib/network/bytes.el:12` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/bytes.el#L12)

在文本、字节数组和缓冲区之间转换网络数据。

## encodeUtf8 {#api-c49ddb5bb423584fbb6a}

源码：`src/stdlib/network/bytes.el:43` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/bytes.el#L43)

将文本编码为 UTF-8 字节数组。

```el-signature
export fn encodeUtf8(text: Text): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：text 要编码的文本。

**返回值**：按 UTF-8 编码顺序排列且每项在 0 到 255 范围内的字节。

### 示例：编码文本

```el
let bytes = encodeUtf8("hello")
```
