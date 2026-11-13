# formats/delimited-text/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 分隔文本 {#api-7a8d075e6bc770430c89}

源码：`src/stdlib/formats/delimited-text/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L1)

提供 RFC 4180 风格 CSV 与制表符分隔文本解析。

## parseCSV {#api-a8e5bd5c6af9392c0c0c}

源码：`src/stdlib/formats/delimited-text/index.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L59)

```el
export fn parseCSV(source: Text, limits: JsonLimits = JsonLimits()): Text[][]
```

按 RFC 4180 引号规则解析逗号分隔文本；单元格保持为文本，不推断表头或类型。

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

源码：`src/stdlib/formats/delimited-text/index.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/index.el#L71)

```el
export fn parseTSV(source: Text, limits: JsonLimits = JsonLimits()): Text[][]
```

按制表符分隔规则解析文本，单元格内容以文本形式保留。

**参数**：source 完整 TSV 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：每行对应一个文本数组的二维数组。

**失败与异常**：引号、分隔符、换行无效或超出限制时抛出解析异常。

### 示例：解析制表符分隔数据

```el
import { parseTSV } from "el:formats/delimited-text/"
let rows = parseTSV("name\trole\nAda\tengineer")
```
