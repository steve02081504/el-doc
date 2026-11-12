# functions/comparison.el

本页由源码注释生成；示例未运行验证。

## 比较函数 {#api-a18c0171171f77de8691}

源码：`src/stdlib/functions/comparison.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L1)

将比较运算符作为二元函数传递；这些函数由默认前导模块重导出。

## greater {#api-8a55f98772b7baf5100c}

源码：`src/stdlib/functions/comparison.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L16)

```el
export fn greater(left, right)
```

返回 `left > right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否大于 2

```el
let result = greater(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```

## less {#api-08588d9928ec79dd4d7d}

源码：`src/stdlib/functions/comparison.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L30)

```el
export fn less(left, right)
```

返回 `left < right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否小于 2

```el
let result = less(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## greaterEqual {#api-52308672941998b72300}

源码：`src/stdlib/functions/comparison.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L44)

```el
export fn greaterEqual(left, right)
```

返回 `left >= right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否大于等于 2

```el
let result = greaterEqual(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```

## lessEqual {#api-9b200632fd4272d3aead}

源码：`src/stdlib/functions/comparison.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L58)

```el
export fn lessEqual(left, right)
```

返回 `left <= right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否小于等于 2

```el
let result = lessEqual(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## equal {#api-2cfd60af70cef1c6c2c0}

源码：`src/stdlib/functions/comparison.el:72` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L72)

```el
export fn equal(left, right)
```

返回 `left == right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否相等 2

```el
let result = equal(3, 2)
// 预期 result 为 nil；此处使用标准库 Number 的比较。
```

## notEqual {#api-38d267c230a373d3b311}

源码：`src/stdlib/functions/comparison.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/comparison.el#L86)

```el
export fn notEqual(left, right)
```

返回 `left != right` 的结果，用于需要二元可调用值的场合。

**参数**：left 左操作数；其类型须支持对应比较运算。

**参数**：right 右操作数，按普通运算符重载规则匹配。

**返回值**：原运算符的返回值；不额外转换成 Bool，也保留条件载体。

**失败与异常**：运算符抛出的异常原样传播。

**复杂度**：等于一次对应运算符调用的开销。

### 示例：判断 3 是否不相等 2

```el
let result = notEqual(3, 2)
// 预期 result 为 t；此处使用标准库 Number 的比较。
```
