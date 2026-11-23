# logic/control.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [SearchInterrupted.reason](#api-a5e27f42e41e0a798bf0)

## 逻辑搜索控制 {#api-c8725f29939f290a5c97}

源码：`src/stdlib/logic/control.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/control.el#L5)

定义逻辑搜索的答案语义、搜索策略、预算和中断信息。

## SearchInterrupted {#api-f2eed514e7ad72951f31}

源码：`src/stdlib/logic/control.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/control.el#L71)

搜索因预算耗尽或主动取消而中断时抛出的信息对象。

```el-signature
export @assign(mode: "shared") class SearchInterrupted
```

### 示例：捕获受限搜索中断

```el
// @external cursor: SearchCursor
try { discard(cursor.next()) }
catch (error) {
	if (error is SearchInterrupted) console.stdout.writeLine(error.reason)
	else throw error
}
```

## SearchInterrupted.reason {#api-a5e27f42e41e0a798bf0}

源码：`src/stdlib/logic/control.el:81` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/control.el#L81)

返回搜索中断的原因。搜索预算耗尽时为 `"limited"`，主动取消时为 `"cancelled"`。

```el-signature
get reason(): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

### 示例：读取中断原因

```el
let interruption = SearchInterrupted("limited")
let reason = interruption.reason
```
