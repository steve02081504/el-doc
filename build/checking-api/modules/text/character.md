# text/character.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/text.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 字符值 {#api-146e9a01b2986776d615}

源码：`src/stdlib/text/character.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/character.el#L1)

提供动态宽度和固定宽度的字符值及字符差。

<span id="api-3166547d46e101216338"></span>

## Char~type {#api-f77d02dfef333b10f57f}

源码：`src/stdlib/text/character.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/character.el#L37)

表示非负字符值；文本构造要求恰有一个字符，否则抛出 RangeError。

```el-signature
@assign(mode: "copy")
export class Char
```

### 示例：用法

```el
let character = Char(65)
let value = character.numeric_value()
```

## Char~width {#api-5b7e35c8d6bfa741ca9d}

源码：`src/stdlib/text/character.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/character.el#L122)

构造固定宽度字符类型；宽度须为正整数，字符值须适合该宽度。

```el-signature
export fn Char(bitWidth): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
let ByteChar = Char<bitWidth: 8>
let character = ByteChar(65)
```
