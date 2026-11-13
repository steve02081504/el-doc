# text/patterns/parser.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/text.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 文本解析器 {#api-456334438bfab20db4a4}

源码：`src/stdlib/text/patterns/parser.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L1)

在连续输入上组合解析器，支持递归规则、结构列表与带偏移的解析失败信息。

## ParseError {#api-134641b6a74ac9dc39ed}

源码：`src/stdlib/text/patterns/parser.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L19)

```el
@assign(mode: "copy")
export class ParseError extends Error
```

表示输入未匹配解析器时的诊断，包含失败偏移、合并后的期望项和规则上下文。

### 示例：捕获 JSON 解析错误

```el
import { ParseError } from "el:text/patterns/index.el"
try { json.parse("true false") }
catch (error) { if (error is ParseError) console.stderr.writeLine(error.offset) }
```

## ParseError.offset {#api-6dd7855dda76480009da}

源码：`src/stdlib/text/patterns/parser.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L27)

```el
let offset: Number
```

输入中第一个没有成功解析的位置，以 Unicode 标量下标计。

### 示例：显示失败偏移

```el
console.stderr.writeLine(error.offset)
```

## ParseError.expected {#api-2b3956bc77cb8ed6d897}

源码：`src/stdlib/text/patterns/parser.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L34)

```el
let expected: Text[]
```

在失败位置可接受的预期项列表。

### 示例：显示预期项

```el
console.stderr.writeLine(error.expected.join(", "))
```

## ParseError.contexts {#api-2d3bebc3de2f96ffe6a8}

源码：`src/stdlib/text/patterns/parser.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L41)

```el
let contexts: Text[]
```

失败时处于活动状态的解析规则上下文栈。

### 示例：显示解析上下文

```el
console.stderr.writeLine(error.contexts.join("/"))
```

## ParseReply.matched {#api-eed8f57e3bc622e71c4d}

源码：`src/stdlib/text/patterns/parser.el:98` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L98)

```el
let matched: Bool
```

指示前缀解析是否成功。

### 示例：检查前缀是否匹配

```el
console.stdout.writeLine(reply.matched)
```

## ParseReply.end {#api-aa042bd0e5020bde8f9a}

源码：`src/stdlib/text/patterns/parser.el:106` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L106)

```el
let end: Number
```

成功解析后第一个未消费位置的标量下标。

### 示例：查看消费偏移

```el
console.stdout.writeLine(reply.end)
```

## ParseReply.error {#api-c04ba9afd567cf3d838f}

源码：`src/stdlib/text/patterns/parser.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L114)

```el
let error: ParseError
```

未匹配时保存的 ParseError。

### 示例：查看失败偏移

```el
console.stderr.writeLine(reply.error.offset)
```

## ParseReply.value {#api-51d18d3ab11cb736b67e}

源码：`src/stdlib/text/patterns/parser.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L145)

```el
fn value(): output
```

返回成功解析得到的语义值；失败时抛出保存的 ParseError。

**返回值**：解析器产生的值。

**失败与异常**：解析未匹配或语义值生成失败时抛出异常。

### 示例：读取成功结果

```el
if (reply.matched) console.stdout.writeLine(reply.value())
```

## Parser.asParser {#api-d229b8c3837af00d72d9}

源码：`src/stdlib/text/patterns/parser.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L216)

```el
fn asParser()
```

将模式包装值转换为解析器；解析器自身调用时也返回自身。

**返回值**：当前解析器。

### 示例：解析完整输入

```el
let value = integer(min: unbounded, max: unbounded, epsilon: 0).asParser().parse("42")
```

## Parser.parse {#api-d313f1ac56d1be2399e2}

源码：`src/stdlib/text/patterns/parser.el:250` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L250)

```el
fn parse(source: Text, limits: PatternLimits = PatternLimits()): output
```

从输入起点解析完整文本；输入有剩余或无法匹配时抛出 ParseError。

**参数**：source 待解析文本。

**参数**：limits 递归深度、步骤数等解析限制。

**返回值**：解析得到的值。

**失败与异常**：输入不匹配、存在未消费后缀或超过解析限制时抛出异常。

### 示例：解析完整整数

```el
import { integer } from "el:text/patterns/index.el"
let value = integer(min: unbounded, max: unbounded, epsilon: 0).asParser().parse("42")
console.stdout.writeLine(value)
```

## Parser.parsePrefix {#api-7aff463fca2745d8ab80}

源码：`src/stdlib/text/patterns/parser.el:270` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L270)

```el
fn parsePrefix(source: Text, from: Number = 0, limits: PatternLimits = PatternLimits()): ParseReply<output: output>
```

从指定偏移尝试解析输入前缀，不要求消费完整文本，并以 ParseReply 返回匹配状态。

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

源码：`src/stdlib/text/patterns/parser.el:596` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L596)

```el
export fn firstOf(first, ...rest)
```

从当前位置依次尝试解析器或文本候选，返回首个成功分支的结果。

**参数**：first 首个候选。

**参数**：rest 后续候选。

**返回值**：按顺序选择的解析器。

### 示例：解析 JSON 字面量

```el
import { firstOf, constant } from "el:text/patterns/index.el"
let literalParser = firstOf(constant("null", nil), constant("true", t))
```

## constant {#api-e3e533cb002f8125c11d}

源码：`src/stdlib/text/patterns/parser.el:637` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L637)

```el
export fn constant(text: Text, value)
```

匹配完整的固定文本，并将指定值作为解析结果。

**参数**：text 必须匹配的文本。

**参数**：value 匹配成功时产生的值。

**返回值**：输出指定值的解析器。

### 示例：解析 JSON 布尔字面量

```el
import { constant } from "el:text/patterns/index.el"
let trueParser = constant("true", t)
```

## pair {#api-cd138cf7450ba86c77a7}

源码：`src/stdlib/text/patterns/parser.el:658` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L658)

```el
export fn pair(left, separator, right)
```

解析左值、分隔符与右值，并返回包含两侧结果的配对值。

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

源码：`src/stdlib/text/patterns/parser.el:745` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/parser.el#L745)

```el
export fn list(open, element, close, separator = ",", allowTrailing: Bool = nil)
```

解析由括号包围、以分隔符隔开的元素序列；默认拒绝尾随分隔符。

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
