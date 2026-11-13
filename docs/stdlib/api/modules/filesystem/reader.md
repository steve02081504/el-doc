# filesystem/reader.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [FileReader.read](#api-de5485f845b68f2bcf8a)
- [FileReader.close](#api-226f1d4ed93e75e92625)

## 文件读取器 {#api-6e76e3b3e1ee0eb46bc7}

源码：`src/stdlib/filesystem/reader.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/reader.el#L15)

提供顺序及可选随机访问的逻辑位置读取器。

## FileReader.read {#api-de5485f845b68f2bcf8a}

源码：`src/stdlib/filesystem/reader.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/reader.el#L142)

从当前位置读取至多指定数量的原始字节。

```el
fn read(maximumBytes: Number): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：maximumBytes 本次最多读取的字节数。

**返回值**：实际读取的字节数组；到达末尾时可为空。

**失败与异常**：读取器关闭、失败或底层读取失败时抛出异常。

### 示例：读取一段二进制内容

```el
let reader = openFileReader("file:./payload.bin")
let bytes = reader.read(1024)
reader.close()
```

## FileReader.close {#api-226f1d4ed93e75e92625}

源码：`src/stdlib/filesystem/reader.el:200` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/reader.el#L200)

关闭读取器并结束其底层资源使用。

```el
fn close(): void_t
```

**返回类型**：[`void_t`](../language/values.md#api-d7b419fab395eef3d142)

**失败与异常**：底层关闭失败时传播文件系统异常。

### 示例：关闭读取器

```el
let reader = openFileReader("file:./payload.bin")
reader.close()
```
