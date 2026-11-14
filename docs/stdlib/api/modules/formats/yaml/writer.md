# formats/yaml/writer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## YAML 编码 {#api-e307cfdde09fd50e7286}

源码：`src/stdlib/formats/yaml/writer.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/writer.el#L1)

将受支持的 EL 值编码为 YAML 流式子集文本。

## writeYAML {#api-189d2f47d242742dd0c4}

源码：`src/stdlib/formats/yaml/writer.el:129` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/writer.el#L129)

将公开数据对象、数组和标量编码为可由 parseYAML 读取的 YAML 流式文档。
数值必须能在解析器的数值词素范围内精确表示；共享对象按树展开。

```el
export fn writeYAML(value: any, limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：value 要编码的值，支持 void、Bool、Text、Number、数组、DynamicObject 和可重建的公开数据对象。

**参数**：limits 输出字节、深度及工作预算。

**返回值**：YAML 文本。

**失败与异常**：不支持的值、循环引用、不可精确表示的数值或输出字节超限时抛出 YamlWriteError；其他预算超限抛出 PatternLimitError。

### 示例：编码映射

```el
import { writeYAML } from "el:formats/yaml/"
let document = writeYAML(@{ name: "EL" })
```
