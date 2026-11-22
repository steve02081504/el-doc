# text/patterns/lexical.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/text.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 词法模式 {#api-e507a9f42c56088740be}

源码：`src/stdlib/text/patterns/lexical.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/lexical.el#L1)

提供数字、标识符与文本的词法匹配模式。

## integer {#api-05bb58ab88da201c5d66}

源码：`src/stdlib/text/patterns/lexical.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/text/patterns/lexical.el#L22)

创建匹配可选符号和十进制数字的整数模式，转换后的值受指定数值约束。

```el-signature
export fn integer(min, max, epsilon)
```

### 示例：用法

```el
let pattern = integer(0, 100, 0)
```
