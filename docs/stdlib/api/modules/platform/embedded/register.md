# platform/embedded/register.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/platform.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 嵌入式寄存器访问 {#api-454f1cf80dbcf8cc1850}

源码：`src/stdlib/platform/embedded/register.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/embedded/register.el#L1)

提供受范围检查的无符号寄存器类型与 MMIO 区域访问原语。

## U8 {#api-86e8d3e236ed444e4ebc}

源码：`src/stdlib/platform/embedded/register.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/embedded/register.el#L19)

取值范围为 0 到 255 的无符号整数类型；越界运算报错。

```el-signature
export let U8: type
```

**类型**：[`type`](../../../../../reference/language/types.md)

### 示例：声明一个字节值

```el
let byte: U8 = U8(255)
```

## U32 {#api-7426cc317fee3bd30c57}

源码：`src/stdlib/platform/embedded/register.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/embedded/register.el#L27)

取值范围为 0 到 4294967295 的无符号整数类型；越界运算报错。

```el-signature
export let U32: type
```

**类型**：[`type`](../../../../../reference/language/types.md)

### 示例：声明一个 32 位无符号值

```el
let word: U32 = U32(4294967295)
```
