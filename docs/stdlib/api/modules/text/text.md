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

## Text.replaceAll {#api-29663683ec276c29c64c}

源码：`src/stdlib/text/text.el:163` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L163)

```el
fn replaceAll(pattern, replacement): Text
```

**返回类型**：`Text`

将文本中所有匹配项替换为指定内容，并返回新文本。

**参数**：pattern 文本或文本模式。

**参数**：replacement 替换文本。

**返回值**：替换后的新文本。

### 示例：更换文件扩展名

```el
let renamed = "summary.txt".replaceAll(".txt", ".md")
console.stdout.writeLine(renamed)
```

## Text.split {#api-571742e199721a51aeb1}

源码：`src/stdlib/text/text.el:180` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L180)

```el
fn split(pattern): Text[]
```

**返回类型**：`Text[]`

按文本分隔符或文本模式拆分内容，返回各段组成的数组。

**参数**：pattern 文本分隔符或支持 split 的模式。

**返回值**：拆分结果数组。

### 示例：拆分路径

```el
let parts = "reports/2026/summary.txt".split("/")
console.stdout.writeLine(parts.join(" | "))
```

## Text.byte_count {#api-13f81dad5b9b0b1e9d52}

源码：`src/stdlib/text/text.el:328` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L328)

```el
get byte_count(): Integer
```

**返回类型**：`Integer`

返回文本编码为 UTF-8 后占用的字节数。

**返回值**：UTF-8 字节数；这与 Unicode 标量数量不同。

### 示例：比较字符数与字节数

```el
let text = "你好"
console.stdout.writeLine(text.count, " ", text.byte_count)
```

## Text.count {#api-19e144cbe3af4ec540f3}

源码：`src/stdlib/text/text.el:347` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L347)

```el
override get count(): Integer
```

**返回类型**：`Integer`

返回文本中的 Unicode 标量数量。

**返回值**：标量数；UTF-8 编码字节数请读取 byte_count。

### 示例：读取文本长度

```el
console.stdout.writeLine("你好".count)
```

## Text.startsWith {#api-92f3f2d6c9caa632ff40}

源码：`src/stdlib/text/text.el:407` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L407)

```el
fn startsWith(prefix: Text): Bool
```

**返回类型**：`Bool`

判断文本是否以给定前缀开头。

**参数**：prefix 要检查的前缀。

**返回值**：匹配时为真，否则为假；空前缀总是匹配。

### 示例：检查目录前缀

```el
console.stdout.writeLine("reports/2026".startsWith("reports"))
```

## Text.endsWith {#api-a0002f7421f94384e4e1}

源码：`src/stdlib/text/text.el:418` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L418)

```el
fn endsWith(suffix: Text): Bool
```

**返回类型**：`Bool`

判断文本是否以给定后缀结尾。

**参数**：suffix 要检查的后缀。

**返回值**：匹配时为真，否则为假；空后缀总是匹配。

### 示例：检查文本扩展名

```el
console.stdout.writeLine("summary.txt".endsWith(".txt"))
```

## Text.contains {#api-60a702a27df0fb3b6913}

源码：`src/stdlib/text/text.el:429` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L429)

```el
fn contains(needle: Text): Bool
```

**返回类型**：`Bool`

判断文本是否包含给定子串。

**参数**：needle 要查找的子串。

**返回值**：包含时为真，否则为假；空子串总是包含在内。

### 示例：检查路径年份

```el
console.stdout.writeLine("reports/2026".contains("2026"))
```

## Text.trimEndChars {#api-3f97c8338da803f449ff}

源码：`src/stdlib/text/text.el:453` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L453)

```el
fn trimEndChars(characters: Text): Text
```

**返回类型**：`Text`

从末尾移除属于给定字符集合的连续标量，返回文本值，不修改接收者。

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

源码：`src/stdlib/text/text.el:490` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L490)

```el
virtual fn character(index: Number): Char
```

**返回类型**：`Char`

读取指定 Unicode 标量下标处的字符。

**参数**：index 从零开始的标量下标。

**返回值**：对应 Char。

**失败与异常**：debug 构建下标越界时抛出 RangeError。

### 示例：读取首字符

```el
let first = "hello".character(0)
console.stdout.writeLine(first)
```

## Text.slice {#api-79542d4a724d1d48d0f4}

源码：`src/stdlib/text/text.el:543` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/text.el#L543)

```el
virtual fn slice(start: Number, to: Number): Text
```

**返回类型**：`Text`

返回指定左闭右开标量下标区间的文本。

**参数**：start 区间起始下标。

**参数**：to 区间结束下标，不包含该位置。

**返回值**：新文本值，接收者不变；起点与终点相同时为空文本。

**失败与异常**：debug 构建中区间越界或终点小于起点时抛出 RangeError。

### 示例：取文本前缀

```el
console.stdout.writeLine("reports/2026".slice(0, 7))
```
