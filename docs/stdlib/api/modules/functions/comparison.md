# functions/comparison.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/functions.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 比较函数 {#api-a18c0171171f77de8691}

源码：`src/stdlib/functions/comparison.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L1)

将比较运算符作为多元函数传递；零个或一个输入返回 t，二元调用保留运算符结果，多元调用短路。

## greater {#api-8a55f98772b7baf5100c}

源码：`src/stdlib/functions/comparison.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L30)

二元调用返回 `left > right` 的结果；零个或一个输入返回 t。
更多输入按从左到右的相邻对比较，遇到失败即停止。

```el
export fn greater(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n-1 次比较。

### 示例：判断 3 是否大于 2

```el
let result = greater(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```

## less {#api-08588d9928ec79dd4d7d}

源码：`src/stdlib/functions/comparison.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L45)

二元调用返回 `left < right` 的结果；零个或一个输入返回 t。
更多输入按从左到右的相邻对比较，遇到失败即停止。

```el
export fn less(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n-1 次比较。

### 示例：判断 3 是否小于 2

```el
let result = less(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## greaterEqual {#api-52308672941998b72300}

源码：`src/stdlib/functions/comparison.el:60` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L60)

二元调用返回 `left >= right` 的结果；零个或一个输入返回 t。
更多输入按从左到右的相邻对比较，遇到失败即停止。

```el
export fn greaterEqual(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n-1 次比较。

### 示例：判断 3 是否大于等于 2

```el
let result = greaterEqual(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```

## lessEqual {#api-9b200632fd4272d3aead}

源码：`src/stdlib/functions/comparison.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L75)

二元调用返回 `left <= right` 的结果；零个或一个输入返回 t。
更多输入按从左到右的相邻对比较，遇到失败即停止。

```el
export fn lessEqual(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n-1 次比较。

### 示例：判断 3 是否小于等于 2

```el
let result = lessEqual(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## equal {#api-2cfd60af70cef1c6c2c0}

源码：`src/stdlib/functions/comparison.el:90` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L90)

二元调用返回 `left == right` 的结果；零个或一个输入返回 t。
更多输入按从左到右的相邻对比较，遇到失败即停止。

```el
export fn equal(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n-1 次比较。

### 示例：判断 3 是否相等 2

```el
let result = equal(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## notEqual {#api-38d267c230a373d3b311}

源码：`src/stdlib/functions/comparison.el:105` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L105)

二元调用返回 `left != right` 的结果；零个或一个输入返回 t。
更多输入检查所有位置对均满足 !=，按后项顺序依次与此前各项比较，遇到失败即停止。

```el
export fn notEqual(...values)
```

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：二元调用原样返回运算符结果；多元调用在前缀通过后返回最后一次比较结果，提前失败返回 nil。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：二元调用执行一次比较；多元调用最多执行 n(n-1)/2 次比较。

### 示例：判断 3 是否不相等 2

```el
let result = notEqual(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```
