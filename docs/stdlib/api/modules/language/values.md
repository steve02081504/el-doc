# language/values.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 条件值与布尔类型 {#api-2d88f5f213a64c0f4b5b}

源码：`src/stdlib/language/values.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L1)

定义真值 t、假值 nil、无结果值 void 及其类型；Bool 是 t_t | nil_t 的类型别名。

## t_t {#api-9d7782192c7a4073755a}

源码：`src/stdlib/language/values.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L13)

真值 t 的类型，带 xata 条件属性；在条件中选择真分支。

```el
@infer(type: nil_t | t_t)
export @builtin:jahu:xata class t_t
```

### 示例：声明真值类型

```el
let confirmed: t_t = t
```

## nil_t {#api-86357ad50ef0535f6333}

源码：`src/stdlib/language/values.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L21)

假值 nil 的类型，带 netra 条件属性；在条件中选择假分支。

```el
@infer(type: nil_t | t_t)
export @builtin:jahu:netra class nil_t
```

### 示例：声明假值类型

```el
let rejected: nil_t = nil
```

## void_t {#api-d7b419fab395eef3d142}

源码：`src/stdlib/language/values.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L29)

无结果值 void 的类型，带 lohk 条件属性；与假值的 nil_t 是不同类型。

```el
@discardable
export @builtin:jahu:lohk class void_t
```

### 示例：声明缺失结果

```el
let missing: void_t = void
```

## t {#api-d518aa3528cdac961832}

源码：`src/stdlib/language/values.el:43` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L43)

标准环境提供的真值绑定，类型为 t_t；它是普通源码值，不是关键字。

```el
export let t: t_t = t_t()
```

**类型**：[`t_t`](values.md#api-9d7782192c7a4073755a)

### 示例：使用真值选择分支

```el
if (t) console.stdout.writeLine("yes")
```
```text
yes
```

## nil {#api-4bd0d9b4e484c9dd0771}

源码：`src/stdlib/language/values.el:54` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L54)

标准环境提供的假值绑定，类型为 nil_t；它不表示缺失结果。

```el
export let nil: nil_t = nil_t()
```

**类型**：[`nil_t`](values.md#api-86357ad50ef0535f6333)

### 示例：使用假值选择分支

```el
if (nil) console.stdout.writeLine("yes")
else console.stdout.writeLine("no")
```
```text
no
```

## void {#api-9df4f08e67ebcfb3d76a}

源码：`src/stdlib/language/values.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L61)

标准环境提供的无结果值绑定，类型为 void_t；它与假值 nil 不同。

```el
export let void: void_t = void_t()
```

**类型**：[`void_t`](values.md#api-d7b419fab395eef3d142)

### 示例：返回无结果

```el
fn finish(): void_t { return void }
```

<span id="api-30bb27bd4dfab8e35a94"></span>

## Bool~type {#api-3f0af31783849ef30c6e}

源码：`src/stdlib/language/values.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L77)

布尔类型别名，定义就是 t_t | nil_t；Bool 的值已经属于该联合，不需要再转换成联合类型。

```el
export let Bool: type = t_t | nil_t
```

**类型**：[`type`](../../../../reference/language/types.md)

**注意**：t 和 nil 是值名字；联合类型中的成员是类型 t_t 和 nil_t。此别名与同名的条件求值函数有不同声明身份。

参见：[language/values::t_t](values.md#api-9d7782192c7a4073755a)

参见：[language/values::nil_t](values.md#api-86357ad50ef0535f6333)

参见：[language/values::Bool~condition](values.md#api-3bcf0c5bba9b54c4a14d)

### 示例：使用布尔类型的两种值

```el
let accepted: Bool = t
let rejected: Bool = nil
```

## Bool~condition {#api-3bcf0c5bba9b54c4a14d}

源码：`src/stdlib/language/values.el:92` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/values.el#L92)

按输入的条件行为返回 t 或 nil；同名的 Bool 类型本身是 t_t | nil_t 的别名。

```el
export fn Bool(value = nil): Bool
```

**返回类型**：[`Bool`](values.md#api-3f0af31783849ef30c6e)

**参数**：value 要判断的值；省略时使用 nil。

**返回值**：条件为真时返回 t，否则返回 nil，返回值的类型为 Bool。

**失败与异常**：条件判断的转换或求值失败时传播异常。

参见：[language/values::Bool~type](values.md#api-3f0af31783849ef30c6e)

### 示例：把数值的条件行为归一为布尔值

```el
if (Bool(1)) console.stdout.writeLine("yes")
```
```text
yes
```
