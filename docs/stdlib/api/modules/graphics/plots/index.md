# graphics/plots/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/graphics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Figure.axis](#api-a0ab54cd34a79111132b)
- [Figure.image](#api-05f4dfef014a883b90ed)
- [Figure.save](#api-4c3befca40a6315cb486)
- [Figure.show](#api-f8da8e4d08474a501002)

## 数值绘图 {#api-0072837f4ccf6b725f73}

源码：`src/stdlib/graphics/plots/index.el:9` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L9)

将浮点张量转换为线图场景，支持导出 SVG、保存文件或在图形环境中打开窗口。

## Figure {#api-daf4fb6b08acdf355a69}

源码：`src/stdlib/graphics/plots/index.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L28)

```el
export @assign(mode: "shared") class Figure
```

持有不可变数据快照生成的绘图坐标场景，可导出 SVG、保存文件或显示窗口。

### 示例：绘制并保存一张曲线图

```el
let figure = plot(xs, ys)
let svg = figure.image(640, 480)
figure.save("curve.svg")
```

## Figure.axis {#api-a0ab54cd34a79111132b}

源码：`src/stdlib/graphics/plots/index.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L35)

```el
let axis: Axis
```

**类型**：[`Axis`](scene.md#api-cb6510f18b0f5b284d67)

可直接配置标题、坐标轴标签、图例、缩放范围的绘图场景对象。

### 示例：设置图标题

```el
figure.axis.title = "二次曲线"
```

## Figure.image {#api-05f4dfef014a883b90ed}

源码：`src/stdlib/graphics/plots/index.el:46` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L46)

```el
fn image(width: Number = 900, height: Number = 600): Text
```

**返回类型**：`Text`

将当前坐标场景渲染为 SVG 文本；不打开窗口。

**参数**：width SVG 画布宽度，默认 900。

**参数**：height SVG 画布高度，默认 600。

**返回值**：SVG 文本。

### 示例：导出 SVG 字符串

```el
let svg = figure.image(640, 480)
```

## Figure.save {#api-4c3befca40a6315cb486}

源码：`src/stdlib/graphics/plots/index.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L56)

```el
fn save(path: Text, width: Number = 900, height: Number = 600)
```

将渲染后的 SVG 文本写入指定文件；不打开窗口。

**参数**：path SVG 目标文件路径。

**参数**：width SVG 画布宽度，默认 900。

**参数**：height SVG 画布高度，默认 600。

### 示例：保存默认尺寸 SVG

```el
figure.save("curve.svg")
```

## Figure.show {#api-f8da8e4d08474a501002}

源码：`src/stdlib/graphics/plots/index.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L64)

```el
fn show()
```

在可用的桌面显示环境中打开图表窗口并阻塞到窗口关闭。

**失败与异常**：当前平台没有可用绘图窗口或显示操作失败时抛出错误。

### 示例：打开交互式图表

```el
figure.show()
```

## PlotHost {#api-5f295492cd4341ff9541}

源码：`src/stdlib/graphics/plots/index.el:91` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L91)

```el
export @assign(mode: "shared") class PlotHost
```

管理多个非阻塞图表窗口，并提供集中轮询、运行与关闭生命周期。

### 示例：在宿主中运行创建的图表

```el
let host = PlotHost()
discard(figure.showOwned(host))
host.run()
```

## plot {#api-99a112e21dc6a727ab6d}

源码：`src/stdlib/graphics/plots/index.el:129` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/index.el#L129)

```el
export fn plot(x: Tensor<element: F64>, y: Tensor<element: F64>): Figure
```

**返回类型**：[`Figure`](index.md#api-daf4fb6b08acdf355a69)

从 F64 张量创建折线图；x 的行数须与 y 的行数相同，y 的每一列对应一条线。

**参数**：x 每个样本的横坐标，可为单列张量。

**参数**：y 样本纵坐标矩阵，每列生成一条曲线。

**返回值**：可配置坐标轴并导出或显示的 Figure。

**失败与异常**：张量形状不匹配、数据无法绘制或坐标轴配置无效时抛出错误。

### 示例：绘制一条曲线并导出 SVG

```el
let figure = plot(xs, ys)
let svg = figure.image(640, 480)
```
