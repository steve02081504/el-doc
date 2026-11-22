# desktop-automation/input.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/input {#api-f1897f3f47023441afdd}

源码：`src/stdlib/desktop-automation/input.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/input.el#L1)

打开桌面键盘与指针输入会话，提供按键、文本、移动、点击、拖动和滚动操作。
使用 `DesktopInput()` 后应调用 `close()`；析构也会关闭后端。显式按下/抬起由调用方配对管理。

## DesktopInput {#api-568554f4935ccab451b7}

源码：`src/stdlib/desktop-automation/input.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/input.el#L52)

持有一个桌面输入后端会话。合成按键/点击会配对释放；`keyDown`、`keyUp`、`buttonDown` 与 `buttonUp` 则由调用方显式配对。
会话关闭后再次操作会抛出 `DesktopError(Closed)`；`close()` 可重复调用，析构时也会关闭后端。

```el-signature
export @assign(mode: "shared") class DesktopInput
```

### 示例：输入文本并关闭会话

```el
scope let input = DesktopInput()
input.sendText("hello")
input.close()
```
