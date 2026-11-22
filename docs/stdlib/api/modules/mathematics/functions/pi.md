# mathematics/functions/pi.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/mathematics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 圆周率细化 {#api-1ab317cb5e6aec57e43a}

源码：`src/stdlib/mathematics/functions/pi.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/pi.el#L1)

圆周率细化相关接口。

## PiRefinement {#api-a9592d2c7bbb5a79c551}

源码：`src/stdlib/mathematics/functions/pi.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/mathematics/functions/pi.el#L87)

持有圆周率级数与已证明区间的细化状态；bounds 按给定精度收紧区间，refine 返回近似值。零精度会抛出 PrecisionError。

```el-signature
export @assign(mode: "copy") class PiRefinement
```

### 示例：用法

```el
import { PiRefinement } from "el:mathematics/functions/pi.el"
let refinement = PiRefinement()
let bounds = refinement.bounds(0.001)
```
