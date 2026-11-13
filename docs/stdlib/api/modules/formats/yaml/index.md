# formats/yaml/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## YAML {#api-22f418b16890bb65cf80}

源码：`src/stdlib/formats/yaml/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/index.el#L1)

解析本实现支持的 YAML 文档子集。

## parseYAML {#api-9cc1ddf8a8c4fb2a80f8}

源码：`src/stdlib/formats/yaml/index.el:368` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/yaml/index.el#L368)

```el
export fn parseYAML(source: Text, limits: JsonLimits = JsonLimits()): any
```

将受支持的单个 YAML 文档解析为动态对象、数组及标量值。

**参数**：source 完整 YAML 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：对应的 EL 值。

**失败与异常**：YAML 语法无效或超出限制时抛出解析异常。

### 示例：解析 YAML 映射

```el
import { parseYAML } from "el:formats/yaml/"
let settings = parseYAML("name: Ada")
```
