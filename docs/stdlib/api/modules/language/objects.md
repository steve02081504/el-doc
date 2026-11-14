# language/objects.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## ownKeyCount {#api-7f663edadbdc0b343c1b}

源码：`src/stdlib/language/objects.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/objects.el#L18)

返回自身字段数量，不先创建键数组，供有界枚举预留工作空间。

```el
export fn ownKeyCount(value): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：查询对象字段数

```el
import { ownKeyCount } from "el:language/objects.el"
console.stdout.writeLine(ownKeyCount(@{ name: "EL", version: "1" }))
```
