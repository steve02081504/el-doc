# number/integer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 整数类型 {#api-68364e4f53a190873a42}

源码：`src/stdlib/number/integer.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer.el#L1)

提供不受机器字宽限制的精确整数类型。

## Integer {#api-5576cb3365ff716689cd}

源码：`src/stdlib/number/integer.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer.el#L17)

精确的有符号无界整数类型；非整数结果等违反约束的情况抛出 RangeError。

```el-signature
export let Integer: type
```

**类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
let value = Integer(-12)
let next = value + 1
```

## UnsignedInteger {#api-18d50d7b9b00bc84279f}

源码：`src/stdlib/number/integer.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/integer.el#L25)

精确的非负无界整数类型；负数等违反约束的情况抛出 RangeError。

```el-signature
export let UnsignedInteger: type
```

**类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
let value = UnsignedInteger(12)
let next = value + 1
```
