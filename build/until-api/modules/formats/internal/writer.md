# formats/internal/writer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## FormatWriteError {#api-c764748c8516ed415ecb}

源码：`src/stdlib/formats/internal/writer.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/internal/writer.el#L14)

表示值无法无损编码为所选文本格式，或输出超过字节限制。

```el
export @assign(mode: "copy") class FormatWriteError extends Error
```

### 示例：捕获格式写入错误

```el
import { FormatWriteError, writeINI } from "el:formats/"
try { discard(writeINI(@{ value: "two\nlines" })) }
catch (error: FormatWriteError) { console.error.value(error) }
```
