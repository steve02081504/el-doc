# desktop-automation/screen.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/screen {#api-d56da774efe3d74179ca}

源码：`src/stdlib/desktop-automation/screen.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/screen.el#L1)

捕获桌面矩形区域为拥有像素资源的帧，并提供帧内坐标到桌面坐标的换算。
`captureScreen` 的宽高必须为正整数；使用完 `DesktopFrame` 后应关闭以释放图像资源。

## captureScreen {#api-55c495b6ab7a18bd6b31}

源码：`src/stdlib/desktop-automation/screen.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/screen.el#L59)

捕获以桌面坐标为原点的矩形区域。原点与尺寸须在有符号 32 位整数范围内，宽高至少为 1；平台不支持时抛出 `DesktopError(Unsupported)`。

```el-signature
export fn captureScreen(origin: DesktopPoint, width: Number, height: Number): DesktopFrame
```

**返回类型**：[`DesktopFrame`](../../types.md#api-74641b15dbfd0bd37b0f)

**参数**：origin 捕获矩形左上角的桌面坐标。

**参数**：width 捕获宽度，正整数。

**参数**：height 捕获高度，正整数。

**返回值**：帧对象；其图像资源由帧拥有，完成使用后调用 `close()`。

### 示例：捕获屏幕左上角 640×480 区域

```el
scope let frame = captureScreen(DesktopPoint(0, 0), 640, 480)
let image = frame.image
```
