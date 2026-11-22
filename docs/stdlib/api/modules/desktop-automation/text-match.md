# desktop-automation/text-match.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/text-match {#api-8d6a1db68c1c02a941f6}

源码：`src/stdlib/desktop-automation/text-match.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/text-match.el#L1)

为窗口标题和可访问文本提供精确、前缀、包含及 Pattern 匹配条件。
Pattern 构造的匹配器优先使用模式搜索；普通文本按所选模式比较。

## DesktopTextMode {#api-ac2424060216790bfd27}

源码：`src/stdlib/desktop-automation/text-match.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/text-match.el#L14)

选择普通文本比较方式：完整相等、前缀或子串包含。

```el-signature
export enum DesktopTextMode
```

### 示例：创建包含匹配条件

```el
let mode = DesktopTextMode.Contains
```

## DesktopTextMatch {#api-fe2facf317ab6ced099f}

源码：`src/stdlib/desktop-automation/text-match.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/text-match.el#L24)

封装窗口文本条件。文本构造器使用精确/前缀/包含比较；Pattern 构造器在目标文本中查找模式。

```el-signature
export @assign(mode: "copy") class DesktopTextMatch
```

**参数**：text 待比较文本。

**参数**：mode 普通文本比较模式，默认精确匹配。

### 示例：用前缀匹配窗口标题

```el
let condition = DesktopTextMatch("项目 - ", DesktopTextMode.Prefix)
```
