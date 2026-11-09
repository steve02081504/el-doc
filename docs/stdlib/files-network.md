# 文件与网络

程序迟早要和外部世界交换数据：读写本地文件、下载一份 JSON、保存用户配置。EL 用一个统一的逻辑文件系统处理这些事，网络请求则是它的另一个 provider。这一页讲清文件读写、格式解码和 HTTP 请求的入口，并给出读写配置文件和请求 JSON 两个完整例子。

## 逻辑文件系统

默认的文件 API 不直接操作操作系统的原生路径，而是操作**逻辑位置**：每个引用都由某个 provider 解析成 `Location`，当前工作目录也是逻辑 cwd，不是进程的 cwd。这样做的好处是同一份代码可以用 `file:` 访问本地文件，也可以用 `https:` 访问网络资源。

```el
import { readTextFile, writeTextFile, readTextFileIfPresent } from "el:filesystem/"

let text = readTextFile("file:./notes.txt")
writeTextFile("file:./copy.txt", text + "\n")
```

常用的 `readTextFile`、`writeTextFile` 等入口 prelude 已经提供；`readTextFileIfPresent` 这类变体需要显式导入。写出来是为了说清它们来自哪个模块，显式导入与 prelude 的同一声明不冲突，也不会重复初始化。

## 读文本与读字节

- `readTextFile(reference, maximumBytes = void)` 读入整个文件并按 UTF-8 解码成 `Text`；
- `writeTextFile(reference, value)` 把 `Text` 按 UTF-8 写入，返回写入的字节数；
- `readFileBytes(reference, maximumBytes = void)` 返回 `Number[]`，每个元素是一个字节；
- `writeFileBytes(reference, bytes)` 写入字节数组，返回写入的字节数；
- `readTextFileIfPresent(reference, maximumBytes = void)` 与 `readFileBytesIfPresent(...)` 在文件不存在时返回 `void`，而不是抛错。

```el
let bytes = readFileBytes("file:./logo.png")
console.stdout.writeLine("size: ", bytes.size, " bytes")

let missing = readTextFileIfPresent("file:./absent.txt")
if (missing is void_t) {
	console.stdout.writeLine("没有这个文件，按默认值处理")
}
```

写入失败、读取失败、编码失败都抛语言异常，不会用零值或空串冒充成功。显式的字节上限用于拒绝过大的输入；不传 `maximumBytes` 表示不额外限制，但仍受实际分配与传输限制。

## 路径与位置

文件 API 接受三类引用：相对引用（`file:./config.json` 或直接 `./config.json`，以逻辑 cwd 为基准）、`file:` 绝对引用，以及其它 provider 的引用（如 `https://...`）。引用只在解析时才与当前上下文结合，`Location` 保存 provider 身份和规范位置。

```el
import { currentDirectory, resolvePath, parentPath, fileName, isDirectory } from "el:filesystem/"

console.stdout.writeLine("cwd: ", currentDirectory().identifier)

let config = resolvePath("file:./config.json")
console.stdout.writeLine("name: ", fileName(config))
console.stdout.writeLine("dir: ", isDirectory(parentPath(config)))
```

常用的位置操作还有 `directoryNames(reference)` 列目录、`makeDirectories(reference)` 建目录、`removeFile(reference)` 删文件、`copyFile(source, target)` 复制、`replaceFile(source, target)` 原子替换。Web 端的 `https:` 位置能读，但不代表能列目录或写入，缺少所请求能力时返回明确错误。

## 用格式读写文件

`readFileAs(format, reference)` 与 `writeFileAs(format, reference, value)` 把“取字节”和“解码/编码”组合起来。格式对象由 `formats` 提供，例如 `formats.JSON`、`formats.Text`、`formats.YAML`、`formats.CSV`。

```el
import { readFileAs, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let json = readFileAs(formats.JSON, "file:./config.json")
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

`writeFileAs` 需要所选格式提供编码器。`formats.Text` 的编码就是原样输出文本；`formats.JSON` 目前只提供解码，调用它的 `encode` 会明确报“这个文本格式没有编码器”。

!!! note "实现状态"
    所以写 JSON 文件时不能靠 `writeFileAs(formats.JSON, ...)`，要把内容先拼成文本再用 `writeTextFile` 写入。需要保存任意结构化对象时，用语言规范第 15 章的 EOL/EOD 序列化入口生成文本或字节，再交给显式写入。

## 解析 JSON

`parseJSON(source, limits = JsonLimits())` 把文本解析成 `Json` 值，失败时抛 `ParseError`；`jsonField(value, key)` 按成员名取值。

```el
let config = parseJSON(readTextFile("file:./config.json"))
let name = jsonField(config, "name")

match name {
	Json.String(text) => { console.stdout.writeLine("name: ", text) }
	_ => { console.stdout.writeLine("name 不是字符串") }
}
```

`Json` 是一个数据声明，成员是 `Json.Null`、`Json.Boolean(value)`、`Json.String(value)`、`Json.Numeric(value)`、`Json.Array(items)`、`Json.Object(fields)`。所以取到成员后通常要 `match` 一次，把“它到底是字符串还是数字”写清楚。`JsonLimits` 控制输入字节上限与解析预算，默认字节上限是 16 MiB。

## 发起 HTTP 请求

`request(url, options)` 返回 `HttpResponse`，它保留状态码、头与完整响应体；HTTP 错误状态**不抛异常**，要自己检查 `response.ok`。

```el
import { request, HttpOptions, HttpStatusError, HttpHeader } from "el:network/"
import { formats } from "el:formats/"

let response = request("https://example.com/status", HttpOptions(@{ timeout: 5000 }))
if (!response.ok) throw HttpStatusError(response)
console.stdout.writeLine("status: ", response.status)
console.stdout.writeLine(response.text())
```

`HttpResponse` 的常用成员：`status`、`ok`、`headers`、`body`、`url`、`header(name)`、`text()`、`json(limits)`、`as(format)`。

### 一步取到解码后的结果

`fetchAs(format, url, options)` 等于“请求 + 检查状态 + 解码”，状态不在 2xx 时直接抛 `HttpStatusError`：

```el
let config = fetchAs(formats.JSON, "https://example.com/config.json", HttpOptions(@{ timeout: 5000 }))
```

### 选项、超时与错误

`HttpOptions` 的字段都有默认值，用对象字面量覆盖需要的项：`method`、`headers`、`body`、`timeout`（毫秒，默认 30000）、`maximumBodyBytes`、`maximumHeaderBytes`、`maximumRedirects`、`forceRefresh`、`tls`。

```el
let options = HttpOptions(@{
	method: "POST",
	headers: @[HttpHeader("Content-Type", "text/plain")],
	body: @[104, 105],
	timeout: 10000
})
```

网络层的失败分两类：连接、DNS、超时、重定向失败抛 `NetworkError`；HTTP 状态不在成功范围时 `fetchAs` 抛 `HttpStatusError`，它的 `response` 字段保留完整响应以便读取状态码与响应头。超时不是重试，超时后请求就失败了。

## 完整例子：读写配置文件

读配置时把“文件不存在”“JSON 损坏”“成员缺失”都当成可回退的情况：

```el
import { readTextFileIfPresent } from "el:filesystem/"

fn loadName(): Text {
	let source = readTextFileIfPresent("file:./config.json")
	if (source is void_t) return "anonymous"

	let config = try { parseJSON(source) } catch { return "anonymous" }
	let value = try { jsonField(config, "name") } catch { return "anonymous" }

	match value {
		Json.String(text) => { return text }
		_ => { return "anonymous" }
	}
}
```

写配置时直接写文本。真实项目里要对插入的字符串做 JSON 转义，这里为了看清流程省略了它：

```el
fn saveName(name: Text) {
	writeTextFile("file:./config.json", `{"name": "${name}"}`)
}
```

## 完整例子：请求并解析 JSON

```el
import { fetchAs, HttpOptions, HttpStatusError, NetworkError } from "el:network/"
import { formats } from "el:formats/"

fn fetchName(url: Text): Text {
	let config = fetchAs(formats.JSON, url, HttpOptions(@{ timeout: 5000 }))
	let value = jsonField(config, "name")
	match value {
		Json.String(text) => { return text }
		_ => { throw StateError("响应里没有 name 字符串") }
	}
}

try {
	console.stdout.writeLine("name: ", fetchName("https://example.com/config.json"))
} catch (error: HttpStatusError) {
	console.error.value(error)
} catch (error: NetworkError) {
	console.error.value(error)
}
```

两个 `catch` 分别处理“服务器返回了错误状态”和“请求本身失败”，其余异常继续向外传播。`console.error.value(error)` 发出该等级的结构化展示记录，默认走 stderr。

## 继续阅读

- [集合与文本](collections.md)：解析出来的 `Json` 最终要变成数组、映射和文本。
- [错误处理与异步](../language/errors-async.md)：超时、状态码和解析失败的类型与捕获写法。
- [测试](testing.md)：用临时目录和本地进程验证读写逻辑。
