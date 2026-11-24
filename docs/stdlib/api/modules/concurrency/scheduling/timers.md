# concurrency/scheduling/timers.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/concurrency.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 定时器 {#api-cab558fb622f8a524d96}

源码：`src/stdlib/concurrency/scheduling/timers.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/scheduling/timers.el#L1)

提供等待与定时回调。

## sleep {#api-1e64fc73745ab400a387}

源码：`src/stdlib/concurrency/scheduling/timers.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/scheduling/timers.el#L148)

挂起当前活动指定的固定时长。时长须非负且有限，调度使用单调时钟。

```el-signature
export fn sleep(duration: TimeDiff)
```

### 示例：用法

```el
sleep(3s)
```
