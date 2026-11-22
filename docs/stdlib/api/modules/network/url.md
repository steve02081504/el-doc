# network/url.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/network.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 网络 URL {#api-eef9e9324d06f2c1e3d5}

源码：`src/stdlib/network/url.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/url.el#L1)

解析受限的 HTTP、HTTPS、WS 与 WSS URL，并解析相对引用。

## NetworkUrl {#api-ce5b237af29ddf9960d5}

源码：`src/stdlib/network/url.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/url.el#L49)

解析受支持的 HTTP、HTTPS、WS 或 WSS 绝对 URL，并提供其规范化组成部分。

```el-signature
export class NetworkUrl
```

**参数**：source 使用 ASCII 字符，非 ASCII 路径内容须百分号编码；主机名须为 IDNA ASCII。

**失败与异常**：URL 无效、包含凭据或使用不支持的协议时抛出 NetworkError。

### 示例：读取 URL 主机

```el
import { NetworkUrl } from "el:network/url.el"
let url = NetworkUrl("https://example.test/docs")
console.stdout.writeLine(url.host)
```

## resolveUrl {#api-e85150a75a8ab3b2c844}

源码：`src/stdlib/network/url.el:110` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/url.el#L110)

根据基础 URL 解析绝对或相对引用，并规范化相对路径中的点段。

```el-signature
export fn resolveUrl(base: NetworkUrl, location: Text): NetworkUrl
```

**返回类型**：[`NetworkUrl`](url.md#api-ce5b237af29ddf9960d5)

**参数**：base 已解析的基础 URL。

**参数**：location 绝对 URL、根相对路径、查询、片段或相对路径引用。

**返回值**：解析后的 NetworkUrl。

**失败与异常**：组合结果不是受支持的 URL 时抛出 NetworkError。

### 示例：解析相对资源路径

```el
import { NetworkUrl, resolveUrl } from "el:network/url.el"
let asset = resolveUrl(NetworkUrl("https://example.test/app/index.html"), "../logo.svg")
```
