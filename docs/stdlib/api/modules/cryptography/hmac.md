# cryptography/hmac.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## HMAC-SHA256 {#api-802e7b20abb60cc9b3a9}

源码：`src/stdlib/cryptography/hmac.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/hmac.el#L1)

提供基于 SHA-256 的 HMAC 标签计算与验证。

## hmac_sha256 {#api-da94cb9868cf324a8d93}

源码：`src/stdlib/cryptography/hmac.el:80` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/hmac.el#L80)

```el
export fn hmac_sha256(key: Number[], message: Number[]): Number[]
```

**返回类型**：`Number[]`

使用 HMAC-SHA256 对消息生成认证标签。

**参数**：key 密钥字节数组。

**参数**：message 要认证的消息字节数组。

**返回值**：32 字节 HMAC 标签。

**失败与异常**：任一输入包含非字节值时抛出 CryptoError。

### 示例：生成 HMAC 标签

```el
import { hmac_sha256 } from "el:cryptography/"
let tag = hmac_sha256(@[1, 2, 3], @[4, 5])
```

## hmac_verify {#api-f40a87cdd333f18b2bac}

源码：`src/stdlib/cryptography/hmac.el:102` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/hmac.el#L102)

```el
export fn hmac_verify(key: Number[], message: Number[], tag: Number[]): Bool
```

**返回类型**：`Bool`

验证消息的 HMAC-SHA256 标签；比较 32 字节标签时调用 constant_time_equal。

**参数**：key 生成标签时使用的密钥字节数组。

**参数**：message 已认证的消息字节数组。

**参数**：tag 待验证标签；长度不是 32 时直接返回假。

**返回值**：标签有效时为真。

**失败与异常**：输入字节无效时抛出 CryptoError。

### 示例：验证 HMAC 标签

```el
import { hmac_sha256, hmac_verify } from "el:cryptography/"
let key = @[1, 2, 3]
let message = @[4, 5]
let valid = hmac_verify(key, message, hmac_sha256(key, message))
```
