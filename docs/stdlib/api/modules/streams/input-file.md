# streams/input-file.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/streams.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 原生输入文件 {#api-e0a8d72b3ff014281d5f}

源码：`src/stdlib/streams/input-file.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/streams/input-file.el#L1)

提供面向原生文件句柄的输入所有权与关闭管理。

## openInputFile {#api-3457cba5be48dc94b859}

源码：`src/stdlib/streams/input-file.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/streams/input-file.el#L138)

```el
export fn openInputFile(path: Text, lock: Bool | void_t = void, protection: FileReadProtection = FileReadProtection(lock is t_t)): NativeInputFile
```

**返回类型**：[`NativeInputFile`](../../types.md#api-cac9566a49a1edb75a36)

打开原生文件作为顺序输入流。

**参数**：path 原生文件系统路径。

**参数**：lock 可选的读取保护请求。

**参数**：protection 记录读取保护请求与观察结果的对象。

**返回值**：拥有原生句柄的输入文件对象；调用方负责关闭或让其析构清理。

**失败与异常**：路径无效、文件打开失败或保护配置状态不匹配时抛出异常。

### 示例：打开并读取输入文件

```el
import { openInputFile } from "el:streams/input-file.el"
let input = openInputFile("data.bin")
input.close()
```

## openOptionalInputFile {#api-ee8a540efdae1657f07b}

源码：`src/stdlib/streams/input-file.el:153` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/streams/input-file.el#L153)

```el
export fn openOptionalInputFile(path: Text): NativeInputFile | void_t
```

**返回类型**：[`NativeInputFile`](../../types.md#api-cac9566a49a1edb75a36) | [`void_t`](../language/values.md#api-d7b419fab395eef3d142)

尝试打开原生输入文件；仅在平台报告文件缺失时返回 void。

**参数**：path 原生文件系统路径。

**返回值**：已打开的输入文件对象，或目标不存在时的 void。

**失败与异常**：除文件缺失以外的打开失败时抛出异常。

### 示例：可选读取输入文件

```el
import { openOptionalInputFile } from "el:streams/input-file.el"
let input = openOptionalInputFile("optional.bin")
```
