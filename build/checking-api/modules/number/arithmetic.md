# number/arithmetic.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 精确数值算术 {#api-d125166f5c4027134eeb}

源码：`src/stdlib/number/arithmetic.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/arithmetic.el#L1)

提供精确整数与有理数的底层算术。

<span id="api-8607b4bec9d7e055ed59"></span>

## add~integer {#api-2722253a063082140483}

源码：`src/stdlib/number/arithmetic.el:290` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/arithmetic.el#L290)

计算两个精确整数的和。

```el-signature
export fn add(left: NumericInt, right: NumericInt): NumericInt
```

**返回类型**：[`NumericInt`](../../types.md#api-185a41c160696f925b31)

### 示例：用法

```el
let sum = add(NumericInt(2), NumericInt(3))
```

## add~ratio {#api-4e965155c389d4df4882}

源码：`src/stdlib/number/arithmetic.el:965` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/arithmetic.el#L965)

计算两个精确有理数的和。

```el-signature
export fn add(left: NumericRatio, right: NumericRatio): NumericRatio
```

**返回类型**：[`NumericRatio`](../../types.md#api-5d824c7b2238be4ee74d)

### 示例：用法

```el
let sum = add(NumericRatio(1, 2), NumericRatio(1, 3))
```
