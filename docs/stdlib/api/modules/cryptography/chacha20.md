# cryptography/chacha20.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## ChaCha20 {#api-3cec491eee1cf4b584c0}

源码：`src/stdlib/cryptography/chacha20.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/chacha20.el#L1)

提供 RFC 8439 ChaCha20 密钥流与字节异或操作。

## chacha20_xor {#api-bc7a25de7cb7e0682650}

源码：`src/stdlib/cryptography/chacha20.el:92` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/chacha20.el#L92)

```el
export fn chacha20_xor(key: Number[], nonce: Number[], initial_counter: Number, input: Number[]): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

将 ChaCha20 密钥流与输入字节异或，得到同长度输出。

**参数**：key 恰好 32 字节的密钥。

**参数**：nonce 恰好 12 字节的 nonce；同一密钥下不得重用。

**参数**：initial_counter 首个 32 位块计数器。

**参数**：input 要处理的字节数组。

**返回值**：与输入等长的异或结果。

**失败与异常**：密钥、nonce、计数器或输入无效，或块计数器将溢出时抛出 CryptoError。

**注意**：此低层流密码操作不提供认证；同一密钥下 nonce 必须唯一。

### 示例：处理一段字节

```el
import { chacha20_xor, secure_random_bytes } from "el:cryptography/"
let key = secure_random_bytes(32)
let nonce = secure_random_bytes(12)
let output = chacha20_xor(key, nonce, 1, @[72, 105])
```
