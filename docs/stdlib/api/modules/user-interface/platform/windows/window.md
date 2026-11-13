# user-interface/platform/windows/window.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../../categories/user-interface.md) · [模块索引](../../../../modules.md) · [符号索引](../../../../symbols.md)

## 成员总览

- [WindowTimer.cancel](#api-8629377d5cfbe5cd888b)
- [Window.theme](#api-e300f3030755d4c6f210)
- [Window.onArrow](#api-0d5ac5569f84380b00ef)
- [Window.every](#api-397c3dde87e61de92229)
- [Window.getById](#api-10abbed4e4f712c61c10)

## Windows 窗口后端 {#api-d5cc2fc198b485a29d89}

源码：`src/stdlib/user-interface/platform/windows/window.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L13)

实现 Windows 原生窗口、窗口事件循环、定时器和界面元素查找接口。

## WindowTimer {#api-9b651467460e89936d5f}

源码：`src/stdlib/user-interface/platform/windows/window.el:171` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L171)

```el
export class WindowTimer
```

由窗口拥有的定时器句柄；取消会停止后续回调并释放回调捕获。

### 示例：取消一个窗口定时器

```el
let timer = window.every(1000, tick => updateClock())
timer.cancel()
```

## WindowTimer.cancel {#api-8629377d5cfbe5cd888b}

源码：`src/stdlib/user-interface/platform/windows/window.el:190` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L190)

```el
fn cancel()
```

停止定时器并释放其回调；重复调用不会产生额外副作用。

**注意**：只能从创建定时器的线程调用。

### 示例：停止定时器

```el
timer.cancel()
```

## Window {#api-9dc34e68c5ad778621d4}

源码：`src/stdlib/user-interface/platform/windows/window.el:216` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L216)

```el
export class Window
```

表示一个原生窗口及其界面视图、输入状态、绘制主题和窗口级资源。

### 示例：创建并运行窗口

```el
let window = showWindow(element("label", "你好"))
runWindow(window)
```

## Window.theme {#api-e300f3030755d4c6f210}

源码：`src/stdlib/user-interface/platform/windows/window.el:260` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L260)

```el
get theme(): PaintTheme
```

**返回类型**：[`PaintTheme`](../../drawing.md#api-4be1353cf98b66267dcf)

读取或替换窗口的绘制主题；赋值后立即刷新绘制。

### 示例：设置深色绘制主题

```el
window.theme = darkPaintTheme()
```

## Window.onArrow {#api-0d5ac5569f84380b00ef}

源码：`src/stdlib/user-interface/platform/windows/window.el:603` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L603)

```el
fn onArrow(action)
```

设置窗口级方向键处理器；没有元素焦点时接收方向键按下事件。

**参数**：action 接收 dx、dy 的回调；传入 void 移除处理器。

### 示例：注册方向键处理

```el
window.onArrow((dx, dy) => moveSelection(dx, dy))
```

## Window.every {#api-397c3dde87e61de92229}

源码：`src/stdlib/user-interface/platform/windows/window.el:619` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L619)

```el
@discardable fn every(milliseconds: Number, action): WindowTimer
```

**返回类型**：[`WindowTimer`](window.md#api-9b651467460e89936d5f)

注册窗口级近似定时器，窗口关闭时自动取消。

**参数**：milliseconds 整数毫秒间隔，范围 10 到 2147483647。

**参数**：action 每次触发时接收 WindowTimer 的回调。

**返回值**：可用于取消定时器的句柄。

**失败与异常**：间隔无效、窗口关闭或原生定时器创建失败时抛出错误。

### 示例：每秒更新标签

```el
discard(window.every(1000, tick => label.text = "更新"))
```

## Window.getById {#api-10abbed4e4f712c61c10}

源码：`src/stdlib/user-interface/platform/windows/window.el:649` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L649)

```el
fn getById(id: Text): ElementHandle
```

**返回类型**：`ElementHandle`

按精确 id 获取当前呈现中的元素句柄。

**参数**：id 非空且在挂载视图中唯一的元素标识。

**返回值**：对应出现位置的 ElementHandle。

**失败与异常**：id 不存在或元素已卸载时抛出错误。

### 示例：更新已挂载标签

```el
let label = window.getById("status")
label.text = "就绪"
```

## runWindow {#api-5a35178b26a593b8361d}

源码：`src/stdlib/user-interface/platform/windows/window.el:745` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L745)

```el
export fn runWindow(window: Window)
```

运行单个窗口的事件循环，并在退出时关闭窗口。

**参数**：window 要运行的窗口。

### 示例：运行窗口直到关闭

```el
runWindow(window)
```

## runWindows {#api-d58299be18ae530eb594}

源码：`src/stdlib/user-interface/platform/windows/window.el:768` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/platform/windows/window.el#L768)

```el
export fn runWindows(windows: Window[])
```

在同一事件循环中运行多个窗口；循环退出时关闭列表中的窗口。

**参数**：windows 要运行的窗口集合。

### 示例：同时运行两个窗口

```el
runWindows(@[firstWindow, secondWindow])
```
