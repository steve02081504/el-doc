# 实战：像 MATLAB 一样算

> 一个二元一次方程组，手算要三步消元；写成矩阵之后，它能不能只剩一行 `solve`？

!!! abstract "🎯 做完这个项目，你能"
    - 用 `@(...)` 矩阵字面量与 `solve` 解方程组，并用残差验证解
    - 分清标量下标与范围下标，知道结果的轴为什么有时消失
    - 用 `.*`、`.^` 广播与 `sum`／`mean` 做逐元素运算和归约
    - 说清精确有理数解与浮点阈值两条路径的边界

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：[运算符与表达式](../language/operators.md)、矩阵字面量、精确数</span>

## 目标与边界

数值脚本适合把公式一行行搬进代码：矩阵、下标、逐元素运算和归约各有固定形状。这一页把矩阵字面量、`solve`、切片、广播与归约串成脚本，并说明精确数与浮点阈值的分工。

刻意不做：推导分解算法、展开绘图后端、讨论稀疏与 GPU 调度。验收标准：

- `solve` 解出的 `x` 满足 `b - a * x` 为零向量
- 多列右端项一次解完，两列结果都是精确有理数
- 标量下标删轴、范围下标留轴，形状与下标一一对应
- 奇异矩阵与形状错误分别抛 `NumericallySingular` 与 `ShapeError`

## 第一步：从消元到一行 `solve`

要求解的方程组是 `3x + y = 9` 与 `x + 2y = 8`。

手算时先把第一式乘 2 得到 `6x + 2y = 18`，两式相减消掉 `2y`，`5x = 10`，所以 `x = 2`；代回第一式得 `y = 3`。

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

`@(...)` 是矩阵字面量：逗号分列，分号分行；`@(3, 1; 1, 2)` 两行两列，`@(9; 8)` 两行一列。元素按行从左到右各求值一次，每行必须等长，不等长报 `ShapeError`。换行不代替分号：`@(1, 2)` 一行两列，`@(1; 2)` 两行一列，`@(1)` 一行一列，`@()` 零行零列。

`let { ... }` 是顺序声明组：四条绑定依次建立，不创建独立作用域，等价于依次写四条 `let`；`x` 用到 `a`、`b`，`residual` 又用到 `x`，书写顺序就是求值顺序。

矩阵下标从 0 开始，先行后列。`solve` 的右端项按列排列，所以 `@(9; 8)` 是一列两行；写成 `@(9, 8)` 就是一行两列，行数与 `a` 对不上。

稠密矩阵按列优先存储：先走完一列再走下一列。`columnMajor` 把这份逻辑顺序显式取出，结果与底层 stride 无关；索引、切片与矩阵乘都按同一套维度约定工作。

!!! success "检查点"
    - [ ] `x` 的两个元素是 2 与 3，`residual` 是零向量
    - [ ] 求解前后打印 `a` 与 `b`，值没有变化
    - [ ] 把 `@(9; 8)` 写成 `@(9, 8)`，`solve` 报 `ShapeError`

## 第二步：一次解多个右端项

同一个系数矩阵配多组右端项时，把右端项按列拼成一个矩阵，`solve` 一次返回同样列数的解：

```el
let a = @(3, 1; 1, 2)
let both = solve(a, @(9, 6; 8, 4))
let first = both[:, 0..1]
let second = both[:, 1..2]
```

`@(9, 6; 8, 4)` 的第一列 `[9; 8]` 就是原来的右端项，解得 `[2; 3]`；第二列 `[6; 4]` 解得 `[8/5; 6/5]`，仍是精确有理数。`both[:, 0..1]` 与 `both[:, 1..2]` 各取一列，两侧都是选择器，结果保持 2 行 1 列。多列右端项共用同一次消元；形状要求不变：右端项 rank 2，行数等于方阵 `a` 的行数。

!!! success "检查点"
    - [ ] 两列解分别是 `[2; 3]` 与 `[8/5; 6/5]`，没有小数近似
    - [ ] 把第二列换成 `[10; 20]`，两个解仍然各自满足自己的方程
    - [ ] 右端项只写一列（rank 1）时 `solve` 报 `ShapeError`

## 第三步：下标、切片与列优先

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

??? question "先猜：`m[:, 1..|1]` 会得到几行几列？"
    2 行 1 列。`:` 保留行轴，`1..|1` 保留列轴并只选中下标 1；两个下标都是选择器时，两边轴都留着。

`m[:, 1..|1]` 的两个下标都是选择器：`:` 保留行轴，`1..|1` 保留列轴并只选中下标 1，结果是 2 行 1 列的 `[2; 5]`。`..` 左闭右开，`..|` 左闭右闭；`0..2` 与 `0..|1` 都选中 0、1，`1..|1` 只选中 1。半开范围右界可等于轴长度，闭范围右界必须小于轴长度。

`columnMajor(m)` 返回列优先展开的一维值 `[1, 4, 2, 5, 3, 6]`：先第一列两个元素，再第二列，最后第三列。

`a = matrix(Number) { 3, 1; 1, 2 }` 是显式元素类型的矩阵字面量：圆括号写类型，花括号按分号分行、逗号分列，形状与 `@(3, 1; 1, 2)` 相同；`@(...)` 直接构造 `Number` 矩阵，需要换元素类型时用 `matrix(...)`。

!!! success "检查点"
    - [ ] `m[0, 2]` 得到 `Number` 值 3，而不是 1 行 1 列
    - [ ] `lastRow` 是一维 `[4, 5, 6]`，`secondColumn` 是 2 行 1 列 `[2; 5]`
    - [ ] 把 `1..|1` 改成 `1..1`，得到空选择而不是第 1 列

## 第四步：矩阵乘、转置与逐元素广播

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

`a * x` 是矩阵积：2×2 的 `a` 乘 2×1 的 `x`，得到 `[9; 8]`。`*` 在 rank 2 上是矩阵积，标量与矩阵相乘是缩放；两个 rank 1 的值相乘时必须先用 `row`、`col` 明确当成行还是列，`*` 不会把一维数组猜成矩阵的行或列。

`m.T` 是转置：2×3 的 `m` 变成 3×2，第一行变成结果第一列，第二行变成第二列。`.T` 只交换两个轴；复数矩阵用 `.H` 取共轭转置。

`m .* m` 是逐元素乘，得到 `[1, 4, 9; 16, 25, 36]`。`.*`、`./`、`.^` 是广播逐元素运算：对应轴对齐，短 shape 末尾补 1，轴相等或一侧为 1 时合法；矩阵乘与逐元素乘用不同运算符区分。

`broadcasted` 把 2×2 与 2×1 相乘：列轴为 1 的一侧扩展到 2，第一行乘 10、第二行乘 20，得到 `[10, 20; 60, 80]`。广播只按轴规则扩展，不因数值碰巧相等改变形状。

`sum(a)` 对全部元素求和，得到 7；`mean(a)` 得到 7/4，这是精确有理数，不经过二进制浮点舍入。`sum(m, 0)` 沿轴 0 归约，显式轴参数保留轴长 1，所以结果是 1 行 3 列的 `[5, 7, 9]`；需要标量时省略轴参数。

默认入口里的裸名 `sum`、`mean` 属于查询聚合，数值版本导出为 `numericsSum` 与 `numericsMean`；这里显式导入数值模块，所以 `sum`、`mean` 指数值归约。空输入也有明确结果：`sum` 单位元是 0，`mean`、`min`、`max` 抛 `EmptyReduction`。

!!! success "检查点"
    - [ ] `product` 是 `[9; 8]`，`m.T` 的形状是 3×2
    - [ ] `m .* m` 的位置与自身相乘，`broadcasted` 是 `[10, 20; 60, 80]`
    - [ ] `mean(a)` 是 `7/4`；把它换成 `mean(@())` 会抛 `EmptyReduction`

## 第五步：精确解与浮点阈值

`solve` 只接受方阵：`a` 是 rank 2 方阵，`b` 也是 rank 2 且行数等于 `a` 的行数，否则在分解前抛 `ShapeError`；元素里有非有限值时抛 `NonFiniteInput`。失败的调用拿不到部分解，也不改动输入的 `a`、`b`。

默认 `Number` 矩阵的 `solve` 走精确有理数消元：只找非零主元，不套用 binary64 容差，也不转成定宽浮点，所以上面的 `residual` 是精确零向量。

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

第一个例子里两行成比例，消元到第二列时找不到非零主元，抛 `NumericallySingular`；第二个例子里 `wide` 是 2 行 3 列，不是方阵，检查形状时就抛 `ShapeError`。`solve` 失败后不会悄悄改成最小二乘，需要拟合时显式调用 `leastSquares`。

`leastSquares` 处理 m×n 的最小二乘：要求 m ≥ n、A 满列数值秩，右端项行数等于 m、多个右端项按列排列；m < n 抛 `ShapeError`，列主元低于阈值抛 `RankDeficient`。它面向 `F64` 稠密矩阵，用列主元 Householder QR，每轮重算剩余列的稳定范数，把反射直接作用到右端项，不构造正规方程，也不先求逆。

F64 路径用不可变的 `NumericsPolicy` 保存容差：默认 eps 是 2^-52，rtol 是 max(m, n) × eps，atol 是 0；构造时校验 0 ≤ rtol < 1、atol 非负，否则抛 `InvalidNumericsPolicy`。LU 用原矩阵最大绝对值作 scale，QR 用首个主元范数作 scale，主元或列范数不大于阈值就报告失败。

这些阈值是公开启发式，不是数学证明：`NumericallySingular` 与 `RankDeficient` 只说明算法在当前策略下拒绝继续，不证明数学秩、不估计条件数、不给前向误差保证。精确路径的“找不到非零主元”与浮点路径的“低于容差”是两种语义，结论不要混用。

要观察 F64 求解过程时，`solveDiagnostic` 与 `leastSquaresDiagnostic` 返回 `SolveReport`：实际方法、容差与阈值、成功判定，以及重算的 `b - a * x` 及其无穷范数；它们仍用同一套算法与策略，不额外证明条件数或前向误差。

!!! success "检查点"
    - [ ] 成比例的两行抛 `NumericallySingular`，非方阵抛 `ShapeError`
    - [ ] `solve` 失败后输入矩阵没有被改动
    - [ ] 用 `solveDiagnostic` 看到的残差范数与手算的 `b - a * x` 一致

## 第六步：画一张图

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

!!! success "检查点"
    - [ ] `curve.svg` 生成成功，用浏览器能打开
    - [ ] `xs` 是 101 行 1 列，`ys` 的形状一致
    - [ ] 把 `x` 的长度改成 100，`plot` 在画线前就报错

## 完整源码

```text
numerics/
├── package.eol
└── src/
    └── main.el
```

`src/main.el` 把每一步按顺序拼起来即可；下面是最小可运行版本，绘图部分按需保留：

```el
import { solve, matrix, columnMajor, sum, mean } from "el:numerical-computing/index.el"

let {
	a = @(3, 1; 1, 2)
	b = @(9; 8)
	x = solve(a, b)
	residual = b - a * x
}

let both = solve(a, @(9, 6; 8, 4))
let m = @(1, 2, 3; 4, 5, 6)
let corner = m[0, 2]
let lastRow = m[1, 0..3]
let secondColumn = m[:, 1..|1]
let flattened = columnMajor(m)
let product = a * x
let transposed = m.T
let elementwise = m .* m
let total = sum(a)
let average = mean(a)
let columnTotals = sum(m, 0)

console.stdout.writeLine("x: ", x[0, 0], ", ", x[1, 0])
console.stdout.writeLine("residual: ", residual[0, 0], ", ", residual[1, 0])
```

## 改成你自己的

1. **换一组方程。** 把系数改成 3×3，右端项换成三列，验证每列残差都为零。验收：三组解各自满足自己的方程，且没有小数误差。
2. **给脚本加一层输入。** 从命令行参数读系数（文本转 `Number`），构造矩阵后求解；参数个数不对就打印用法。验收：换一组数字不改代码就能跑，形状错误时给出明确报错。
3. **把精确解与浮点解并排。** 用 `F64` 布局重做同一个方程组，比较两条路径的残差；再用 `solveDiagnostic` 打印残差无穷范数。验收：能说出两条路径各自的判定依据，不把浮点阈值当成数学秩的证明。

## 卡住了？

- **现象：`solve` 报 `ShapeError`，但矩阵看上去是方的。** 右端项 `@(9, 8)` 是一行两列。检查：`b` 的行数必须等于 `a` 的行数。
- **现象：切片结果的维度比预期少一维。** 标量下标会删掉对应的轴。检查：想保留轴就用 `:` 或范围。
- **现象：`.*` 报形状不匹配。** 广播只按轴规则扩展，不按数值。检查：两侧轴长要么相等，要么一侧为 1。
- **现象：`NumericallySingular` 出现但你确信矩阵可逆。** 精确路径只找非零主元，浮点路径按阈值拒绝。检查：换 `F64` 与 `solveDiagnostic` 看实际主元与阈值，别混用两者结论。

## 带走这三样

- 方程组先写成 `a * x = b`，再用 `solve`；`b - a * x` 是随手可写的验收。
- 形状由下标与广播规则决定：标量删轴、范围留轴、短 shape 末尾补 1。
- 精确 `Number` 与 `F64` 是两条路径：一条找非零主元，一条按容差判定，结论不能互相替代。

## 下一站：[从其他语言过来](../appendix/coming-from.md)

> 你已经见过窗口、规则、证明和矩阵。如果带着别的语言的直觉来，哪些习惯会在这里失效？

- 主推进：[从其他语言过来](../appendix/coming-from.md)：把熟悉的语法映射到 EL，避开最容易踩的语义差异。
- 想回看集合基础：[集合与文本](../stdlib/collections.md)：数组与矩阵字面量的区别。
