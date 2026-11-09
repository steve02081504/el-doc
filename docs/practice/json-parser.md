# 实战：手写 JSON 解析器

这一页不借助解析器生成器，从零写一个 JSON 解析器：先用手写递归下降把游标与字符读清楚，再换成 `el:text/patterns/index.el` 的 Parser 组合子写同一份语法。读完你能判断两种写法各自适合什么场景，也能看懂解析器内部的选择、递归与回溯。

JSON 是很好的练习对象：它的规则不多，却已经包含字符串、数字、嵌套数组、嵌套对象、字面量与空白这些真实解析器都会遇到的部分。下面的实现覆盖 JSON 的核心子集，重点是让“解析”从黑盒变成可以逐行跟踪的流程。

## 先定义结果类型

解析器把一段 `Text` 变成 `Json` 值。值类型用 `data` 声明，成员覆盖 JSON 的六种值；对象成员单独用一个类保存键值对。

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

`Json` 是递归声明：`Array` 持有 `Json[]`，`Object` 持有 `JsonMember[]`，成员又可以指回 `Json`。对象成员用数组而不是映射保存：JSON 允许重复键，而解析结果通常还要保留书写顺序，数组能同时保住两者，是否合并重复键由调用者决定。

`JsonMember` 标成 `@assign(mode: "copy")`，赋值时复制 `key` 与 `value`，不共享可变状态。数据类只负责承载结果，解析行为都放在下面的解析器里。

## 手写递归下降

递归下降的骨架很直接：每个非终结符对应一个方法，方法按语法读走一段，游标 `at` 是唯一的状态。`parseValue` 按首字符分派到 `parseObject`、`parseArray`、`parseString` 与 `parseNumber`，后两者处理完又会回到 `parseValue`，这就是递归。解析器本身是一台有状态的机器，类上用 `@assign(mode: "shared")`，赋值时共享同一个游标。

```el
import { ParseError, decodeQuoted, QuotedTextFormat } from "el:text/patterns/index.el"

fn isDigit(ch: Char): Bool {
	let code = Number(ch)
	return code >= 48 & code <= 57
}

@assign(mode: "shared")
class JsonParser {
	let source: Text
	let at: Number = 0

	constructor(source: Text) { init this; this.source = source }

	fn atEnd(): Bool => this.at >= Number(this.source.count)
	fn peek(): Char => this.source.character(this.at)

	fn skipWhitespace() {
		while (!this.atEnd()) {
			let ch = this.peek()
			if (ch != Char(" ") & ch != Char("\t") & ch != Char("\r") & ch != Char("\n")) return
			this.at += 1
		}
	}

	fn expect(text: Text) {
		let end = this.at + Number(text.count)
		if (end > Number(this.source.count) | this.source.slice(this.at, end) != text) throw ParseError(this.at, @[text])
		this.at = end
	}

	fn parse(): Json {
		let value = this.parseValue()
		this.skipWhitespace()
		if (!this.atEnd()) throw ParseError(this.at, @["输入结束"])
		return value
	}

	fn parseValue(): Json {
		this.skipWhitespace()
		if (this.atEnd()) throw ParseError(this.at, @["一个 JSON 值"])
		let ch = this.peek()
		if (ch == Char("{")) return this.parseObject()
		if (ch == Char("[")) return this.parseArray()
		if (ch == Char("\"")) return Json.String(this.parseString())
		if (ch == Char("n")) { this.expect("null"); return Json.Null }
		if (ch == Char("t")) { this.expect("true"); return Json.Boolean(t) }
		if (ch == Char("f")) { this.expect("false"); return Json.Boolean(nil) }
		return Json.Numeric(this.parseNumber())
	}

	fn parseObject(): Json {
		this.expect("{")
		let members: JsonMember[] = @[]
		this.skipWhitespace()
		if (!this.atEnd() & this.peek() == Char("}")) { this.at += 1; return Json.Object(members) }
		while (t) {
			this.skipWhitespace()
			if (this.atEnd() | this.peek() != Char("\"")) throw ParseError(this.at, @["带引号的对象键"])
			let key = this.parseString()
			this.skipWhitespace()
			this.expect(":")
			let value = this.parseValue()
			members.push(JsonMember(key, value))
			this.skipWhitespace()
			if (!this.atEnd() & this.peek() == Char("}")) { this.at += 1; return Json.Object(members) }
			this.expect(",")
		}
		throw ParseError(this.at, @["对象成员"])
	}

	fn parseArray(): Json {
		this.expect("[")
		let items: Json[] = @[]
		this.skipWhitespace()
		if (!this.atEnd() & this.peek() == Char("]")) { this.at += 1; return Json.Array(items) }
		while (t) {
			items.push(this.parseValue())
			this.skipWhitespace()
			if (!this.atEnd() & this.peek() == Char("]")) { this.at += 1; return Json.Array(items) }
			this.expect(",")
		}
		throw ParseError(this.at, @["数组元素"])
	}

	fn parseString(): Text {
		let start = this.at
		this.expect("\"")
		while (t) {
			if (this.atEnd()) throw ParseError(this.at, @["字符串的结束引号"])
			let ch = this.peek()
			this.at += 1
			if (ch == Char("\"")) break
			if (ch == Char("\\")) this.at += 1
		}
		let raw = this.source.slice(start, this.at)
		try { return decodeQuoted(raw, QuotedTextFormat.Json) }
		catch (error) {
			if (error is ParseError) throw ParseError(start + error.offset, error.expected)
			throw error
		}
	}

	fn parseNumber(): Number {
		let start = this.at
		if (!this.atEnd() & this.peek() == Char("-")) this.at += 1
		let integral = this.at
		while (!this.atEnd() & isDigit(this.peek())) this.at += 1
		if (this.at == integral) throw ParseError(this.at, @["数字"])
		if (this.at - integral > 1 & this.source.character(integral) == Char("0")) throw ParseError(integral, @["无前导零的整数部分"])
		if (!this.atEnd() & this.peek() == Char(".")) {
			this.at += 1
			let fraction = this.at
			while (!this.atEnd() & isDigit(this.peek())) this.at += 1
			if (this.at == fraction) throw ParseError(this.at, @["小数点后的数字"])
		}
		if (!this.atEnd() & (this.peek() == Char("e") | this.peek() == Char("E"))) {
			this.at += 1
			if (!this.atEnd() & (this.peek() == Char("+") | this.peek() == Char("-"))) this.at += 1
			let exponent = this.at
			while (!this.atEnd() & isDigit(this.peek())) this.at += 1
			if (this.at == exponent) throw ParseError(this.at, @["指数数字"])
		}
		return Number(this.source.slice(start, this.at))
	}
}
```

`atEnd`、`peek`、`skipWhitespace` 组成读取层：`peek` 只返回当前位置的 `Char`，不推进游标，需要检查边界时先调用 `atEnd`。`expect` 匹配一段固定文本并推进，失败时抛出带偏移与期望的 `ParseError`。

`parseNumber` 按符号、整数、小数、指数四段扫描，`Number(...)` 在这里执行的是文本到数值的转换。`parseString` 只负责找字符串边界，转义、控制字符与代理对的解码复用标准库的 `decodeQuoted`；它报出的偏移相对字符串起点，这里加回 `start` 再抛。

顶层 `parse` 在读完值之后再跳过尾随空白，并要求输入恰好结束；`JsonParser(source).parse()` 就是完整入口。

## 换成 Parser 组合子

`parser { ... }` 构造一个可复用的 Parser：body 每次执行都重新求值，`let` 绑定的是直接读取的结果，单独的文本字面量语句表示匹配这段文本，静态确认为 `Text` 的裸名字表达式语句也按同样方式匹配，`return` 返回这次解析的值。`integer()` 与 `readText(n)` 是需要当前解析上下文的直接读取 API，分别产出 `Number` 与 `Text`；需要保存解析器对象时，用 `parsers.integer`、`parsers.readText(n)` 这样的构造入口。

```el
import { parser, parsers, integer, readText } from "el:text/patterns/index.el"

let framed = parser {
	let length = integer()
	":"
	return readText(length)
}

let ratio = parser {
	let numerator = integer()
	"/"
	let denominator = integer()
	return @[numerator, denominator]
}

let saved = parsers.readText(2)
```

`framed("4:你好")` 是严格的全输入校验：解析完还有剩余文本就抛 `ParseError`。`saved` 是构造期就定好宽度的可复用 Parser，`saved.parsePrefix("你好吗")` 只读自己那两个标量，返回带 `matched`、`end` 与 `value()` 的回复；把 `saved` 直接当函数调用（`p(text)`）则仍要求吃完整个输入。

## 用 grammar 描述递归语法

手写版的递归靠方法互相调用；组合子版里，`value` 的定义内部还要出现 `value`，需要 `grammar` 的 `rule` 先放一个带类型的占位符。`token` 在连续原始输入上识别，内部不再跳过空白；`skip` 只在结构边界与 token 入口生效。

```el
import { grammar, firstOf, constant, list, pair, many, chars, quotedText, decimal, QuotedTextFormat, DecimalFormat } from "el:text/patterns/index.el"

let json = grammar {
	skip many(chars(" \t\r\n"))
	token text = quotedText(format: QuotedTextFormat.Json)
	token number = decimal(format: DecimalFormat.Json)
	rule value: Json = firstOf(
		constant("null", Json.Null),
		constant("true", Json.Boolean(t)),
		constant("false", Json.Boolean(nil)),
		text.map(Json.String),
		number.map(Json.Numeric),
		list("[", value, "]", separator: ",").map(Json.Array),
		list("{", pair(text, ":", value).map((entry) => JsonMember(entry.first, entry.second)), "}", separator: ",").map(Json.Object)
	)
	start value
}
```

`quotedText(format: QuotedTextFormat.Json)` 与 `decimal(format: DecimalFormat.Json)` 是两个按 JSON 规则收紧的词法单元：前者检查控制字符、JSON 转义与 UTF-16 代理对，后者检查符号、前导零、小数与指数。`list` 默认拒绝尾逗号，`pair` 保留左右值，对象键的顺序与重复键都原样保留。

## 递归、选择与回溯

**递归**：`rule value` 在构造期先占位、解析时再展开，所以定义体里可以引用定义中的自己，递归规则必须写显式结果类型；手写版的方法互相调用做的是同一件事。

**有序选择**：`firstOf` 从同一个起点按参数顺序尝试，第一个成功的分支立即胜出；没有任何分支成功或提交时，才比较各分支的错误偏移，保留最远的那个并合并期望文本。分支顺序因此同时决定解析结果与错误报告。

**提交与回溯**：某一步成功后，提交状态会让后续失败无法退回上层选择；`attempt()` 只取消失败子解析的提交，让 `firstOf` 还能尝试下一个分支，不抹掉父序列此前已有的提交。两者都是 Parser 的方法，写作 `p.commit()` 与 `p.attempt()`，不是顶层函数。

**重复必须有进展**：`repeat` 的每次成功都必须消费输入，否则抛错而不是空转；`list` 对元素与分隔符同样要求非空。否则“可选项 + 重复”就会在零宽匹配上死循环。

**失配不是异常**：内部不匹配会变成未匹配的回复，普通 `catch` 捕不到；只有走到 `parse` 或 `p(text)` 这种边界，未匹配才变成带偏移、期望与上下文的 `ParseError`。回溯只恢复局部游标与局部状态，不回滚预算、变量或已经发生的 I/O。

在边界上报错时，`ParseError` 的字段可以直接用于输出或日志：

```el
import { ParseError } from "el:text/patterns/index.el"

try {
	json.parse("{\"x\": 1,}")
} catch (error) {
	if (error is ParseError) {
		console.stderr.writeLine("offset ", error.offset, ", expected: ", error.expected.join(", "))
	} else {
		throw error
	}
}
```

需要把失败当普通值处理时，用 `parsePrefix` 取回复并检查 `matched`，不要用 `catch` 驱动正常解析流程。

## 两种写法怎么选

手写版把每个字符判断都放在眼前，适合教学、协议固定，或需要精确控制错误位置与恢复策略的场合；代价是字符串、数字、空白这些细节都要自己维护。组合子版复用标准库现成的词法单元，用 `firstOf`、`list`、`pair` 与 `grammar` 把结构写得更短，递归、回溯与错误合并交给库统一处理；代价是要理解有序选择、提交边界与“重复必须消费输入”，否则语法看着对，行为却可能和预期不同。

两个版本共用同一套 `Json` 类型，可以用同一组输入对照阅读。

## 继续阅读

- [函数与闭包](../language/functions.md)：递归方法、闭包与 `return` 语义。
- [集合与文本](../stdlib/collections.md)：`Text` 的索引、切片与数组操作。
- [规范与实现边界](../appendix/implementation-status.md)：教程按规范写，落地前先用最小片段确认。
