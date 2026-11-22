# language/layout/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/language.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 类布局策略 {#api-259089dd384923a2e451}

源码：`src/stdlib/language/layout/index.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L6)

描述字段与基类存储区域，并将自定义布局策略转换为经编译器校验的布局计划。

## LayoutInput {#api-e3db0b318c805d3389ea}

源码：`src/stdlib/language/layout/index.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L30)

收集待布局的全部区域，并单独记录普通字段与基类区域。

```el-signature
export class LayoutInput
```

### 示例：创建空布局输入

```el
let input = LayoutInput()
```

## LayoutPlan {#api-61af6e4750ca6adb4921}

源码：`src/stdlib/language/layout/index.el:60` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L60)

保存区域放置结果以及对象的总大小、对齐和打包参数。

```el-signature
export class LayoutPlan
```

### 示例：创建布局计划并设置结果

```el
let plan = LayoutPlan()
plan.finish(size: 16, align: 8)
```

## LayoutContext {#api-fee883c2b432dd442f03}

源码：`src/stdlib/language/layout/index.el:76` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L76)

提供自定义布局策略可用的最大对象大小和最大对齐值。

```el-signature
export class LayoutContext
```

### 示例：为目标布局创建上下文

```el
let context = LayoutContext(4096, 16)
```

<span id="api-962a14e982f5a5053868"></span>

## layouts~field-order {#api-4c46acc4d1f39e4c3b74}

源码：`src/stdlib/language/layout/index.el:203` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L203)

按字段名给出的顺序安排字段；未列出的基类区域会附加到字段之后。

```el-signature
export fn layouts(specification: Text[], options = @{})
```

**参数**：specification 字段名数组，必须恰好覆盖所有普通字段且不能重复。

**参数**：options 布局选项，可指定 align、size、fixed 或 pack。

**返回值**：接受 LayoutInput 与 LayoutContext 并生成 LayoutPlan 的策略。

**失败与异常**：当字段遗漏、重复、未知或选项导致布局约束冲突时抛出错误。

### 示例：指定字段顺序

```el
let policy = layouts(@["payload", "tag"])
```

## layouts~delegate {#api-473c732a320e5d20faa5}

源码：`src/stdlib/language/layout/index.el:226` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/layout/index.el#L226)

将已有布局策略包装为可传入布局选项的策略。

```el-signature
export fn layouts(specification, options = @{})
```

**参数**：specification 接受输入和上下文并返回 LayoutPlan 的布局策略。

**参数**：options 传递给该策略的选项值。

**返回值**：接受 LayoutInput 与 LayoutContext 并调用原策略的函数。

### 示例：包装现有策略

```el
let policy = layouts(compact, @{})
```
