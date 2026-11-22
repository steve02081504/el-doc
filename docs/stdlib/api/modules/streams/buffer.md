# streams/buffer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/streams.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 字节缓冲区 {#api-ca201872cdd382f13f7d}

源码：`src/stdlib/streams/buffer.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/streams/buffer.el#L5)

在目标存储单元数组和普通数值字节数组之间转换。

## bufferFromBytes {#api-fb6f09fd21ddefe91f98}

源码：`src/stdlib/streams/buffer.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/streams/buffer.el#L21)

将数值字节数组转换为目标存储单元组成的 Buffer。

```el-signature
export fn bufferFromBytes(bytes: Number[]): Buffer
```

**返回类型**：[`Buffer`](../../types.md#api-80af2b4a017fc9c8d506)

**参数**：bytes 每个元素都必须能转换为 Byte 的数值数组。

**返回值**：按输入顺序保存元素的新 Buffer。

**失败与异常**：某个值无法转换为目标 Byte 类型时抛出转换错误。

### 示例：从两个字节创建缓冲区

```el
let buffer = bufferFromBytes(@[65, 66])
```
