# formats/yaml/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## YAML {#api-22f418b16890bb65cf80}

源码：`src/stdlib/formats/yaml/index.el:3` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/index.el#L3)

解析与编码本实现支持的 YAML 文档子集。

## parseYAML {#api-9cc1ddf8a8c4fb2a80f8}

源码：`src/stdlib/formats/yaml/index.el:371` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/index.el#L371)

将受支持的单个 YAML 文档解析为动态对象、数组及标量值。

```el-signature
export fn parseYAML(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

**参数**：source 完整 YAML 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：对应的 EL 值。

**失败与异常**：YAML 语法无效或超出限制时抛出解析异常。

### 示例：解析 YAML 映射

```el
import { parseYAML } from "el:formats/yaml/"
let settings = parseYAML("name: Ada")
```

## parseOrderedYAML {#api-bd520a15ef20f49b9075}

源码：`src/stdlib/formats/yaml/index.el:380` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/index.el#L380)

解析 YAML 并递归保留映射键的首次插入顺序；重复键覆盖不移动位置。

```el-signature
export fn parseOrderedYAML(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

### 示例：按输入顺序解析两个键

```el
import { parseOrderedYAML } from "el:formats/yaml/index.el"
let parsed = parseOrderedYAML("first: 1\nsecond: 2\n")
```
