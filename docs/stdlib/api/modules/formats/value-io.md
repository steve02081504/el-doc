# formats/value-io.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/formats.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 格式值读写 {#api-af355377b4ec9c76f856}

源码：`src/stdlib/formats/value-io.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/value-io.el#L1)

按格式读写内存中的文本或字节。

## parseAs {#api-ea08b9e7893fb3fb521d}

源码：`src/stdlib/formats/value-io.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/value-io.el#L11)

使用所选格式读取内存里的文本或字节。

```el-signature
export fn parseAs(format, source: Text)
```

### 示例：从已有的 JSON 文本读取值

```el
import { parseAs, formats } from "el:formats/"
let value = parseAs(formats.JSON, "{\"enabled\":true}")
```

## serializeAs {#api-f5c7b4e7bf5e8f2e2a57}

源码：`src/stdlib/formats/value-io.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/value-io.el#L21)

将值写入内存。文本格式返回 Text，二进制格式返回字节数组。

```el-signature
export fn serializeAs(format, value)
```

### 示例：把值写成 JSON 文本

```el
import { serializeAs, formats } from "el:formats/"
let source = serializeAs(formats.JSON, @{ enabled: t })
```
