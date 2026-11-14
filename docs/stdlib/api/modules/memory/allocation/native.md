# memory/allocation/native.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 原生对齐分配 {#api-4cb354bcb019652ebf21}

源码：`src/stdlib/memory/allocation/native.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/native.el#L1)

按目标平台选择 native_allocate、native_resize 和 native_release。分配失败返回空指针；调整失败保留原块，成功后使用返回的新指针。调用者以 native_release 释放成功的块，不能与语言存储释放入口混用。

### 示例：分配和释放

```el
import { native_allocate, native_release } from "el:memory/allocation/native.el"
import { AllocationSize } from "el:memory/allocation/types.el"
import { null_pointer } from "el:memory/storage/raw.el"
let block: ptr = null_pointer()
unsafe { block = native_allocate(AllocationSize(64), AllocationSize(8)) }
if (block != null_pointer()) {
	try {
		// 在这里使用申请到的存储。
	}
	finally { unsafe { native_release(block) } }
}
```
