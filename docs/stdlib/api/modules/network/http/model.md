# network/http/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/network.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [HttpHeader.constructor](#api-0549edb36255a79d2ca5)
- [HttpOptions.method](#api-475f97593e614073ed6d)
- [HttpOptions.headers](#api-b62e4b8b5709bbc9f08c)
- [HttpOptions.body](#api-2423c7ff209b593cab3b)
- [HttpOptions.timeout](#api-144a9e027290b0df45e4)
- [HttpOptions.maximumBodyBytes](#api-63fa6a530786b3e21d04)
- [HttpOptions.maximumHeaderBytes](#api-0adac10b091b2a26a25c)
- [HttpOptions.maximumRedirects](#api-1114afde4fc20fb2667e)
- [HttpOptions.forceRefresh](#api-9a787364b17ad804ed35)
- [HttpOptions.tls](#api-d641795490ee1d451170)
- [HttpOptions.constructor](#api-98d4531c02450c1b7eb2)
- [HttpResponse.status](#api-94a7ee2eb19c23484254)
- [HttpResponse.headers](#api-13457e67b9172ccbf05d)
- [HttpResponse.body](#api-c6cdd2d8c232982199d4)
- [HttpResponse.url](#api-c72aa9a6acb07d01133a)
- [HttpResponse.ok](#api-833651302d6ba4264de8)
- [HttpResponse.text](#api-6cda717c77ed293047df)
- [HttpResponse.json](#api-fd727a1f0f4a5400e858)
- [HttpResponse.as](#api-babd6c7262ef7ec82f76)
- [HttpResponse.header](#api-af4458df84318ed403f0)
- [HttpStatusError.response](#api-84ea870701b770626b47)
- [HttpStatusError.constructor](#api-8cd621216a6f8df9a3be)

## HTTP 请求与响应模型 {#api-4c1eab6b042d0bb5f906}

源码：`src/stdlib/network/http/model.el:2` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L2)

定义请求选项、响应头、HTTP 响应及状态错误。

## HttpHeader {#api-de461259064c77488732}

源码：`src/stdlib/network/http/model.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L34)

表示一个经校验的 HTTP 请求或响应头名称和值。

```el-signature
export class HttpHeader
```

**参数**：name 符合 HTTP token 语法的头名称。

**参数**：value 不含禁止控制字符的 ASCII 头值。

**失败与异常**：头名或头值违反格式要求时抛 NetworkError。

### 示例：构造内容类型头

```el
import { HttpHeader } from "el:network/"
let header = HttpHeader("Content-Type", "application/json")
```

## HttpHeader.constructor {#api-0549edb36255a79d2ca5}

源码：`src/stdlib/network/http/model.el:46` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L46)

创建并校验一条 HTTP 头。

```el-signature
constructor(name: Text, value: Text)
```

**参数**：name 符合 HTTP token 语法的名称。

**参数**：value 允许的 ASCII 头值。

**失败与异常**：名称或值格式无效时抛 NetworkError。

### 示例：创建接受类型头

```el
let header = HttpHeader("Accept", "application/json")
```

## HttpOptions {#api-5047f246ebfdff685043}

源码：`src/stdlib/network/http/model.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L71)

配置 HTTP 请求方法、头、请求体、资源上限与 TLS 行为。

```el-signature
export class HttpOptions
```

### 示例：设置请求超时

```el
import { HttpOptions } from "el:network/"
let options = HttpOptions(@{ timeout: 5000 })
```

## HttpOptions.method {#api-475f97593e614073ed6d}

源码：`src/stdlib/network/http/model.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L78)

请求使用的 HTTP 方法，默认是 GET。

```el-signature
let method: Text
```

**类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

### 示例：指定 POST 方法

```el
let options = HttpOptions(@{ method: "POST" })
```

## HttpOptions.headers {#api-b62e4b8b5709bbc9f08c}

源码：`src/stdlib/network/http/model.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L85)

要发送的请求头数组。

```el-signature
let headers: HttpHeader[]
```

**类型**：[`HttpHeader`](model.md#api-de461259064c77488732)[]

### 示例：设置请求头

```el
let options = HttpOptions(@{ headers: @[HttpHeader("Accept", "application/json")] })
```

## HttpOptions.body {#api-2423c7ff209b593cab3b}

源码：`src/stdlib/network/http/model.el:92` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L92)

要发送的请求体字节；GET 与 HEAD 不接受非空请求体。

```el-signature
let body: Number[]
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：设置字节请求体

```el
let options = HttpOptions(@{ method: "POST", body: @[65, 66] })
```

## HttpOptions.timeout {#api-144a9e027290b0df45e4}

源码：`src/stdlib/network/http/model.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L99)

请求超时毫秒数，默认 30000，必须为正数。

```el-signature
let timeout: Number
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：设置五秒超时

```el
let options = HttpOptions(@{ timeout: 5000 })
```

## HttpOptions.maximumBodyBytes {#api-63fa6a530786b3e21d04}

源码：`src/stdlib/network/http/model.el:107` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L107)

请求或响应消息体字节上限；nil 表示不设显式上限。

```el-signature
let maximumBodyBytes: Number | nil_t
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：限制响应体大小

```el
let options = HttpOptions(@{ maximumBodyBytes: 1048576 })
```

## HttpOptions.maximumHeaderBytes {#api-0adac10b091b2a26a25c}

源码：`src/stdlib/network/http/model.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L114)

请求与响应头的最大字节数。

```el-signature
let maximumHeaderBytes: Number | nil_t
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：设置头部上限

```el
let options = HttpOptions(@{ maximumHeaderBytes: 16384 })
```

## HttpOptions.maximumRedirects {#api-1114afde4fc20fb2667e}

源码：`src/stdlib/network/http/model.el:121` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L121)

允许跟随的最大重定向次数。

```el-signature
let maximumRedirects: Number | nil_t
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

### 示例：禁止自动跟随重定向

```el
let options = HttpOptions(@{ maximumRedirects: 0 })
```

## HttpOptions.forceRefresh {#api-9a787364b17ad804ed35}

源码：`src/stdlib/network/http/model.el:128` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L128)

请求是否绕过可复用的缓存响应。

```el-signature
let forceRefresh: Bool
```

**类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：强制刷新响应

```el
let options = HttpOptions(@{ forceRefresh: t })
```

## HttpOptions.tls {#api-d641795490ee1d451170}

源码：`src/stdlib/network/http/model.el:135` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L135)

HTTPS 请求使用的 TLS 配置。

```el-signature
let tls: TlsOptions
```

**类型**：[`TlsOptions`](../tls/options.md#api-d66684475437485e3301)

### 示例：使用默认 TLS 配置

```el
let options = HttpOptions(@{ tls: TlsOptions() })
```

## HttpOptions.constructor {#api-98d4531c02450c1b7eb2}

源码：`src/stdlib/network/http/model.el:144` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L144)

用字段对象覆盖默认请求配置，并在创建时校验字段范围和组合。

```el-signature
constructor(changes = @{})
```

**参数**：changes 要覆盖的请求字段。

**失败与异常**：方法、头、超时或资源上限违反合同时时抛 NetworkError。

### 示例：创建有超时限制的请求选项

```el
let options = HttpOptions(@{ timeout: 5000, maximumRedirects: 3 })
```

## HttpResponse {#api-e49096dfd951764c068f}

源码：`src/stdlib/network/http/model.el:194` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L194)

保存 HTTP 状态码、响应头、响应体和最终 URL，并提供常用解码操作。

```el-signature
export class HttpResponse
```

### 示例：检查请求状态

```el
let response = request("https://example.com/")
console.stdout.writeLine(response.status, " ", response.ok)
```

## HttpResponse.status {#api-94a7ee2eb19c23484254}

源码：`src/stdlib/network/http/model.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L201)

HTTP 状态码。

```el-signature
let status: Number
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：检查状态码（需调用方提供对象或绑定）

```el
console.stdout.writeLine(response.status)
```

## HttpResponse.headers {#api-13457e67b9172ccbf05d}

源码：`src/stdlib/network/http/model.el:209` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L209)

响应头列表。

```el-signature
let headers: HttpHeader[]
```

**类型**：[`HttpHeader`](model.md#api-de461259064c77488732)[]

### 示例：检查响应头数

```el
// @external response
console.stdout.writeLine(response.headers.count)
```

## HttpResponse.body {#api-c6cdd2d8c232982199d4}

源码：`src/stdlib/network/http/model.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L216)

响应体的原始字节。

```el-signature
let body: Number[]
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：检查响应体字节数（需调用方提供对象或绑定）

```el
console.stdout.writeLine(response.body.count)
```

## HttpResponse.url {#api-c72aa9a6acb07d01133a}

源码：`src/stdlib/network/http/model.el:224` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L224)

请求跟随重定向后的最终 URL。

```el-signature
let url: Text
```

**类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

### 示例：查看最终 URL

```el
// @external response
console.stdout.writeLine(response.url)
```

## HttpResponse.ok {#api-833651302d6ba4264de8}

源码：`src/stdlib/network/http/model.el:233` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L233)

判断状态码是否位于 200 到 299 的成功范围。

```el-signature
get ok(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：成功范围内为真。

### 示例：判断响应是否成功（需调用方提供对象或绑定）

```el
if (response.ok) console.stdout.writeLine("success")
```

## HttpResponse.text {#api-6cda717c77ed293047df}

源码：`src/stdlib/network/http/model.el:243` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L243)

将响应体按 UTF-8 解码为文本；拒绝未解码的非 identity 内容编码。

```el-signature
fn text(): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**返回值**：响应文本。

**失败与异常**：响应内容编码不受支持或 UTF-8 无效时抛出异常。

### 示例：读取文本响应

```el
// @external response
console.stdout.writeLine(response.text())
```

## HttpResponse.json {#api-fd727a1f0f4a5400e858}

源码：`src/stdlib/network/http/model.el:257` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L257)

将响应文本解析为 JSON 值。

```el-signature
fn json(limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

**参数**：limits JSON 解析资源限制。

**返回值**：解码后的 JSON 值。

**失败与异常**：内容编码、UTF-8 或 JSON 解析失败时抛出异常。

### 示例：解码 JSON 响应（需调用方提供对象或绑定）

```el
let configuration = response.json()
```

## HttpResponse.as {#api-babd6c7262ef7ec82f76}

源码：`src/stdlib/network/http/model.el:268` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L268)

使用指定格式对象解码响应体。

```el-signature
fn as(format)
```

**参数**：format 提供 decode 方法的格式对象。

**返回值**：格式解码后的值。

**失败与异常**：内容编码或格式解码失败时抛出异常。

### 示例：使用 JSON 格式解码

```el
// @external response
let config = response.as(formats.JSON)
```

## HttpResponse.header {#api-af4458df84318ed403f0}

源码：`src/stdlib/network/http/model.el:281` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L281)

按大小写无关的名称查找首个响应头。

```el-signature
fn header(name: Text): Text | nil_t
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a) | [`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

**参数**：name 响应头名称。

**返回值**：响应头值；不存在时返回 nil。

### 示例：读取内容类型（需调用方提供对象或绑定）

```el
let contentType = response.header("Content-Type")
```

## HttpStatusError {#api-b0c306dbfe7c9ba3158d}

源码：`src/stdlib/network/http/model.el:293` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L293)

表示 HTTP 响应状态不成功；异常保留原始响应供调用方检查。

```el-signature
export class HttpStatusError extends Error
```

### 示例：捕获并检查错误响应

```el
// @external url
try { fetchAs(formats.JSON, url) }
catch (error: HttpStatusError) { console.stderr.writeLine(error.response.status) }
```

## HttpStatusError.response {#api-84ea870701b770626b47}

源码：`src/stdlib/network/http/model.el:300` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L300)

引发状态错误的完整 HTTP 响应。

```el-signature
let response: HttpResponse
```

**类型**：[`HttpResponse`](model.md#api-e49096dfd951764c068f)

### 示例：查看错误状态（需调用方提供对象或绑定）

```el
console.stderr.writeLine(error.response.status)
```

## HttpStatusError.constructor {#api-8cd621216a6f8df9a3be}

源码：`src/stdlib/network/http/model.el:309` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/http/model.el#L309)

将不成功的 HTTP 响应封装为状态异常。

```el-signature
constructor(response: HttpResponse)
```

**参数**：response 要附加到异常的完整响应。

### 示例：手动将错误状态转成异常

```el
// @external response
if (!response.ok) throw HttpStatusError(response)
```
