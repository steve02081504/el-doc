# text/patterns/combinators.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/text.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 文本模式组合子 {#api-513366e809a4be863729}

源码：`src/stdlib/text/patterns/combinators.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L1)

提供字符集、序列、选择与重复等模式构造器，用于识别文本结构。

## scalarSet {#api-6e8d4cb55ce806bebd5d}

源码：`src/stdlib/text/patterns/combinators.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L30)

```el
export fn scalarSet(ranges: Number[], negate: Bool = nil): Pattern<output: Char>
```

**返回类型**：`Pattern<output: Char>`

根据成对的 Unicode 标量起止值构造字符集合模式。

**参数**：ranges 按起止顺序排列的闭区间端点。

**参数**：negate 为真时匹配区间集合之外的字符。

**返回值**：匹配单个 Unicode 标量的模式。

### 示例：构造可打印字符集合

```el
import { scalarSet } from "el:text/patterns/index.el"
let printable = scalarSet(@[32, 33, 35, 91, 93, 1114111])
```

## chars {#api-94ce174e6824f8a6bf5a}

源码：`src/stdlib/text/patterns/combinators.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L50)

```el
export fn chars(text: Text): Pattern<output: Char>
```

**返回类型**：`Pattern<output: Char>`

构造匹配给定文本中任一字符的模式。

**参数**：text 候选字符集合。

**返回值**：匹配其中一个字符的模式。

### 示例：匹配十六进制字母

```el
import { chars } from "el:text/patterns/index.el"
let hexLetter = chars("abcdefABCDEF")
```

## range {#api-34c63714beff83abf769}

源码：`src/stdlib/text/patterns/combinators.el:70` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L70)

```el
export fn range(first: Text, last: Text): Pattern<output: Char>
```

**返回类型**：`Pattern<output: Char>`

构造匹配首尾字符标量值之间任一字符的模式，端点包含在内。

**参数**：first 区间首字符。

**参数**：last 区间末字符。

**返回值**：单字符区间模式。

### 示例：匹配小写字母

```el
import { range } from "el:text/patterns/index.el"
let lower = range("a", "z")
```

## sequence {#api-dd83ce8439cbe4fa0868}

源码：`src/stdlib/text/patterns/combinators.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L88)

```el
export fn sequence(...elements): Pattern<output: Text>
```

**返回类型**：`Pattern<output: Text>`

按顺序匹配多个文本片段或模式，并合并为一个文本结果。

**参数**：elements 依次匹配的文本或模式。

**返回值**：顺序组合后的模式。

### 示例：匹配转义前缀

```el
import { sequence, chars } from "el:text/patterns/index.el"
let escapedQuote = sequence("\\", chars("\""))
```

## anyOf {#api-3876f251f8585cfa3c5a}

源码：`src/stdlib/text/patterns/combinators.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L114)

```el
export fn anyOf(first, ...rest): Pattern<output: Text>
```

**返回类型**：`Pattern<output: Text>`

从同一起点按顺序尝试候选模式，匹配第一个成功的候选。

**参数**：first 首个候选文本或模式。

**参数**：rest 后续候选文本或模式。

**返回值**：分支选择模式。

### 示例：选择候选转义符

```el
import { anyOf, sequence, chars } from "el:text/patterns/index.el"
let escape = anyOf(sequence("\\", chars("nrt")), sequence("\\", chars("\\\"")))
```

## many {#api-3805e29d6c725ee7c9c8}

源码：`src/stdlib/text/patterns/combinators.el:146` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L146)

```el
export fn many(element, min: Number = 0, max: Number = -1, greedy: Bool = t)
```

重复匹配一个文本或模式，并可指定最少与最多次数。

**参数**：element 要重复的文本或模式。

**参数**：min 最少匹配次数，默认 0。

**参数**：max 最多匹配次数；负值表示不限。

**参数**：greedy 为真时优先取得较长匹配。

**返回值**：重复模式。

### 示例：匹配零个或多个空格

```el
import { many, chars } from "el:text/patterns/index.el"
let spaces = many(chars(" "))
```

## exactly {#api-7007858c46655109f135}

源码：`src/stdlib/text/patterns/combinators.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L158)

```el
export fn exactly(count: Number, element)
```

构造恰好重复指定次数的模式。

**参数**：count 匹配次数。

**参数**：element 要匹配的文本或模式。

**返回值**：固定次数重复模式。

### 示例：匹配四位数字

```el
import { exactly, range } from "el:text/patterns/index.el"
let fourDigits = exactly(4, range("0", "9"))
```

## optional {#api-55180568f6c1181ab847}

源码：`src/stdlib/text/patterns/combinators.el:169` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/combinators.el#L169)

```el
export fn optional(element)
```

将模式设为可选，匹配零次或一次。

**参数**：element 可选的文本或模式。

**返回值**：可选模式。

### 示例：匹配可选负号

```el
import { optional } from "el:text/patterns/index.el"
let sign = optional("-")
```
