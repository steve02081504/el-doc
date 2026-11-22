# number/working-float.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 工作浮点类型 {#api-bf9889b1c7ac7cfdbb40}

源码：`src/stdlib/number/working-float.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/working-float.el#L1)

工作浮点类型相关接口。

## WorkingFloat {#api-c2c00a6f77d95afbdb5e}

源码：`src/stdlib/number/working-float.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/working-float.el#L28)

根据目标数位基数配置的工作浮点类型，其精度和指数范围由同模块常量确定。

```el-signature
export const WorkingFloat: type
```

**类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
import { WorkingFloat } from "el:number/working-float.el"
let value = WorkingFloat(1)
```
