# memory/storage/raw.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 原始存储 {#api-49f4f11ba68a9e8eae0c}

源码：`src/stdlib/memory/storage/raw.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L1)

提供原生指针和原始存储访问接口。

## null_pointer {#api-4ba01f78fbc0e7f9d54c}

源码：`src/stdlib/memory/storage/raw.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L22)

返回空原生指针；它不指向可解引用的存储。

```el-signature
export @builtin:vome:raw:pointer:null fn null_pointer(): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

### 示例：用法

```el
import { null_pointer } from "el:memory/storage/raw.el"
let pointer = null_pointer()
```

## scalar_load {#api-434a60afcb17b8b68d9c}

源码：`src/stdlib/memory/storage/raw.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L50)

从 pointer 的 byte_offset 处读取标量；调用方须保证存储有效、范围和对齐满足原生访问要求。

```el-signature
export @builtin:vome:raw:scalar:load fn scalar_load(pointer: ptr, byte_offset: Integer): Integer
```

**返回类型**：[`Integer`](../../platform/machine/integer.md#api-45690472287900730a5f)

### 示例：用法

```el
import { scalar_load } from "el:memory/storage/raw.el"
fn readScalar(pointer: ptr) { return scalar_load(pointer, 0) }
```

## scalar_store {#api-fd0e9c100c89857ad579}

源码：`src/stdlib/memory/storage/raw.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L58)

向 pointer 的 byte_offset 处写入标量；调用方须保证存储可写且范围、对齐满足原生访问要求。

```el-signature
export @builtin:vome:raw:scalar:store fn scalar_store(pointer: ptr, byte_offset: Integer, replacement: Integer): Integer
```

**返回类型**：[`Integer`](../../platform/machine/integer.md#api-45690472287900730a5f)

### 示例：用法

```el
import { scalar_store } from "el:memory/storage/raw.el"
fn writeScalar(pointer: ptr) { return scalar_store(pointer, 0, 65) }
```
