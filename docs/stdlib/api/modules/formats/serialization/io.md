# formats/serialization/io.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## EOL 与 EOD 文件简写 {#api-83cce906e8a1f13d7af0}

源码：`src/stdlib/formats/serialization/io.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/io.el#L1)

使用 EOL 或 EOD 格式读写文件的简写。

## writeFile {#api-dce886b7156dfdf64882}

源码：`src/stdlib/formats/serialization/io.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/io.el#L14)

将值序列化为 EOD 文件并返回写入字节数。

```el-signature
export fn writeFile(path, value): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：写入 EOD 快照

```el
import { writeFile } from "el:formats/serialization/io.el"
discard(writeFile("file:./snapshot.eod", @[1, 2, 3]))
```

## readFile {#api-3c4981f21f454858a12a}

源码：`src/stdlib/formats/serialization/io.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/io.el#L22)

读取 EOD 文件并反序列化为 EL 值。

```el-signature
export fn readFile(path)
```

### 示例：读取 EOD 快照

```el
import { readFile } from "el:formats/serialization/io.el"
let snapshot = readFile("file:./snapshot.eod")
```

## printFile {#api-69f145632c056e9641a4}

源码：`src/stdlib/formats/serialization/io.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/io.el#L30)

将值序列化为 EOL 文件并返回写入字节数。

```el-signature
export fn printFile(path, value): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：写入 EOL 快照

```el
import { printFile } from "el:formats/serialization/io.el"
discard(printFile("file:./snapshot.eol", @[1, 2, 3]))
```

## scanFile {#api-26698a25bfd82e6f43b6}

源码：`src/stdlib/formats/serialization/io.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/io.el#L38)

读取 EOL 文件并反序列化为 EL 值。

```el-signature
export fn scanFile(path)
```

### 示例：读取 EOL 快照

```el
import { scanFile } from "el:formats/serialization/io.el"
let snapshot = scanFile("file:./snapshot.eol")
```
