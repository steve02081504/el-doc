# network/http/index.el

本页由源码注释生成；示例未运行验证。

## HTTP 客户端 {#api-f427db0b17ef488d9837}

源码：`src/stdlib/network/http/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/index.el#L1)

提供阻塞式 HTTP/HTTPS 请求入口及响应模型；实际协议能力取决于目标平台。

## request {#api-12cc1d63b1d2ff501929}

源码：`src/stdlib/network/http/index.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/index.el#L59)

```el
export fn request(url: Text, options: HttpOptions = HttpOptions()): HttpResponse
```

发送 HTTP 请求并返回状态、响应头与响应体。

**参数**：url HTTP 或 HTTPS URL。

**参数**：options 请求方法、请求头、请求体与重定向等选项。

**返回值**：HTTP 响应；非成功状态仍作为响应返回，除非调用方另行检查状态。

**失败与异常**：网络、协议、重定向策略或当前目标不支持时抛出 NetworkError。

### 示例：读取 HTTP 响应状态

```el
import { request } from "el:network/http/"
let response = request("https://example.com/")
console.stdout.writeLine(response.status)
```

## fetchAs {#api-fe57871ae4aba18485ea}

源码：`src/stdlib/network/http/index.el:83` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/index.el#L83)

```el
export fn fetchAs(format, url: Text, options: HttpOptions = HttpOptions())
```

请求 URL，并用指定格式解码成功响应体。

**参数**：format 提供 decode 方法的格式对象。

**参数**：url HTTP 或 HTTPS URL。

**参数**：options 请求选项。

**返回值**：解码后的格式值。

**失败与异常**：网络请求失败、响应状态不成功或格式解码失败时抛出异常；HTTP 状态错误包含响应。

### 示例：获取 JSON 配置

```el
import { fetchAs, HttpOptions } from "el:network/"
import { formats } from "el:formats/"
let config = fetchAs(formats.JSON, "https://example.com/config.json", HttpOptions(@{ timeout: 5000 }))
```
