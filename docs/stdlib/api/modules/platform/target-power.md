# platform/target-power.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/platform.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标数位基数幂 {#api-05a81dba24371d3a685f}

源码：`src/stdlib/platform/target-power.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/target-power.el#L1)

用精确数值表示目标数位可编码的状态数。

## dit_exp {#api-1d1dcfb1639cfcb94502}

源码：`src/stdlib/platform/target-power.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/target-power.el#L16)

返回目标数位基数的 exponent 次方，指数遵循 Number 幂运算的合同。

```el-signature
export fn dit_exp(exponent: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：exponent 幂的指数。

**返回值**：精确 Number 结果。

### 示例：计算四个目标数位的状态数

```el
import { dit_exp } from "el:platform/target.el"
let states = dit_exp(4)
```
