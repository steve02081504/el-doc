# number/integer-text.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 整数文本转换 {#api-aecc462ed0f764c1a40d}

源码：`src/stdlib/number/integer-text.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer-text.el#L1)

整数文本转换相关接口。

<span id="api-a26b4f794e7427331de2"></span>

## parse_integer~decimal {#api-c06d67ac4215f21403f4}

源码：`src/stdlib/number/integer-text.el:82` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer-text.el#L82)

将十进制文本解析为大整数；支持符号和数字分隔符，非法或空文本触发数值诊断。

```el-signature
export fn parse_integer(text: Text): NumericInt
```

**返回类型**：[`NumericInt`](arithmetic.md#api-185a41c160696f925b31)

### 示例：用法

```el
import { parse_integer } from "el:number/integer-text.el"
let value = parse_integer("123_456")
```

## parse_integer~radix {#api-375b627d008e11d6cb38}

源码：`src/stdlib/number/integer-text.el:121` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer-text.el#L121)

按 2 至 36 的指定进制解析大整数，允许符号、匹配进制的前缀和下划线分隔符；非法输入触发数值诊断。

```el-signature
export fn parse_integer(text: Text, base: Integer): NumericInt
```

**返回类型**：[`NumericInt`](arithmetic.md#api-185a41c160696f925b31)

### 示例：用法

```el
import { parse_integer } from "el:number/integer-text.el"
let value = parse_integer("0xff", 16)
```
