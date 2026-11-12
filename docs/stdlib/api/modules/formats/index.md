# formats/index.el

本页由源码注释生成；示例未运行验证。

## 文件格式 {#api-06411e5ab51d129e868f}

源码：`src/stdlib/formats/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L1)

提供可复用的文本与字节格式对象，以及 JSON、YAML、TOML、CSV 等格式入口。

## TextFormat {#api-c603856b0e561e7ac3e8}

源码：`src/stdlib/formats/index.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L44)

```el
export fn TextFormat(output: type, input: type = output): type
```

创建文本格式对象，按需解码文本，并可选提供反向编码器。

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

源码：`src/stdlib/formats/index.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L115)

```el
get Text()
```

返回按 UTF-8 读取和写入原样文本的格式对象。

### 示例：将文本格式写入文件

```el
import { formats } from "el:formats/"
import { writeFileAs } from "el:filesystem/"
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

## Formats.JSON {#api-82a6375e413cd8e3c5b0}

源码：`src/stdlib/formats/index.el:125` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L125)

```el
get JSON()
```

返回严格 JSON 格式对象；支持 JSON 解码与编码。

### 示例：读取 JSON 文件

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.JSON, "file:./config.json")
```

## Formats.YAML {#api-b651a1c802ea9634a3bd}

源码：`src/stdlib/formats/index.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L137)

```el
get YAML()
```

返回 YAML 文本解码格式；当前对象只提供解码器。

### 示例：读取 YAML 配置

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.YAML, "file:./config.yaml")
```

## Formats.CSV {#api-1489e37be5f3818f494f}

源码：`src/stdlib/formats/index.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L148)

```el
get CSV()
```

返回 CSV 表格解码格式，解析结果为文本单元格二维数组。

### 示例：读取 CSV 文件

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let rows = readFileAs(formats.CSV, "file:./table.csv")
```

## formats {#api-a357aae7f29cecb69598}

源码：`src/stdlib/formats/index.el:166` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/index.el#L166)

```el
export const formats
```

标准格式对象集合，提供 Text、JSON、YAML、CSV 等格式值。

### 示例：选择 JSON 解码器

```el
import { formats } from "el:formats/"
import { readFileAs } from "el:filesystem/"
let config = readFileAs(formats.JSON, "file:./config.json")
```
