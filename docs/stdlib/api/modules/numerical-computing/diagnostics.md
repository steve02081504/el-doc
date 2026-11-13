# numerical-computing/diagnostics.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值求解诊断 {#api-fc9691112daee7143abd}

源码：`src/stdlib/numerical-computing/diagnostics.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/diagnostics.el#L10)

返回浮点求解结果、残差范数、实际方法与阈值判定信息。

<span id="api-90f3bafe179eee9379d1"></span>

## solveDiagnostic~dense {#api-e0ab268d3c4c908e5d38}

源码：`src/stdlib/numerical-computing/diagnostics.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/diagnostics.el#L41)

```el
export fn solveDiagnostic(a: Tensor<element: F64>, b: Tensor<element: F64>, policy: NumericsPolicy = NumericsPolicy()): SolveReport
```

**返回类型**：[`SolveReport`](../../types.md#api-cdf1898479477137a49b)

用 F64 稠密 LU 求解并返回残差与主元阈值诊断。

**参数**：a 方阵系数矩阵。

**参数**：b rank-2 右端项。

**参数**：policy 浮点容差策略。

**返回值**：含解、重算残差、残差无穷范数、方法与阈值的报告。

### 示例：读取诊断报告中的残差范数

```el
let report = solveDiagnostic(a, b)
let residualMagnitude = report.residualNorm
```

## leastSquaresDiagnostic {#api-5db73d0f1734381d6751}

源码：`src/stdlib/numerical-computing/diagnostics.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/diagnostics.el#L61)

```el
export fn leastSquaresDiagnostic(a: Tensor<element: F64>, b: Tensor<element: F64>, policy: NumericsPolicy = NumericsPolicy()): SolveReport
```

**返回类型**：[`SolveReport`](../../types.md#api-cdf1898479477137a49b)

用 F64 列主元 QR 求最小二乘解并返回残差与秩阈值诊断。

**参数**：a rank-2 系数矩阵，行数不得少于列数。

**参数**：b rank-2 右端项，行数须与 a 相同。

**参数**：policy 浮点容差策略。

**返回值**：含解、重算残差、残差无穷范数、方法与阈值的报告。

### 示例：查看最小二乘残差

```el
let report = leastSquaresDiagnostic(a, b)
let residualMagnitude = report.residualNorm
```
