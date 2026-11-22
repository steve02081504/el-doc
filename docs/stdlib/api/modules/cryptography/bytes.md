# cryptography/bytes.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 密码学字节辅助 {#api-140bf57c5b24fa46050e}

源码：`src/stdlib/cryptography/bytes.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L1)

密码学字节辅助相关接口。

## append_u32le {#api-62c62e0594b0769368fd}

源码：`src/stdlib/cryptography/bytes.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L63)

将无符号 32 位整数按小端顺序追加到目标数组。

```el-signature
export fn append_u32le(target: Number[], value: Number)
```

**失败与异常**：值不是范围内的整数时抛出 CryptoError。

### 示例：使用示例

```el
import { append_u32le } from "el:cryptography/bytes.el"
let bytes: Number[] = @[]
append_u32le(bytes, 258)
```

## read_u32le {#api-af807339462b26e6a4b9}

源码：`src/stdlib/cryptography/bytes.el:115` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L115)

从给定偏移读取四个小端字节，返回无符号整数。

```el-signature
export fn read_u32le(source: Number[], at: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**失败与异常**：范围越界或输入包含无效字节时抛出 CryptoError。

### 示例：使用示例

```el
import { read_u32le } from "el:cryptography/bytes.el"
let value = read_u32le(@[2, 1, 0, 0], 0)
```

## hex_of {#api-44c4d8572ee965483683}

源码：`src/stdlib/cryptography/bytes.el:163` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L163)

将字节数组编码为小写十六进制文本。

```el-signature
export fn hex_of(bytes: Number[]): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

**失败与异常**：输入包含无效字节时抛出 CryptoError。

### 示例：使用示例

```el
import { hex_of } from "el:cryptography/bytes.el"
let encoded = hex_of(@[0, 255])
```

## hex_bytes {#api-aa9c1315980ca9917228}

源码：`src/stdlib/cryptography/bytes.el:189` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L189)

将偶数长度的十六进制文本解码为字节数组。

```el-signature
export fn hex_bytes(text: Text): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**失败与异常**：文本长度为奇数或包含非十六进制字符时抛出 CryptoError。

### 示例：使用示例

```el
import { hex_bytes } from "el:cryptography/bytes.el"
let bytes = hex_bytes("00ff")
```

## constant_time_equal {#api-8d93c2aef9939ebe4a96}

源码：`src/stdlib/cryptography/bytes.el:214` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/bytes.el#L214)

比较字节数组；长度不同立即返回，等长内容累积差异。

```el-signature
export fn constant_time_equal(left: Number[], right: Number[]): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**注意**：等长比较具有常数时间意图，尚非侧信道实测证明。

### 示例：使用示例

```el
import { constant_time_equal } from "el:cryptography/bytes.el"
let equal = constant_time_equal(@[1, 2], @[1, 2])
```
