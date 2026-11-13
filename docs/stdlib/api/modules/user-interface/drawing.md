# user-interface/drawing.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/user-interface.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 界面绘制主题 {#api-5c268392242b9719f437}

源码：`src/stdlib/user-interface/drawing.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/drawing.el#L17)

定义窗口绘制阶段使用的颜色与度量，并把解析后的语义主题角色映射到绘制值。

## PaintTheme {#api-4be1353cf98b66267dcf}

源码：`src/stdlib/user-interface/drawing.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/drawing.el#L37)

提供窗口绘制所需的背景、文字、按钮、选区和字体等颜色与度量；与 Definition.theme 的 Theme 类型不同。

```el
export class PaintTheme
```

### 示例：修改窗口绘制背景色

```el
let paint = darkPaintTheme()
paint.background = 0x20242B
window.theme = paint
```

## darkPaintTheme {#api-507fa392da014efe2281}

源码：`src/stdlib/user-interface/drawing.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/drawing.el#L117)

创建一份深色窗口绘制主题。

```el
export fn darkPaintTheme(): PaintTheme
```

**返回类型**：[`PaintTheme`](drawing.md#api-4be1353cf98b66267dcf)

**返回值**：可供 Window.theme 使用的 PaintTheme。

### 示例：设置窗口绘制主题

```el
window.theme = darkPaintTheme()
```
