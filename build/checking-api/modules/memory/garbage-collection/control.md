# memory/garbage-collection/control.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 垃圾回收控制 {#api-de43549f5c14e4f3989d}

源码：`src/stdlib/memory/garbage-collection/control.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/garbage-collection/control.el#L1)

提供主动收集和垃圾收集阈值设置。

## gc_collect {#api-bdf0742f458e829fd507}

源码：`src/stdlib/memory/garbage-collection/control.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/garbage-collection/control.el#L21)

同步请求一轮垃圾收集，返回本轮清扫实际释放的受管理负载字节数；无可回收存储或请求合并时返回零。

```el-signature
export fn gc_collect(): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：用法

```el
let collected = gc_collect()
```

## gc_set_threshold {#api-effad26c1ab2c1ab2a07}

源码：`src/stdlib/memory/garbage-collection/control.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/garbage-collection/control.el#L29)

设置触发安全点回收的分配欠账字节阈值；零允许每个启用回收的安全点请求回收，负值被拒绝。进程启动时的显式配置优先。

```el-signature
export fn gc_set_threshold(bytes)
```

### 示例：用法

```el
gc_set_threshold(1048576)
```
