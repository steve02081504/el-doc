# text/operations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/text.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文本辅助操作 {#api-93af0ee011db6adba6ea}

源码：`src/stdlib/text/operations.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/operations.el#L1)

提供文本定帧函数。

## frame {#api-df8b8d8436fc50452262}

源码：`src/stdlib/text/operations.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/operations.el#L15)

将文本编码为十进制标量长度、冒号和原文组成的定帧。

```el
export fn frame(text: Text): Text
```

**返回类型**：[`Text`](text.md#api-6116e54b075df026a90a)

**参数**：text 要编码的文本。

### 示例：对含分隔符的文本定帧

```el
import { frame } from "el:text/operations.el"
frame("猫:咪")
```
预期结果：3:猫:咪。

**返回值**：长度定帧文本。
