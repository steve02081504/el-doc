# text/text.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/text.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Text.replaceAll](#api-29663683ec276c29c64c)
- [Text.split](#api-571742e199721a51aeb1)
- [Text.byte_count](#api-13f81dad5b9b0b1e9d52)
- [Text.count](#api-19e144cbe3af4ec540f3)
- [Text.startsWith](#api-92f3f2d6c9caa632ff40)
- [Text.endsWith](#api-a0002f7421f94384e4e1)
- [Text.contains](#api-60a702a27df0fb3b6913)
- [Text.trimEndChars](#api-3f97c8338da803f449ff)
- [Text.character](#api-72c219d2c7971b4efd7e)
- [Text.slice](#api-79542d4a724d1d48d0f4)

## 文本与字符 {#api-df8646ac427828d0bbf5}

源码：`src/stdlib/text/text.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L1)

提供 Unicode 标量文本、切片、查找、分割和字符转换等操作。文本下标按标量计数，编码字节数另行统计。

<span id="api-57699486a79aacef58f4"></span>

## Text~type {#api-6116e54b075df026a90a}

源码：`src/stdlib/text/text.el:132` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L132)

拥有 Unicode 标量序列的可变文本值；按值复制，UTF-8 字节数由 byte_count 单独提供。
裸文本视图装载时会复制其标量。切片与拼接可共享不可变 rope 节点，但得到独立 Text 值。

```el
@pure
@assign(mode: "copy")
export class Text extends Array<element: Char>
```

### 示例：读取标量数与 UTF-8 字节数

```el
let text = "你好"
console.stdout.writeLine(text.count, " ", text.byte_count)
```
预期标准输出：
```text
2 6
```

## Text.replaceAll {#api-29663683ec276c29c64c}

源码：`src/stdlib/text/text.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L175)

将文本中所有匹配项替换为指定内容，并返回新文本。

```el
fn replaceAll(pattern, replacement): Text
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)

**参数**：pattern 文本或文本模式。

**参数**：replacement 替换文本。

**返回值**：替换后的新文本。

### 示例：更换文件扩展名

```el
let renamed = "summary.txt".replaceAll(".txt", ".md")
console.stdout.writeLine(renamed)
```

## Text.split {#api-571742e199721a51aeb1}

源码：`src/stdlib/text/text.el:192` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L192)

按文本分隔符或文本模式拆分内容，返回各段组成的数组。

```el
fn split(pattern): Text[]
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)[]

**参数**：pattern 文本分隔符或支持 split 的模式。

**返回值**：拆分结果数组。

### 示例：拆分路径

```el
let parts = "reports/2026/summary.txt".split("/")
console.stdout.writeLine(parts.join(" | "))
```

## Text.byte_count {#api-13f81dad5b9b0b1e9d52}

源码：`src/stdlib/text/text.el:340` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L340)

返回文本编码为 UTF-8 后占用的字节数。

```el
get byte_count(): Integer
```

**返回类型**：[`Integer`](../../types.md#api-45690472287900730a5f)

**返回值**：UTF-8 字节数；这与 Unicode 标量数量不同。

### 示例：比较字符数与字节数

```el
let text = "你好"
console.stdout.writeLine(text.count, " ", text.byte_count)
```

## Text.count {#api-19e144cbe3af4ec540f3}

源码：`src/stdlib/text/text.el:359` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L359)

返回文本中的 Unicode 标量数量。

```el
override get count(): Integer
```

**返回类型**：[`Integer`](../../types.md#api-45690472287900730a5f)

**返回值**：标量数；UTF-8 编码字节数请读取 byte_count。

### 示例：读取文本长度

```el
console.stdout.writeLine("你好".count)
```

## Text.startsWith {#api-92f3f2d6c9caa632ff40}

源码：`src/stdlib/text/text.el:419` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L419)

判断文本是否以给定前缀开头。

```el
fn startsWith(prefix: Text): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：prefix 要检查的前缀。

**返回值**：匹配时为真，否则为假；空前缀总是匹配。

### 示例：检查目录前缀

```el
console.stdout.writeLine("reports/2026".startsWith("reports"))
```

## Text.endsWith {#api-a0002f7421f94384e4e1}

源码：`src/stdlib/text/text.el:430` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L430)

判断文本是否以给定后缀结尾。

```el
fn endsWith(suffix: Text): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：suffix 要检查的后缀。

**返回值**：匹配时为真，否则为假；空后缀总是匹配。

### 示例：检查文本扩展名

```el
console.stdout.writeLine("summary.txt".endsWith(".txt"))
```

## Text.contains {#api-60a702a27df0fb3b6913}

源码：`src/stdlib/text/text.el:441` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L441)

判断文本是否包含给定子串。

```el
fn contains(needle: Text): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：needle 要查找的子串。

**返回值**：包含时为真，否则为假；空子串总是包含在内。

### 示例：检查路径年份

```el
console.stdout.writeLine("reports/2026".contains("2026"))
```

## Text.trimEndChars {#api-3f97c8338da803f449ff}

源码：`src/stdlib/text/text.el:465` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L465)

从末尾移除属于给定字符集合的连续标量，返回文本值，不修改接收者。

```el
fn trimEndChars(characters: Text): Text
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)

**参数**：characters 要移除的字符集合；空文本不移除任何字符。

**返回值**：去除末尾匹配标量后的文本。

### 示例：去除路径末尾分隔符

```el
console.stdout.writeLine("reports///".trimEndChars("/"))
console.stdout.writeLine("abc".trimEndChars(""))
```
预期标准输出：
```text
reports
abc
```

## Text.character {#api-72c219d2c7971b4efd7e}

源码：`src/stdlib/text/text.el:502` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L502)

读取指定 Unicode 标量下标处的字符。

```el
virtual fn character(index: Number): Char
```

**返回类型**：[`Char`](../../types.md#api-3166547d46e101216338)

**参数**：index 从零开始的标量下标。

**返回值**：对应 Char。

**失败与异常**：debug 构建下标越界时抛出 RangeError。

### 示例：读取首字符

```el
let first = "hello".character(0)
console.stdout.writeLine(first)
```

## Text.slice {#api-79542d4a724d1d48d0f4}

源码：`src/stdlib/text/text.el:555` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L555)

返回指定左闭右开标量下标区间的文本。

```el
virtual fn slice(start: Number, to: Number): Text
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)

**参数**：start 区间起始下标。

**参数**：to 区间结束下标，不包含该位置。

**返回值**：新文本值，接收者不变；起点与终点相同时为空文本。

**失败与异常**：debug 构建中区间越界或终点小于起点时抛出 RangeError。

### 示例：取文本前缀

```el
console.stdout.writeLine("reports/2026".slice(0, 7))
```

## text_scalar {#api-0d11d4c56187bc5fad70}

源码：`src/stdlib/text/text.el:685` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L685)

将 Unicode 标量值转换为只含该标量的文本；拒绝代理项和超出 Unicode 范围的值。

```el
export fn text_scalar(value: Integer): Text
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)

**参数**：value Unicode 标量数值，范围为 0 到 1114111，且不在代理项区间内。

**返回值**：含一个 Unicode 标量的 Text。

**失败与异常**：EncodingError 当 value 不是 Unicode 标量时。

### 示例：从码点构造文本

```el
console.stdout.writeLine(text_scalar(20013))
```
预期标准输出：
```text
中
```

<span id="api-5684c75000d17c66817d"></span>

## TextView~constraints {#api-0c1cf6c54bcc86167e47}

源码：`src/stdlib/text/text.el:843` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L843)

创建只读 TextView 类型；可将元素统一宽度 bitWidth 和标量数量 size 固定为正值。
0 表示该维度不固定。固定宽度要求来源宽度相同，固定长度要求请求的视图长度相同。

```el
export fn TextView(bitWidth = 0, size = 0): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：bitWidth 固定的元素宽度；0 表示沿用来源宽度。

**参数**：size 固定的 Unicode 标量数量；0 表示长度动态。

**返回值**：具有指定宽度和长度约束的只读 TextView 类型。

**失败与异常**：RangeError 构造的视图不满足固定宽度、长度或范围约束时。

### 示例：从文本创建固定长度视图

```el
let source = "hello"
let View = TextView<size: 2>
let view = View(source, 1, 2)
console.stdout.writeLine(view.count())
```
预期标准输出：
```text
2
```

## Text~constraints {#api-82ffe95d03da0efc6fde}

源码：`src/stdlib/text/text.el:892` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L892)

创建受约束的 Text 类型。bitWidth 固定统一元素宽度，size 固定 Unicode 标量数量；0 表示不固定。
固定宽度构造和写入会检查字符声明宽度及标量值，固定长度文本不能改变长度。

```el
export fn Text(bitWidth = 0, size = 0): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：bitWidth 固定元素宽度，必须能容纳构造和写入的字符；0 表示动态宽度。

**参数**：size 固定 Unicode 标量数量；0 表示动态长度。

**返回值**：满足给定约束的 Text 类型。

**失败与异常**：RangeError 初始值不满足宽度/长度约束，或操作试图违反固定约束时。

### 示例：创建固定宽度文本

```el
let NarrowText = Text<bitWidth: 16>
let text = NarrowText("EL")
console.stdout.writeLine(text.count, " ", text.bitWidth())
```
预期标准输出：
```text
2 16
```
