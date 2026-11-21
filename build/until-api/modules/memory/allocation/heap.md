# memory/allocation/heap.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 平台堆分配 {#api-691dfe2147d80e2577ba}

源码：`src/stdlib/memory/allocation/heap.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/heap.el#L1)

提供平台堆的直接分配和释放入口。

## try_heap_alloc {#api-ed06bd17d4112704658d}

源码：`src/stdlib/memory/allocation/heap.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/heap.el#L27)

尝试从平台堆分配，不主动触发压力回收。

```el
export fn try_heap_alloc(bytes: Number): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：bytes 请求的字节数。

**返回值**：成功时返回指针，失败时返回空指针；成功的块须用 heap_free 释放。

### 示例：检查并释放

```el
import { try_heap_alloc, heap_free } from "el:memory/allocation/heap.el"
import { null_pointer } from "el:memory/storage/raw.el"
let block = try_heap_alloc(64)
if (block != null_pointer()) {
	try {
		// 在这里使用申请到的存储。
	}
	finally { heap_free(block) }
}
```

## heap_alloc {#api-b7871e91d49bbde9993d}

源码：`src/stdlib/memory/allocation/heap.el:43` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/heap.el#L43)

从平台堆分配；首次失败后请求压力回收并重试一次。

```el
export fn heap_alloc(bytes: Number): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：bytes 请求的字节数。

**返回值**：成功的分配指针，调用者须用 heap_free 释放。

**失败与异常**：重试失败时抛出 AllocationError。

### 示例：分配和释放

```el
import { heap_alloc, heap_free } from "el:memory/allocation/heap.el"
let block = heap_alloc(64)
try {
	// 在这里使用申请到的存储。
}
finally { heap_free(block) }
```

## heap_free {#api-0f5cb29929b7fbf1ffbe}

源码：`src/stdlib/memory/allocation/heap.el:65` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/heap.el#L65)

释放由平台堆分配入口取得的块。

```el
export fn heap_free(block: ptr): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：block 待释放的堆指针。

**返回值**：平台释放操作的数值结果。

### 示例：分配和释放

```el
import { heap_alloc, heap_free } from "el:memory/allocation/heap.el"
let block = heap_alloc(64)
try {
	// 在这里使用申请到的存储。
}
finally { heap_free(block) }
```
