# concurrency/promises.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/concurrency.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 异步结果 {#api-28d69e701d620c851328}

源码：`src/stdlib/concurrency/promises.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/promises.el#L1)

提供异步结果、任务启动和结果组合。

## spawn {#api-54380b40af09da4dcbfe}

源码：`src/stdlib/concurrency/promises.el:248` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/promises.el#L248)

提交无参数工作函数，返回代表其结果或异常的 Promise；可选参数指定调度上下文。

```el-signature
export fn spawn(work, scheduling: SchedulingContext | nil_t = nil)
```

### 示例：用法

```el
let result = spawn(fn() { return 42 })
let value = result.get()
```

## all {#api-e49ec99da7f01ad520e4}

源码：`src/stdlib/concurrency/promises.el:331` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/promises.el#L331)

组合 Promise；全部成功时按输入顺序返回结果数组，任一失败时传播失败，空输入产生空数组。

```el-signature
export fn all(inputs)
```

### 示例：用法

```el
let first = spawn(fn() { return 1 })
let second = spawn(fn() { return 2 })
let values = all(@[first, second]).get()
```
