# multimedia/capture/binary.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 多媒体二进制缓冲区 {#api-2094845b17e849d7f613}

源码：`src/stdlib/multimedia/capture/binary.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/binary.el#L1)

提供媒体载荷缓冲区的字节读写、复制与标签辅助函数。

## put {#api-63ad5caf77920fa2e7b1}

源码：`src/stdlib/multimedia/capture/binary.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/binary.el#L31)

将数值按小端字节序写入原生缓冲区；调用者负责提供有效缓冲区及足够空间。

```el-signature
export fn put(data: ptr, at: Number, value: Number, width: Number)
```

**参数**：data 写入目标地址。

**参数**：at 起始字节偏移。

**参数**：value 要写入的非负数值。

**参数**：width 写入字节数。

### 示例：写入一个四字节值

```el
// @external data: ptr
put(data, 0, 305419896, 4)
```
