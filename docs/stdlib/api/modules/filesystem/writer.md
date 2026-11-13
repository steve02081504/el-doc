# filesystem/writer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [FileWriter.write](#api-60eb68cfed70401fd999)
- [FileWriter.close](#api-95af169891a6620e73da)

## 文件写入器 {#api-f9004a464dbaefb64a37}

源码：`src/stdlib/filesystem/writer.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/writer.el#L1)

提供逻辑位置写入器，显式报告写入回执并支持可选刷新。

## FileWriter.write {#api-60eb68cfed70401fd999}

源码：`src/stdlib/filesystem/writer.el:135` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/writer.el#L135)

```el
fn write(bytes: Number[]): WriteReceipt
```

**返回类型**：`WriteReceipt`

将字节数组快照写入目标位置并返回写入回执。

**参数**：bytes 要写出的字节数组。

**返回值**：描述成功写入数量与状态的 WriteReceipt。

**失败与异常**：输入不是合法字节、写入器关闭或 provider 写入失败时抛出异常。

### 示例：写出二进制内容

```el
let writer = openFileWriter("file:./output.bin")
let receipt = writer.write(@[72, 105])
writer.close()
```

## FileWriter.close {#api-95af169891a6620e73da}

源码：`src/stdlib/filesystem/writer.el:173` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/writer.el#L173)

```el
fn close(): void_t
```

**返回类型**：`void_t`

完成写入器并关闭底层资源。

**失败与异常**：provider 关闭失败或关闭结果不确定时抛出异常。

### 示例：关闭写入器

```el
let writer = openFileWriter("file:./output.bin")
writer.close()
```
