# tools/debugger/attachment.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/tools.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## debuggerAttached {#api-bc0ad4d86df37ca429c9}

源码：`src/stdlib/tools/debugger/attachment.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/debugger/attachment.el#L10)

查询当前这次执行是否处在 EL 的交互式调试会话中；不查询外部调试器。

```el
export fn debuggerAttached(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：普通运行返回 f；由 el debug 执行时返回 t。

### 示例：在 EL 调试会话中启用额外诊断

```el
if (debuggerAttached()) console.stdout.writeLine("EL debugger attached")
```

## debuggerPause {#api-7398874336422e919732}

源码：`src/stdlib/tools/debugger/attachment.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/debugger/attachment.el#L24)

在当前 EL 调试会话中暂停，保留调用栈和局部值；普通运行什么也不做。

```el
export fn debuggerPause()
```

### 示例：到达检查点后暂停

```el
debuggerPause()
```
