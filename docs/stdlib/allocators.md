# 分配器与内存跟踪

> 一段程序算出了正确答案，却越跑越占内存。怎样只看这段工作的内存记录，又怎样给它安排一块临时工作区？

!!! abstract "🎯 读完这页，你能"
    - 给一段计算加上内存统计，分清“申请过多少”和“还留着多少”。
    - 把一批临时对象放进 arena，并检查能否归还它占用的内存。
    - 判断一个返回值为什么会让临时工作区无法重置。

    <span class="el-chip">⏱ 约 20 分钟</span> <span class="el-chip">前置：[函数与闭包](../language/functions.md)、[生命周期与析构](../language/lifetimes.md)</span>

## 先给整理购物清单的程序加一张账单

假设你在写一个购物清单工具：给每个商品名加上“待买”标记。我们先关心它做了多少内存分配，不改变它整理清单的办法。

**分配**就是程序申请一块内存来存放数据。通常你只需写数组、文本和对象，标准库会处理这些申请。**分配器**负责提供存储空间；这里先用一个 tracker（追踪器）给申请和释放记账。

把下面的完整程序保存为 `shopping-memory.el`。它使用标准库导入，不要求文件放在源码仓库的某个位置。

```el
import { allocation_tracker } from "el:memory/"

let tracker = allocation_tracker()
let shoppingList = tracker.run(fn() {
	let products = @["铅笔", "橡皮", "练习本"]
	return products.map(product => product + "：待买")
})

let stats = tracker.snapshot()
console.stdout.writeLine("商品数：", shoppingList.count)
console.stdout.writeLine("累计申请字节：", stats.cumulative_bytes)
console.stdout.writeLine("当前存活字节：", stats.live_bytes)
console.stdout.writeLine("存活字节峰值：", stats.peak_live_bytes)
```

在文件所在目录运行：

```sh
el run shopping-memory.el
```

第一行预期是 `商品数：3`，后面三行分别显示累计、当前存活和峰值字节数。具体数字受编译器优化和运行环境影响，不需要与你的同伴相同。

!!! note "示例验证范围"
    这里假定你已按[第一个程序](../getting-started.md)准备好可用的 `el` 命令。本文示例已按当前源码接口静态核对，尚未编译或运行；上述结果是预期值。

这几行新增代码各管一件事：

1. `allocation_tracker()` 创建账本。
2. `tracker.run(...)` 执行你交给它的函数，把这段工作及其后代资源里的分配记到账本上。函数原来返回什么，它仍返回什么。
3. `tracker.snapshot()` 取出一张统计快照。之后再发生申请或释放，不会改写已经取出的快照。

账单打印在 `run` 外面，是为了让展示账单时产生的分配留在被测工作之外。

## 申请过的内存，不等于现在还占着的内存

想象你为整理桌面借了几个盒子。有些盒子用完已经归还，有些仍装着东西。“一共借过多少”与“现在手里有多少”是两笔账。

| 你想问的问题 | 看哪个字段 |
| --- | --- |
| 这段工作累计申请过多少字节？ | `cumulative_bytes` |
| 拍快照时还有多少字节没有释放？ | `live_bytes` |
| 最拥挤的时候，同时存活过多少字节？ | `peak_live_bytes` |
| 一共发生过多少次分配、多少次释放？ | `allocations`、`releases` |

累计申请量会把先后发生的申请加起来。一个程序反复申请、及时释放，也可能有很高的累计量和较低的存活峰值。看到累计量很大，不能直接判定它泄漏了内存。

??? question "先猜：run 结束了，live_bytes 就应该是 0 吗？"
    不一定。例子把整理好的清单返回给了 `shoppingList`，后面的代码还要使用它。清单需要的存储不能因为 `run` 结束就被收走。`run` 负责恢复之前的分配环境，值的正常生命周期仍然有效。

!!! example "动手：多整理一种商品"
    在 `products` 中增加 `"尺子"`，再次运行。第一行应变成 `商品数：4`。比较后面的统计数字：它们有没有变化？不要预设每增加一种商品就恰好多分配一次；数组扩容、文本构造和优化都会影响记录。

要比较两种实现，先固定同一份商品清单，再分别创建 tracker 测量。若一直复用一个 tracker，它的累计量会把多次运行加在一起。

## 临时工作很多时，可以交给 arena

追踪器回答“哪里在用内存”。arena 则改变存储的组织方式：它先申请较大的内存块，再从中切出小块给对象使用。这样的较大块常叫 **slab**；你可以先把它理解成一张能摆下许多临时物品的工作台。

假设只需要算出商品数量，不需要把临时清单带到外面。下面是另一个完整程序，保存为 `shopping-arena.el`，用 `el run shopping-arena.el` 运行：

```el
import { allocation_arena } from "el:memory/"

let arena = allocation_arena()
arena.run(fn() {
	let products = @["铅笔", "橡皮", "练习本"]
	console.stdout.writeLine("商品数：", products.count)
})

let stats = arena.snapshot()
console.stdout.writeLine("工作区持有字节：", stats.physical_bytes)
if (arena.reset()) {
	console.stdout.writeLine("工作区已归还")
} else {
	console.stdout.writeLine("还有分配存活，暂时不能重置")
}
```

第一行预期是 `商品数：3`。中间一行显示 arena 自己持有的内存块容量；本例的临时值在回调结束后不再使用，最后预期走到“工作区已归还”分支。

`physical_bytes` 和前面的 `live_bytes` 口径不同。即使临时对象已经释放，arena 仍可能保留它们使用过的 slab。这个容量包括块头和暂时空着的部分，可以继续供后续分配使用；成功的 `reset()` 会归还这些块。

!!! warning "常见坑：把 reset 当成强制清场"
    `reset()` 返回失败，说明此时不能重置。它不会替你销毁仍在使用的对象，也不能用来让悬空指针变得安全。先处理仍存活的值，再检查返回结果；对普通 tracker 调用它也会失败。

arena 适合“处理一批输入，临时对象集中出现、集中结束”的工作，例如分析一份文件。它是否更快、是否节省内存，需要用自己的输入测量，不能只凭换了分配器就下结论。

## 要把结果带出去，就给结果留下位置

第一段程序要保留整理好的清单，第二段只在工作区内使用清单。两种需求都合理；区别在于结果还需不需要那块存储。

如果你让 `arena.run(...)` 返回一个数组，而外面仍在使用它，arena 就可能还有存活分配，此时不能期待 `reset()` 成功。不要为了让检查通过而丢掉程序真正需要的结果。

另一种常见情况是子任务：`run` 返回了，任务却还在处理清单。`run` 不会自动等待这些任务。任务可以继承分配绑定，退出当前回调并不意味着它们持有的数据已释放。

??? question "先猜：等子任务结束，就一定能 reset 吗？"
    仍不一定。任务结束后，它返回的数组、文本或对象可能还在外面使用。重置看的是 arena 是否还有存活分配；“任务已经结束”与“结果已经不用了”是两件事。

刚开始使用时，先选一段不返回容器、也不启动子任务的临时计算放进 arena。边界清楚后，再考虑让结果或异步工作跨出这段范围。

## 既想用 arena，又想记账，可以把两者套起来

下面是一个独立的完整程序。外层 tracker 记录这段工作，内层 arena 提供临时存储。

```el
import { allocation_tracker, allocation_arena } from "el:memory/"

let tracker = allocation_tracker()
let arena = allocation_arena()
tracker.run(fn() {
	arena.run(fn() {
		let products = @["铅笔", "橡皮", "练习本"]
		console.stdout.writeLine("商品数：", products.count)
	})
})

let stats = tracker.snapshot()
console.stdout.writeLine("累计申请字节：", stats.cumulative_bytes)
console.stdout.writeLine("工作区持有字节：", arena.physical_bytes())
if (arena.reset()) console.stdout.writeLine("工作区已归还")
```

预期先显示三件商品，再显示两个不同口径的字节数。tracker 记录作用域里的逻辑分配；要问 arena 自己持有多少 slab，就向 `arena` 取数。普通 tracker 的 `physical_bytes` 不是整个资源链、更不是整个进程的物理内存总量。

??? note "可选 · 需要更细的诊断或自己的分配器时"
    [分配资源 API](api/modules/memory/allocation/resources.md)还提供空检查、自定义存储提供器和观察器。`check_empty()` 立即检查；`check_when_idle()` 可把检查推迟到参与者空闲，两者都不是强制释放操作。

    `allocation_resource(...)` 的分配和释放回调工作在底层边界，必须同步、不能重入分配引擎，也不能抛异常。回调可能并发执行；显式的 `code_owner` 要让回调代码及模块一直有效到退役。arena 可以指定这种自定义资源作为上游。

    `allocation_observer(...)` 接收分配事件。它的回调不能分配或重入，所以不要直接在里面拼接文本、向数组追加记录或打印普通日志。事件里的地址是诊断用的整数令牌，不是可以解引用的借用指针。开始写这类回调前，先读 API 的参数、事件编号和失败合同。

## 带走这三样

- 想知道一段工作的分配情况，用 tracker 包住它，再取快照。
- 临时对象可以放进 arena；存活字节与 arena 保留的块容量分开看。
- `run` 返回不会收走仍在使用的结果；重置前检查 `reset()` 的返回值。

## 下一站：[性能与底层优化](../language/performance.md)

拿到两份内存账单后，怎样判断一次改写真的改善了程序？下一页继续讨论如何选择和验证优化。
