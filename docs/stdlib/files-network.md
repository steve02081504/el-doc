# 文件与网络

> 读一个文件只要一行。真正花时间的是失败之后：路径解析错了、编码不对、JSON 坏了，还是网络根本没通？这一页按“入口 → 参数 → 边界”把这些层分开。

!!! abstract "🎯 读完这页，你能"
    - 用一行读入文本、一行写出文本，并在文件不存在时给出默认值
    - 分清逻辑路径与系统路径，知道 `file:` 和 `https:` 引用各自能做什么
    - 用 `parseJSON` 解析配置，并处理“不是字符串”这类成员类型问题
    - 发起 HTTP 请求，判断该检查 `response.ok` 还是该捕获异常

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[集合与文本](collections.md)</span>

## 最小入口：读一行、写一行

```el
import { readTextFile, writeTextFile, readTextFileIfPresent } from "el:filesystem/"

let text = readTextFile("file:./notes.txt")
writeTextFile("file:./copy.txt", text + "\n")
```

常用的 `readTextFile`、`writeTextFile` 等入口 prelude 已经提供，写出来是为了说清它们来自 `el:filesystem/`；显式导入与 prelude 的同一声明不冲突，也不会重复初始化。`readTextFileIfPresent` 这类变体需要显式导入。

!!! example "动手 30 秒"
    把 `notes.txt` 换成不存在的文件名再跑一次。`readTextFile` 会抛异常，而 `readTextFileIfPresent` 返回 `void`；看到“没有这个文件”就说明分支生效。

## 读文本还是读字节

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

写入失败、读取失败、编码失败都抛语言异常，不会用零值或空串冒充成功。`maximumBytes` 用于拒绝过大的输入；不传表示不额外限制，但仍受实际分配与传输限制。

## 路径是逻辑位置，不是系统路径

默认的文件 API 不直接操作操作系统的原生路径，而是操作**逻辑位置**：每个引用都由某个 provider 解析成 `Location`，当前工作目录也是逻辑 cwd，不是进程的 cwd。好处是同一份代码可以用 `file:` 访问本地文件，也可以用 `https:` 访问网络资源。

文件 API 接受三类引用：相对引用（`file:./config.json` 或直接 `./config.json`，以逻辑 cwd 为基准）、`file:` 绝对引用，以及其它 provider 的引用（如 `https://...`）。引用只在解析时才与当前上下文结合，`Location` 保存 provider 身份和规范位置。

```el
import { currentDirectory, resolvePath, parentPath, fileName, isDirectory } from "el:filesystem/"

console.stdout.writeLine("cwd: ", currentDirectory().identifier)

let config = resolvePath("file:./config.json")
console.stdout.writeLine("name: ", fileName(config))
console.stdout.writeLine("dir: ", isDirectory(parentPath(config)))
```

常用的位置操作还有 `directoryNames(reference)` 列目录、`makeDirectories(reference)` 建目录、`removeFile(reference)` 删文件、`copyFile(source, target)` 复制、`replaceFile(source, target)` 原子替换。Web 端的 `https:` 位置能读，但不代表能列目录或写入；缺少所请求能力时返回明确错误。

## 用格式读写：把字节转换交给格式对象

`readFileAs(format, reference)` 与 `writeFileAs(format, reference, value)` 把“取字节”和“解码/编码”组合起来。格式对象由 `formats` 提供，例如 `formats.JSON`、`formats.Text`、`formats.YAML`、`formats.CSV`。这些内置格式均提供编码器；下表列出写入时使用的值类型。

```el
import { readFileAs, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let json = readFileAs(formats.JSON, "file:./config.json")
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

`writeFileAs` 需要所选格式提供编码器。`formats.Text` 的编码就是原样输出文本；`formats.JSON` 通过 `writeJSON` 编码支持的 JSON 值。自定义 `TextFormat` 如果没有提供编码器，调用它的 `encode` 会明确报“这个文本格式没有编码器”。

| 格式对象 | 写入值 | 编码约定 |
| --- | --- | --- |
| `formats.Text` / `formats.Buffer` | `Text` / `Buffer` | 原样 UTF-8 文本或字节。 |
| `formats.JSON` / `formats.JSONC` / `formats.JSON5` | 支持的标量、数组和公开数据对象 | JSONC 输出严格 JSON；JSON5 另允许非有限数。 |
| `formats.JSONLines` | 值数组 | 每个值一行 JSON。 |
| `formats.YAML` | 支持的标量、数组和公开数据对象 | 输出带引号键的流式集合，支持非有限数；共享对象按树展开，循环引用报错。 |
| `formats.TOML` | `Toml.Table` 根表 | 嵌套表编码为内联表，保留日期时间类型；重复键报错。 |
| `formats.XML` | `XmlDocument` | 验证文档结构并转义文本和属性；拒绝非法节点内容。 |
| `formats.CSV` / `formats.TSV` | `Text[][]` | 按需加引号、内部引号双写，以 CRLF 结束记录；每行至少一个单元格。 |
| `formats.INI` | 文本字段和一层节对象组成的公开数据对象 | 根键先于节输出，拒绝无法无损表示的名称和值。 |
| `formats.EOL` / `formats.EOD` | 满足对应序列化能力合同的值 | 使用现有自包含序列化编码，保存 EL 的类型与共享关系。 |
| `formats.XLSX` / `formats.ODS` | `Workbook` | 使用工作簿模型编码。 |
| `formats.DOCX` / `formats.ODT` | `WordDocument` | 使用文档模型编码。 |

这些编码器重新生成内容，不保留原文件的注释或排版。JSON、YAML 和 TOML 写入器对数值使用精确转换；格式数值词素范围内不能精确表示的数（例如 `1 / 3`）会报错，不会静默舍入。可以先修改解码得到的数据，再用同一种格式写出；TOML 和 XML 保留各自的数据模型，不把任意 EL 对象当作对应文档。

文本格式通过 `JsonLimits` 控制输出字节与编码工作预算。EOL/EOD 格式中的 `SerializationLimits` 节点、深度和整数限制只用于解码；编码调用对应序列化入口，生成完整结果后才检查字节上限。自定义 `TextFormat` 仍可只提供解码器。

!!! note "JSON 与 EL 序列化的用途"
    JSON 编码只接受编码器支持的值，并受格式预算限制。需要按 EL 序列化合同保存结构化值时，使用语言规范第 15 章的 EOL/EOD 入口生成文本或字节，再交给显式写入。

## INI 配置：节和键保留名字，值保持文本

下面是一个完整的内存解析示例；`jsonField` 也可以读取 INI 返回的动态对象成员：

```el
import { parseINI } from "el:formats/ini/"
import { jsonField } from "el:formats/json/"

let config = parseINI("name=demo\n[server]\nport=8080\n")
let server = jsonField(config, "server")
console.stdout.writeLine(jsonField(config, "name"))
console.stdout.writeLine(jsonField(server, "port"))
```

预期输出：

```text
demo
8080
```

`port` 的值是文本 `"8080"`，不会自动变成数字。若配置已保存在 UTF-8 文件 `config.ini` 中，可以直接读取：

```el
import { readFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let config = readFileAs(formats.INI, "file:./config.ini")
```

当前支持轻量 INI 方言：

- 节写作 `[server]`；第一个节之前的键放在根对象中，节内的键放在对应节对象中。
- 键和值以 `=` 或 `:` 分隔，两端空格和制表符会去掉；节名和键名区分大小写。
- `;` 和 `#` 支持整行注释；节头后也允许注释。值中的这些字符仍是文本，不会作为行尾注释去掉。
- 重复键使用最后一个值，重复节合并；标量键与节名冲突会报错。
- 值按字面文本保留，不处理引号、转义、插值或多行值。

`parseINI` 的第二个参数可传 `JsonLimits`，限制输入字节数与解析资源。语法错误或资源超限会抛异常。使用 `writeINI(value)` 可得到文本；也可以直接写入文件：

```el
import { writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

writeFileAs(formats.INI, "file:./config.ini", @{ name: "demo", server: @{ port: "8080" } })
```

写入器不自动将数字转换成文本；空白位于名称或值两端、多行值、超过一层的节，以及含语法分隔符的名称都会报错，避免写出后含义改变。接口参数见 [INI API 参考](api/modules/formats/ini/index.md)。

## 先猜：服务器返回 404，`request` 会抛异常吗？

??? question "先猜：`request("https://example.com/missing")` 收到 404 时，是抛异常还是正常返回？"
    正常返回。HTTP 错误状态**不抛异常**，`request` 把状态码、头与完整响应体交给你，要自己检查 `response.ok`。只有连接、DNS、超时这类传输层失败才抛 `NetworkError`。

## HTTP 错误状态不抛异常，要自己检查

`request(url, options)` 返回 `HttpResponse`，它保留状态码、头与完整响应体。

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

### 选项都有默认值，超时不是重试

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

## JSON 取到成员后，先 match 一次

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

## 完整例子：读写配置文件

读配置时把“文件不存在”“JSON 损坏”“成员缺失”都当成可回退的情况：

```el
import { readTextFileIfPresent } from "el:filesystem/"

fn loadName() {
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

写配置时交给 JSON 编码器处理引号、反斜杠和换行：

```el
import { writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

fn saveName(name: Text) {
	discard(writeFileAs(formats.JSON, "file:./config.json", @{ name: name }))
}
```

## 完整例子：请求并解析 JSON

```el
import { fetchAs, HttpOptions, HttpStatusError, NetworkError } from "el:network/"
import { formats } from "el:formats/"

fn fetchName(url: Text) {
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

!!! warning "常见坑：错误发生在哪一层"
    - 文件不存在却得到空串：那是代码把失败吞了。默认入口抛异常，只有 `...IfPresent` 系列返回 `void`。
    - 自定义 `TextFormat` 报“没有编码器”：构造它时需要传入 `write`；内置 INI 已提供编码器，值仍须符合其文本与节结构限制。
    - 404 之后程序继续往下跑：`request` 不抛 HTTP 错误，必须检查 `response.ok`，或用 `fetchAs`。
    - 用 `https://...` 去列目录或写文件：Web provider 只保证读，缺能力时返回明确错误。

文件与网络共用同一套失败语义：失败要用异常或 `void` 表达，上限要在解码之前生效，而不是靠猜一个默认值继续跑。

??? note "可选 · 深入：为什么要有逻辑文件系统"
    逻辑位置的意义是让同一段代码换一个 provider 就换一种存储：本地文件、HTTP 资源、未来的其它后端都走同一套 `Location`、读、写与失败语义。代价是你不能把系统路径直接塞进去，也不能假设“文件系统”只有本地磁盘。`maximumBytes`、`HttpOptions.maximumBodyBytes` 这些上限是这套模型的一部分：它们在解析之前就把过大的输入挡掉。

## 带走这三样

- 读文本用 `readTextFile`，读字节用 `readFileBytes`；想允许缺失用 `...IfPresent`，其余情况让异常抛出来。
- 路径是逻辑位置，`file:` 和 `https:` 是不同 provider；引用在解析时才和当前上下文结合。
- HTTP 错误状态不抛异常，`request` 要看 `response.ok`；`fetchAs` 把“请求 + 检查 + 解码”合成一步。

## 下一站：图形界面

> 数据能在终端里读写之后，下一步是让它出现在窗口里。EL 的界面用什么描述，又为什么不是 HTML？

- 主推进：[图形界面](gui.md)：对象图、两种建界面入口、事件与定时器。
- 想先练手：[命令行工具](../practice/cli-tool.md)：把文件读写、参数和退出码串成一个工具。
- 后面会用到：[错误处理与异步](../language/errors-async.md)：超时、状态码和解析失败的类型与捕获写法。
