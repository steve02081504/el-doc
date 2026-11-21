# graphics/plots/scene.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/graphics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Axis.title](#api-a4d4797ed3404ce71849)
- [Axis.xLabel](#api-f10c0642fe5d004d0498)
- [Axis.legend](#api-f02143990b2a187771a6)
- [Axis.zoom](#api-18baa6ba4368d91ece80)
- [Axis.reset](#api-ff466b801a4f53e1e402)

## 绘图坐标场景 {#api-14c028464fad264c9025}

源码：`src/stdlib/graphics/plots/scene.el:9` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L9)

保存折线数据、坐标轴标签、图例和视图范围，并按指定尺寸生成绘制帧。

## Axis {#api-cb6510f18b0f5b284d67}

源码：`src/stdlib/graphics/plots/scene.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L53)

可配置图表线条、标题、坐标标签及图例，并维护当前缩放范围。

```el
export @assign(mode: "shared") class Axis
```

### 示例：设置标题和图例

```el
figure.axis.title = "二次曲线"
figure.axis.legend = @["估计值"]
```

## Axis.title {#api-a4d4797ed3404ce71849}

源码：`src/stdlib/graphics/plots/scene.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L61)

绘图标题。

```el
let title: Text
```

**类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

### 示例：设置绘图标题

```el
figure.axis.title = "趋势"
```

## Axis.xLabel {#api-f10c0642fe5d004d0498}

源码：`src/stdlib/graphics/plots/scene.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L68)

横坐标轴标签。

```el
let xLabel: Text
```

**类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)

### 示例：标注横轴

```el
figure.axis.xLabel = "时间"
```

## Axis.legend {#api-f02143990b2a187771a6}

源码：`src/stdlib/graphics/plots/scene.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L75)

每条线对应的图例文本；若非空，数量必须与线条数一致。

```el
let legend: Text[]
```

**类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)[]

### 示例：设置一条线的图例

```el
figure.axis.legend = @["预测"]
```

## Axis.zoom {#api-18baa6ba4368d91ece80}

源码：`src/stdlib/graphics/plots/scene.el:100` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L100)

以当前视图中心缩放横纵坐标范围。

```el
fn zoom(factor: Number)
```

**参数**：factor 正的有限缩放倍数；大于 1 放大，小于 1 缩小。

**失败与异常**：缩放倍数无效时抛出 ShapeError。

### 示例：放大两倍

```el
figure.axis.zoom(2)
```

## Axis.reset {#api-ff466b801a4f53e1e402}

源码：`src/stdlib/graphics/plots/scene.el:112` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/scene.el#L112)

清除显式缩放范围，使范围重新按数据自动计算。

```el
fn reset()
```

### 示例：重置图表范围

```el
figure.axis.reset()
```
