# text/patterns/parser.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/text.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [ParseError.offset](#api-6dd7855dda76480009da)
- [ParseError.expected](#api-2b3956bc77cb8ed6d897)
- [ParseError.contexts](#api-2d3bebc3de2f96ffe6a8)
- [ParseReply.matched](#api-eed8f57e3bc622e71c4d)
- [ParseReply.end](#api-aa042bd0e5020bde8f9a)
- [ParseReply.error](#api-c04ba9afd567cf3d838f)
- [ParseReply.value](#api-51d18d3ab11cb736b67e)
- [Parser.asParser](#api-d229b8c3837af00d72d9)
- [Parser.parse](#api-d313f1ac56d1be2399e2)
- [Parser.parsePrefix](#api-7aff463fca2745d8ab80)

## 文本解析器 {#api-456334438bfab20db4a4}

源码：`src/stdlib/text/patterns/parser.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L1)

在连续输入上组合解析器，支持递归规则、结构列表与带偏移的解析失败信息。

## ParseError {#api-134641b6a74ac9dc39ed}

源码：`src/stdlib/text/patterns/parser.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L19)

表示输入未匹配解析器时的诊断，包含失败偏移、合并后的期望项和规则上下文。

```el-signature
@assign(mode: "copy")
export class ParseError extends Error
```

### 示例：查看解析错误的失败偏移

```el
import { ParseError } from "el:text/patterns/index.el"
let failure = ParseError(5, @["value"])
console.stderr.writeLine(failure.offset)
```

## ParseError.offset {#api-6dd7855dda76480009da}

源码：`src/stdlib/text/patterns/parser.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L28)

输入中第一个没有成功解析的位置，以 Unicode 标量下标计。

```el-signature
let offset: Number
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：显示失败偏移

```el
// @external error: ParseError
console.stderr.writeLine(error.offset)
```

## ParseError.expected {#api-2b3956bc77cb8ed6d897}

源码：`src/stdlib/text/patterns/parser.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L36)

在失败位置可接受的预期项列表。

```el-signature
let expected: Text[]
```

**类型**：[`Text`](../text.md#api-6116e54b075df026a90a)[]

### 示例：显示预期项（需调用方提供对象或绑定）

```el
// @external error: ParseError
console.stderr.writeLine(error.expected.join(", "))
```

## ParseError.contexts {#api-2d3bebc3de2f96ffe6a8}

源码：`src/stdlib/text/patterns/parser.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L44)

失败时处于活动状态的解析规则上下文栈。

```el-signature
let contexts: Text[]
```

**类型**：[`Text`](../text.md#api-6116e54b075df026a90a)[]

### 示例：显示解析上下文

```el
// @external error: ParseError
console.stderr.writeLine(error.contexts.join("/"))
```

## ParseReply {#api-97a3a0dc8d534b09c3e7}

源码：`src/stdlib/text/patterns/parser.el:103` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L103)

根据语义输出类型构造解析结果类型；每个结果保存匹配状态、结束偏移或解析错误。

```el-signature
export fn ParseReply(output: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：output 解析成功时产生的语义值类型。

**返回值**：可表示成功结果或携带 ParseError 的失败结果类型。

### 示例：构造成功结果类型并保存匹配值

```el
let Reply = ParseReply(Number)
let reply = Reply(2, () => 72)
console.stdout.writeLine(reply.matched, " ", reply.end)
```

## ParseReply.matched {#api-eed8f57e3bc622e71c4d}

源码：`src/stdlib/text/patterns/parser.el:112` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L112)

指示前缀解析是否成功。

```el-signature
let matched: Bool
```

**类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：检查前缀是否匹配（需调用方提供对象或绑定）

```el
// @external reply: ParseReply<output: Number>
console.stdout.writeLine(reply.matched)
```

## ParseReply.end {#api-aa042bd0e5020bde8f9a}

源码：`src/stdlib/text/patterns/parser.el:121` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L121)

成功解析后第一个未消费位置的标量下标。

```el-signature
let end: Number
```

**类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：查看消费偏移

```el
// @external reply: ParseReply<output: Number>
console.stdout.writeLine(reply.end)
```

## ParseReply.error {#api-c04ba9afd567cf3d838f}

源码：`src/stdlib/text/patterns/parser.el:130` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L130)

未匹配时保存的 ParseError。

```el-signature
let error: ParseError
```

**类型**：[`ParseError`](parser.md#api-134641b6a74ac9dc39ed)

### 示例：查看失败偏移（需调用方提供对象或绑定）

```el
// @external reply: ParseReply<output: Number>
console.stderr.writeLine(reply.error.offset)
```

## ParseReply.value {#api-51d18d3ab11cb736b67e}

源码：`src/stdlib/text/patterns/parser.el:162` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L162)

返回成功解析得到的语义值；失败时抛出保存的 ParseError。

```el-signature
fn value(): output
```

**返回类型**：[`output`](../../../types.md#api-d0a2a8f4c1260d3b7433)

**返回值**：解析器产生的值。

**失败与异常**：解析未匹配或语义值生成失败时抛出异常。

### 示例：读取成功结果

```el
// @external reply: ParseReply<output: Number>
if (reply.matched) console.stdout.writeLine(reply.value())
```

## Parser {#api-93c73ae8c76ebc48d097}

源码：`src/stdlib/text/patterns/parser.el:211` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L211)

根据语义输出类型构造解析器类型。解析器保存从输入上下文与起点读取 ParseReply 的函数。

```el-signature
export fn Parser(output: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：output 解析成功时产生的语义值类型。

**返回值**：可封装解析函数并提供完整解析、前缀解析和预览操作的解析器类型。

### 示例：将整数模式包装成有类型的解析器

```el
import { Parser, integer } from "el:text/patterns/index.el"
let parser: Parser<output: Number<min: unbounded, max: unbounded, epsilon: 0, integer: t>> = integer(min: unbounded, max: unbounded, epsilon: 0).asParser()
let value = parser.parse("72")
```

## Parser.asParser {#api-d229b8c3837af00d72d9}

源码：`src/stdlib/text/patterns/parser.el:243` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L243)

将模式包装值转换为解析器；解析器自身调用时也返回自身。

```el-signature
fn asParser()
```

**返回值**：当前解析器。

### 示例：解析完整输入

```el
let value = integer(min: unbounded, max: unbounded, epsilon: 0).asParser().parse("72")
```

## Parser.parse {#api-d313f1ac56d1be2399e2}

源码：`src/stdlib/text/patterns/parser.el:277` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L277)

从输入起点解析完整文本；输入有剩余或无法匹配时抛出 ParseError。

```el-signature
fn parse(source: Text, limits: PatternLimits = PatternLimits()): output
```

**返回类型**：[`output`](../../../types.md#api-df976d47c60f3dbf87f5)

**参数**：source 待解析文本。

**参数**：limits 递归深度、步骤数等解析限制。

**返回值**：解析得到的值。

**失败与异常**：输入不匹配、存在未消费后缀或超过解析限制时抛出异常。

### 示例：解析完整整数

```el
import { integer } from "el:text/patterns/index.el"
let value = integer(min: unbounded, max: unbounded, epsilon: 0).asParser().parse("72")
console.stdout.writeLine(value)
```

## Parser.parsePrefix {#api-7aff463fca2745d8ab80}

源码：`src/stdlib/text/patterns/parser.el:297` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L297)

从指定偏移尝试解析输入前缀，不要求消费完整文本，并以 ParseReply 返回匹配状态。

```el-signature
fn parsePrefix(source: Text, from: Number = 0, limits: PatternLimits = PatternLimits()): ParseReply<output: output>
```

**返回类型**：[`ParseReply`](parser.md#api-97a3a0dc8d534b09c3e7)<output: [`output`](../../../types.md#api-df976d47c60f3dbf87f5)>

**参数**：source 待解析文本。

**参数**：from 起始标量偏移，默认为 0。

**参数**：limits 解析资源限制。

**返回值**：包含 matched、end、error 和惰性 value() 的结果。

### 示例：只解析数字前缀

```el
import { integer } from "el:text/patterns/index.el"
let reply = integer(min: unbounded, max: unbounded, epsilon: 0).asParser().parsePrefix("12 items")
console.stdout.writeLine(reply.matched, " ", reply.end)
```

## firstOf {#api-f45406a31ca93535cd3d}

源码：`src/stdlib/text/patterns/parser.el:623` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L623)

从当前位置依次尝试解析器或文本候选，返回首个成功分支的结果。

```el-signature
export fn firstOf(first, ...rest)
```

**参数**：first 首个候选。

**参数**：rest 后续候选。

**返回值**：按顺序选择的解析器。

### 示例：解析 JSON 字面量

```el
import { firstOf, constant } from "el:text/patterns/index.el"
let literalParser = firstOf(constant("null", f), constant("true", t))
```

## constant {#api-e3e533cb002f8125c11d}

源码：`src/stdlib/text/patterns/parser.el:664` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L664)

匹配完整的固定文本，并将指定值作为解析结果。

```el-signature
export fn constant(text: Text, value)
```

**参数**：text 必须匹配的文本。

**参数**：value 匹配成功时产生的值。

**返回值**：输出指定值的解析器。

### 示例：解析 JSON 布尔字面量

```el
import { constant } from "el:text/patterns/index.el"
let trueParser = constant("true", t)
```

## pair {#api-cd138cf7450ba86c77a7}

源码：`src/stdlib/text/patterns/parser.el:685` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L685)

解析左值、分隔符与右值，并返回包含两侧结果的配对值。

```el-signature
export fn pair(left, separator, right)
```

**参数**：left 左侧解析器或文本。

**参数**：separator 两侧之间的解析器或文本。

**参数**：right 右侧解析器或文本。

**返回值**：保存 first 与 second 的解析结果。

### 示例：解析键值对

```el
import { pair } from "el:text/patterns/index.el"
let member = pair("name", ":", "EL")
```

## list {#api-71fc4d87dd834fa519c1}

源码：`src/stdlib/text/patterns/parser.el:772` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L772)

解析由括号包围、以分隔符隔开的元素序列；默认拒绝尾随分隔符。

```el-signature
export fn list(open, element, close, separator = ",", allowTrailing: Bool = f)
```

**参数**：open 起始解析器或文本。

**参数**：element 单个元素的解析器。

**参数**：close 结束解析器或文本。

**参数**：separator 元素分隔符，默认为逗号。

**参数**：allowTrailing 为真时允许末尾出现分隔符。

**返回值**：元素数组解析器。

### 示例：解析逗号分隔数组

```el
import { list, integer } from "el:text/patterns/index.el"
let numbers = list("[", integer(min: unbounded, max: unbounded, epsilon: 0), "]", separator: ",")
```
