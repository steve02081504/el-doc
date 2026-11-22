# foreign-functions/abi.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/foreign-functions.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 外部调用 ABI {#api-4dda9e9d4c1cd0e8de9e}

源码：`src/stdlib/foreign-functions/abi.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/abi.el#L14)

提供外部函数参数寄存器规则及调用帧规划所需的数据结构。

## first {#api-bb1c894f7b65a20d77fa}

源码：`src/stdlib/foreign-functions/abi.el:520` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/foreign-functions/abi.el#L520)

创建按顺序指定的外部调用通用寄存器参数规则。

```el-signature
export fn first(registers: Number[]): AbiArguments
```

**返回类型**：[`AbiArguments`](../../types.md#api-69e3253ededec3fc60b4)

**参数**：registers 不重复的物理通用寄存器编号，每个值须为 0 到 31 的整数。

**返回值**：保存寄存器顺序的 AbiArguments。

**失败与异常**：寄存器编号非法或重复时抛出错误。

### 示例：指定前两个参数寄存器

```el
let arguments = first(@[7, 6])
```
