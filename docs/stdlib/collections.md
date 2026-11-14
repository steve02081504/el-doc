# 集合与文本

> 一组数、一张键值表、一段文字，看起来是三件事；写起来其实是同一个问题：你要按下标找、按键找，还是只想知道某样东西在不在？

!!! abstract "🎯 读完这页，你能"
    - 拿到一组值就选对容器：`Array`、`Map`、`Set`、`BitSet` 还是 `Sequence`
    - 用最常用的增删、查找与遍历操作处理数组和映射
    - 分清文本的字符数、字节数与下标，不把中文切坏
    - 写出一段词频统计，把数组变成映射再输出

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[值与类型](../language/values.md)</span>

## 先选容器：要下标、要键，还是要“在不在”

日常数据大部分落在下面几张表里。先选容器，再往下看细节：

| 我要…… | 用它 | 最小入口 |
| --- | --- | --- |
| 按下标存一串会变长的值 | `Array` | `@[1, 2, 3]` |
| 用键查值 | `Map` | `Map<key: Text, value: Number>()` |
| 只关心“在不在” | `Set` | `Set<element: Text>()` |
| 固定宽度的位标记 | `BitSet` | `BitSet<size: 8>(5)` |
| 数据很多但只用前几项 | `Sequence` | `lazy @[...]` |
| 处理一段文字 | `Text` | `"hello"` |

下面按使用频率讲 `Array`、`Map`、`Set` 与 `Text`；惰性序列和矩阵放到“可选 · 深入”。

## Array：改长度比改元素更常用

数组字面量写 `@[...]`，类型是 `Array<element: T>` 的实例。最常见的写法是直接声明：

```el
let values = @[10, 20, 30]

console.stdout.writeLine("count: ", values.count)
console.stdout.writeLine("first: ", values[0])

values.push(40)          // 追加到末尾，返回数组本身
values.unshift(0)        // 插到开头，返回数组本身
let last = values.pop()  // 取走末尾
let first = values.shift()  // 取走开头
```

`count` 是只读长度，返回机器整数 `NativeSignedInteger`，可以直接进行机器整数运算；需要按普通 `Number` 语义运算时，显式写 `Number(values.count)`，例如 `total / Number(values.count)`。这里的机器整数与公开的数学类型 `Integer`（受整数约束的 `Number`）不同。

索引读取写 `values[i]`，赋值写 `values[i] = value`。越界在 debug 构建下抛 `RangeError`；release 构建省去这类安全检查，调用方必须先保证下标在范围内。

!!! example "动手 30 秒"
    在第一个代码块末尾加一行 `console.stdout.writeLine(values[0])`，再把 `values.push(40)` 改成 `values.unshift(40)` 重跑。这一行从 `10` 变成 `40`：`unshift` 从开头插入，`push` 才是末尾追加。

切片时注意两个名字：`slice` 返回长度由区间决定的定长切片，`sliceDynamic` 返回变长数组副本。遍历用 `for in`，省略变量时用 `it` 指代当前元素：

```el
let window = values.slice(1, 3)        // 定长切片：长度由区间决定
let copy = values.sliceDynamic(1, 3)   // 变长数组副本

for (let value in values) {
	console.stdout.writeLine("value: ", value)
}
```

数组还提供一组链式操作：`map`、`filter`、`some`、`all`、`indexOf`、`includes`、`join`、`reversed`。

想把同一道统计题从手写循环逐步写成组合表达式，可以接着读[从遍历到函数组合](function-composition.md)：从 filter 开始，再用 batch/keep 和 over 提取重复处理。

```el
let doubled = values.map(value => value * 2)
let big = values.filter(value => value > 20)
let text = values.join(", ")
```

`sort` 返回排好序的新数组，不修改原数组；`reverse` 原地反转并返回它，`reversed` 返回反转后的新数组。数组相加 `a + b` 得到拼接后的新数组。

## Map：先实例化类型，再装数据

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
for (let {key, value} in scores) {
	console.stdout.writeLine(key, " = ", value)
}
```

这个片段接在上面的 `scores` 示例后，输出包含 `ada = 98` 和 `grace = 96` 两行；哈希映射不保证两行的先后顺序。也可以写 `for (let entry in scores)`，再读取条目的 `key` 和 `value`。

需要换成业务名称时，使用[对象解构](../reference/language/destructuring.md)的重命名写法：

```el
for (let {key: name, value: score} in scores) {
	console.stdout.writeLine(name, ": ", score)
}
```

`for` 接受一个元素绑定或解构模式，不支持 `for (let key, value in scores)`。当前 Map 的迭代器先取得条目数组快照，需要与条目数成正比的额外空间；循环期间新增、删除或替换映射条目不会改变这份快照。快照不深复制共享对象，修改共享值的字段仍可能被其他引用看到。给解构变量重新赋值不会写回映射；要替换映射中的值，显式调用 `scores.set(key, newValue)`。

下标写法 `scores["ada"]` 也能读，但键不存在时抛 `MissingKeyError`，而不是返回 `void`。需要“缺失可接受”时用 `get` 或 `getOr`。

## Set 去重，BitSet 记位

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

## Text：先数清楚，再切

`Text` 是统一宽度的字符序列，`"..."` 和 `'...'` 字面量都是 `Text`。拼接用 `+`，插值用反引号里的 `${...}`：

```el
let name = "EL"
let greeting = "hello, " + name
let message = `count=${3 + 4}, name=${name}`
console.stdout.writeLine(message)     // count=7, name=EL
```

插值在运行时从左到右逐个求值并拼接，和手写 `+` 等价。

??? question "先猜：`"你好".count` 和 `"你好".byte_count` 一样吗？"
    不一样。`count` 是 Unicode 标量数，`byte_count` 是 UTF-8 字节数。一个汉字 `count` 是 1，`byte_count` 常是 3；只有 ASCII 内容两者才相等。

### 字符数、索引和字节数是三件事

```el
let text = "hello"
console.stdout.writeLine("chars: ", text.count, " bytes: ", text.byte_count)

let first = text.character(0)       // Char
let code = Number(first.code())     // 字符的码点
text[0] = Char(72)                  // 下标也是可写位置
console.stdout.writeLine(text)      // Hello
```

`count` 是字符（Unicode 标量）数，`byte_count` 是按 UTF-8 编码后的字节数。索引位置返回字符视图，取值得到宽度匹配的 `Char`；定宽文本 `Text<bitWidth: N>` 的索引返回 `Char<bitWidth: N>`。

### 判断、切分、替换各有一个入口

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

`wordCounts` 用 `getOr(word, 0) + 1` 完成“没有就按 0 起算”，避免了先判断再取值的分支；`uniqueWords` 用 `Set` 去重，`values()` 把集合还原成数组。==先想清楚“缺了怎么办”，大多数集合代码就不需要 if。==

## 可选 · 深入：惰性序列与矩阵

`lazy @[...]` 创建一个惰性序列（`Sequence`）。它不在构造时把所有元素算完，而是在每次迭代到某一步时才求值那一步。

```el
let numbers = lazy @[1, 2, 3, 4, 5]
let result = numbers.map(value => value * 2).filter(value => value > 4).collect()
console.stdout.writeLine(result.join(", "))   // 6, 8, 10
```

`Sequence` 的常用操作：`map`、`filter`、`drop`、`take`、`slice`、`sum`、`collect`、`consume`，也可以直接 `for in` 遍历。它适合“数据很多但只用到前几项”的场景：`take(10)` 之后，后面的元素根本不会被求值。

`@[1, 2, 3]` 是长度可变的一维数组；`@(1, 2; 3, 4)` 是矩阵字面量，构造的是固定形状的数值表，两者不是同一种类型。矩阵的索引、运算与广播规则属于数值计算库的内容，不在这一页展开。

!!! warning "常见坑：三种“取不到”和一次“没生效”"
    - `Map["缺失键"]` 抛 `MissingKeyError`，不是返回 `void`；不确定有没有时用 `get` 或 `getOr`。
    - `sort` 不修改原数组，`reverse` 才原地改；把 `sort` 的返回值丢掉，会以为排序没生效。
    - release 构建不做数组越界检查，`values[10]` 不报错，只会给出无法预期的结果。

## 带走这三样

- 要下标用 `Array`，要键用 `Map`，只要“在不在”用 `Set`；选择发生在写第一行代码之前。
- 缺失用 `getOr` 接住，遍历用 `for in` 拿键和值，链式操作能省掉大部分临时变量。
- `Text` 按 Unicode 标量计数；字符数与字节数不是一回事，切中文前先确认用的是哪一种。

## 下一站：文件与网络

> 数据在内存里摆好了。怎么把它写进文件、发到网络，并在失败时知道错在哪一层？

- 主推进：[文件与网络](files-network.md)：文本与字节读写、逻辑路径、HTTP 请求和错误分类。
- 想先练手：[Console 与日志](console.md)：把统计结果按需要的格式写出去。
- 后面会用到：[模块与包](../language/modules.md)：把这些函数拆进自己的模块，用 `export` 交出去。
