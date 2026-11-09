# 集合与文本

日常程序的大部分工作是摆弄数据：一组值、一张键值表、一段文字。EL 的数组、映射、集合与惰性序列都来自标准库，`Text` 本身就是一个字符数组。这一页按“怎么建、怎么改、怎么遍历”的顺序讲完它们，最后给一个词频统计的完整例子。

## Array：变长数组

数组字面量写 `@[...]`，类型是 `Array<element: T>` 的实例。最常见的类型推断写法是直接声明 `let values = @[1, 2, 3]`。

```el
let values = @[10, 20, 30]

console.stdout.writeLine("count: ", values.count)
console.stdout.writeLine("first: ", values[0])

values.push(40)          // 追加到末尾，返回数组本身
values.unshift(0)        // 插到开头，返回数组本身
let last = values.pop()  // 取走末尾
let first = values.shift()  // 取走开头
```

`count` 与 `length` 是同义的只读长度，底层类型是机器整数 `Integer`；需要参与普通数值运算时写 `Number(values.count)`。`size` 在具体数组类型上也有同样含义。

索引读取写 `values[i]`，赋值写 `values[i] = value`。越界在 debug 构建下抛 `RangeError`；release 构建省去这类安全检查，调用方必须先保证下标在范围内。

### 切片与遍历

```el
let window = values.slice(1, 3)        // 定长切片：长度由区间决定
let copy = values.sliceDynamic(1, 3)   // 变长数组副本

for (let value in values) {
	console.stdout.writeLine("value: ", value)
}
```

`for in` 直接遍历元素，也可以在省略变量时用 `it` 指代当前元素。数组还提供一组链式操作：`map`、`filter`、`some`、`all`、`indexOf`、`includes`、`join`、`reversed`。

```el
let doubled = values.map(value => value * 2)
let big = values.filter(value => value > 20)
let text = values.join(", ")
```

`sort` 返回排好序的新数组，不修改原数组；`reverse` 原地反转并返回它，`reversed` 返回反转后的新数组。数组相加 `a + b` 得到拼接后的新数组。

## Map：键值表

`Map` 是一个类型工厂：先用键和值的类型实例化，再构造对象。

```el
let scores = Map<key: Text, value: Number>()
scores.set("ada", 98)
scores.set("grace", 96)

let ada = scores.getOr("ada", 0)
let count = scores.count
console.stdout.writeLine("ada: ", ada, " entries: ", count)
console.stdout.writeLine("has grace: ", scores.has("grace"))
```

- `set(key, value)` 写入并返回是否新增了键；
- `get(key)` 返回 `value | void_t`，键不存在时得到 `void`；
- `getOr(key, fallback)` 在缺失时返回默认值；
- `has(key)` 判断键是否存在；
- `count` 是条目数，`remove(key)` 删除，`clear()` 清空；
- `keys()`、`values()`、`entries()` 取快照数组，`for in` 遍历条目。

```el
for (let entry in scores) {
	console.stdout.writeLine(entry.key, " = ", entry.value)
}
```

下标写法 `scores["ada"]` 也能读，但键不存在时抛 `MissingKeyError`，而不是返回 `void`。需要“缺失可接受”时用 `get` 或 `getOr`。

## Set 与 BitSet

`Set<element: T>` 是去重的元素集合，用 `add`、`has`、`remove`，用 `values()` 取数组。

```el
let tags = Set<element: Text>()
tags.add("el")
tags.add("doc")
tags.add("el")
console.stdout.writeLine("tags: ", tags.count)   // 2
```

`Set` 还提供 `union`、`intersection`、`difference`、`symmetricDifference`、`isSubsetOf`、`isSupersetOf`、`isDisjointFrom`，这些运算返回新的集合。

`BitSet<size: N>` 是固定宽度的位集合，构造时把非负整数展开成 N 位，支持 `&`、`|`、`^`、`!`、`<<`、`>>` 以及 `rotateLeft`、`rotateRight`。

```el
let flags = BitSet<size: 8>(5)     // 二进制 00000101
console.stdout.writeLine("bits: ", flags.toNumber())
```

## Sequence：惰性序列

`lazy @[...]` 创建一个惰性序列（`Sequence`）。它不在构造时把所有元素算完，而是在每次迭代到某一步时才求值那一步。

```el
let numbers = lazy @[1, 2, 3, 4, 5]
let result = numbers.map(value => value * 2).filter(value => value > 4).collect()
console.stdout.writeLine(result.join(", "))   // 6, 8, 10
```

`Sequence` 的常用操作：`map`、`filter`、`drop`、`take`、`slice`、`sum`、`collect`、`consume`，也可以直接 `for in` 遍历。它适合“数据很多但只用到前几项”的场景：`take(10)` 之后，后面的元素根本不会被求值。

## Text：文本

`Text` 是统一宽度的字符序列，`"..."` 和 `'...'` 字面量都是 `Text`。拼接用 `+`，插值用反引号里的 `${...}`：

```el
let name = "EL"
let greeting = "hello, " + name
let message = `count=${3 + 4}, name=${name}`
console.stdout.writeLine(message)     // count=7, name=EL
```

插值在运行时从左到右逐个求值并拼接，和手写 `+` 等价。

### 长度、索引与字节

```el
let text = "hello"
console.stdout.writeLine("chars: ", text.count, " bytes: ", text.byte_count)

let first = text.character(0)       // Char
let code = Number(first.code())     // 字符的码点
text[0] = Char(72)                  // 下标也是可写位置
console.stdout.writeLine(text)      // Hello
```

`count` 是字符（Unicode 标量）数，`byte_count` 是按 UTF-8 编码后的字节数；两者对 ASCII 之外的内容不一样，比如一个汉字 `count` 是 1，`byte_count` 常是 3。索引位置返回字符视图，取值得到宽度匹配的 `Char`；定宽文本 `Text<bitWidth: N>` 的索引返回 `Char<bitWidth: N>`。

### 常用文本函数

```el
let path = "reports/2026/summary.txt"

console.stdout.writeLine(path.startsWith("reports"))
console.stdout.writeLine(path.endsWith(".txt"))
console.stdout.writeLine(path.contains("2026"))

let parts = path.split("/")          // Text[]
console.stdout.writeLine(parts.count)         // 3
console.stdout.writeLine(parts.join(" | "))   // reports | 2026 | summary.txt

let renamed = path.replaceAll(".txt", ".md")
let head = path.slice(0, 7)          // "reports"
```

`slice(start, end)` 是左闭右开区间；`replaceAll` 的第一个参数可以是字面文本，也可以是文本模式库里的模式对象。`find_text(text, needle, start)` 是 `el:text/` 里的普通函数，返回首次出现的下标，找不到返回 -1。

## 例子：词频统计

把一段单词数组变成“单词到次数”的表，再挑出只出现一次的词。

```el
fn wordCounts(words: Text[]): Map<key: Text, value: Number> {
	let counts = Map<key: Text, value: Number>()
	for (let word in words) {
		counts.set(word, counts.getOr(word, 0) + 1)
	}
	return counts
}

fn uniqueWords(words: Text[]): Text[] {
	let seen = Set<element: Text>()
	for (let word in words) seen.add(word)
	return seen.values()
}

let words = @["red", "blue", "red", "green", "blue", "red"]
let counts = wordCounts(words)

for (let entry in counts) {
	console.stdout.writeLine(entry.key, ": ", entry.value)
}
console.stdout.writeLine("unique: ", uniqueWords(words).join(", "))
```

`wordCounts` 用 `getOr(word, 0) + 1` 完成“没有就按 0 起算”，避免了先判断再取值的分支；`uniqueWords` 用 `Set` 去重，`values()` 把集合还原成数组。

## 数组与矩阵

`@[1, 2, 3]` 是长度可变的一维数组；`@(1, 2; 3, 4)` 是矩阵字面量，构造的是固定形状的数值表，两者不是同一种类型。矩阵的索引、运算与广播规则属于数值计算库的内容，不在这一页展开。

## 继续阅读

- [模块与包](../language/modules.md)：把这些函数拆进自己的模块，用 `export` 交出去。
- [错误处理与异步](../language/errors-async.md)：`Map` 缺失键、数组越界走的都是异常通道。
- [Console 与日志](console.md)：把统计结果按需要的格式写出去。
