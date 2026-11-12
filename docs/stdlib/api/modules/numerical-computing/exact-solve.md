# numerical-computing/exact-solve.el

本页由源码注释生成；示例未运行验证。

## solve {#api-6f0056070dbd04cf6e3a}

源码：`src/stdlib/numerical-computing/exact-solve.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/exact-solve.el#L21)

```el
export fn solve(borrow input: Matrix, borrow right: Matrix): Matrix
```

用精确 Number 消元求解方阵系统 A X = B；不使用浮点主元阈值。

**参数**：input 方阵 A，按借用读取。

**参数**：right rank-2 右端项 B，行数须与 A 相同，可含多列。

**返回值**：与 right 同列数的解矩阵 X。

**失败与异常**：ShapeError 当 A 非方阵或 B 形状不匹配时抛出。

**失败与异常**：NonFiniteInput 当输入包含非有限元素时抛出。

**失败与异常**：NumericallySingular 当消元步骤找不到非零主元时抛出。

### 示例：求解二元线性系统

```el
let solution = solve(@(3, 1; 1, 2), @(9; 8))
```
示例展示接口用法；未运行验证。
