# network/http/wire.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/network.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## HTTP 线协议读取 {#api-b080b198ca5ff984c0d2}

源码：`src/stdlib/network/http/wire.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/wire.el#L18)

缓冲读取 HTTP 响应头与消息体所需的线协议字节。

## HttpWireReader {#api-5856ea17e3ac530bb530}

源码：`src/stdlib/network/http/wire.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/wire.el#L33)

管理 HTTP 连接的缓冲字节读取和单次操作超时期限。

```el-signature
export class HttpWireReader
```

**参数**：connection 提供接收操作的字节连接。

**参数**：timeout 读取期限，单位为毫秒。

**失败与异常**：读取超过期限或消息被截断时抛出 NetworkError。

### 示例：为连接创建线读取器

```el
// @external connection: ByteConnection
let reader = HttpWireReader(connection, 30000)
```
