# memory/allocation/context.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 分配来源上下文 {#api-bf1fc074ac9c795c8fa6}

源码：`src/stdlib/memory/allocation/context.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/context.el#L1)

在拥有者原始分配来源中构造依赖存储。

## with_allocation_owner {#api-8c691c298879362345cc}

源码：`src/stdlib/memory/allocation/context.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/context.el#L28)

借用 owner，在其原始分配绑定中执行 body 并返回结果；结束或异常时恢复调用前的绑定。owner 必须在调用期间保持有效。

```el
export fn with_allocation_owner(borrow owner, body)
```

### 示例：使用示例

```el
import { with_allocation_owner } from "el:memory/allocation/context.el"
let owner = @[1, 2]
let result = with_allocation_owner(owner, fn() { return 1 })
```
