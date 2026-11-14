# formats/ini/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## INI {#api-5b373451fbea9ce8c4c7}

源码：`src/stdlib/formats/ini/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/ini/index.el#L1)

解析本模块定义的轻量 INI 方言。

## parseINI {#api-e4172fc09fb95d53c347}

源码：`src/stdlib/formats/ini/index.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/ini/index.el#L33)

解析轻量 INI 方言，生成嵌套动态对象，键和值均保持文本。
节名和键区分大小写；键值以 `=` 或 `:` 分隔，`;` 或 `#` 开头的整行是注释。
值按字面文本读取，不转换数字或布尔值，也不解析行内注释；重复节合并，重复键以最后一个值为准。

```el
export fn parseINI(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

**参数**：source 完整 INI 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：根对象；节名映射到节对象，键映射到文本值。

**失败与异常**：语法无效、标量与节冲突或超出限制时抛出解析异常。

### 示例：读取 INI 节

```el
import { parseINI } from "el:formats/ini/"
let settings = parseINI("[server]\nport=8080")
```

## writeINI {#api-d2152ba4c73076d311c6}

源码：`src/stdlib/formats/ini/index.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/ini/index.el#L115)

将根对象的文本字段和一层节对象编码为轻量 INI；根键先于各节输出。
不保留原注释或排版；不转换非文本值，不静默去除空白或换行。

```el
export fn writeINI(value: any, limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：value 动态对象或公开数据对象；节内字段必须为文本。

**参数**：limits 输出字节数与编码资源限制。

**返回值**：可由 parseINI 读取的文本。

**失败与异常**：名称、值或嵌套结构无法无损表示时抛出 FormatWriteError；资源超限也会失败。

### 示例：写出配置

```el
import { writeINI, parseINI } from "el:formats/ini/"
let text = writeINI(parseINI("name=demo\n[server]\nport=8080\n"))
```
