# logic/goal.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 逻辑目标 {#api-a6acd8066373a2005190}

源码：`src/stdlib/logic/goal.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L5)

将统一、关系调用、合取、备选和否定等逻辑操作表示为可组合的 Goal 值。

## unify {#api-dcdf93cd11ed18b33734}

源码：`src/stdlib/logic/goal.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L45)

```el
export fn unify(left: Term, right: Term): Goal
```

**返回类型**：`Goal`

要求两个逻辑项统一，并将所得绑定传递给后续目标。

**参数**：left 第一个待统一项。

**参数**：right 第二个待统一项。

**返回值**：表示统一目标的 Goal。

### 示例：匹配变量和原子

```el
let goal = unify(variable(0), atom("Ada"))
```

## dif {#api-c04632f30e82c884636e}

源码：`src/stdlib/logic/goal.el:55` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L55)

```el
export fn dif(left: Term, right: Term): Goal
```

**返回类型**：`Goal`

延迟检查两个逻辑项不可相等的约束。

**参数**：left 第一个逻辑项。

**参数**：right 第二个逻辑项。

**返回值**：表示不等约束的 Goal。

### 示例：要求两个名字不同

```el
let goal = dif(variable(0), atom("Ada"))
```

## call {#api-ba744e200119324d52ac}

源码：`src/stdlib/logic/goal.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L64)

```el
export fn call(term: Term): Goal
```

**返回类型**：`Goal`

调用由构造子项表示的关系。

**参数**：term 关系名与参数组成的关系项。

**返回值**：关系调用 Goal。

### 示例：查询某个关系项

```el
let goal = call(compound("person", @[variable(0)]))
```

## all {#api-064c6979924b05a1874a}

源码：`src/stdlib/logic/goal.el:73` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L73)

```el
export fn all(goals: Goal[]): Goal
```

**返回类型**：`Goal`

按顺序执行一组目标，并在目标间传递逻辑绑定。

**参数**：goals 顺序执行的目标。

**返回值**：合取 Goal。

### 示例：合并两个条件

```el
let goal = all(@[call(compound("person", @[x])), dif(x, atom("Ada"))])
```

## choice {#api-6e9cf1260ffb06318a44}

源码：`src/stdlib/logic/goal.el:82` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/goal.el#L82)

```el
export fn choice(goals: Goal[]): Goal
```

**返回类型**：`Goal`

构造一组可选逻辑分支；各分支独立枚举答案。

**参数**：goals 备选分支。

**返回值**：备选 Goal。

### 示例：在两种状态中择一

```el
let goal = choice(@[call(atom("ready")), call(atom("waiting"))])
```
