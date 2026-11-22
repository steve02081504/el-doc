# memory/allocation/resources.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [AllocationResource.run](#api-4594f61d969df01f11c4)
- [AllocationResource.snapshot](#api-0b6ef92ff8094e1cbbe3)
- [AllocationResource.live_allocations](#api-5c03c0ca799f66aa7d73)
- [AllocationResource.live_bytes](#api-c980a03effcac60dbbff)
- [AllocationResource.allocations](#api-c99c9345210af5d3fc7f)
- [AllocationResource.releases](#api-34385919c82bc7e37c76)
- [AllocationResource.cumulative_bytes](#api-b4aed26da644089ff7c2)
- [AllocationResource.peak_live_bytes](#api-b9bf0dcf44cea02a2df2)
- [AllocationResource.incomplete_observations](#api-13a43d2e72a34a6dd6e5)
- [AllocationResource.participants](#api-91bdf3f280f723a62e3e)
- [AllocationResource.physical_bytes](#api-b5e3b89a8c582a97acf3)
- [AllocationResource.check_empty](#api-8d62410eb64ebec2d90e)
- [AllocationResource.check_when_idle](#api-fd2600d92cd142340fe1)
- [AllocationResource.reset](#api-f3a34cf7aca61613268a)

## 分配资源与观察 {#api-4900dd123dd125db0a00}

源码：`src/stdlib/memory/allocation/resources.el:2` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L2)

组合分配资源、统计和观察器；分配的释放沿其原始来源进行。

## AllocationResourceError {#api-74c8810a150913ec336d}

源码：`src/stdlib/memory/allocation/resources.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L52)

创建资源、运行作用域或采集快照失败时使用的错误。

```el-signature
export @assign(mode: "copy") class AllocationResourceError extends Error
```

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
```

## AllocationSnapshot {#api-2ebb6b2c7191b869a60b}

源码：`src/stdlib/memory/allocation/resources.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L145)

同一时刻的资源统计：存活分配数和字节、累计分配与释放次数、累计字节、存活峰值、物理字节、未完整观察次数及参与者数。计数使用目标原生表示。

```el-signature
export @assign(mode: "copy") class AllocationSnapshot
```

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
let snapshot = tracker.snapshot()
```

## AllocationResource {#api-8eba7d4cbf772f8d630b}

源码：`src/stdlib/memory/allocation/resources.el:180` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L180)

共享的分配资源句柄；复制句柄共享状态。作用域及其后代的分配可在 run 返回后继续计入。

```el-signature
export @assign(mode: "shared") class AllocationResource
```

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
```

## AllocationResource.run {#api-4594f61d969df01f11c4}

源码：`src/stdlib/memory/allocation/resources.el:247` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L247)

将资源与当前资源及观察器组合后执行 body，返回其结果，并在正常返回或异常时恢复原上下文。

```el-signature
fn run(body)
```

**参数**：body 在组合后的资源上下文中执行的无参回调。

**返回值**：body 的结果。

**失败与异常**：资源绑定创建失败抛出 AllocationResourceError；body 的异常向上传播。

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
```

## AllocationResource.snapshot {#api-0b6ef92ff8094e1cbbe3}

源码：`src/stdlib/memory/allocation/resources.el:299` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L299)

取得一致时刻的统计快照；各独立计数方法分别读取，不能保证属于同一时刻。

```el-signature
fn snapshot(): AllocationSnapshot
```

**返回类型**：[`AllocationSnapshot`](resources.md#api-2ebb6b2c7191b869a60b)

**失败与异常**：快照创建失败时抛出 AllocationResourceError。

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
let snapshot = tracker.snapshot()
```

## AllocationResource.live_allocations {#api-5c03c0ca799f66aa7d73}

源码：`src/stdlib/memory/allocation/resources.el:339` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L339)

读取当前存活的分配数；计数使用目标原生表示。

```el-signature
fn live_allocations(): RuntimeWord
```

**返回类型**：[`RuntimeWord`](../../../types.md#api-b33b987a810fb17f83e0)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.live_allocations()
```

## AllocationResource.live_bytes {#api-c980a03effcac60dbbff}

源码：`src/stdlib/memory/allocation/resources.el:348` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L348)

读取当前存活的逻辑字节数；计数使用目标原生表示。

```el-signature
fn live_bytes(): NativeStorageSize
```

**返回类型**：[`NativeStorageSize`](../../../types.md#api-56e936010cbf9fb04ba1)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.live_bytes()
```

## AllocationResource.allocations {#api-c99c9345210af5d3fc7f}

源码：`src/stdlib/memory/allocation/resources.el:357` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L357)

读取累计分配次数；计数使用目标原生表示。

```el-signature
fn allocations(): RuntimeWord
```

**返回类型**：[`RuntimeWord`](../../../types.md#api-b33b987a810fb17f83e0)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.allocations()
```

## AllocationResource.releases {#api-34385919c82bc7e37c76}

源码：`src/stdlib/memory/allocation/resources.el:366` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L366)

读取累计释放次数；计数使用目标原生表示。

```el-signature
fn releases(): RuntimeWord
```

**返回类型**：[`RuntimeWord`](../../../types.md#api-b33b987a810fb17f83e0)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.releases()
```

## AllocationResource.cumulative_bytes {#api-b4aed26da644089ff7c2}

源码：`src/stdlib/memory/allocation/resources.el:375` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L375)

读取累计分配的逻辑字节数；计数使用目标原生表示。

```el-signature
fn cumulative_bytes(): NativeStorageSize
```

**返回类型**：[`NativeStorageSize`](../../../types.md#api-56e936010cbf9fb04ba1)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.cumulative_bytes()
```

## AllocationResource.peak_live_bytes {#api-b9bf0dcf44cea02a2df2}

源码：`src/stdlib/memory/allocation/resources.el:384` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L384)

读取存活逻辑字节数的峰值；计数使用目标原生表示。

```el-signature
fn peak_live_bytes(): NativeStorageSize
```

**返回类型**：[`NativeStorageSize`](../../../types.md#api-56e936010cbf9fb04ba1)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.peak_live_bytes()
```

## AllocationResource.incomplete_observations {#api-13a43d2e72a34a6dd6e5}

源码：`src/stdlib/memory/allocation/resources.el:393` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L393)

读取未完整交付的观察事件数；计数使用目标原生表示。

```el-signature
fn incomplete_observations(): RuntimeWord
```

**返回类型**：[`RuntimeWord`](../../../types.md#api-b33b987a810fb17f83e0)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.incomplete_observations()
```

## AllocationResource.participants {#api-91bdf3f280f723a62e3e}

源码：`src/stdlib/memory/allocation/resources.el:402` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L402)

读取当前参与者数；计数使用目标原生表示。

```el-signature
fn participants(): RuntimeWord
```

**返回类型**：[`RuntimeWord`](../../../types.md#api-b33b987a810fb17f83e0)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.participants()
```

## AllocationResource.physical_bytes {#api-b5e3b89a8c582a97acf3}

源码：`src/stdlib/memory/allocation/resources.el:412` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L412)

读取本资源拥有的 arena slab 物理字节数，包含头部和未用容量；计数使用目标原生表示。

```el-signature
fn physical_bytes(): NativeStorageSize
```

**返回类型**：[`NativeStorageSize`](../../../types.md#api-56e936010cbf9fb04ba1)

### 示例：读取统计

```el
import { allocation_tracker } from "el:memory/"
let tracker = allocation_tracker()
let value = tracker.physical_bytes()
```

## AllocationResource.check_empty {#api-8d62410eb64ebec2d90e}

源码：`src/stdlib/memory/allocation/resources.el:423` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L423)

立即检查并报告存活分配；子任务或返回值仍可能持有分配。

```el-signature
fn check_empty(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
let empty = tracker.check_empty()
```

## AllocationResource.check_when_idle {#api-fd2600d92cd142340fe1}

源码：`src/stdlib/memory/allocation/resources.el:435` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L435)

参与者空闲时检查并报告：返回 0 表示延期，1 表示为空，2 表示报告了非空快照。

```el-signature
fn check_when_idle(): Integer
```

**返回类型**：[`Integer`](../../../types.md#api-45690472287900730a5f)

**失败与异常**：无法安排检查时抛出 AllocationResourceError。

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
let result = tracker.check_when_idle()
```

## AllocationResource.reset {#api-f3a34cf7aca61613268a}

源码：`src/stdlib/memory/allocation/resources.el:452` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L452)

重置 arena；tracker 或仍有后代存活分配时返回 f。成功后释放 arena 所持的块。

```el-signature
fn reset(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let arena = allocation_arena()
arena.run(fn() { return 1 })
let reset = arena.reset()
```

## allocation_tracker {#api-e8fa0007d514f447ec99}

源码：`src/stdlib/memory/allocation/resources.el:478` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L478)

创建统计资源；check_on_drop 为真时析构时立即检查是否为空。

```el-signature
export fn allocation_tracker(check_on_drop: Bool = f): AllocationResource
```

**返回类型**：[`AllocationResource`](resources.md#api-8eba7d4cbf772f8d630b)

**参数**：check_on_drop 是否在句柄析构时立即检查。

**返回值**：共享的统计资源。

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let tracker = allocation_tracker()
tracker.run(fn() { return 1 })
```

## allocation_arena {#api-d7c42030098dd223bcbb}

源码：`src/stdlib/memory/allocation/resources.el:491` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L491)

创建 arena；省略 upstream 时使用基础堆，显式 upstream 须为自定义终端分配资源，不能是 arena 或观察器。

```el-signature
export fn allocation_arena(upstream: AllocationResource | nil_t = nil): AllocationResource
```

**返回类型**：[`AllocationResource`](resources.md#api-8eba7d4cbf772f8d630b)

**参数**：upstream 可选的终端分配资源；nil 选择基础堆。

**返回值**：共享的 arena 资源。

### 示例：使用示例

```el
import { allocation_tracker, allocation_arena } from "el:memory/"
let arena = allocation_arena()
arena.run(fn() { return 1 })
```

## allocation_resource {#api-909a6f9e1fc2a3457a85}

源码：`src/stdlib/memory/allocation/resources.el:524` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L524)

创建自定义终端分配资源。回调同步执行、可能并发，不能重新进入分配引擎或抛异常；回调抛异常会触发陷阱。

```el-signature
@callbackSafe(parameter: "allocate") @callbackSafe(parameter: "release")
export fn allocation_resource(allocate: @sync fn(size: NativeStorageSize, alignment: NativeStorageSize): ptr, release: @sync fn(pointer: ptr, size: NativeStorageSize, alignment: NativeStorageSize): RuntimeWord, code_owner): AllocationResource
```

**返回类型**：[`AllocationResource`](resources.md#api-8eba7d4cbf772f8d630b)

**参数**：allocate 接收物理范围大小和对齐，返回存储指针；普通分配失败返回空指针。

**参数**：release 接收分配时的指针、物理范围大小和对齐；成功返回 RuntimeWord(1)；对齐由目标布局决定。

**参数**：code_owner 保持回调代码及其模块在资源和分配退役前有效的所有者。

**返回值**：共享的分配资源句柄。

### 示例：使用原生对齐分配作为后端

```el
import { allocation_resource } from "el:memory/"
import { native_allocate, native_release } from "el:memory/allocation/native.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { NativeSignedInteger as Integer } from "el:platform/machine/integer.el"
import { NativeStorageSize, NativeSignedWord as RuntimeWord } from "el:runtime/native-types.el"
import { sync } from "el:language/contracts.el"
let resource = allocation_resource(
	@sync fn(size: NativeStorageSize, alignment: NativeStorageSize): ptr {
		unsafe { return native_allocate(AllocationSize(size), AllocationSize(alignment)) }
	},
	@sync fn(pointer: ptr, size: NativeStorageSize, alignment: NativeStorageSize): RuntimeWord {
		unsafe { native_release(pointer) }
		return RuntimeWord(1)
	},
	nil
)
resource.run(fn() { let values = @[1, 2, 3]; return values.count })
```

**注意**：此示例的回调定义在当前程序模块中；动态加载的回调须提供保持代码加载的所有者。

## with_allocation_tracking {#api-3ab81e903cbcfb4211ca}

源码：`src/stdlib/memory/allocation/resources.el:543` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L543)

在新 tracker 中运行 body 并返回结果；check_empty 选择结束时检查，final 选择参与者空闲后检查。返回值和仍运行的子任务可能保留分配。

```el-signature
export fn with_allocation_tracking(body, check_empty: Bool = f, final: Bool = f)
```

**参数**：body 在统计上下文中执行的无参回调。

**参数**：check_empty 是否在结束时检查存活分配。

**参数**：final 为真时将检查推迟到参与者空闲。

**返回值**：body 的结果。

### 示例：使用示例

```el
import { with_allocation_tracking } from "el:memory/"
let result = with_allocation_tracking(fn() { return 1 })
```

## allocation_observer {#api-745b0e48de8321bdb0ba}

源码：`src/stdlib/memory/allocation/resources.el:587` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/resources.el#L587)

创建观察资源。事件 1、2 是逻辑分配和释放，3、4 是成功和失败的调整大小，5、6 是物理 slab 分配和释放；成功调整也产生底层分配和释放事件。

```el-signature
@callbackSafe(parameter: "observe")
export fn allocation_observer(observe: @sync fn(event: RuntimeWord, identity: RuntimeWord, address: NativeStorageSize, size: NativeStorageSize, alignment: NativeStorageSize, backing_identity: RuntimeWord): RuntimeWord, code_owner): AllocationResource
```

**返回类型**：[`AllocationResource`](resources.md#api-8eba7d4cbf772f8d630b)

**参数**：observe 同步观察回调；返回 1 表示完整，返回 0 或抛异常记为不完整。

**参数**：code_owner 保持回调代码及其模块在资源和分配退役前有效的所有者。

**返回值**：共享的观察资源句柄。

**注意**：identity 标识成功分配，address 是整数令牌而非借用；backing_identity 为关联 slab 的身份，0 表示无 slab。调整成功使用新 identity，失败使用旧 identity。回调可能并发，不能分配或重新进入。

### 示例：接收观察事件

```el
import { allocation_observer } from "el:memory/"
import { NativeSignedInteger as Integer } from "el:platform/machine/integer.el"
import { NativeStorageSize, NativeSignedWord as RuntimeWord } from "el:runtime/native-types.el"
import { sync } from "el:language/contracts.el"
let observer = allocation_observer(
	@sync fn(event: RuntimeWord, identity: RuntimeWord, address: NativeStorageSize, size: NativeStorageSize, alignment: NativeStorageSize, backing_identity: RuntimeWord): RuntimeWord {
		return RuntimeWord(1)
	},
	nil
)
observer.run(fn() { let values = @[1, 2, 3]; return values.count })
```

**注意**：此无状态回调位于当前程序模块；动态加载的回调须提供保持代码加载的所有者。
