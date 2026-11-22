# errors/error.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/errors.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 基础错误 {#api-4194fe8f99de2f238f75}

源码：`src/stdlib/errors/error.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/error.el#L1)

提供基础诊断错误及状态错误类型。

## Error {#api-f8d67201610919a9342d}

源码：`src/stdlib/errors/error.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/error.el#L17)

标准库错误基类，保存诊断键、参数、原因和栈；复制与重抛保留构造时捕获的栈。

```el-signature
export @assign(mode: "copy") class Error
```

### 示例：用法

```el
let error = Error("error.range")
let key = error.diagnosticKey
```

## StateError {#api-25ffa202d772fa517e70}

源码：`src/stdlib/errors/error.el:83` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/error.el#L83)

表示操作所需状态不满足的错误，使用给定诊断键和可选原因。

```el-signature
export @assign(mode: "copy") class StateError extends Error
```

### 示例：用法

```el
let error = StateError("stdlib.state.invalid")
```
