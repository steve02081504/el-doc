# graphics/plots/font.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/graphics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 绘图字体 {#api-f64ae59363b442fe9d00}

源码：`src/stdlib/graphics/plots/font.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/font.el#L1)

为绘图配置系统字体或数位字形文件。

## digitPlotFont {#api-3d2d8ed27a8c642d35a7}

源码：`src/stdlib/graphics/plots/font.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/plots/font.el#L117)

从数位字体文件读取绘图用字形。按 paths 顺序查找字符，缺省使用目标基数。

```el-signature
export fn digitPlotFont(paths: FilePath[], radix: Number | nil_t = nil): PlotFont
```

**返回类型**：[`PlotFont`](../../../types.md#api-74d8685d683489e27de6)

### 示例：设置绘图字形来源

```el
import { digitPlotFont } from "el:graphics/plots/"
import { Path } from "el:filesystem/"
let font = digitPlotFont(@[Path("plot.ttf")])
```
