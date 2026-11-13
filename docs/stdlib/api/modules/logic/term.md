# logic/term.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 逻辑项 {#api-649e018218a84eac0f6c}

源码：`src/stdlib/logic/term.el:3` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L3)

以变量、原子和带构造子项表示关系查询中的值，并提供受作用域约束的变量身份。

## Term {#api-7560e808aaee9c6517d2}

源码：`src/stdlib/logic/term.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L34)

逻辑搜索使用的项；变量以索引和作用域身份区分，复合项保存构造子及字段。

```el
export @assign(mode: "shared") class Term
```

### 示例：构造一个关系参数

```el
let person = compound("person", @[atom("Ada")])
```

## variable_scope {#api-eca5da0b5d022e6d8dc0}

源码：`src/stdlib/logic/term.el:74` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L74)

创建一份独立的逻辑变量作用域，使不同作用域中的同索引变量互不相同。

```el
export fn variable_scope(): VariableScope
```

**返回类型**：[`VariableScope`](../../types.md#api-bef3353d1cb343b10b6c)

**返回值**：新的变量作用域身份。

### 示例：创建作用域和变量

```el
let scope = variable_scope()
let x = variable(0, scope)
```

## variable {#api-c456fe7ff5956d254aa2}

源码：`src/stdlib/logic/term.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L86)

创建指定索引的逻辑变量，可显式提供作用域以避免变量身份冲突。

```el
export fn variable(index: Number, scope: VariableScope | void_t = void): Term
```

**返回类型**：[`Term`](term.md#api-7560e808aaee9c6517d2)

**参数**：index 非负整数变量索引。

**参数**：scope 可选变量作用域；省略时使用匿名作用域身份。

**返回值**：表示逻辑变量的 Term。

**失败与异常**：索引不是非负整数时抛出 TermError。

### 示例：创建查询变量

```el
let x = variable(0, variable_scope())
```

## atom {#api-1c020ac00b2b4255febc}

源码：`src/stdlib/logic/term.el:98` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L98)

创建由文本符号标识的零元逻辑项。

```el
export fn atom(symbol: Text): Term
```

**返回类型**：[`Term`](term.md#api-7560e808aaee9c6517d2)

**参数**：symbol 原子名称。

**返回值**：零元 Term。

### 示例：创建一个原子

```el
let ada = atom("Ada")
```

## compound {#api-369e82d0107bb36bce88}

源码：`src/stdlib/logic/term.el:108` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/term.el#L108)

创建带文本符号及有序字段的复合逻辑项。

```el
export fn compound(symbol: Text, fields: Term[]): Term
```

**返回类型**：[`Term`](term.md#api-7560e808aaee9c6517d2)

**参数**：symbol 构造子名称。

**参数**：fields 按构造子参数顺序排列的项。

**返回值**：复合 Term。

### 示例：表示带名字的记录项

```el
let person = compound("person", @[atom("Ada")])
```
