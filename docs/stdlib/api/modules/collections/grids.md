# collections/grids.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/collections.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 二维网格 {#api-596d82bdf449321273ba}

源码：`src/stdlib/collections/grids.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/grids.el#L1)

二维网格相关接口。

## Grid {#api-4bd5d51097168c2493df}

源码：`src/stdlib/collections/grids.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/grids.el#L51)

创建元素类型固定的二维网格类型。坐标从零开始，宽高必须是非负整数。

```el-signature
export fn Grid(element: type): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**失败与异常**：非法尺寸或越界访问时抛出 RangeError。

### 示例：使用示例

```el
import { Grid } from "el:collections/grids"
let NumberGrid = Grid(Number)
let grid = NumberGrid(2, 3, 0)
grid[1, 2] = 7
let value = grid[1, 2]
```
