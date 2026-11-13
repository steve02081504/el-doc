# cryptography/pbkdf2.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## PBKDF2 {#api-47dd3213b5fe3ac00853}

源码：`src/stdlib/cryptography/pbkdf2.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/pbkdf2.el#L1)

提供基于 HMAC-SHA1 与 HMAC-SHA256 的 PBKDF2 密钥派生。

## pbkdf2_sha1 {#api-d020f6a2cb3f95fd05e0}

源码：`src/stdlib/cryptography/pbkdf2.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/pbkdf2.el#L53)

```el
export fn pbkdf2_sha1(password: Number[], salt: Number[], iterations: Number, count: Number): Number[]
```

**返回类型**：`Number[]`

使用 PBKDF2-HMAC-SHA1 从密码和盐派生密钥字节。

**参数**：password 密码字节。

**参数**：salt 派生盐字节。

**参数**：iterations 正整数迭代次数，最大为 4294967295。

**参数**：count 输出字节数，范围为 0 到 1048576。

**返回值**：派生的密钥字节。

**失败与异常**：参数不是范围内的整数、迭代次数为零或字节输入无效时抛出 CryptoError。

### 示例：派生密码密钥

```el
import { pbkdf2_sha1 } from "el:cryptography/"
let derived = pbkdf2_sha1(@[112, 97, 115, 115], @[1, 2, 3, 4], 1000, 32)
```

## pbkdf2_sha256 {#api-652e43357d7e243dfb59}

源码：`src/stdlib/cryptography/pbkdf2.el:67` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/pbkdf2.el#L67)

```el
export fn pbkdf2_sha256(password: Number[], salt: Number[], iterations: Number, count: Number): Number[]
```

**返回类型**：`Number[]`

使用 PBKDF2-HMAC-SHA256 从密码和盐派生密钥字节。

**参数**：password 密码字节。

**参数**：salt 派生盐字节。

**参数**：iterations 正整数迭代次数，最大为 4294967295。

**参数**：count 输出字节数，范围为 0 到 1048576。

**返回值**：派生的密钥字节。

**失败与异常**：参数不是范围内的整数、迭代次数为零或字节输入无效时抛出 CryptoError。

### 示例：派生密码密钥

```el
import { pbkdf2_sha256 } from "el:cryptography/"
let derived = pbkdf2_sha256(@[112, 97, 115, 115], @[1, 2, 3, 4], 1000, 32)
```
