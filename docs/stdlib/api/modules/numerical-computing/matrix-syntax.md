# numerical-computing/matrix-syntax.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 矩阵字面量宏 {#api-48b7562a1a347b3658c3}

源码：`src/stdlib/numerical-computing/matrix-syntax.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/matrix-syntax.el#L5)

提供按显式元素类型、逗号分列和分号分行的矩阵构造语法。

## matrix {#api-68271cb36d88cd6a7f40}

源码：`src/stdlib/numerical-computing/matrix-syntax.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/matrix-syntax.el#L29)

```el
export syntax matrix
```

以类型名和花括号行列表构造指定元素类型的二维张量。

**参数**：element 矩阵元素类型。

**参数**：rows 以逗号分列、分号分行的元素表达式；各行长度必须相同。

**返回值**：按列优先布局构造的二维 Tensor。

**失败与异常**：ShapeError 当各行长度不一致时由 matrixRows 抛出。

### 示例：构造一个整数系数矩阵

```el
let coefficients = matrix(Number) { 3, 1; 1, 2 }
```
示例展示接口用法；未运行验证。
