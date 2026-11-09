# 实战：像 MATLAB 一样算

这一页从一个二元一次方程组出发，把矩阵字面量、`solve`、下标、逐元素运算与归约串成一个脚本，再说明精确数与浮点阈值各自负责什么；读完你能把一段矩阵公式直接写成 EL。

## 从消元到一行 `solve`

要求解的方程组是 `3x + y = 9` 与 `x + 2y = 8`。

手算时先把第一式乘 2，得到 `6x + 2y = 18`；两式相减，`2y` 消掉，常数项相减得到 10，于是 `5x = 10`，所以 `x = 2`。把 `x = 2` 代回第一式，`6 + y = 9`，得到 `y = 3`。

这两条式子写成矩阵形式是 `a * x = b`，其中 `a` 是系数矩阵，`b` 是右端项。EL 把消元交给 `solve`：

```el
let {
	a = @(3, 1; 1, 2)
	b = @(9; 8)
	x = solve(a, b)
	residual = b - a * x
}
```

`x` 是 2 行 1 列的列向量，两个元素依次是 2 与 3；`residual` 是同样形状的零向量。`b - a * x` 用解出的 `x` 重算右端项再相减，为零表示解精确满足两条方程。

`solve` 按借用读取 `a`、`b`，返回新的解矩阵；求解结束后两个输入仍是原来的值。需要保留原矩阵时不需要额外复制，求解内部已经用自己的工作副本完成消元。

`@(...)` 是矩阵字面量：逗号分列，分号分行。`@(3, 1; 1, 2)` 是两行两列，`@(9; 8)` 是两行一列。元素按行从左到右各求值一次；每行长度必须相等，不等长报 `ShapeError`。换行不代替分号，`@(1, 2)` 是一行两列，`@(1; 2)` 是两行一列，`@(1)` 是一行一列，`@()` 是零行零列。

`let { ... }` 是顺序声明组：四条绑定依次建立，不创建独立作用域，等价于在原位置依次写四条 `let`。这里 `x` 的初始化用到前面的 `a`、`b`，`residual` 又用到 `x`，书写顺序就是求值顺序。

矩阵下标从 0 开始，也就是零基索引，先写行下标，再写列下标。`solve` 的右端项按列排列，所以 `@(9; 8)` 是一列两行，而不是一行两列；若写成 `@(9, 8)`，它就是一行两列，行数与 `a` 对不上。

稠密矩阵按列优先存储：元素顺序先走完一列再走下一列。`columnMajor` 把这份逻辑顺序显式取出来，得到的结果与底层 stride 无关；索引、切片和矩阵乘都按同一套维度约定工作。

## 一次解多个右端项

同一个系数矩阵配多组右端项时，把右端项按列拼成一个矩阵，`solve` 一次返回同样列数的解：

```el
let a = @(3, 1; 1, 2)
let both = solve(a, @(9, 6; 8, 4))
let first = both[:, 0..1]
let second = both[:, 1..2]
```

`@(9, 6; 8, 4)` 的第一列 `[9; 8]` 就是原来的右端项，解得 `[2; 3]`；第二列 `[6; 4]` 对应另一个方程组，解得 `[8/5; 6/5]`，仍是精确有理数。`both[:, 0..1]` 与 `both[:, 1..2]` 各取一列，两侧都是选择器，所以结果保持 2 行 1 列。

多列右端项共用同一次消元，不必为每一列分别调用一次 `solve`。形状要求不变：右端项仍是 rank 2，行数必须等于方阵 `a` 的行数。

## 下标、切片与显式元素类型

```el
import { matrix, columnMajor } from "el:numerical-computing/index.el"

let m = @(1, 2, 3; 4, 5, 6)
let a = matrix(Number) { 3, 1; 1, 2 }
let corner = m[0, 2]
let lastRow = m[1, 0..3]
let secondColumn = m[:, 1..|1]
let flattened = columnMajor(m)
```

`m` 是 2 行 3 列。`m[0, 2]` 取第一行第三列，两个下标都是标量，结果是一个 `Number`，值为 3。

`m[1, 0..3]` 把行下标写成标量、列下标写成范围：标量下标删掉行轴，范围下标保留列轴，所以结果是一维的 `[4, 5, 6]`，而不是 1 行 3 列。

`m[:, 1..|1]` 的两个下标都是选择器：`:` 保留行轴，`1..|1` 保留列轴，并且只选中下标 1，结果是 2 行 1 列的 `[2; 5]`。`..` 是左闭右开范围，`..|` 是左闭右闭范围；`0..2` 选中 0、1，`0..|1` 选中 0、1，而 `1..|1` 只选中 1。切片下标同样从 0 开始，半开范围的右界可以等于轴长度，闭范围右界必须小于轴长度。

`columnMajor(m)` 返回列优先展开的一维值 `[1, 4, 2, 5, 3, 6]`：先读第一列的两个元素，再读第二列，最后读第三列。

`a = matrix(Number) { 3, 1; 1, 2 }` 是显式元素类型的矩阵字面量：圆括号里写元素类型，花括号里按分号分行、逗号分列。它与 `@(3, 1; 1, 2)` 构造的形状和元素都相同；`@(...)` 由默认提供者直接构造 `Number` 矩阵，而 `matrix(Number) { ... }` 把元素类型写出来，需要换元素类型时用这种写法。

## 矩阵乘、转置与逐元素运算

```el
import { sum, mean } from "el:numerical-computing/index.el"

let a = @(3, 1; 1, 2)
let m = @(1, 2, 3; 4, 5, 6)
let x = @(2; 3)
let product = a * x
let transposed = m.T
let elementwise = m .* m
let broadcasted = @(1, 2; 3, 4) .* @(10; 20)
let total = sum(a)
let average = mean(a)
let columnTotals = sum(m, 0)
```

`a * x` 是矩阵积：2×2 的 `a` 乘 2×1 的 `x`，得到 2×1 的 `[9; 8]`。`*` 在 rank 2 上是矩阵积，标量与矩阵相乘是缩放；两个 rank 1 的值相乘时必须先用 `row`、`col` 明确当成行还是列，`*` 不会把一维数组自动猜成矩阵的一行或一列。

`m.T` 是转置，2×3 的 `m` 变成 3×2：第一行 `[1, 2, 3]` 变成结果的第一列，第二行 `[4, 5, 6]` 变成第二列。`.T` 只交换两个轴；复数矩阵用 `.H` 取共轭转置。

`m .* m` 是逐元素乘，每个位置与自己的对应位置相乘，得到 `[1, 4, 9; 16, 25, 36]`。`.*`、`./`、`.^` 都是广播逐元素运算：对应轴对齐，短 shape 在末尾补 1，轴相等或一侧为 1 时合法，矩阵乘与逐元素乘用不同运算符区分。

`broadcasted` 把 2×2 与 2×1 相乘：列轴长度为 1 的一侧扩展到 2，第一行乘 10、第二行乘 20，得到 `[10, 20; 60, 80]`。广播只按声明的轴规则扩展，不会因为元素值碰巧相等就改变形状。

`sum(a)` 对全部元素求和，得到 7；`mean(a)` 得到 7/4，这是精确有理数，不经过二进制浮点舍入。`sum(m, 0)` 沿轴 0 归约，显式轴参数保留轴长 1，所以结果是 1 行 3 列的 `[5, 7, 9]`；需要标量时省略轴参数。

默认入口里的裸名 `sum`、`mean` 属于查询聚合；数值版本导出为 `numericsSum` 与 `numericsMean`。上面显式导入数值计算模块，所以代码里的 `sum`、`mean` 指代数值归约。归约的空输入也有明确结果：`sum` 的单位元是 0，而 `mean`、`min`、`max` 对空输入抛 `EmptyReduction`。

## 精确解与浮点阈值

`solve` 只接受方阵：`a` 必须是 rank 2 的方阵，`b` 必须也是 rank 2 且行数等于 `a` 的行数，否则在分解前抛 `ShapeError`。元素中出现非有限值时抛 `NonFiniteInput`。不满足这些形状检查的调用不会拿到部分解，也不会改动输入的 `a`、`b`。

默认 `Number` 矩阵的 `solve` 走精确有理数消元：只寻找非零主元，不套用 binary64 容差，也不把数据转成定宽浮点。因此上面的 `residual` 可以是精确的零向量，而不是接近零的浮点数。

```el
let singular = @(1, 2; 2, 4)
let rhs = @(3; 6)
try {
	discard(solve(singular, rhs))
} catch (error: NumericallySingular) {
	console.log.value(error)
}

let wide = @(1, 2, 3; 4, 5, 6)
try {
	discard(solve(wide, @(1; 2)))
} catch (error: ShapeError) {
	console.log.value(error)
}
```

第一个例子里两行成比例，消元到第二列时找不到非零主元，抛 `NumericallySingular`。第二个例子的 `wide` 是 2 行 3 列，不是方阵，`solve` 在检查形状时就抛 `ShapeError`。`solve` 失败后不会悄悄改成最小二乘或别的目标；需要拟合时显式调用 `leastSquares`。

`leastSquares` 处理 m×n 的最小二乘问题：要求 m ≥ n，且 A 满列数值秩，右端项的行数必须等于 m，多个右端项按列排列。m < n 抛 `ShapeError`；列主元在阈值下被判为零时抛 `RankDeficient`。它面向 `F64` 稠密矩阵：用列主元 Householder QR，每轮重新计算剩余列的稳定范数，把反射直接作用到右端项，不构造正规方程，也不先求逆。

F64 路径用不可变的 `NumericsPolicy` 保存容差：默认 eps 是 2^-52，rtol 是 max(m, n) × eps，atol 是 0。构造策略时就校验容差，rtol 必须满足 0 ≤ rtol < 1、atol 必须非负，否则抛 `InvalidNumericsPolicy`。LU 判断用原矩阵的最大绝对值作 scale，QR 判断用首个主元范数作 scale；主元或列范数不大于阈值就报告失败。

这些阈值是公开启发式，不是数学证明：`NumericallySingular` 与 `RankDeficient` 只说明算法在当前策略下拒绝继续，不证明矩阵的数学秩，不估计条件数，也不给前向误差保证。精确 `Number` 路径的奇异判定是“找不到非零主元”，与浮点路径“低于容差”是两种不同语义，不要混用两者的结论。

需要观察 F64 求解过程时，`solveDiagnostic` 与 `leastSquaresDiagnostic` 返回 `SolveReport`，里面有实际使用的方法、容差与阈值、成功判定，以及重新计算的 `b - a * x` 及其无穷范数。它们仍使用同一套算法与策略，不额外证明条件数或前向误差。

## 画一张图

`plot(x, Y)` 把输入数据拷贝成不可变快照，返回 `Figure` 场景对象；`Y` 的每一列画一条线，`x` 的长度必须等于 `Y` 的行数；如果设置了图例，标签数必须等于线数。当前入口接受 `F64` 元素的 `Tensor`，所以先给出本地的 `F64` 布局，再用 `linspace` 生成样本。

```el
import { plot, linspace, col } from "el:numerical-computing/index.el"
import { BitFloat } from "el:number/index.el"

let F64 = BitFloat<sign_bits: 1, fraction_bits: 52, exponent_bits: 11, exponent_bias: 1023>
let xs = col(linspace<F64>(-1, 1, 101))
let ys = 2 - 0.5 * xs + 0.25 * xs.^2
let figure = plot(xs, ys)
let svg = figure.image(640, 480)
figure.save("curve.svg")
```

`figure.image(640, 480)` 返回一段 SVG 文本，`figure.save(path)` 把同一张图写入文件；这两个入口都不打开窗口。`figure.axis` 是场景对象，标题与图例可以随后设置；`image` 与 `save` 的尺寸参数都可省略，默认是 900×600。`figure.show()` 才持有窗口并阻塞到关闭，这一页不展开 GUI 后端。

## 继续阅读

- [集合与文本](../stdlib/collections.md)：数组与矩阵字面量的区别，以及动态数组的常用操作。
- [运算符与表达式](../language/operators.md)：`*`、`.*`、`.^` 等运算符的结合性与优先级。
- [值与类型](../language/values.md)：`Number` 的精确值语义，以及值类型与引用类型的区别。
