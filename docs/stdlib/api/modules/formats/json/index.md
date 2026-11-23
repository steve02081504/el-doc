# formats/json/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## JSON 解码 {#api-7ea00058a6d26927fcd0}

源码：`src/stdlib/formats/json/index.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/index.el#L6)

将严格 JSON 文本解析为 EL 的动态对象、数组、文本、数值与布尔/空值。

## jsonField {#api-aa387b2b22b62084db00}

源码：`src/stdlib/formats/json/index.el:152` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/index.el#L152)

从 JSON 对象中按名称读取成员。

```el-signature
export fn jsonField(value: any, key: Text): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

**参数**：value JSON 对象。

**参数**：key 成员名称。

**返回值**：对应成员的值。

**失败与异常**：value 不是对象或对象中没有该成员时抛出 ParseError。

### 示例：读取配置名称

```el
import { jsonField } from "el:formats/json/"
import { formats, parseAs } from "el:formats/"
let name = jsonField(parseAs(formats.JSON, "{\"name\":\"EL\"}"), "name")
console.stdout.writeLine(name)
```
