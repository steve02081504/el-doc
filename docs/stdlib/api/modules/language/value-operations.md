# language/value-operations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 值操作 {#api-280ebc2abd7e81d204df}

源码：`src/stdlib/language/value-operations.el:3` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/value-operations.el#L3)

提供移动值、丢弃结果和交换值的操作。

## discard {#api-b9bad8e4863ef390b4f6}

源码：`src/stdlib/language/value-operations.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/value-operations.el#L20)

显式消费实参并返回 nil。实参按通常规则求值、传播异常并清理。

```el-signature
export fn discard(value)
```

### 示例：丢弃一次读取的结果

```el
// @external readValue: fn(): Number
discard(readValue())
```
