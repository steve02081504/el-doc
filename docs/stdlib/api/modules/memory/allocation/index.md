# memory/allocation/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 语言存储分配入口 {#api-33181d7d04d7a5258649}

源码：`src/stdlib/memory/allocation/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/index.el#L1)

提供语言存储分配、调整和按原来源释放的底层入口。

## allocate_language_storage {#api-c430ee85d47ae6953bce}

源码：`src/stdlib/memory/allocation/index.el:57` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/index.el#L57)

通过当前资源分配语言存储，零大小实际请求至少一个字节。

```el
@builtin:vome:allocator
@builtin:vome:effect:alloc(family: @[ProcessStorageFamily])
export fn allocate_language_storage(size: AllocationSize, alignment: AllocationSize): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：size 请求的字节数。

**参数**：alignment 请求的对齐。

**返回值**：分配指针；失败时为空指针，成功后由调用者释放。

### 示例：分配和释放

```el
import { allocate_language_storage, release_language_storage } from "el:memory/allocation/index.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { null_pointer } from "el:memory/storage/raw.el"
let size = AllocationSize(64)
let alignment = AllocationSize(8)
let block = allocate_language_storage(size, alignment)
if (block != null_pointer()) {
	try {
		// 在这里使用申请到的存储。
	}
	finally { release_language_storage(block, size, alignment) }
}
```

## release_language_storage {#api-6d666a4c8607cbf1aed6}

源码：`src/stdlib/memory/allocation/index.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/index.el#L88)

按分配时的原始来源释放语言存储。

```el
@builtin:vome:deallocator
@builtin:vome:effect:free(family: @[ProcessStorageFamily])
export fn release_language_storage(pointer: ptr, size: AllocationSize, alignment: AllocationSize)
```

**参数**：pointer 待释放的分配指针。

**参数**：size 原分配大小。

**参数**：alignment 原分配对齐。

### 示例：分配和释放

```el
import { allocate_language_storage, release_language_storage } from "el:memory/allocation/index.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { null_pointer } from "el:memory/storage/raw.el"
let size = AllocationSize(64)
let alignment = AllocationSize(8)
let block = allocate_language_storage(size, alignment)
if (block != null_pointer()) {
	try {
		// 在这里使用申请到的存储。
	}
	finally { release_language_storage(block, size, alignment) }
}
```

## resize_language_storage {#api-9bc40f7cd2a0908eb370}

源码：`src/stdlib/memory/allocation/index.el:120` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/index.el#L120)

调整存储大小；新大小为零时实际请求至少一个字节。失败时原块仍归调用者，成功时改用返回指针。

```el
@builtin:vome:reallocator
@builtin:vome:effect:realloc(family: @[ProcessStorageFamily])
export fn resize_language_storage(pointer: ptr, old_size: AllocationSize, new_size: AllocationSize, alignment: AllocationSize): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：pointer 原分配指针。

**参数**：old_size 原大小。

**参数**：new_size 新大小。

**参数**：alignment 分配对齐。

**返回值**：新指针；失败时为空指针。

### 示例：调整后释放

```el
import { allocate_language_storage, resize_language_storage, release_language_storage } from "el:memory/allocation/index.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { null_pointer } from "el:memory/storage/raw.el"
let size = AllocationSize(64)
let alignment = AllocationSize(8)
let block = allocate_language_storage(size, alignment)
if (block != null_pointer()) {
	try {
		let grown = resize_language_storage(block, size, AllocationSize(128), alignment)
		if (grown != null_pointer()) { block = grown; size = AllocationSize(128) }
	} finally { release_language_storage(block, size, alignment) }
}
```

## allocate_language_base_storage {#api-8c56a155720c90622dcd}

源码：`src/stdlib/memory/allocation/index.el:163` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/index.el#L163)

绕过用户资源链从基础资源分配，保留来源释放和调试登记。

```el
@builtin:vome:effect:alloc(family: @[ProcessStorageFamily])
export fn allocate_language_base_storage(size: AllocationSize, alignment: AllocationSize): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：size 请求的字节数。

**参数**：alignment 请求的对齐。

**返回值**：分配指针；失败时为空指针，成功后用 release_language_storage 释放。

### 示例：使用基础资源

```el
import { allocate_language_base_storage, release_language_storage } from "el:memory/allocation/index.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { null_pointer } from "el:memory/storage/raw.el"
let size = AllocationSize(64)
let alignment = AllocationSize(8)
let block = allocate_language_base_storage(size, alignment)
if (block != null_pointer()) {
	try {
		// 在这里使用申请到的存储。
	}
	finally { release_language_storage(block, size, alignment) }
}
```
