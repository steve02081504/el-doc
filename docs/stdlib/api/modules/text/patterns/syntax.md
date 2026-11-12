# text/patterns/syntax.el

本页由源码注释生成；示例未运行验证。

## 文本模式与语法宏 {#api-b7abcbebb991f46b29d3}

源码：`src/stdlib/text/patterns/syntax.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/syntax.el#L1)

将模式与解析规则的声明式语法展开为普通解析器表达式。

## grammar {#api-c66aeec62768f05c8f42}

源码：`src/stdlib/text/patterns/syntax.el:320` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/syntax.el#L320)

```el
export syntax grammar
```

声明可组合的解析语法，支持空白跳过、token、递归 rule 与起始规则。

### 示例：定义整数起始规则

```el
import { grammar, many, range } from "el:text/patterns/index.el"
let numbers = grammar {
	token digits = many(range("0", "9"), 1)
	rule value: Number = digits.map(Number)
	start value
}
```
