# text/operations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/text.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文本辅助操作 {#api-93af0ee011db6adba6ea}

源码：`src/stdlib/text/operations.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/operations.el#L1)

提供定帧与子串查找等文本函数。

## frame {#api-df8b8d8436fc50452262}

源码：`src/stdlib/text/operations.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/operations.el#L15)

```el
export fn frame(text: Text): Text
```

将文本编码为十进制标量长度、冒号和原文组成的定帧。

**参数**：text 要编码的文本。

### 示例：示例

```el
import { frame } from "el:text/operations.el"
frame("猫:咪")
```
预期结果：3:猫:咪。

## find_text {#api-57c9ddeea00803ab4467}

源码：`src/stdlib/text/operations.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/operations.el#L28)

```el
export fn find_text(text: Text, needle: Text, start: Number): Number
```

在文本中从给定标量下标开始查找子串，返回首次匹配位置；未找到时返回 -1。

**参数**：text 要搜索的文本。

**参数**：needle 要查找的子串。

**参数**：start 起始标量下标。

**返回值**：子串起始下标；未找到为 -1。

### 示例：查找路径片段

```el
import { find_text } from "el:text/operations.el"
find_text("reports/2026", "2026", 0)
```
