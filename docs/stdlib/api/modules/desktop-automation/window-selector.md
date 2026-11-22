# desktop-automation/window-selector.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/window-selector {#api-08d85ac7af5d3b127262}

源码：`src/stdlib/desktop-automation/window-selector.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/window-selector.el#L1)

组合标题、进程、可见/活动状态、可访问文本及工作区等条件筛选桌面窗口。
`findUniqueDesktopWindow` 对多个匹配项报歧义；`findActiveDesktopWindow` 只查询当前活动窗口。

## WindowSelector {#api-6647b3c427285c6b8da9}

源码：`src/stdlib/desktop-automation/window-selector.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/window-selector.el#L25)

按可选属性组合筛选窗口。字符串字段可使用精确、前缀、包含或模式匹配；可访问树文本可通过 `text`/`excludeText` 匹配。
`processId` 必须为正整数，`executablePath` 必须为绝对路径，`workspaceId` 不得为空；未指定的条件不参与筛选。

```el-signature
export @assign(mode: "copy") class WindowSelector
```

**参数**：title 标题匹配条件。

### 示例：查找标题包含“编辑器”的窗口

```el
let selector = WindowSelector(title: WindowTextMatch("编辑器", WindowTextMode.Contains))
let matches = selectDesktopWindows(selector)
```

## selectDesktopWindows {#api-6e7d2ef1321480dba3a1}

源码：`src/stdlib/desktop-automation/window-selector.el:169` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/window-selector.el#L169)

按选择条件筛选窗口；已失效的窗口会被忽略。

```el-signature
export fn selectDesktopWindows(selector: WindowSelector, windows: DesktopWindow[] = listDesktopWindows()): DesktopWindow[]
```

**返回类型**：[`DesktopWindow`](../../types.md#api-b8c3f4d8bfbaa26f61f4)[]

**参数**：selector 窗口选择条件。

**参数**：windows 待筛选窗口，默认枚举当前桌面窗口。

**返回值**：匹配的窗口数组。

**失败与异常**：无法确定匹配所需的窗口属性时抛出 DesktopError。

### 示例：筛选桌面窗口

```el
let matches = selectDesktopWindows(WindowSelector())
```

## findActiveDesktopWindow {#api-e8eccc1eedc881c42d08}

源码：`src/stdlib/desktop-automation/window-selector.el:196` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/window-selector.el#L196)

检查当前活动窗口是否符合选择器；若窗口已消失或不匹配则返回 `nil`。选择器显式要求 `active: f` 属于无效输入。

```el-signature
export fn findActiveDesktopWindow(selector: WindowSelector): DesktopWindow | nil_t
```

**返回类型**：[`DesktopWindow`](../../types.md#api-b8c3f4d8bfbaa26f61f4) | [`nil_t`](../language/values.md#api-86357ad50ef0535f6333)

**参数**：selector 窗口筛选条件。

**返回值**：匹配的活动窗口，或 `nil`。

### 示例：获取标题匹配的当前活动窗口

```el
let window = findActiveDesktopWindow(WindowSelector(title: WindowTextMatch("终端")))
```
