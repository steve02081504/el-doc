# filesystem/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文件系统 {#api-8338b2740fc177d87b85}

源码：`src/stdlib/filesystem/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L1)

提供逻辑路径解析、文件读写、目录操作和文本/字节转换入口。

## resolvePath {#api-2c3e211bba2a57b4ba86}

源码：`src/stdlib/filesystem/index.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L34)

将路径或 provider 引用解析为当前文件系统上下文中的逻辑位置。

```el-signature
export fn resolvePath(reference): Location
```

**返回类型**：[`Location`](../../types.md#api-547a9b261b17d994f444)

**参数**：reference 相对路径、绝对 file 引用或已注册 provider 的引用。

**返回值**：带有 provider 身份的 Location。

**失败与异常**：引用无法由当前上下文解析时抛出异常。

### 示例：解析配置文件位置

```el
import { resolvePath } from "el:filesystem/"
let config = resolvePath("file:./config.json")
```

## currentDirectory {#api-74f08b3b759d683d084e}

源码：`src/stdlib/filesystem/index.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L44)

返回当前逻辑文件系统上下文的位置。

```el-signature
export fn currentDirectory(): Location
```

**返回类型**：[`Location`](../../types.md#api-547a9b261b17d994f444)

**返回值**：当前工作目录的 Location。

### 示例：显示逻辑工作目录

```el
import { currentDirectory } from "el:filesystem/"
console.stdout.writeLine(currentDirectory().identifier)
```

## resolveFrom {#api-163ed262fe20828c9ad6}

源码：`src/stdlib/filesystem/index.el:55` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L55)

先解析基准位置，再以该位置为上下文解析另一个引用。

```el-signature
export fn resolveFrom(base, reference): Location
```

**返回类型**：[`Location`](../../types.md#api-547a9b261b17d994f444)

**参数**：base 基准路径或位置。

**参数**：reference 相对于基准位置的引用。

**返回值**：解析后的 Location。

### 示例：从配置目录解析资源

```el
import { resolveFrom } from "el:filesystem/"
let resource = resolveFrom("file:./config", "assets/logo.png")
```

## fileName {#api-0ed89f254561e8445dfb}

源码：`src/stdlib/filesystem/index.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L68)

返回给定位置的末级名称。

```el-signature
export fn fileName(reference): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

**参数**：reference 路径或位置引用。

**返回值**：文件或目录名称。

### 示例：读取文件名

```el
import { fileName } from "el:filesystem/"
console.stdout.writeLine(fileName("file:./config.json"))
```

## openFileReader {#api-c23461742bf817d5cab2}

源码：`src/stdlib/filesystem/index.el:82` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L82)

为逻辑位置打开顺序读取器；需要随机访问时使用 openRandomFileReader。

```el-signature
export fn openFileReader(reference, lock: Bool | nil_t = nil): FileReader
```

**返回类型**：[`FileReader`](../../types.md#api-3152ff28a38c0533af33)

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**返回值**：打开的 FileReader。

**失败与异常**：位置解析或打开失败时抛出文件系统异常。

### 示例：打开文件读取器

```el
import { openFileReader } from "el:filesystem/"
let reader = openFileReader("file:./logo.png")
let bytes = reader.read(8kd)
reader.close()
```

## openRandomFileReader {#api-ad810a684ec6f474efc0}

源码：`src/stdlib/filesystem/index.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L96)

打开支持随机访问的文件读取器。

```el-signature
export fn openRandomFileReader(reference, lock: Bool | nil_t = nil): FileReader
```

**返回类型**：[`FileReader`](../../types.md#api-3152ff28a38c0533af33)

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**返回值**：可读取并定位的 FileReader。

**失败与异常**：位置解析、打开或随机访问能力不可用时抛出文件系统异常。

### 示例：按需读取文件内容

```el
import { openRandomFileReader } from "el:filesystem/"
let reader = openRandomFileReader("file:./archive.bin")
let prefix = reader.readAt(0dit, FileSize.fromAddressUnits(8))
reader.close()
```

## openFileWriter {#api-941828b08ea8e39ace73}

源码：`src/stdlib/filesystem/index.el:109` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L109)

为逻辑位置打开文件写入器。

```el-signature
export fn openFileWriter(reference): FileWriter
```

**返回类型**：[`FileWriter`](../../types.md#api-4abf891ad64ec031618d)

**参数**：reference 目标文件或 provider 位置引用。

**返回值**：打开的 FileWriter。

**失败与异常**：位置解析或写入器创建失败时抛出异常。

### 示例：打开文件写入器

```el
import { openFileWriter } from "el:filesystem/"
let writer = openFileWriter("file:./output.bin")
writer.write(@[72, 105])
writer.close()
```

## readFileBuffer {#api-92cbab09967c14d143de}

源码：`src/stdlib/filesystem/index.el:123` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L123)

将文件内容读入拥有其底层存储的 FileBuffer，可设置字节上限。

```el-signature
export fn readFileBuffer(reference, maximumSize: FileSize | nil_t = nil): FileBuffer
```

**返回类型**：[`FileBuffer`](../../types.md#api-46bf41868bd77b4bb737)

**参数**：reference 文件或 provider 位置引用。

**参数**：maximumSize 可选最大字节数。

**返回值**：调用方负责关闭的 FileBuffer。

**失败与异常**：读取失败、超出显式上限或 provider 违反上限时抛出异常。

### 示例：读取并释放文件缓冲区

```el
import { readFileBuffer } from "el:filesystem/"
let buffer = readFileBuffer("file:./image.bin")
let size = buffer.count
buffer.close()
```

## readFileAs {#api-cff0ea6ed476cb036085}

源码：`src/stdlib/filesystem/index.el:160` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L160)

读取文件字节并使用指定格式解码。

```el-signature
export fn readFileAs(format, reference, lock: Bool | nil_t = nil, maximumSize: FileSize | nil_t = nil)
```

**参数**：format 提供 decode 方法的格式对象。

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**参数**：maximumSize 可选的最大读取字节数，与格式自身的限制同时生效。

**返回值**：格式解码得到的值。

**失败与异常**：文件读取失败、超出字节限制或格式解码失败时抛出异常。

### 示例：读取 JSON 文件

```el
import { readFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
let config = readFileAs(formats.JSON, "file:./config.json")
```

### 示例：在指定字节上限内读取 UTF-8 文本

```el
import { readFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
let notes = readFileAs(formats.Text, "file:./notes.txt", maximumSize: 32kd)
```

## writeFileAs {#api-5ea2e001353e67ba555f}

源码：`src/stdlib/filesystem/index.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L201)

使用指定格式编码完整内容。provider 能安全比较时，只写变化的区间，必要时调整文件长度。

```el-signature
export fn writeFileAs(format, reference, value): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：format 提供 encode 方法的格式对象。

**参数**：reference 目标文件或 provider 位置引用。

**参数**：value 要编码的值。

**返回值**：写入的字节数。

**失败与异常**：文件写入失败，或格式不提供编码器时抛出异常。

### 示例：写入纯文本文件

```el
import { writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
writeFileAs(formats.Text, "file:./copy.txt", "already text")
```

## directoryNames {#api-2e6df4d53b39fb02da5d}

源码：`src/stdlib/filesystem/index.el:219` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L219)

列出逻辑目录中的名称。

```el-signature
export fn directoryNames(reference): Text[]
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)[]

**参数**：reference 目录路径或位置引用。

**返回值**：目录项名称数组。

**失败与异常**：位置不是可列举目录或 provider 不支持列举时抛出异常。

### 示例：列出目录

```el
import { directoryNames } from "el:filesystem/"
for (let name in directoryNames("file:./config")) console.stdout.writeLine(name)
```

## exists {#api-d5557a390b8cdcda4bc0}

源码：`src/stdlib/filesystem/index.el:234` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L234)

查询逻辑位置当前是否存在。与同一路径的单条 writeFileAs 搭配时，条件由只打开已有文件的结果决定。

```el-signature
@optimize(using: optimizeFileExists, region: "guarded-call", data: @{ writer: writeFileAs, discard: discard, apply: writeFileIfExisting })
export fn exists(reference): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：reference 文件或 provider 位置引用。

**返回值**：位置存在时为真。

**失败与异常**：位置解析、能力查询或原生检查失败时抛出异常。

### 示例：仅写入已存在的文件

```el
import { exists, writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
let path = "file:./settings.txt"
if (exists(path)) { discard(writeFileAs(formats.Text, path, "updated")) }
```

## isDirectory {#api-f293d8e1a091e956afb7}

源码：`src/stdlib/filesystem/index.el:246` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L246)

判断逻辑位置是否为目录。

```el-signature
export fn isDirectory(reference): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：reference 路径或位置引用。

**返回值**：位置为目录时为真。

### 示例：检查父路径

```el
import { isDirectory, resolvePath } from "el:filesystem/"
console.stdout.writeLine(isDirectory(resolvePath("file:./config.json").parent))
```

## makeDirectories {#api-e81e7c2a8174ea07561d}

源码：`src/stdlib/filesystem/index.el:256` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L256)

创建指定目录及其尚不存在的父目录。

```el-signature
export fn makeDirectories(reference): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：reference 目标目录路径或位置引用。

**失败与异常**：provider 不支持创建目录或操作失败时抛出异常。

### 示例：创建输出目录

```el
import { makeDirectories } from "el:filesystem/"
makeDirectories("file:./output/reports")
```

## removeFile {#api-9fe2fe3278290a7205a1}

源码：`src/stdlib/filesystem/index.el:266` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L266)

删除指定文件。

```el-signature
export fn removeFile(reference): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：reference 文件路径或位置引用。

**失败与异常**：目标不能删除或 provider 操作失败时抛出异常。

### 示例：删除临时文件

```el
import { removeFile } from "el:filesystem/"
removeFile("file:./temporary.txt")
```

## replaceFile {#api-801d5c08c7f9a46b97dd}

源码：`src/stdlib/filesystem/index.el:277` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L277)

将源文件原子替换到目标位置。

```el-signature
export fn replaceFile(source, target): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：source 已存在的源文件路径。

**参数**：target 替换目标路径。

**失败与异常**：provider 不支持替换或替换失败时抛出异常。

### 示例：发布生成文件

```el
import { replaceFile } from "el:filesystem/"
replaceFile("file:./report.tmp", "file:./report.txt")
```

## moveFile {#api-db9fedfc31e75c79a968}

源码：`src/stdlib/filesystem/index.el:292` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L292)

在同一 provider 内移动源文件。如果目标已存在就原子替换。

```el-signature
export fn moveFile(source, target): nil_t
```

**返回类型**：[`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：source 已存在的源位置。

**参数**：target 移动目标位置。

**失败与异常**：provider 不支持原子移动或移动失败时抛出异常。

### 示例：移动已生成的文件

```el
import { moveFile } from "el:filesystem/"
moveFile("file:./draft.txt", "file:./final.txt")
```

## copyFile {#api-3600e50270be961b4bb9}

源码：`src/stdlib/filesystem/index.el:305` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L305)

将源文件内容复制到目标位置。

```el-signature
export fn copyFile(source, target): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：source 源文件路径。

**参数**：target 目标文件路径。

**返回值**：复制的字节数。

**失败与异常**：读取源或写入目标失败时抛出异常。

### 示例：复制文本文件

```el
import { copyFile } from "el:filesystem/"
let copied = copyFile("file:./source.txt", "file:./copy.txt")
console.stdout.writeLine(copied)
```

## publishFileAs {#api-9ade59f34a4d7ffcf8cd}

源码：`src/stdlib/filesystem/index.el:328` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L328)

编码并完整写入暂存文件，关闭成功后原子替换目标。

```el-signature
export fn publishFileAs(format, path, value, temporary = nil): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：format 提供 encode 的文件格式。

**参数**：path 目标位置。

**参数**：value 要编码的值。

**参数**：temporary 可选的 .tmp 首选位置。省略时在目标旁使用完整目标文件名加随机段和 .tmp，例如 report.txt.<随机串>.tmp。指定名称发生碰撞时也在 .tmp 前添加随机段。

**返回值**：发布的字节数。

**失败与异常**：编码、暂存、关闭或替换失败时抛出异常。

### 示例：自动选择暂存文件并发布文本

```el
import { publishFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
publishFileAs(formats.Text, "file:./report.txt", "hello")
```
