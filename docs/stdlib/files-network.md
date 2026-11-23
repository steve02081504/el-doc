# 文件与网络

> 读一个文件只要一行。真正花时间的是失败之后：路径解析错了、编码不对、JSON 坏了，还是网络根本没通？这一页按“入口 → 参数 → 边界”把这些层分开。

!!! abstract "🎯 读完这页，你能"
    - 用一行读入文本、一行写出文本，并在文件不存在时给出默认值
    - 分清逻辑路径与系统路径，知道 `file:` 和 `https:` 引用各自能做什么
    - 读取 JSON 配置，并处理“不是字符串”这类成员类型问题
    - 发起 HTTP 请求，判断该检查 `response.ok` 还是该捕获异常

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[集合与文本](collections.md)</span>

## 读取和写入 UTF-8 文本

```el
import { readFileAs, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let text = readFileAs(formats.Text, "file:./notes.txt")
writeFileAs(formats.Text, "file:./copy.txt", text + "\n")
```

可以从 prelude 直接使用 `readFileAs`、`writeFileAs` 和 `formats`。这里显式导入，便于查找它们所属的模块。

!!! example "动手 30 秒"
    把 `notes.txt` 换成不存在的文件名再跑一次，观察读取抛出的异常。

## 读文本还是读字节

- `readFileAs(formats.Text, reference, maximumBytes: limit)` 在可选的字节上限内读取整个文件，并按 UTF-8 解码成 `Text`；
- `writeFileAs(formats.Text, reference, value)` 把 `Text` 按 UTF-8 写入，返回写入的字节数；
- `readFileAs(formats.Buffer, reference, maximumBytes: limit)` 在可选的字节上限内读取整个文件，返回 `Buffer`；
- `writeFileAs(formats.Buffer, reference, buffer)` 写入缓冲区并返回字节数。用 `bufferFromBytes(bytes)` 把数值字节数组转为缓冲区。
- 字节层的 `Location.readOptionalBytes()` 在实际打开确认目标缺失时返回 `nil`。文件存在时交付原始字节，空文件返回空数组。

```el
import { readFileAs, resolvePath } from "el:filesystem/"
import { formats } from "el:formats/"

let buffer = readFileAs(formats.Buffer, "file:./logo.png")
console.stdout.writeLine("size: ", buffer.count, " bytes")

let missing = resolvePath("file:./absent.txt").readOptionalBytes()
if (missing is nil_t) {
	console.stdout.writeLine("没有这个文件，按默认值处理")
}
```

写入失败、读取失败、编码失败都抛语言异常，不会用零值或空串冒充成功。`maximumBytes` 用于拒绝过大的输入；不传表示不额外限制，但仍受实际分配与传输限制。

## 路径是逻辑位置，不是系统路径

默认的文件 API 不直接操作操作系统的原生路径，而是操作**逻辑位置**：每个引用都由某个 provider 解析成 `Location`，当前工作目录也是逻辑 cwd，不是进程的 cwd。好处是同一份代码可以用 `file:` 访问本地文件，也可以用 `https:` 访问网络资源。

文件 API 接受三类引用：相对引用（`file:./config.json` 或直接 `./config.json`，以逻辑 cwd 为基准）、`file:` 绝对引用，以及其它 provider 的引用（如 `https://...`）。引用只在解析时才与当前上下文结合，`Location` 保存 provider 身份和规范位置。

```el
import { currentDirectory, resolvePath, fileName, isDirectory } from "el:filesystem/"

console.stdout.writeLine("cwd: ", currentDirectory().identifier)

let config = resolvePath("file:./config.json")
console.stdout.writeLine("name: ", fileName(config))
console.stdout.writeLine("dir: ", isDirectory(config.parent))
```

常用的位置操作还有 `directoryNames(reference)` 列目录、`makeDirectories(reference)` 建目录、`removeFile(reference)` 删文件、`copyFile(source, target)` 复制、`moveFile(source, target)` 在同一 provider 内移动并替换目标。Web 端的 `https:` 位置能读，但不代表能列目录或写入；缺少所请求能力时返回明确错误。

## 条件写入与格式

`exists(path)` 单独调用时查询位置当前是否存在。条件块只有一条普通 `writeFileAs` 调用，且两处使用同一局部路径绑定时，标准库策略把条件交给写入打开。文件在实际打开时缺失就跳过，打开后沿同一文件句柄写入。这个入口要求 provider 支持条件写入，整文件原子发布用 `publishFileAs`。

```el
import { exists, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let path = "file:./notes.txt"
if (exists(path)) { discard(writeFileAs(formats.Text, path, "updated")) }
```

## 按字节位置修改文件

`reader.position` 是顺序读取已交付的字节数。定位读保持这个位置，文本字符数也不能代替 UTF-8 字节偏移。确定要操作的原始字节和偏移后，对解析出的 `Location` 调用 `writeBytesAt(offset, bytes)` 覆盖，`insertBytes(offset, bytes)` 插入并后移旧后缀，或调用 `appendBytes(bytes)` 在文件尾追加。需要以整文件为单位原子发布时，使用 `publishFileAs`。

直接把完整的新内容交给 `writeFileAs`。provider 支持安全比较时会跳过未变区间，并在只有新增尾部时只写尾部。Linux 的 `PrivateRandomFileSystem` 在实际文件支持范围插入时，可以为对齐的中段新增保留旧后缀的块映射。显式导入 `el:operating-system/files/` 的同名函数可以直写原生路径。

## 用格式读写：把字节转换交给格式对象

`readFileAs(format, reference)` 与 `writeFileAs(format, reference, value)` 把“取字节”和“解码/编码”组合起来。格式对象由 `formats` 提供，例如 `formats.JSON`、`formats.Text`、`formats.YAML`、`formats.CSV`。这些内置格式均提供编码器；下表列出写入时使用的值类型。

```el
import { readFileAs, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"

let json = readFileAs(formats.JSON, "file:./config.json")
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

`writeFileAs` 需要所选格式提供编码器。用 `publishFileAs(formats.Text, path, value)` 可以先写入并关闭暂存文件，再原子替换目标。省略 `temporary` 时，file provider 在目标旁独占创建暂存文件。目标为 `a.exe` 时，自动暂存名为 `a.exe.<随机串>.tmp`。显式名称必须以 `.tmp` 结尾，发生碰撞时在 `.tmp` 前加入随机段重试。`formats.Text` 的编码就是原样输出文本；`formats.JSON` 编码支持的 JSON 值。自定义 `TextFormat` 如果没有提供编码器，调用它的 `encode` 会明确报“这个文本格式没有编码器”。

`el:formats/serialization/io.el` 提供文件读写简写。EOL 用 `scanFile(path)` 和 `printFile(path, value)`，EOD 用 `readFile(path)` 和 `writeFile(path, value)`。

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
import { formats, parseAs } from "el:formats/"
import { jsonField } from "el:formats/json/"

let config = parseAs(formats.INI, "name=demo\n[server]\nport=8080\n")
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

可通过 `INIFormat(limits)` 构造带输入字节和解析预算的格式对象。语法错误或资源超限会抛异常。内存编码用 `serializeAs(formats.INI, value)`，写入文件用 `writeFileAs`。

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

## JSON 取到成员后，检查值的类型

`readFileAs` 使用 `formats.JSON` 读取并解析文件。JSON 格式错误会抛出 `ParseError`。用 `jsonField(value, key)` 按成员名取值。

```el
let config = readFileAs(formats.JSON, "file:./config.json")
let name = jsonField(config, "name")

if (name is Text) console.stdout.writeLine("name: ", name)
else console.stdout.writeLine("name 不是字符串")
```

JSON 的 `null` 解析为 `nil`，布尔值解析为 `t` 或 `f`，字符串和数值分别解析为 `Text` 和 `Number`，数组和对象解析为对应的 EL 容器。读取对象成员后，可以用 `is` 检查值的类型。可以用 `maximumBytes` 限制文件读取字节数。

## 完整例子：读写配置文件

读配置时把“文件不存在”“JSON 损坏”“成员缺失”都当成可回退的情况：

```el
import { resolvePath } from "el:filesystem/"
import { formats, parseAs } from "el:formats/"
import { jsonField } from "el:formats/json/"

fn loadName() {
	let source = resolvePath("file:./config.json").readOptionalBytes()
	if (source is nil_t) return "anonymous"

	let config = try { parseAs(formats.JSON, source) } catch { return "anonymous" }
	let value = try { jsonField(config, "name") } catch { return "anonymous" }

	if (value is Text) return value
	return "anonymous"
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
	if (value is Text) return value
	throw StateError("响应里没有 name 字符串")
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
    - 文件不存在却得到空串：那是代码把失败吞了。默认入口抛异常，只有 `...IfPresent` 系列返回 `nil`。
    - 自定义 `TextFormat` 报“没有编码器”：构造它时需要传入 `write`；内置 INI 已提供编码器，值仍须符合其文本与节结构限制。
    - 404 之后程序继续往下跑：`request` 不抛 HTTP 错误，必须检查 `response.ok`，或用 `fetchAs`。
    - 用 `https://...` 去列目录或写文件：Web provider 只保证读，缺能力时返回明确错误。

文件与网络共用同一套失败语义：失败要用异常或 `nil` 表达，上限要在解码之前生效，而不是靠猜一个默认值继续跑。

??? note "可选 · 深入：为什么要有逻辑文件系统"
    逻辑位置的意义是让同一段代码换一个 provider 就换一种存储：本地文件、HTTP 资源、未来的其它后端都走同一套 `Location`、读、写与失败语义。代价是你不能把系统路径直接塞进去，也不能假设“文件系统”只有本地磁盘。`maximumBytes`、`HttpOptions.maximumBodyBytes` 这些上限是这套模型的一部分：它们在解析之前就把过大的输入挡掉。

## 带走这三样

- 用 `formats.Text` 或 `formats.Buffer` 指定 `As` 读写的格式。文件可以缺失时先调用 `Location.readOptionalBytes`，再解码已有内容。
- 路径是逻辑位置，`file:` 和 `https:` 是不同 provider；引用在解析时才和当前上下文结合。
- HTTP 错误状态不抛异常，`request` 要看 `response.ok`；`fetchAs` 把“请求 + 检查 + 解码”合成一步。

## 下一站：图形界面

> 数据能在终端里读写之后，下一步是让它出现在窗口里。EL 的界面用什么描述，又为什么不是 HTML？

- 主推进：[图形界面](gui.md)：对象图、两种建界面入口、事件与定时器。
- 想先练手：[命令行工具](../practice/cli-tool.md)：把文件读写、参数和退出码串成一个工具。
- 后面会用到：[错误处理与异步](../language/errors-async.md)：超时、状态码和解析失败的类型与捕获写法。
