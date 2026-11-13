# filesystem/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文件系统 {#api-8338b2740fc177d87b85}

源码：`src/stdlib/filesystem/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L1)

提供逻辑路径解析、文件读写、目录操作和文本/字节转换入口。

## resolvePath {#api-2c3e211bba2a57b4ba86}

源码：`src/stdlib/filesystem/index.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L31)

```el
export fn resolvePath(reference): Location
```

将路径或 provider 引用解析为当前文件系统上下文中的逻辑位置。

**参数**：reference 相对路径、绝对 file 引用或已注册 provider 的引用。

**返回值**：带有 provider 身份的 Location。

**失败与异常**：引用无法由当前上下文解析时抛出异常。

### 示例：解析配置文件位置

```el
import { resolvePath } from "el:filesystem/"
let config = resolvePath("file:./config.json")
```

## currentDirectory {#api-74f08b3b759d683d084e}

源码：`src/stdlib/filesystem/index.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L40)

```el
export fn currentDirectory(): Location
```

返回当前逻辑文件系统上下文的位置。

**返回值**：当前工作目录的 Location。

### 示例：显示逻辑工作目录

```el
import { currentDirectory } from "el:filesystem/"
console.stdout.writeLine(currentDirectory().identifier)
```

## resolveFrom {#api-163ed262fe20828c9ad6}

源码：`src/stdlib/filesystem/index.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L51)

```el
export fn resolveFrom(base, reference): Location
```

先解析基准位置，再以该位置为上下文解析另一个引用。

**参数**：base 基准路径或位置。

**参数**：reference 相对于基准位置的引用。

**返回值**：解析后的 Location。

### 示例：从配置目录解析资源

```el
import { resolveFrom } from "el:filesystem/"
let resource = resolveFrom("file:./config", "assets/logo.png")
```

## parentPath {#api-b73b697330965f107109}

源码：`src/stdlib/filesystem/index.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L64)

```el
export fn parentPath(reference): Location
```

返回给定位置的父目录 Location。

**参数**：reference 路径或位置引用。

**返回值**：父目录位置。

### 示例：读取配置目录

```el
import { parentPath } from "el:filesystem/"
let directory = parentPath("file:./config.json")
```

## fileName {#api-0ed89f254561e8445dfb}

源码：`src/stdlib/filesystem/index.el:74` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L74)

```el
export fn fileName(reference): Text
```

返回给定位置的末级名称。

**参数**：reference 路径或位置引用。

**返回值**：文件或目录名称。

### 示例：读取文件名

```el
import { fileName } from "el:filesystem/"
console.stdout.writeLine(fileName("file:./config.json"))
```

## openFileReader {#api-c23461742bf817d5cab2}

源码：`src/stdlib/filesystem/index.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L88)

```el
export fn openFileReader(reference, lock: Bool | void_t = void): FileReader
```

为逻辑位置打开顺序读取器；需要随机访问时使用 openRandomFileReader。

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**返回值**：打开的 FileReader。

**失败与异常**：位置解析或打开失败时抛出文件系统异常。

### 示例：打开文件读取器

```el
import { openFileReader } from "el:filesystem/"
let reader = openFileReader("file:./logo.png")
let bytes = reader.read(1024)
reader.close()
```

## openRandomFileReader {#api-ad810a684ec6f474efc0}

源码：`src/stdlib/filesystem/index.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L102)

```el
export fn openRandomFileReader(reference, lock: Bool | void_t = void): FileReader
```

打开支持随机访问的文件读取器。

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**返回值**：可读取并定位的 FileReader。

**失败与异常**：位置解析、打开或随机访问能力不可用时抛出文件系统异常。

### 示例：按需读取文件内容

```el
import { openRandomFileReader } from "el:filesystem/"
let reader = openRandomFileReader("file:./archive.bin")
let prefix = reader.readAt(0, 8)
reader.close()
```

## openFileWriter {#api-941828b08ea8e39ace73}

源码：`src/stdlib/filesystem/index.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L115)

```el
export fn openFileWriter(reference): FileWriter
```

为逻辑位置打开文件写入器。

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

## readFileBytes {#api-0fe112b23b7c1bbe2b89}

源码：`src/stdlib/filesystem/index.el:128` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L128)

```el
export fn readFileBytes(reference, maximumBytes: Number | void_t = void): Number[]
```

读取文件原始字节，可选地设置读取上限。

**参数**：reference 文件或 provider 位置引用。

**参数**：maximumBytes 可选的最大读取字节数。

**返回值**：取值为 0 到 255 的字节数组。

**失败与异常**：读取失败或超过限制时抛出异常。

### 示例：读取二进制文件

```el
import { readFileBytes } from "el:filesystem/"
let bytes = readFileBytes("file:./logo.png")
console.stdout.writeLine(bytes.count)
```

## readFileBytesIfPresent {#api-96a7f4f820c29fb04c90}

源码：`src/stdlib/filesystem/index.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L140)

```el
export fn readFileBytesIfPresent(reference, maximumBytes: Number | void_t = void): Number[] | void_t
```

读取文件原始字节；目标不存在时返回 void。

**参数**：reference 文件或 provider 位置引用。

**参数**：maximumBytes 可选的最大读取字节数。

**返回值**：字节数组，或表示缺失的 void。

**失败与异常**：除缺失以外的读取失败或超过限制时抛出异常。

### 示例：可选读取文件

```el
import { readFileBytesIfPresent } from "el:filesystem/"
let bytes = readFileBytesIfPresent("file:./optional.bin")
```

## readTextFileIfPresent {#api-c11e9a934447ba0ec1ac}

源码：`src/stdlib/filesystem/index.el:153` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L153)

```el
export fn readTextFileIfPresent(reference, maximumBytes: Number | void_t = void): Text | void_t
```

读取并解码文本文件；目标不存在时返回 void。

**参数**：reference 文件或 provider 位置引用。

**参数**：maximumBytes 可选的最大读取字节数。

**返回值**：UTF-8 文本，或表示缺失的 void。

**失败与异常**：除缺失以外的读取或 UTF-8 解码失败时抛出异常。

### 示例：使用缺失文件默认值

```el
import { readTextFileIfPresent } from "el:filesystem/"
let text = readTextFileIfPresent("file:./absent.txt")
if (text is void_t) console.stdout.writeLine("missing")
```

## writeFileBytes {#api-b2192b677345809bb08f}

源码：`src/stdlib/filesystem/index.el:169` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L169)

```el
export fn writeFileBytes(reference, bytes: Number[]): Number
```

将字节数组原样写入文件。

**参数**：reference 目标文件或 provider 位置引用。

**参数**：bytes 取值为 0 到 255 的字节数组。

**返回值**：写入的字节数。

**失败与异常**：创建或写入失败时抛出异常。

### 示例：写入二进制文件

```el
import { writeFileBytes } from "el:filesystem/"
writeFileBytes("file:./message.bin", @[72, 105])
```

## readFileBuffer {#api-92cbab09967c14d143de}

源码：`src/stdlib/filesystem/index.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L183)

```el
export fn readFileBuffer(reference, maximumBytes: Number | void_t = void): FileBuffer
```

将文件内容读入拥有其底层存储的 FileBuffer，可设置字节上限。

**参数**：reference 文件或 provider 位置引用。

**参数**：maximumBytes 可选最大字节数。

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

源码：`src/stdlib/filesystem/index.el:213` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L213)

```el
export fn readFileAs(format, reference, lock: Bool | void_t = void)
```

读取文件字节并使用指定格式解码。

**参数**：format 提供 decode 方法的格式对象。

**参数**：reference 文件或 provider 位置引用。

**参数**：lock 可选的读取保护配置。

**返回值**：格式解码得到的值。

**失败与异常**：文件读取或格式解码失败时抛出异常。

### 示例：读取 JSON 文件

```el
import { readFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
let config = readFileAs(formats.JSON, "file:./config.json")
```

## writeFileAs {#api-5ea2e001353e67ba555f}

源码：`src/stdlib/filesystem/index.el:252` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L252)

```el
export fn writeFileAs(format, reference, value): Number
```

使用指定格式编码值并将结果写入文件。

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

## readTextFile {#api-029c59b6a5f88aba0c0a}

源码：`src/stdlib/filesystem/index.el:270` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L270)

```el
export fn readTextFile(reference, maximumBytes: Number | void_t = void): Text
```

读取文件并按 UTF-8 解码为文本。

**参数**：reference 文件路径或可解析的位置引用。

**参数**：maximumBytes 可选的最大读取字节数。

**返回值**：文件的文本内容。

**失败与异常**：文件访问失败、超出限制或字节序列不是有效 UTF-8 时抛出异常。

### 示例：读取配置文本

```el
import { readTextFile } from "el:filesystem/"
let configuration = readTextFile("settings.json")
console.stdout.writeLine(configuration.count)
```

## writeTextFile {#api-19066393ecef9611add1}

源码：`src/stdlib/filesystem/index.el:282` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L282)

```el
export fn writeTextFile(reference, value: Text): Number
```

将文本编码为 UTF-8 并写入文件。

**参数**：reference 目标文件路径或位置引用。

**参数**：value 要写入的文本。

**返回值**：写入的 UTF-8 字节数。

**失败与异常**：文件创建或写入失败时抛出异常。

### 示例：写入配置文本

```el
import { writeTextFile } from "el:filesystem/"
writeTextFile("settings.json", "{}")
```

## directoryNames {#api-2e6df4d53b39fb02da5d}

源码：`src/stdlib/filesystem/index.el:293` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L293)

```el
export fn directoryNames(reference): Text[]
```

列出逻辑目录中的名称。

**参数**：reference 目录路径或位置引用。

**返回值**：目录项名称数组。

**失败与异常**：位置不是可列举目录或 provider 不支持列举时抛出异常。

### 示例：列出目录

```el
import { directoryNames } from "el:filesystem/"
for (let name in directoryNames("file:./config")) console.stdout.writeLine(name)
```

## isDirectory {#api-f293d8e1a091e956afb7}

源码：`src/stdlib/filesystem/index.el:303` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L303)

```el
export fn isDirectory(reference): Bool
```

判断逻辑位置是否为目录。

**参数**：reference 路径或位置引用。

**返回值**：位置为目录时为真。

### 示例：检查父路径

```el
import { isDirectory, parentPath } from "el:filesystem/"
console.stdout.writeLine(isDirectory(parentPath("file:./config.json")))
```

## makeDirectories {#api-e81e7c2a8174ea07561d}

源码：`src/stdlib/filesystem/index.el:313` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L313)

```el
export fn makeDirectories(reference): void_t
```

创建指定目录及其尚不存在的父目录。

**参数**：reference 目标目录路径或位置引用。

**失败与异常**：provider 不支持创建目录或操作失败时抛出异常。

### 示例：创建输出目录

```el
import { makeDirectories } from "el:filesystem/"
makeDirectories("file:./output/reports")
```

## removeFile {#api-9fe2fe3278290a7205a1}

源码：`src/stdlib/filesystem/index.el:323` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L323)

```el
export fn removeFile(reference): void_t
```

删除指定文件。

**参数**：reference 文件路径或位置引用。

**失败与异常**：目标不能删除或 provider 操作失败时抛出异常。

### 示例：删除临时文件

```el
import { removeFile } from "el:filesystem/"
removeFile("file:./temporary.txt")
```

## replaceFile {#api-801d5c08c7f9a46b97dd}

源码：`src/stdlib/filesystem/index.el:334` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L334)

```el
export fn replaceFile(source, target): void_t
```

将源文件原子替换到目标位置。

**参数**：source 已存在的源文件路径。

**参数**：target 替换目标路径。

**失败与异常**：provider 不支持替换或替换失败时抛出异常。

### 示例：发布生成文件

```el
import { replaceFile } from "el:filesystem/"
replaceFile("file:./report.tmp", "file:./report.txt")
```

## copyFile {#api-3600e50270be961b4bb9}

源码：`src/stdlib/filesystem/index.el:351` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/index.el#L351)

```el
export fn copyFile(source, target): Number
```

将源文件内容复制到目标位置。

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
