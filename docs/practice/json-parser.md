# 实战：手写 JSON 解析器

> 正则能把 `{"a":1}` 拆开，遇到三层嵌套就崩了。能不能从三个字面量开始，每次只加一条规则，最后拼出完整的 JSON 解析器？

!!! abstract "🎯 做完这个项目，你能"
    - 用 `constant`、`sequence`、`many` 拼出只认三个字面量的最小解析器
    - 给数字与字符串补全规则，包括前导零、`\uXXXX` 与代理项配对
    - 用 `grammar` 的递归规则让数组和对象回到自己
    - 判断什么时候该换手写递归下降，并读懂 `ParseError` 的三个字段

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：[集合与文本](../stdlib/collections.md)、[函数与闭包](../language/functions.md)、递归</span>

## 目标与边界

==能用“先 A 再 B，或者 C”描述的语言，交给组合子；需要逐字符控制游标、流式处理，或者在固定位置尝试自定义错误恢复时，手写递归下降更直接。== 这一页先用组合子拼出一个完整 JSON 解析器，最后给一份递归下降的对照。

输入是 JSON 文本，输出是 `Json` 值：六种值各一个成员，对象成员用一个 `copy` 类保存键值对。字符串转义和数字校验都逐字符写在这一页里，不依赖内置 JSON 词法单元，规则和代码能一行行对上。正文代码块按顺序追加到同一文件，每块只导入这一节新增的名字；折叠块复用已有绑定。

验收标准：

- `literalParser("true")` 得到 `Json.Boolean(t)`，传入 `"nul"` 抛 `ParseError`
- `jsonNumber` 拒绝 `01`、`1.`、`1e`、`+1`，接受 `-2.5e3`
- `jsonString` 接受短转义与 `\u` 标量，拒绝孤立的高、低代理项
- `json.parse` 处理嵌套的 `{"a": [1, true, null]}`，保留键序与重复键

不做的部分：数字到定宽整数的转换、错误恢复、流式输入。

## 第一步：先定结果类型

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

`members` 故意用数组而不是映射：JSON 文本允许重复键，解析结果通常还要保留书写顺序，数组能同时保住两者；要不要合并重复键由调用者决定。`JsonMember` 是 `copy` 类型，赋值时复制键与值。

!!! success "检查点"
    - [ ] 六个成员都能构造：`Json.Null`、`Json.Boolean(t)`、`Json.Array(@[])` 等
    - [ ] 类声明里必须有 `@assign(mode: "copy")`，没写会被编译器拒绝

## 第二步：只认三个字面量

`firstOf` 按参数顺序尝试，`constant` 匹配一段固定文本并返回给定的 `Json` 值。

```el
import { firstOf, constant } from "el:text/patterns/index.el"

let literalParser = firstOf(
	constant("null", Json.Null),
	constant("true", Json.Boolean(t)),
	constant("false", Json.Boolean(nil))
)
```

`literalParser` 是一个 Parser：调用 `literalParser("true")` 会吃完整个输入并得到 `Json.Boolean(t)`，输入不匹配或末尾还有剩文本时抛 `ParseError`。这里的调用是严格的全输入校验，后面每一版都沿用这条约定。

```text
literalParser("true")   → Json.Boolean(t)
literalParser("tru")    → ParseError
literalParser("true ")  → ParseError（末尾还有剩文本）
```

!!! success "检查点"
    - [ ] `literalParser("false")` 得到 `Json.Boolean(nil)`
    - [ ] `literalParser("nullx")` 抛错，而不是返回 `Json.Null`

## 第三步：给数字补一条完整规则

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

??? question "先猜：`jsonNumber` 解析 `01` 会得到 `1`，还是报错？"
    报错。规则只能匹配单个 `0`，后面剩的 `1` 让全输入校验失败。前导零被禁不是因为“值一样”，而是因为 JSON 语法里整数部分只有那两种形状。

`many(digit).text()` 把字符序列还原成文本，`.map(Number)` 再做文本到数值的转换。把 `jsonNumber.map(Json.Numeric)` 接进 `firstOf`，数字就进入值规则；`01`、`1.`、`1e`、`+1` 都不会被完整匹配，因为对应形状在 `sequence` 里没有定义。`Number` 是精确有理数，所以 `0.1` 得到的是精确值，不经过二进制近似。

!!! success "检查点"
    - [ ] `jsonNumber("0")` 得到 `0`，`jsonNumber("-2.5e3")` 得到 `-2500`
    - [ ] `jsonNumber("01")`、`jsonNumber("1.")`、`jsonNumber("+1")` 都抛错

## 第四步：字符串的难点在转义

JSON 字符串由一对双引号包住，中间是普通字符或转义序列：普通字符不能是双引号、反斜杠，也不能是小于 32 的控制字符；短转义是 `\"`、`\\`、`\/`、`\b`、`\f`、`\n`、`\r`、`\t`；`\uXXXX` 必须后接四个十六进制数字。UTF-16 代理项必须成对出现：`\uD800` 到 `\uDBFF` 的高代理项只能紧跟 `\uDC00` 到 `\uDFFF` 的低代理项。

把规则写成 Pattern：普通字符用 `scalarSet` 的四段闭区间，短转义是一个固定集合，`\u` 分成三类——普通标量、`D0xx` 到 `D7xx` 的标量，以及必须与低代理项成对的高代理项。

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

`plain` 的四段区间正好避开控制字符、`34` 的双引号与 `92` 的反斜杠；`scalar` 两路覆盖普通标量与 `D000`–`D7FF`，`D8`–`DF` 只出现在配对分支里，所以孤立代理项在模式层直接失配。

生成值交给 `decodeJsonText`：按同一张转义表拼接结果，`\u` 分支算出标量，高代理项再合并紧随的低代理项。模式已经排除了孤立代理项，解码器不再重复校验。

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

普通字符直接拼接；`\"`、`\\`、`\/` 落在最后的 `else`；`b`、`f`、`n`、`r`、`t` 映射到控制字符；`\u` 由 `hexValue` 按四位十六进制换算。把 `jsonString.map(Json.String)` 接进 `firstOf`，字符串就完成了。

!!! success "检查点"
    - [ ] `jsonString` 能解析含 `\n`、`\t` 与中文的字符串
    - [ ] 一对合法的高／低代理项被合成一个标量，而不是两个字符
    - [ ] 单独一个高代理项抛错，不会悄悄变成替换字符

## 第五步：数组和对象把规则递归回自己

数组和对象会把值递归地套回自己，所以这一步换成 `grammar`：递归规则 `rule value: Json` 必须先声明结果类型，`grammar` 才能为它放一个可前向引用的占位符。`skip` 只处理空白，`token` 在连续输入上识别字符串和数字；`list` 与 `pair` 负责逗号分隔和键值对。

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

!!! success "检查点"
    - [ ] `json.parse("{\"a\": [1, true, null]}")` 得到三成员对象，第一个成员是数组
    - [ ] `{"a":1,"b":2}` 的键序与书写顺序一致，`{"a":1,"a":2}` 保留两个成员
    - [ ] `[1, 2,]` 抛错，`[1, 2]` 正常；`"a b"` 里的空格不参与空白跳过

## 第六步：错误发生在哪个偏移

词法层的失败在 token 起点变成未匹配，结构层的失败可能发生在更后面；`parse` 在边界把最终失败变成 `ParseError`，它带 `offset`、`expected` 与 `contexts`。内部失配不会抛异常，只有 `parse` 或 `p(text)` 这种边界才把未匹配变成异常。

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

!!! success "检查点"
    - [ ] `json.parse("true false")` 的 `offset` 指向没能继续解析的位置，不是输入开头
    - [ ] 报错里的 `expected` 列出多个候选，而不是只有一条
    - [ ] 用 `parsePrefix` 读 `1 2` 不抛错，`matched` 为真，`end` 小于整段长度

第六步只讲了失败怎么变成 `ParseError`。下面三条机制只在你要改库或排查奇怪回溯时才用得上，折起来，主线可以跳过。

??? note "可选 · 深入：递归、选择与回溯"
    **递归**：`rule value` 构造期先占位、解析时再展开，定义体里能直接引用 `value`；手写版靠 `parseValue` 调 `parseObject`、`parseArray` 再回来。**选择**：`firstOf` 从同一起点按顺序尝试，第一个成功的分支胜出；全失败时保留最远偏移并合并期望。JSON 的分支首字符互不重叠，顺序不改变结果，只影响失败报告。**回溯**：`commit()` 让后续失败不能退回上层选择，`attempt()` 只取消失败子解析的提交，供共享前缀的分支使用；JSON 两个都不需要。

## 什么时候手写递归下降

组合子版把词法、选择与错误合并交给库，日常用 `grammar` 就够了。需要逐字符控制游标、边读边流式处理，或在固定位置自定义错误恢复时，手写递归下降更直接：每个非终结符一个方法，游标是唯一状态，失败点自己决定。代价是空白、转义、数字边界和每层递归都要自己维护，提交与回溯也归你管。

下面这份对照只手写结构和游标，字符串与数字继续复用上文的 `jsonString` 与 `jsonNumber`，把注意力放在递归本身。

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

## 完整源码

把正文的块按顺序拼起来，就是 `json-parser.el`：

```el
import {
	firstOf, constant, anyOf, sequence, optional, many, range,
	scalarSet, chars, exactly, grammar, list, pair
} from "el:text/patterns/index.el"

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

let literalParser = firstOf(
	constant("null", Json.Null),
	constant("true", Json.Boolean(t)),
	constant("false", Json.Boolean(nil))
)

let digit = range("0", "9")
let tailDigits = many(digit).text()
let needed = many(digit, 1).text()
let jsonNumber = sequence(
	optional("-"),
	anyOf("0", sequence(range("1", "9"), tailDigits)),
	optional(sequence(".", needed)),
	optional(sequence(anyOf("e", "E"), optional(anyOf("+", "-")), needed))
).map(Number)

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

第六步的 `import { ParseError }` 属于调用方，不在这份解析器文件里：解析器只负责产生失败，捕获与展示是使用者的选择。

## 改成你自己的

1. **把 `Json` 编码回去。** 写 `encodeJson(value: Json): Text`，用 `match` 分派六个成员，对象按 `members` 的顺序输出键值对。验收：解析再编码两次得到一样的文本，且重复键仍然出现两次。
2. **报告重复键。** 遍历 `Json.Object` 的 `members` 统计每个键出现的次数，超过一次就带位置报告。验收：`{"a":1,"a":2}` 报出 `a` 重复，`{"a":1,"b":2}` 不报。
3. **给递归下降加错误恢复。** 在折叠块基础上，让 `parseObject` 遇到坏成员时跳到下一个逗号继续，并收集所有失败位置。验收：同一份坏输入，组合子版只报最远的一个错误，你的版本报出全部。

## 卡住了？

- **现象：`01`、`1.`、`1e` 被当成合法数字。** 检查 `jsonNumber` 的整数部分是不是 `anyOf("0", ...)`，小数与指数是不是用了至少一位的 `needed`。
- **现象：含 `\u` 的字符串解析失败。** 孤立代理项在模式层就被排除了，这是规范要求。检查：`\u` 后是否正好四位十六进制数字，代理对是否成对。
- **现象：数组少写一个元素就报错。** `list` 默认拒绝尾逗号。检查：去掉最后一个逗号再试，别改成允许尾逗号来“修好”它。
- **现象：报错只有一个 `offset`，看不出期望什么。** 打印 `error.expected` 与 `error.contexts`，它们分别是合并后的候选期望和规则栈。

## 带走这三样

- 组合子的写法：常量、序列、选择、重复，一层层拼；递归规则先用 `rule` 占位，解析时再展开。
- 规范细节要逐字符写清楚：前导零、小数与指数的最少位数、控制字符、代理项配对，都不是“看起来像”就能过的。
- 失败报告也是接口：`ParseError` 的 `offset`、`expected`、`contexts` 决定别人能不能修好输入。

## 下一站：[规则式下棋机器人](logic-game.md)

> 解析器只回答“这段文本合不合法”。那“这盘棋该下哪一步”这种要在所有可能里挑一个的问题，能不能也用声明式规则写出来？

- 主推进：[规则式下棋机器人](logic-game.md)：把落子、胜负和优先级写成规则，让搜索去找答案。
- 想先补文本基础：[集合与文本](../stdlib/collections.md)：`Text` 的索引、切片与数组操作。
