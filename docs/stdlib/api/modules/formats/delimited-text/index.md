# formats/delimited-text/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [CsvRowWriter.writeBatch](#api-7e1dbba9af5c9b6c1b6b)

## 分隔文本 {#api-7a8d075e6bc770430c89}

源码：`src/stdlib/formats/delimited-text/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L1)

提供 RFC 4180 风格 CSV 与制表符分隔文本的解析和编码。

## parseCSV {#api-a8e5bd5c6af9392c0c0c}

源码：`src/stdlib/formats/delimited-text/index.el:65` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L65)

按 RFC 4180 引号规则解析逗号分隔文本；单元格保持为文本，不推断表头或类型。

```el-signature
export fn parseCSV(source: Text, limits: JsonLimits = JsonLimits()): Text[][]
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)[][]

**参数**：source 完整 CSV 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：每行对应一个文本数组的二维数组。

**失败与异常**：引号、分隔符、换行无效或超出限制时抛出解析异常。

### 示例：解析两列 CSV

```el
import { parseCSV } from "el:formats/delimited-text/"
let rows = parseCSV("name,role\nAda,engineer")
```

## parseTSV {#api-6b18fbbb8111d0a23c0e}

源码：`src/stdlib/formats/delimited-text/index.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L77)

按制表符分隔规则解析文本，单元格内容以文本形式保留。

```el-signature
export fn parseTSV(source: Text, limits: JsonLimits = JsonLimits()): Text[][]
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)[][]

**参数**：source 完整 TSV 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：每行对应一个文本数组的二维数组。

**失败与异常**：引号、分隔符、换行无效或超出限制时抛出解析异常。

### 示例：解析制表符分隔数据

```el
import { parseTSV } from "el:formats/delimited-text/"
let rows = parseTSV("name\trole\nAda\tengineer")
```

## writeDelimited {#api-c6f0fe52fab397d738da}

源码：`src/stdlib/formats/delimited-text/index.el:93` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L93)

编码文本行数组；含分隔符、引号或换行的单元格加引号，内部引号双写。

```el-signature
export fn writeDelimited(rows: Text[][], delimiter: Text = ",", limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：rows 文本单元格二维数组；每行至少有一个单元格。

**参数**：delimiter 单个标量分隔符，不能是引号、CR 或 LF。

**参数**：limits 输出字节数与编码资源限制。

**返回值**：以 CRLF 结束每条记录的分隔文本；空表返回空文本。

**失败与异常**：分隔符无效、空行数组不可表示或资源超限时失败。

### 示例：编码分号分隔的表格

```el
import { writeDelimited } from "el:formats/delimited-text/"
let text = writeDelimited(@[@["name", "role"], @["Ada", "engineer"]], ";")
```

## writeCSV {#api-6923a298b8fb07b04435}

源码：`src/stdlib/formats/delimited-text/index.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L138)

将文本单元格二维数组编码为 RFC 4180 风格 CSV，不添加表头或推断类型。

```el-signature
export fn writeCSV(rows: Text[][], limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：rows 每行至少包含一个文本单元格；空表允许。

**参数**：limits 输出与编码资源限制。

**返回值**：逗号分隔、CRLF 记录结束的文本。

**失败与异常**：不可表示的空行数组或资源超限时失败。

### 示例：写出 CSV

```el
import { writeCSV } from "el:formats/delimited-text/"
let text = writeCSV(@[@["name", "role"], @["Ada", "engineer"]])
```

## writeTSV {#api-26c2444ceca591f8fbee}

源码：`src/stdlib/formats/delimited-text/index.el:151` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L151)

将文本单元格二维数组编码为制表符分隔文本，使用与 CSV 相同的引号规则。

```el-signature
export fn writeTSV(rows: Text[][], limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：rows 每行至少包含一个文本单元格；空表允许。

**参数**：limits 输出与编码资源限制。

**返回值**：制表符分隔、CRLF 记录结束的文本。

**失败与异常**：不可表示的空行数组或资源超限时失败。

### 示例：写出 TSV

```el
import { writeTSV } from "el:formats/delimited-text/"
let text = writeTSV(@[@["name", "role"], @["Ada", "engineer"]])
```

## CsvRowWriter {#api-ed8b9a1c196cad0dc6d6}

源码：`src/stdlib/formats/delimited-text/index.el:164` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L164)

持有一个 CSV 输出流。每次写入按 UTF-8 追加一批完整的 CRLF 记录。

```el-signature
export @assign(mode: "shared") class CsvRowWriter
```

### 示例：逐批写入一条 CSV 记录

```el
import { openCSVWriter } from "el:formats/delimited-text/index.el"
let writer = openCSVWriter("output.csv")
writer.writeBatch(@[@["name", "Ada"]])
writer.close()
```

## CsvRowWriter.writeBatch {#api-7e1dbba9af5c9b6c1b6b}

源码：`src/stdlib/formats/delimited-text/index.el:179` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L179)

编码并写出一批记录。编码限制按批应用，批内编码成功后才开始写入。

```el-signature
fn writeBatch(rows: Text[][], limits: JsonLimits = JsonLimits()): nil_t
```

**返回类型**：[`nil_t`](../../language/values.md#api-86357ad50ef0535f6333)

**参数**：rows 文本字段组成的记录。

**参数**：limits 本批的输出字节数与编码资源限制。

**失败与异常**：编码、I/O 或写入状态错误；I/O 失败可能已写出字节前缀。

### 示例：写入一批 CSV 记录

```el
import { openCSVWriter } from "el:formats/delimited-text/index.el"
let writer = openCSVWriter("output.csv")
writer.writeBatch(@[@["name", "Ada"]])
writer.close()
```

## openCSVWriter {#api-6bc989c7af5ed7660d74}

源码：`src/stdlib/formats/delimited-text/index.el:195` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L195)

创建或截断目标文件并打开 UTF-8 CSV 写入器。调用方应在完成后关闭。

```el-signature
export fn openCSVWriter(reference): CsvRowWriter
```

**返回类型**：[`CsvRowWriter`](index.md#api-ed8b9a1c196cad0dc6d6)

**参数**：reference 文件路径或可解析的位置引用。

**返回值**：逐批写入 CSV 的写入器。

### 示例：打开 CSV 文件并关闭写入器

```el
import { openCSVWriter } from "el:formats/delimited-text/index.el"
let writer = openCSVWriter("output.csv")
writer.close()
```
