# user-interface/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/user-interface.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Definition.theme](#api-5faf0a2c3aefbf7d59fd)
- [Definition.textMask](#api-b3f8e6d993e4cc443109)

## 界面对象模型 {#api-df995c8f898cdfd44f5d}

源码：`src/stdlib/user-interface/model.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L11)

以 Definition 与带键 Edge 组成可复用的界面对象图；布局、事件与绘制阶段读取这份模型。

## LayoutStyle {#api-531edebc70e3c82ee7a8}

源码：`src/stdlib/user-interface/model.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L22)

描述节点的流向、间距、尺寸约束、权重、换行与滚动溢出策略；属性变更会发布变化通知。

```el-signature
@assign(mode: "shared")
export class LayoutStyle
```

### 示例：设置行布局和间距

```el
let style = LayoutStyle()
style.flow = "row"
style.gap = 8
```

## Definition {#api-92b8f0fb1d93b4e22dc2}

源码：`src/stdlib/user-interface/model.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L79)

一个可观察的界面定义节点，保存元素种类、文本、标识、样式、主题、监听器和子边。

```el-signature
@assign(mode: "shared")
export class Definition
```

### 示例：创建并配置标签

```el
import { element } from "el:user-interface/index.el"
let title = element("label", "欢迎", "title")
title.enabled = t
```

## Definition.theme {#api-5faf0a2c3aefbf7d59fd}

源码：`src/stdlib/user-interface/model.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L89)

可选的局部语义 Theme，按当前出现位置参与父子主题解析。

```el-signature
let theme: Theme | nil_t
```

**类型**：[`Theme`](../theme/model.md#api-2f8f76e6db4068dfe678) | [`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

### 示例：为根节点设置主色（需调用方提供对象或绑定）

```el
title.theme = Theme(@{primary: 0x80A7F0})
```

## Definition.textMask {#api-b3f8e6d993e4cc443109}

源码：`src/stdlib/user-interface/model.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L117)

用一个 Unicode 标量替代每个绘制的文本标量。设置后，输入框跳过热字符串匹配。

```el-signature
get textMask(): Text | nil_t
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a) | [`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

### 示例：掩蔽输入框的显示文本

```el
let password = element("input")
password.textMask = "•"
```

## GuiEvent {#api-d0161616ebcc781b1631}

源码：`src/stdlib/user-interface/model.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L138)

一次 GUI 输入事件的可变传播状态与载荷；监听器可停止传播或阻止默认处理。

```el-signature
@assign(mode: "shared")
export class GuiEvent
```

### 示例：在监听器中阻止默认行为

```el
// @external button: Definition
on(button, "click", event => event.preventDefault())
```

## on {#api-bec5c16251ba4e97600c}

源码：`src/stdlib/user-interface/model.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L183)

为定义节点注册指定类型的事件监听器，可选择在捕获阶段运行。

```el-signature
export fn on(element: Definition, kind: Text, action, capture: Bool = f)
```

**参数**：element 接收事件的界面定义。

**参数**：kind 事件类型，例如 `click`、`input` 或 `itemactivate`。

**参数**：action 接收 GuiEvent 的回调。

**参数**：capture 为真时在捕获阶段调用。

### 示例：注册按钮点击处理

```el
// @external button: Definition, status: Definition
on(button, "click", event => status.text = "已点击")
```

## element {#api-8fd177f7546412758246}

源码：`src/stdlib/user-interface/model.el:198` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L198)

创建 `column`、`row`、`label`、`button` 或 `input` 定义；未知种类会抛出错误。

```el-signature
export fn element(kind: Text, text: Text = "", id: Text = ""): Definition
```

**返回类型**：[`Definition`](model.md#api-92b8f0fb1d93b4e22dc2)

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

源码：`src/stdlib/user-interface/model.el:225` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L225)

将目标定义作为带键子边追加到父节点，并发布父节点变化。

```el-signature
export fn appendChild(parent: Definition, key: Text, target: Definition)
```

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

源码：`src/stdlib/user-interface/model.el:243` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L243)

按子边键移除第一个匹配项；未找到时不修改模型。

```el-signature
export fn removeChild(parent: Definition, key: Text): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**参数**：parent 要修改的父定义。

**参数**：key 要移除的边键。

**返回值**：找到并移除时为真，否则为假。

### 示例：移除可选说明行

```el
// @external root: Definition
let removed = removeChild(root, "hint")
```

## moveChild {#api-0a122f09a5627320ce81}

源码：`src/stdlib/user-interface/model.el:266` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/model.el#L266)

将已有子边移动到指定的最终索引；这是重排，不会创建新的边。

```el-signature
export fn moveChild(parent: Definition, key: Text, destination: Number)
```

**参数**：parent 子边所属父定义。

**参数**：key 要移动的边键。

**参数**：destination 移动完成后的零起始索引。

**失败与异常**：找不到 key 时抛出错误；调试模式还会检查索引有效性。

### 示例：将第二项移到首位

```el
// @external root: Definition
moveChild(root, "second", 0)
```
