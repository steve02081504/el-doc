# foreign-functions/callbacks.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/foreign-functions.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 外部回调 {#api-270a66788a9ea8ce5e9c}

源码：`src/stdlib/foreign-functions/callbacks.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/callbacks.el#L1)

外部回调相关接口。

## callback_address {#api-6c8eb6ba08fe56146d8b}

源码：`src/stdlib/foreign-functions/callbacks.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/callbacks.el#L52)

为同步外部回调创建原生入口。入口借用闭包，调用方须使闭包在所有调用及释放期间存活，并在调用结束后释放入口。

```el-signature
@builtin:vome:effect:alloc(family: @[CallbackFamily])
export fn callback_address(callback): ptr
```

**返回类型**：[`ptr`](../../../../reference/language/foreign.md)

### 示例：用法

```el
import { callback_address, release_callback } from "el:foreign-functions/callbacks.el"
fn useCallback(callback, invoke) {
	let address = callback_address(callback)
	try { invoke(address) } finally { release_callback(address) }
}
```

## release_callback {#api-39ecd01aada00cdb72ee}

源码：`src/stdlib/foreign-functions/callbacks.el:183` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/callbacks.el#L183)

释放先前创建的回调入口；必须等待所有原生调用返回且闭包仍然存活。空指针无需释放。

```el-signature
@builtin:vome:effect:free(family: @[CallbackFamily])
export fn release_callback(address: ptr)
```

### 示例：用法

```el
import { release_callback } from "el:foreign-functions/callbacks.el"
fn releaseFinishedCallback(address: ptr) { release_callback(address) }
```
