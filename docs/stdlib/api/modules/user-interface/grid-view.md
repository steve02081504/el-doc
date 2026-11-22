# user-interface/grid-view.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/user-interface.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 网格数据视图 {#api-7aee84e1930c2e236823}

源码：`src/stdlib/user-interface/grid-view.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/grid-view.el#L7)

将二维数据源转换为可按坐标读取的呈现视图。

## dataView {#api-f2ebc0934aca73231ec0}

源码：`src/stdlib/user-interface/grid-view.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/grid-view.el#L69)

将二维数据源包装为网格视图，并把每个单元转换为 DataCell。

```el-signature
export fn dataView(source): DataView
```

**返回类型**：[`DataView`](../../types.md#api-fe55397ce53724d83a5e)

**参数**：source 提供 rowCount()、columnCount() 和 cellAt(row, column) 的数据源。

**返回值**：列数、行数和按坐标访问单元的 DataView。

### 示例：从二维数据源创建视图（需调用方提供对象或绑定）

```el
// @external source: Tensor<element: Number>
let view = dataView(source)
```
