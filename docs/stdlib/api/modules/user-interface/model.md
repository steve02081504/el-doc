# user-interface/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/user-interface.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Definition.theme](#api-5faf0a2c3aefbf7d59fd)

## 界面对象模型 {#api-df995c8f898cdfd44f5d}

源码：`src/stdlib/user-interface/model.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L10)

以 Definition 与带键 Edge 组成可复用的界面对象图；布局、事件与绘制阶段读取这份模型。

## LayoutStyle {#api-531edebc70e3c82ee7a8}

源码：`src/stdlib/user-interface/model.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L21)

```el
@assign(mode: "shared")
export class LayoutStyle
```

描述节点的流向、间距、尺寸约束、权重、换行与滚动溢出策略；属性变更会发布变化通知。

### 示例：设置行布局和间距

```el
let style = LayoutStyle()
style.flow = "row"
style.gap = 8
```

## Definition {#api-92b8f0fb1d93b4e22dc2}

源码：`src/stdlib/user-interface/model.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L78)

```el
@assign(mode: "shared")
export class Definition
```

一个可观察的界面定义节点，保存元素种类、文本、标识、样式、主题、监听器和子边。

### 示例：创建并配置标签

```el
import { element } from "el:user-interface/index.el"
let title = element("label", "欢迎", "title")
title.enabled = t
```

## Definition.theme {#api-5faf0a2c3aefbf7d59fd}

源码：`src/stdlib/user-interface/model.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L88)

```el
let theme: Theme | void_t
```

**类型**：[`Theme`](../theme/model.md#api-2f8f76e6db4068dfe678) | [`void_t`](../language/values.md#api-d7b419fab395eef3d142)

可选的局部语义 Theme，按当前出现位置参与父子主题解析。

### 示例：为根节点设置主色

```el
root.theme = Theme(@{primary: 0x80A7F0})
```

## GuiEvent {#api-d0161616ebcc781b1631}

源码：`src/stdlib/user-interface/model.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L117)

```el
@assign(mode: "shared")
export class GuiEvent
```

一次 GUI 输入事件的可变传播状态与载荷；监听器可停止传播或阻止默认处理。

### 示例：在监听器中阻止默认行为

```el
on(button, "click", event => event.preventDefault())
```

## on {#api-bec5c16251ba4e97600c}

源码：`src/stdlib/user-interface/model.el:160` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L160)

```el
export fn on(element: Definition, kind: Text, action, capture: Bool = nil)
```

为定义节点注册指定类型的事件监听器，可选择在捕获阶段运行。

**参数**：element 接收事件的界面定义。

**参数**：kind 事件类型，例如 `click`、`input` 或 `itemactivate`。

**参数**：action 接收 GuiEvent 的回调。

**参数**：capture 为真时在捕获阶段调用。

### 示例：注册按钮点击处理

```el
on(button, "click", event => status.text = "已点击")
```

## element {#api-8fd177f7546412758246}

源码：`src/stdlib/user-interface/model.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L175)

```el
export fn element(kind: Text, text: Text = "", id: Text = ""): Definition
```

**返回类型**：[`Definition`](model.md#api-92b8f0fb1d93b4e22dc2)

创建 `column`、`row`、`label`、`button` 或 `input` 定义；未知种类会抛出错误。

**参数**：kind 支持的元素种类。

**参数**：text 初始文本。

**参数**：id 可选的查找标识。

**返回值**：新建的共享 Definition。

**失败与异常**：传入未知 kind 时抛出 GUI 错误。

### 示例：生成一个带标识的按钮

```el
let save = element("button", "保存", "save")
```

## appendChild {#api-cdf7dba1323f03ef85c8}

源码：`src/stdlib/user-interface/model.el:202` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L202)

```el
export fn appendChild(parent: Definition, key: Text, target: Definition)
```

将目标定义作为带键子边追加到父节点，并发布父节点变化。

**参数**：parent 接收新子边的定义。

**参数**：key 在该父节点内唯一的子边键。

**参数**：target 被引用的子定义；定义可在多个位置复用。

**失败与异常**：同一父节点已有相同 key 时抛出错误。

### 示例：组装窗口内容

```el
let root = element("column")
appendChild(root, "heading", element("label", "设置"))
```

## removeChild {#api-89c99015e38050658540}

源码：`src/stdlib/user-interface/model.el:219` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L219)

```el
export fn removeChild(parent: Definition, key: Text): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

按子边键移除第一个匹配项；未找到时不修改模型。

**参数**：parent 要修改的父定义。

**参数**：key 要移除的边键。

**返回值**：找到并移除时为真，否则为假。

### 示例：移除可选说明行

```el
let removed = removeChild(root, "hint")
```

## moveChild {#api-0a122f09a5627320ce81}

源码：`src/stdlib/user-interface/model.el:241` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L241)

```el
export fn moveChild(parent: Definition, key: Text, destination: Number)
```

将已有子边移动到指定的最终索引；这是重排，不会创建新的边。

**参数**：parent 子边所属父定义。

**参数**：key 要移动的边键。

**参数**：destination 移动完成后的零起始索引。

**失败与异常**：找不到 key 时抛出错误；调试模式还会检查索引有效性。

### 示例：将第二项移到首位

```el
moveChild(root, "second", 0)
```
