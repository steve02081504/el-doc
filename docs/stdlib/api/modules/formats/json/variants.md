# formats/json/variants.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## parseOrderedJSONC {#api-6b7cc691bb029a8d80d1}

源码：`src/stdlib/formats/json/variants.el:224` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/variants.el#L224)

解析 JSONC 并递归保留映射键的首次插入顺序；重复键覆盖不移动位置。

```el
export fn parseOrderedJSONC(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

### 示例：按输入顺序解析两个键

```el
import { parseOrderedJSONC } from "el:formats/json/variants.el"
let parsed = parseOrderedJSONC("{\"first\":1,/* keep order */\"second\":2}")
```

## parseOrderedJSON5 {#api-8f168af352cd23c13804}

源码：`src/stdlib/formats/json/variants.el:233` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/variants.el#L233)

解析 JSON5 并递归保留映射键的首次插入顺序；重复键覆盖不移动位置。

```el
export fn parseOrderedJSON5(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

### 示例：按输入顺序解析两个键

```el
import { parseOrderedJSON5 } from "el:formats/json/variants.el"
let parsed = parseOrderedJSON5("{first:1,second:2,}")
```

## parseOrderedJSONLines {#api-504082fee10734d04334}

源码：`src/stdlib/formats/json/variants.el:242` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/variants.el#L242)

解析 JSONLines 并递归保留映射键的首次插入顺序；重复键覆盖不移动位置。

```el
export fn parseOrderedJSONLines(source: Text, limits: JsonLimits = JsonLimits()): any[]
```

**返回类型**：[`any`](../../../../../reference/language/types.md)[]

### 示例：按输入顺序解析两个键

```el
import { parseOrderedJSONLines } from "el:formats/json/variants.el"
let parsed = parseOrderedJSONLines("{\"first\":1,\"second\":2}\n{\"first\":3,\"second\":4}\n")
```
