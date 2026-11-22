# user-interface/platform/macos/window.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../../categories/user-interface.md) · [模块索引](../../../../modules.md) · [符号索引](../../../../symbols.md)

## macOS 原生窗口 {#api-26aedcdb857c3ff99e82}

源码：`src/stdlib/user-interface/platform/macos/window.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/macos/window.el#L1)

提供 macOS 原生窗口和事件循环。

## runWindow {#api-53fcc931b59bf0bc7698}

源码：`src/stdlib/user-interface/platform/macos/window.el:411` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/macos/window.el#L411)

运行单个窗口的事件循环，并在退出时关闭窗口。

```el-signature
export fn runWindow(window: Window)
```

### 示例：用法

```el
runWindow(window)
```
