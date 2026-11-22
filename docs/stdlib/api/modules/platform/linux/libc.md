# platform/linux/libc.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/platform.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## Linux libc ABI {#api-7d2ea856d070786c50a8}

源码：`src/stdlib/platform/linux/libc.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/linux/libc.el#L1)

提供 Linux x86-64 libc 原生类型和经过目标环境选择的 ABI 声明。

## NativeInt {#api-5fc2beb1be963b400238}

源码：`src/stdlib/platform/linux/libc.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/linux/libc.el#L14)

Linux x86-64 libc 使用的有符号 32 位整数载体；原生 ABI 数值须显式转换到此类型。

```el-signature
export @builtin:vome:signed:integer(format: "digits(5)") class NativeInt
```

### 示例：构造原生整数参数

```el
let status = NativeInt(0)
```
