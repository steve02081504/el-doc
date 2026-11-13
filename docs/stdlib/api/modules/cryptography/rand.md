# cryptography/rand.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 密码学随机数 {#api-a638b58a863d8f30f33d}

源码：`src/stdlib/cryptography/rand.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/rand.el#L1)

提供从操作系统密码学随机源读取字节的接口。

## secure_random_bytes {#api-419282ad372a03627bc4}

源码：`src/stdlib/cryptography/rand.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/rand.el#L24)

从操作系统随机源读取指定数量的密码学随机字节。

```el
export fn secure_random_bytes(count: Number): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：count 要读取的字节数，范围为 0 到 1048576。

**返回值**：随机字节数组。

**失败与异常**：字节数无效或操作系统熵源失败时抛出 CryptoError；不会回退到弱生成器。

### 示例：生成随机 nonce 字节

```el
import { secure_random_bytes } from "el:cryptography/"
let nonce = secure_random_bytes(12)
```

## secure_random_hex {#api-c454f904317622bce76d}

源码：`src/stdlib/cryptography/rand.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/rand.el#L51)

读取密码学随机字节并返回小写十六进制编码。

```el
export fn secure_random_hex(count: Number): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

**参数**：count 随机字节数，范围为 0 到 1048576。

**返回值**：长度为 count 乘以 2 的十六进制文本。

**失败与异常**：字节数无效或操作系统熵源失败时抛出 CryptoError。

### 示例：生成随机令牌文本

```el
import { secure_random_hex } from "el:cryptography/"
let token = secure_random_hex(16)
```
