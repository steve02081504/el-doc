# network/sockets.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/network.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 网络套接字 {#api-5aa5e78a4ebdaed3e2cd}

源码：`src/stdlib/network/sockets.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/sockets.el#L1)

提供 TCP 连接、监听和 UDP 套接字接口。

## connectTcp {#api-9e19203d508cfc9d0fcd}

源码：`src/stdlib/network/sockets.el:187` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/sockets.el#L187)

连接到指定主机和 TCP 端口，并返回连接对象。

```el-signature
export fn connectTcp(host: Text, port: Number, timeout: Number = 30000): TcpConnection
```

**返回类型**：[`TcpConnection`](../../types.md#api-1090d8149506627ae338)

**参数**：host 主机名或数值地址。

**参数**：port 目标端口。

**参数**：timeout 连接超时毫秒数。

**返回值**：已连接的 TcpConnection；调用方负责关闭连接。

**失败与异常**：地址解析、连接或超时失败时抛出网络异常。

### 示例：连接到可访问的服务并关闭连接

```el
import { connectTcp } from "el:network/"
// 将地址与端口替换为正在监听的服务。
let connection = connectTcp("127.0.0.1", 443)
try {
	connection.send(@[72, 105])
} finally {
	connection.close()
}
```

## listenTcp {#api-6bb0a5a15cfb7ecef1a9}

源码：`src/stdlib/network/sockets.el:271` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/sockets.el#L271)

在指定地址创建 TCP 监听器；端口 0 由系统选择可用端口。

```el-signature
export fn listenTcp(host: Text = "127.0.0.1", port: Number = 0, backlog: Number = 64): TcpListener
```

**返回类型**：[`TcpListener`](../../types.md#api-b10a4f9710e5ae8987a1)

**参数**：host 绑定主机名或地址，默认仅监听回环地址。

**参数**：port 绑定端口，取值为 0 到 65535。

**参数**：backlog 连接等待队列长度，取值为 1 到 65535。

**返回值**：可接受 TCP 连接并可关闭的监听器。

**失败与异常**：地址解析、绑定或监听失败时抛出 NetworkError。

### 示例：在回环地址选择空闲端口

```el
let listener = listenTcp()
```
