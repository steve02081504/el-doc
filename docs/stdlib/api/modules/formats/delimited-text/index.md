# formats/delimited-text/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 分隔文本 {#api-7a8d075e6bc770430c89}

源码：`src/stdlib/formats/delimited-text/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L1)

提供 RFC 4180 风格 CSV 与制表符分隔文本的解析和编码。

## parseCSV {#api-a8e5bd5c6af9392c0c0c}

源码：`src/stdlib/formats/delimited-text/index.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L61)

按 RFC 4180 引号规则解析逗号分隔文本；单元格保持为文本，不推断表头或类型。

```el
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

源码：`src/stdlib/formats/delimited-text/index.el:73` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L73)

按制表符分隔规则解析文本，单元格内容以文本形式保留。

```el
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

源码：`src/stdlib/formats/delimited-text/index.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L89)

编码文本行数组；含分隔符、引号或换行的单元格加引号，内部引号双写。

```el
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

源码：`src/stdlib/formats/delimited-text/index.el:133` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L133)

将文本单元格二维数组编码为 RFC 4180 风格 CSV，不添加表头或推断类型。

```el
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

源码：`src/stdlib/formats/delimited-text/index.el:146` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L146)

将文本单元格二维数组编码为制表符分隔文本，使用与 CSV 相同的引号规则。

```el
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
