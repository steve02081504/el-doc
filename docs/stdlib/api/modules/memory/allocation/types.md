# memory/allocation/types.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 存储分配类型 {#api-8301c2e61e60f212c7be}

源码：`src/stdlib/memory/allocation/types.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/types.el#L1)

提供分配大小和进程存储族的类型。

## AllocationSize {#api-4b4432c821d87942e622}

源码：`src/stdlib/memory/allocation/types.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/types.el#L13)

表示分配大小的底层无符号整数类型，其表示由目标平台确定。

```el-signature
export @builtin:vome:size:integer class AllocationSize
```

### 示例：用法

```el
import { AllocationSize } from "el:memory/allocation/types.el"
let size = AllocationSize(16)
```
