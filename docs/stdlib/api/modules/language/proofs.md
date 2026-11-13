# language/proofs.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 证明内核原语 {#api-61171ddb609ecb13e078}

源码：`src/stdlib/language/proofs.el:2` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/proofs.el#L2)

提供 sort、依赖函数类型与相等证明所需的语言原语；具体证明脚本由普通语法和 tactic 库组合。

## Prop {#api-a376131941dc82f3eb3f}

源码：`src/stdlib/language/proofs.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/proofs.el#L13)

```el
export @builtin:qeth:proof:prop class Prop
```

命题的 sort；命题类型中的证明由证明内核检查，不作为普通运行时数据使用。

### 示例：声明一个命题值

```el
let proposition: Prop = Eq(Nat, zero, zero)
```

## Type {#api-2c69e2f6858e85964893}

源码：`src/stdlib/language/proofs.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/proofs.el#L20)

```el
export @builtin:qeth:proof:type fn Type(level): type
```

**返回类型**：`type`

表示给定 universe 层级的类型 sort。

### 示例：在类型注解中使用 Type

```el
let naturalType: type = Type(0)
```

## Eq {#api-d323fe4b5742a94294fc}

源码：`src/stdlib/language/proofs.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/proofs.el#L36)

```el
export @builtin:qeth:proof:eq fn Eq(carrier: type, left, right): type
```

**返回类型**：`type`

构造载体类型上两个项相等的命题；载体参数明确指定被比较项的类型。

**参数**：carrier 两端项的载体类型。

**参数**：left 等式左端。

**参数**：right 等式右端。

**返回值**：一个 Prop 命题类型。

### 示例：写出 Nat 上的反身等式

```el
let same: type = Eq(Nat, zero, zero)
```

## refl {#api-216f2c238f4488e3dbb6}

源码：`src/stdlib/language/proofs.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/proofs.el#L45)

```el
export @builtin:qeth:proof:refl fn refl(carrier: type, value)
```

为定义上相等的两端构造反身性证据；内核会检查载体与项的一致性。

**参数**：carrier 被比较项的载体类型。

**参数**：value 同时作为等式两端的项。

### 示例：证明零与自身相等

```el
fn zeroEqZero(): Eq(Nat, zero, zero) => prove { refl }
```
