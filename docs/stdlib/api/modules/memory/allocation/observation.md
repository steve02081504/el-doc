# memory/allocation/observation.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 内存压力观察 {#api-479f49865d3fa66ae0e4}

源码：`src/stdlib/memory/allocation/observation.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/observation.el#L1)

读取进程压力变化令牌，不安装压力服务。

## PressureGeneration {#api-c6a2c947c022768dfb89}

源码：`src/stdlib/memory/allocation/observation.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/observation.el#L14)

只用于相等比较的进程观察令牌，不拥有资源；计数按 2^64 回绕，完整回绕前须轮询才能区分变化。

```el
export @builtin:vome:unsigned:integer(bits: 64) class PressureGeneration
```

### 示例：使用示例

```el
import { allocationPressureGeneration } from "el:memory/allocation/observation.el"
let generation = allocationPressureGeneration()
```

## allocationPressureGeneration {#api-267daf03156006de316b}

源码：`src/stdlib/memory/allocation/observation.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/observation.el#L31)

读取当前压力令牌；新的消费者应先保存初值，之后在自身同步下比较，历史压力不会重放。令牌反映安全压力分派尝试，不表示释放字节或可用内存。

```el
export fn allocationPressureGeneration(): PressureGeneration
```

**返回类型**：[`PressureGeneration`](observation.md#api-c6a2c947c022768dfb89)

### 示例：使用示例

```el
import { allocationPressureGeneration } from "el:memory/allocation/observation.el"
let before = allocationPressureGeneration()
let changed = allocationPressureGeneration() != before
```
