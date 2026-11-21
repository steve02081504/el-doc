# cryptography/aead.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## ChaCha20-Poly1305 {#api-97bbeac53127324887c0}

源码：`src/stdlib/cryptography/aead.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/aead.el#L1)

提供认证加密与先验证后解密的 ChaCha20-Poly1305 接口。

## chacha20_poly1305_encrypt {#api-08ed02675294d0f1cc7d}

源码：`src/stdlib/cryptography/aead.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/aead.el#L56)

使用 ChaCha20-Poly1305 加密并认证明文及关联数据。

```el
export fn chacha20_poly1305_encrypt(key: Number[], nonce: Number[], associated_data: Number[], plaintext: Number[]): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：key 恰好 32 字节的密钥。

**参数**：nonce 恰好 12 字节且不可在同一密钥下重用的 nonce。

**参数**：associated_data 不加密但参与认证的字节。

**参数**：plaintext 待加密明文字节。

**返回值**：密文后附加 16 字节认证标签。

**失败与异常**：字节输入无效或消息超过算法长度范围时抛出 CryptoError。

### 示例：加密短消息

```el
import { chacha20_poly1305_encrypt, secure_random_bytes } from "el:cryptography/"
let key = secure_random_bytes(32)
let nonce = secure_random_bytes(12)
let sealed = chacha20_poly1305_encrypt(key, nonce, @[], @[72, 105])
```

## chacha20_poly1305_decrypt {#api-12a7d04f1b0e750acedd}

源码：`src/stdlib/cryptography/aead.el:92` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/aead.el#L92)

验证 ChaCha20-Poly1305 标签后解密密文。

```el
export fn chacha20_poly1305_decrypt(key: Number[], nonce: Number[], associated_data: Number[], sealed: Number[]): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：key 加密时使用的 32 字节密钥。

**参数**：nonce 加密时使用的 12 字节 nonce。

**参数**：associated_data 加密时认证的关联数据。

**参数**：sealed 密文及其末尾的 16 字节标签。

**返回值**：认证成功后的明文字节；验证失败不会返回明文。

**失败与异常**：输入格式无效或标签验证失败时抛出 CryptoError。

### 示例：解密并认证密文

```el
import { chacha20_poly1305_decrypt, chacha20_poly1305_encrypt, secure_random_bytes } from "el:cryptography/"
let key = secure_random_bytes(32)
let nonce = secure_random_bytes(12)
let sealed = chacha20_poly1305_encrypt(key, nonce, @[], @[72, 105])
let plaintext = chacha20_poly1305_decrypt(key, nonce, @[], sealed)
```
