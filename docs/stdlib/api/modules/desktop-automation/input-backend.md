# desktop-automation/input-backend.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/input-backend {#api-798f8b63b7274b962778}

源码：`src/stdlib/desktop-automation/input-backend.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/input-backend.el#L1)

定义桌面输入的通用坐标、鼠标按钮和可扩展后端接口；平台实现通过该接口提供原生输入能力。
`DesktopPoint` 使用桌面坐标，x 向右、y 向下；坐标是否落在屏幕范围内由具体操作/后端决定。

## DesktopPoint {#api-e3f56505abb1e96b961e}

源码：`src/stdlib/desktop-automation/input-backend.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/input-backend.el#L19)

表示桌面坐标或相对位移的二维数值对。该值本身不裁剪到屏幕范围。

```el-signature
export @assign(mode: "copy") class DesktopPoint
```

**参数**：x 水平坐标或位移。

**参数**：y 垂直坐标或位移。

### 示例：创建屏幕位置

```el
let point = DesktopPoint(640, 360)
```
