# formats/json/writer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## JSON 编码 {#api-77c89b399f4b08f225be}

源码：`src/stdlib/formats/json/writer.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/writer.el#L1)

将受支持的 EL 值编码为 JSON 文本，并支持受限输出与 JSON Lines。

## writeJSON {#api-9d180199328600f27fc7}

源码：`src/stdlib/formats/json/writer.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/writer.el#L183)

将 EL 值编码为严格 JSON 文本，并按给定限制控制递归与输出规模。

```el
export fn writeJSON(value: any, limits: JsonLimits = JsonLimits()): Text
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

**参数**：value 要编码的值；可编码类型受 JSON 数据模型约束。

**参数**：limits 深度、字节数等编码资源限制。

**返回值**：JSON 文本。

**失败与异常**：值不可编码、存在循环引用或超过限制时抛出 JsonWriteError。

### 示例：编码对象

```el
import { writeJSON } from "el:formats/json/"
let json = writeJSON(@{ name: "EL", count: 3 })
console.stdout.writeLine(json)
```
