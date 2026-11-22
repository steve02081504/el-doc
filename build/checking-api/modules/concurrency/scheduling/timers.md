# concurrency/scheduling/timers.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/concurrency.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 定时器 {#api-cab558fb622f8a524d96}

源码：`src/stdlib/concurrency/scheduling/timers.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/scheduling/timers.el#L1)

提供等待与定时回调。

<span id="api-1e64fc73745ab400a387"></span>

## sleep~milliseconds {#api-76f2a9edcc37ac311d2a}

源码：`src/stdlib/concurrency/scheduling/timers.el:150` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/scheduling/timers.el#L150)

挂起当前活动指定的毫秒数；毫秒数须为非负、有限且在计时器范围内的整数，否则抛出 RangeError。

```el-signature
export fn sleep(milliseconds: Number)
```

### 示例：用法

```el
sleep(10)
```

## sleep~duration {#api-57202b2d1b02a0978c4a}

源码：`src/stdlib/concurrency/scheduling/timers.el:168` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/scheduling/timers.el#L168)

按时间差的总毫秒数挂起当前活动；总毫秒数须满足毫秒重载的约束。

```el-signature
export fn sleep(duration: TimeDiff)
```

### 示例：用法

```el
let duration: TimeDiff = TimeDiff()
sleep(duration)
```
