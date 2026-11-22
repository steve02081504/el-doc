# formats/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/formats.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Formats.Text](#api-f86695e611fe3e71fa9d)
- [Formats.JSON](#api-82a6375e413cd8e3c5b0)
- [Formats.YAML](#api-b651a1c802ea9634a3bd)
- [Formats.TOML](#api-164a5d9b563b6f25f9d5)
- [Formats.XML](#api-628fee3513a3531d0e12)
- [Formats.CSV](#api-1489e37be5f3818f494f)
- [Formats.TSV](#api-318f5a03d7a4da9c00e9)
- [Formats.INI](#api-b61644417a01eaaa15ee)
- [Formats.EOL](#api-88f51cd42742b14a0df6)
- [Formats.EOD](#api-9ebcb5f224a4de1a6115)

## 文件格式 {#api-06411e5ab51d129e868f}

源码：`src/stdlib/formats/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L1)

提供可复用的文本与字节格式对象，以及 JSON、YAML、TOML、CSV 等格式入口。

## TextFormat {#api-c603856b0e561e7ac3e8}

源码：`src/stdlib/formats/index.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L49)

创建文本格式对象，按需解码文本，并可选提供反向编码器。

```el-fragment
export fn TextFormat(output: type, input: type = output): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：output 解码后的值类型。

**参数**：input 可编码输入类型，默认与 output 相同。

**返回值**：支持 inputByteLimit、decode 与可选 encode 的格式对象类型。

### 示例：创建只解码的 JSON 格式

```el
import { TextFormat } from "el:formats/"
import { JsonLimits, parseJSON } from "el:formats/json/"
let jsonFormat = TextFormat<output: any>((source: Text, limits: JsonLimits) => parseJSON(source, limits))
```

## Formats.Text {#api-f86695e611fe3e71fa9d}

源码：`src/stdlib/formats/index.el:135` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L135)

返回按 UTF-8 读取和写入原样文本的格式对象。

```el-fragment
get Text()
```

### 示例：将文本格式写入文件

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

## Formats.JSON {#api-82a6375e413cd8e3c5b0}

源码：`src/stdlib/formats/index.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L145)

返回严格 JSON 格式对象；支持 JSON 解码与编码。

```el-fragment
get JSON()
```

### 示例：读取 JSON 文件

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.JSON, "file:./config.json")
```

## Formats.YAML {#api-b651a1c802ea9634a3bd}

源码：`src/stdlib/formats/index.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L161)

返回 YAML 文本读写格式；编码输出流式集合，不保留注释或排版。

```el-fragment
get YAML()
```

### 示例：读取 YAML 配置

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.YAML, "file:./config.yaml")
```

## Formats.TOML {#api-164a5d9b563b6f25f9d5}

源码：`src/stdlib/formats/index.el:172` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L172)

返回保留 TOML 值类型的读写格式，写入根值须为 Toml.Table。

```el-fragment
get TOML()
```

### 示例：写出 TOML

```el
import { formats, parseTOML } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
let value = parseTOML("port = 8080")
writeFileAs(formats.TOML, "file:./config.toml", value)
```

## Formats.XML {#api-628fee3513a3531d0e12}

源码：`src/stdlib/formats/index.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L183)

返回 XmlDocument 文档读写格式。

```el-fragment
get XML()
```

### 示例：写出 XML

```el
import { formats, parseXML } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
let value = parseXML("<message>hello</message>")
writeFileAs(formats.XML, "file:./message.xml", value)
```

## Formats.CSV {#api-1489e37be5f3818f494f}

源码：`src/stdlib/formats/index.el:192` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L192)

返回 CSV 表格读写格式，单元格使用文本，编码使用 CRLF 记录结束。

```el-fragment
get CSV()
```

### 示例：读取 CSV 文件

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let rows = readFileAs(formats.CSV, "file:./table.csv")
```

## Formats.TSV {#api-318f5a03d7a4da9c00e9}

源码：`src/stdlib/formats/index.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L201)

返回制表符分隔文本读写格式；单元格使用文本。

```el-fragment
get TSV()
```

### 示例：写出 TSV

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.TSV, "file:./table.tsv", @[@["name", "role"], @["Ada", "engineer"]])
```

## Formats.INI {#api-b61644417a01eaaa15ee}

源码：`src/stdlib/formats/index.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L216)

返回轻量 INI 方言的文本读写格式；编码拒绝无法无损表示的名称、值和嵌套结构。

```el-fragment
get INI()
```

### 示例：读取 INI 配置

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.INI, "file:./config.ini")
```

### 示例：写出 INI 配置

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.INI, "file:./config.ini", @{ name: "demo", server: @{ port: "8080" } })
```

## Formats.EOL {#api-88f51cd42742b14a0df6}

源码：`src/stdlib/formats/index.el:226` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L226)

返回自包含 EOL 文本读写格式；节点、深度和整数限制用于解码，字节上限也在编码完成后检查。

```el-fragment
get EOL()
```

### 示例：写出 EOL

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.EOL, "file:./value.eol", @[1, 2, 3])
```

## Formats.EOD {#api-9ebcb5f224a4de1a6115}

源码：`src/stdlib/formats/index.el:235` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L235)

返回自包含 EOD 二进制读写格式；节点、深度和整数限制用于解码，字节上限也在编码完成后检查。

```el-fragment
get EOD()
```

### 示例：写出 EOD

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.EOD, "file:./value.eod", @[1, 2, 3])
```

## formats {#api-a357aae7f29cecb69598}

源码：`src/stdlib/formats/index.el:255` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L255)

标准格式对象集合，提供 Text、JSON、YAML、CSV 等格式值。

```el-fragment
export const formats = Formats()
```

**类型**：[`Formats`](../../types.md#api-6768ac9ca087f5de0440)

### 示例：选择 JSON 解码器

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.JSON, "file:./config.json")
```
