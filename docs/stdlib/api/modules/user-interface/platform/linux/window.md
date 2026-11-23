# user-interface/platform/linux/window.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../../categories/user-interface.md) · [模块索引](../../../../modules.md) · [符号索引](../../../../symbols.md)

## Linux 原生窗口 {#api-0b5f4f168a213adc6c39}

源码：`src/stdlib/user-interface/platform/linux/window.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/linux/window.el#L1)

提供 Linux 原生窗口和事件循环。

## runWindow {#api-fb6617debeb1a88a85d9}

源码：`src/stdlib/user-interface/platform/linux/window.el:735` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/linux/window.el#L735)

运行单个窗口的事件循环，并在退出时关闭窗口。

```el-signature
export fn runWindow(window: Window)
```

### 示例：用法

```el
// @external window: Window
runWindow(window)
```
