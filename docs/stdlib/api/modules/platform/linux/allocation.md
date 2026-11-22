# platform/linux/allocation.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/platform.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## Linux 原生分配器 {#api-9130596d0174a7d1ab7d}

源码：`src/stdlib/platform/linux/allocation.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/linux/allocation.el#L1)

提供 Linux 平台的对齐原生存储分配、调整与释放实现。

## native_allocate {#api-722954afa51ff8e2ee59}

源码：`src/stdlib/platform/linux/allocation.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/linux/allocation.el#L78)

按指定大小和对齐方式分配原生存储；失败时返回空指针。

```el-signature
export fn native_allocate(size: AllocationSize, alignment: AllocationSize): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

**参数**：size 请求的载荷大小。

**参数**：alignment 要求的对齐值。

**返回值**：对齐后的载荷指针，失败时为空指针。

### 示例：分配并释放原生存储

```el
let memory = native_allocate(AllocationSize(16), AllocationSize(8))
native_release(memory)
```

## native_release {#api-8e0e19c5a2fad7e5e438}

源码：`src/stdlib/platform/linux/allocation.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/linux/allocation.el#L118)

释放由 native_allocate 返回的原生存储；空指针可安全传入。

```el-signature
export fn native_release(pointer: ptr)
```

**参数**：pointer native_allocate 返回的载荷指针。

### 示例：释放调用者持有的原生存储

```el
// @external pointer: ptr
native_release(pointer)
```
