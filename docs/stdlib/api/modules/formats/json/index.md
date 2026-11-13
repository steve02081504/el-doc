# formats/json/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## JSON 解码 {#api-7ea00058a6d26927fcd0}

源码：`src/stdlib/formats/json/index.el:2` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/index.el#L2)

将严格 JSON 文本解析为 EL 的动态对象、数组、文本、数值与布尔/空值。

## parseJSON {#api-c4f131a4d226bac61cce}

源码：`src/stdlib/formats/json/index.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/index.el#L138)

```el
export fn parseJSON(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：`any`

将完整严格 JSON 文本解析为 EL 值，并应用输入字节数与解析资源限制。

**参数**：source 待解析的 JSON 文本。

**参数**：limits JSON 输入和解析限制。

**返回值**：对象、数组、文本、数值或对应布尔/空值。

**失败与异常**：JSON 无效、重复键策略拒绝输入或超过限制时抛出 ParseError 或限制异常。

### 示例：解析配置对象

```el
import { parseJSON } from "el:formats/json/"
let config = parseJSON("{\"name\":\"EL\"}")
```

## jsonField {#api-aa387b2b22b62084db00}

源码：`src/stdlib/formats/json/index.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/index.el#L161)

```el
export fn jsonField(value: any, key: Text): any
```

**返回类型**：`any`

从 JSON 对象中按名称读取成员。

**参数**：value 由 parseJSON 产生的 JSON 对象。

**参数**：key 成员名称。

**返回值**：对应成员的值。

**失败与异常**：value 不是对象或对象中没有该成员时抛出 ParseError。

### 示例：读取配置名称

```el
import { jsonField, parseJSON } from "el:formats/json/"
let name = jsonField(parseJSON("{\"name\":\"EL\"}"), "name")
console.stdout.writeLine(name)
```
