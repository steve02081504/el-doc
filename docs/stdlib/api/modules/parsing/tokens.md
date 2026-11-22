# parsing/tokens.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/parsing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 输入记号解析 {#api-767caa034634fc0893b1}

源码：`src/stdlib/parsing/tokens.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/parsing/tokens.el#L1)

提供以 ASCII 空白分隔的输入记号解析器。

## decimal {#api-5f3b4e076722a4edc4ee}

源码：`src/stdlib/parsing/tokens.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/parsing/tokens.el#L31)

构造解析十进制数字记号的解析器；前导 ASCII 空白会被跳过。

```el-signature
export fn decimal(min, max, epsilon)
```

**参数**：min 最小允许值。

**参数**：max 最大允许值。

**参数**：epsilon 数值解析精度。

**返回值**：解析数字记号的解析器。

### 示例：解析十进制记号

```el
import { decimal } from "el:parsing/tokens.el"
let value = decimal(unbounded, unbounded, 0).parse(" 1.5")
```
