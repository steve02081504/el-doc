# 实战：手写 JSON 解析器

这一页从最小的 JSON 值开始，用 Parser 组合子和 `grammar` 一步步拼出一个能用的 JSON 解析器：先认字面量，再补数字与字符串，最后加数组和对象，每一步只加一条规则。写完后还有一份折叠的递归下降对照，用来比较两种写法的分工。

字符串转义和数字校验都逐字符写在这个页面里，不依赖内置的 JSON 词法单元，所以规则和代码可以一行行对上。正文代码块按顺序追加到同一个文件，每块只导入这一节新增的名字；折叠块复用同一文件里已有的绑定。

## 先定结果类型

解析器的输出是 `Json`。值类型用 `data` 声明，六种 JSON 值各一个成员；对象成员单独用一个类保存键值对。

```el
data Json {
	Null
	Boolean(value: Bool)
	String(value: Text)
	Numeric(value: Number)
	Array(items: Json[])
	Object(members: JsonMember[])
}

@assign(mode: "copy")
class JsonMember {
	let key: Text
	let value: Json
	constructor(key: Text, value: Json) { init this; this.key = key; this.value = value }
}
```

`members` 故意用数组而不是映射：JSON 文本允许重复键，解析结果通常还要保留书写顺序，数组能同时保住两者；要不要合并重复键由调用者决定，解析器只原样保留。`JsonMember` 是 `copy` 类型，赋值时复制键与值。

## 第一步：只认字面量

最小的解析器只要认 `null`、`true`、`false` 三个字面量。`firstOf` 按参数顺序尝试，`constant` 匹配一段固定文本并返回给定的 `Json` 值；这一步先用最少的组合子，第四步再换成带 `skip` 与 `token` 的 `grammar`。

```el
import { firstOf, constant } from "el:text/patterns/index.el"

let literalParser = firstOf(
	constant("null", Json.Null),
	constant("true", Json.Boolean(t)),
	constant("false", Json.Boolean(nil))
)
```

`literalParser` 是一个 Parser：调用 `literalParser("true")` 会吃完整个输入并得到 `Json.Boolean(t)`，输入不匹配或末尾还有剩文本时抛 `ParseError`。这里的调用是严格的全输入校验，后面每一版都沿用同一条约定。

## 第二步：加数字

JSON 数字只有一种写法：可选的负号、整数部分、可选的小数、可选的指数。整数部分要么是单个 `0`，要么以 `1` 到 `9` 开头再接任意位数字，这就是前导零规则；小数与指数部分在符号之后都至少要有一位数字，正号只允许出现在指数里。

```el
import { anyOf, sequence, optional, many, range } from "el:text/patterns/index.el"

let digit = range("0", "9")
let tailDigits = many(digit).text()
let needed = many(digit, 1).text()
let jsonNumber = sequence(
	optional("-"),
	anyOf("0", sequence(range("1", "9"), tailDigits)),
	optional(sequence(".", needed)),
	optional(sequence(anyOf("e", "E"), optional(anyOf("+", "-")), needed))
).map(Number)
```

`many(digit).text()` 把字符序列还原成文本，`.map(Number)` 再做文本到数值的转换。把 `jsonNumber.map(Json.Numeric)` 接进 `firstOf`，数字就进入值规则；`01`、`1.`、`1e`、`+1` 都不会被完整匹配，因为对应形状在 `sequence` 里没有定义。

## 第三步：加字符串

字符串的难点在转义。JSON 字符串由一对双引号包住，中间是普通字符或转义序列：普通字符不能是双引号、反斜杠，也不能是小于 32 的控制字符；短转义是 `\"`、`\\`、`\/`、`\b`、`\f`、`\n`、`\r`、`\t`；`\uXXXX` 必须后接四个十六进制数字。UTF-16 代理项必须成对出现：`\uD800` 到 `\uDBFF` 的高代理项只能紧跟 `\uDC00` 到 `\uDFFF` 的低代理项，孤立的高、低代理项都不合法。

把这条规则写成 Pattern：普通字符用 `scalarSet` 的四段闭区间表示，短转义是一个固定集合，`\u` 分成三类：普通标量、`D0xx` 到 `D7xx` 的标量，以及必须与低代理项成对的高代理项。

```el
import { scalarSet, chars, exactly } from "el:text/patterns/index.el"

let hex = chars("0123456789abcdefABCDEF")
let plain = scalarSet(@[32, 33, 35, 91, 93, 55295, 57344, 1114111])
let short = sequence("\\", chars("\"\\/bfnrt"))
let scalar = anyOf(
	sequence("\\u", chars("0123456789ABCabcefEF"), exactly(3, hex)),
	sequence("\\u", chars("Dd"), range("0", "7"), exactly(2, hex))
)
let high = sequence("\\u", chars("Dd"), chars("89ABab"), exactly(2, hex))
let low = sequence("\\u", chars("Dd"), chars("CDEFcdef"), exactly(2, hex))
let escape = anyOf(short, scalar, sequence(high, low))
```

`plain` 的四段区间是 `32–33`、`35–91`、`93–55295`、`57344–1114111`，正好避开控制字符、`34` 的双引号与 `92` 的反斜杠。`scalar` 的第一路覆盖首数字为 `0` 到 `9`、`A` 到 `C`、`E` 到 `F` 的标量，第二路覆盖 `D000` 到 `D7FF`；`D8` 到 `DF` 只出现在 `high` 与 `low` 的配对分支里，因此孤立的代理项会在模式层直接失配。

形状确定后，生成值交给 `decodeJsonText`：它按同一张转义表拼接结果，`\u` 分支算出标量，高代理项再合并紧随的低代理项。模式已经排除了孤立代理项，所以解码器不再重复校验。最后一行用 `sequence` 把开引号、若干普通字符或转义、闭引号接起来，再映射到解码函数。

```el
fn decodeJsonText(raw: Text) {
	let result = ""
	let at = 1
	let end = Number(raw.count) - 1
	while (at < end) {
		let ch = raw.character(at)
		at += 1
		if (ch != Char("\\")) { result += Text(ch); continue }
		let code = raw.character(at)
		at += 1
		if (code == Char("b")) { result += Text(Char(8)) }
		else if (code == Char("f")) { result += Text(Char(12)) }
		else if (code == Char("n")) { result += "\n" }
		else if (code == Char("r")) { result += "\r" }
		else if (code == Char("t")) { result += "\t" }
		else if (code == Char("u")) {
			let value = hexValue(raw, at)
			at += 4
			if (value >= 55296 & value <= 56319) {
				value = 65536 + (value - 55296) * 1024 + hexValue(raw, at + 2) - 56320
				at += 6
			}
			result += Text(Char(value))
		}
		else { result += Text(code) }
	}
	return result
}

fn hexValue(raw: Text, at: Number) {
	let value = 0
	for (let index in 0..4) {
		let code = Number(raw.character(at + index))
		if (code <= 57) value = value * 16 + code - 48
		else if (code <= 70) value = value * 16 + code - 55
		else value = value * 16 + code - 87
	}
	return value
}

let jsonString = sequence("\"", many(anyOf(plain, escape)), "\"").map(decodeJsonText)
```

普通字符直接拼接；`\"`、`\\`、`\/` 落在最后的 `else`；`b`、`f`、`n`、`r`、`t` 各映射到控制字符；`\u` 由 `hexValue` 按四个十六进制数字换算，高代理项再与低代理项合成一个标量。现在把 `jsonString.map(Json.String)` 接进 `firstOf`，字符串就完成了。

## 第四步：加数组和对象

数组和对象会把 `value` 递归地套回自己，所以这一步换成 `grammar`：递归规则 `rule value: Json` 必须先声明结果类型，`grammar` 才能为它放一个可前向引用的占位符。`skip` 只处理空白，`token` 在连续输入上识别字符串和数字；`list` 与 `pair` 负责逗号分隔和键值对。

```el
import { grammar, list, pair } from "el:text/patterns/index.el"

let json = grammar {
	skip many(chars(" \t\r\n"))
	token str = jsonString
	token num = jsonNumber
	rule value: Json = firstOf(
		literalParser,
		num.map(Json.Numeric),
		str.map(Json.String),
		list("[", value, "]", separator: ",").map(Json.Array),
		list("{", pair(str, ":", value).map(entry => JsonMember(entry.first, entry.second)), "}", separator: ",").map(Json.Object)
	)
	start value
}
```

`list` 默认拒绝尾逗号，`pair` 保留键与值，再装进 `JsonMember` 数组，因此键序和重复键都原样保留。空白只在结构边界与 token 入口跳过，字符串内部的空格属于字符串内容。

## 递归、选择与错误

**递归**：`rule value` 在构造期先占位、解析时再展开，定义体里可以直接引用 `value`；手写版则靠 `parseValue` 调 `parseObject`、`parseArray`，再回到 `parseValue`。

**选择**：`firstOf` 从同一个起点按顺序尝试，第一个成功的分支胜出；所有分支都失败时，保留最远的错误偏移并合并各分支的期望。JSON 的分支首字符互不重叠，所以这里的分支顺序不会改变结果，只会影响失败时的报告。

**回溯**：Parser 记录提交状态，`commit()` 让后续失败不能退回上层选择，`attempt()` 只取消失败子解析的提交，供共享前缀的分支使用；这两个都是 Parser 的方法。JSON 不需要它们，因为每个分支的首字符已经把选择分开了。

**错误**：词法层的 Pattern 失败在 token 起点变成未匹配，结构层的失败可能发生在更后面；`parse` 在边界把最终失败变成 `ParseError`，它带 `offset`、`expected` 与 `contexts`。内部失配不会抛异常，只有 `parse` 或 `p(text)` 这种边界才把未匹配变成异常。

```el
import { ParseError } from "el:text/patterns/index.el"

try {
	json.parse("true false")
} catch (error) {
	if (error is ParseError) console.stderr.writeLine(error.offset, " ", error.expected.join(", "), " ", error.contexts.join("/"))
	else throw error
}
```

偏移指向第一个没有被消费的字符；`expected` 是合并后的候选期望，`contexts` 是规则栈。需要不抛异常地检查一段前缀时，用 `parsePrefix` 读 `ParseReply`，看 `matched`、`end` 与 `value()`。

## 什么时候手写递归下降

组合子版把词法、选择与错误合并交给库，日常用 `grammar` 就够了。需要逐字符控制游标、边读边做流式处理，或者在固定位置尝试自定义错误恢复时，手写递归下降更直接：每个非终结符一个方法，游标是唯一状态，失败点可以自己决定。

代价是空白、转义、数字边界和每层递归都要自己维护，分支之间的提交与回溯也由你负责。下面这份对照只手写结构和游标，字符串与数字继续复用上文的 `jsonString` 与 `jsonNumber`，方便把注意力放在递归本身。

??? example "可选：手写递归下降对照"

    ```el
    @assign(mode: "shared")
    class JsonReader {
    	let source: Text
    	let at = 0

    	constructor(source: Text) { init this; this.source = source }

    	fn end() => this.at >= Number(this.source.count)
    	fn peek() => this.source.character(this.at)
    	fn nextIs(text: Text) => !this.end() & Text(this.peek()) == text

    	fn skip() {
    		while (!this.end() & " \t\r\n".contains(Text(this.peek()))) this.at += 1
    	}

    	fn expect(text: Text) {
    		let end = this.at + Number(text.count)
    		if (end > Number(this.source.count) | this.source.slice(this.at, end) != text) throw ParseError(this.at, @[text])
    		this.at = end
    	}

    	fn parse(): Json {
    		let value = this.parseValue()
    		this.skip()
    		if (!this.end()) throw ParseError(this.at, @["输入结束"])
    		return value
    	}

    	fn parseString() {
    		let reply = jsonString.asParser().parsePrefix(this.source, this.at)
    		if (!reply.matched) throw reply.error
    		this.at = reply.end
    		return reply.value()
    	}

    	fn parseNumber() {
    		let reply = jsonNumber.asParser().parsePrefix(this.source, this.at)
    		if (!reply.matched) throw reply.error
    		this.at = reply.end
    		return reply.value()
    	}

    	fn parseValue(): Json {
    		this.skip()
    		if (this.end()) throw ParseError(this.at, @["JSON 值"])
    		if (this.nextIs("{")) return this.parseObject()
    		if (this.nextIs("[")) return this.parseArray()
    		if (this.nextIs("\"")) return Json.String(this.parseString())
    		if (this.nextIs("n")) { this.expect("null"); return Json.Null }
    		if (this.nextIs("t")) { this.expect("true"); return Json.Boolean(t) }
    		if (this.nextIs("f")) { this.expect("false"); return Json.Boolean(nil) }
    		return Json.Numeric(this.parseNumber())
    	}

    	fn parseArray(): Json {
    		this.expect("[")
    		let items: Json[] = @[]
    		this.skip()
    		if (this.nextIs("]")) { this.at += 1; return Json.Array(items) }
    		while (t) {
    			items.push(this.parseValue())
    			this.skip()
    			if (this.nextIs("]")) { this.at += 1; return Json.Array(items) }
    			this.expect(",")
    		}
    		throw ParseError(this.at, @["]"])
    	}

    	fn parseObject(): Json {
    		this.expect("{")
    		let members: JsonMember[] = @[]
    		this.skip()
    		if (this.nextIs("}")) { this.at += 1; return Json.Object(members) }
    		while (t) {
    			this.skip()
    			let key = this.parseString()
    			this.skip()
    			this.expect(":")
    			let value = this.parseValue()
    			members.push(JsonMember(key, value))
    			this.skip()
    			if (this.nextIs("}")) { this.at += 1; return Json.Object(members) }
    			this.expect(",")
    		}
    		throw ParseError(this.at, @["}"])
    	}
    }
    ```

递归下降版的 `parseValue` 用游标分派、用 `parsePrefix` 复用词法规则，`parseArray` 与 `parseObject` 在读完元素后回到 `parseValue`；`JsonReader(source).parse()` 负责尾随检查。和 `grammar` 版相比，它没有规则占位符和统一的错误合并，但每一步的读取与失败点都握在手里。

## 继续阅读

- [函数与闭包](../language/functions.md)：递归方法、闭包与 `return` 语义。
- [集合与文本](../stdlib/collections.md)：`Text` 的索引、切片与数组操作。
- [规范与实现边界](../appendix/implementation-status.md)：教程按规范写，落地前先用最小片段确认。
