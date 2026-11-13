# logic/control.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/logic.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 逻辑搜索控制 {#api-c8725f29939f290a5c97}

源码：`src/stdlib/logic/control.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/control.el#L5)

定义逻辑搜索的答案语义、搜索策略、预算和中断信息。

## SearchInterrupted {#api-f2eed514e7ad72951f31}

源码：`src/stdlib/logic/control.el:67` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/control.el#L67)

```el
export @assign(mode: "shared") class SearchInterrupted
```

搜索因预算耗尽或主动取消而中断时抛出的信息对象。

### 示例：捕获受限搜索中断

```el
try { discard(cursor.next()) }
catch (error) { if (error is SearchInterrupted) console.stdout.writeLine(error.reason) }
```
