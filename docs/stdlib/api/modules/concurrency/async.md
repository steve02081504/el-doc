# concurrency/async.el

本页由源码注释生成；示例未运行验证。

## async 与 await 语法 {#api-18c3f6e86eba2c32a087}

源码：`src/stdlib/concurrency/async.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/async.el#L1)

提供启动异步回调和读取 Promise 结果的局部语法。

## async {#api-5f7a8df0d58d965b59ba}

源码：`src/stdlib/concurrency/async.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/async.el#L18)

```el
export syntax async
```

将代码块作为异步回调交给 spawn 执行，并立即返回 Promise。

### 示例：并发启动并等待两个任务

```el
import { async, await } from "el:concurrency/"
let first = async { return loadText() }
let second = async { return loadCount() }
let text = await(first)
let count = await(second)
```

## await {#api-ece413859fcabbb6a22f}

源码：`src/stdlib/concurrency/async.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/async.el#L40)

```el
export syntax await
```

读取 Promise 的结果；宏只完成 Promise.get() 调用，不自动把普通函数变成异步函数。

**参数**：promise 要读取结果的 Promise 表达式。

**返回值**：Promise 完成后的值，具体类型由该 Promise 决定。

### 示例：等待异步任务

```el
import { async, await } from "el:concurrency/"
let task = async { return 42 }
let result = await(task)
console.stdout.writeLine(result)
```
