# text/patterns/parsers.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/text.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 文本模式解析器 {#api-891062a4954b954deeb8}

源码：`src/stdlib/text/patterns/parsers.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parsers.el#L5)

提供从词法模式创建解析器的便捷构造入口。

## parsers {#api-a99b3fa5dc38a9c0e767}

源码：`src/stdlib/text/patterns/parsers.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parsers.el#L20)

提供整数模式和定长文本读取解析器的构造方法。

```el-signature
export const parsers = ParserConstructors()
```

**类型**：[`ParserConstructors`](../../../types.md#api-4bb2a777f1220c56d3f7)

### 示例：构造读取三个字符的解析器

```el
let parser = parsers.readText(3)
```
