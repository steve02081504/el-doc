# formats/delimited-text/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [CsvRowWriter.writeBatch](#api-7e1dbba9af5c9b6c1b6b)

## 分隔文本 {#api-7a8d075e6bc770430c89}

源码：`src/stdlib/formats/delimited-text/index.el:2` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L2)

提供 RFC 4180 风格 CSV 与制表符分隔文本的解析和编码。

## CsvRowWriter {#api-ed8b9a1c196cad0dc6d6}

源码：`src/stdlib/formats/delimited-text/index.el:109` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L109)

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

源码：`src/stdlib/formats/delimited-text/index.el:124` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L124)

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

源码：`src/stdlib/formats/delimited-text/index.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L140)

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
