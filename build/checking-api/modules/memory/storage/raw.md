# memory/storage/raw.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 原始存储 {#api-49f4f11ba68a9e8eae0c}

源码：`src/stdlib/memory/storage/raw.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L1)

提供原生指针和原始存储访问接口。

## null_pointer {#api-4ba01f78fbc0e7f9d54c}

源码：`src/stdlib/memory/storage/raw.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/storage/raw.el#L21)

返回空原生指针；它不指向可解引用的存储。

```el-signature
export @builtin:vome:raw:pointer:null fn null_pointer(): ptr
```

**返回类型**：[`ptr`](../../../../../reference/language/foreign.md)

### 示例：用法

```el
let pointer = null_pointer()
```
