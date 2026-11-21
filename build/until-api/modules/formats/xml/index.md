# formats/xml/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## XML {#api-797d9c3d02dc77067666}

源码：`src/stdlib/formats/xml/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/xml/index.el#L1)

解析受限 XML 文档并保留节点结构。

## parseXML {#api-73adee4c1adc13b296b2}

源码：`src/stdlib/formats/xml/index.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/xml/index.el#L158)

解析受限的 XML 文档，保留元素、文本、CDATA、注释和处理指令节点。

```el
export fn parseXML(source: Text, limits: JsonLimits = JsonLimits()): XmlDocument
```

**返回类型**：[`XmlDocument`](../../../types.md#api-a9b268230a0106556c55)

**参数**：source 完整 XML 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：包含声明属性和顶层节点的 XmlDocument。

**失败与异常**：XML 语法无效、包含 DTD/实体声明或超出限制时抛出解析异常。

### 示例：解析 XML 根节点

```el
import { parseXML } from "el:formats/xml/"
let document = parseXML("<message>hello</message>")
```

## writeXML {#api-57cd03717e66684e353a}

源码：`src/stdlib/formats/xml/index.el:270` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/xml/index.el#L270)

将 XML 文档编码为 XML 1.0 文本，并验证节点、声明和文档结构。

```el
export fn writeXML(value: XmlDocument, limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：value 要编码的文档。

**参数**：limits 输出字节、深度和工作预算。

**返回值**：UTF-8 XML 文本。

**失败与异常**：文档不可表示、结构无效或超出限制时抛出异常。

### 示例：编码文档

```el
import { parseXML, writeXML } from "el:formats/xml/"
let text = writeXML(parseXML("<message>hello</message>"))
```
