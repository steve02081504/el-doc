# cryptography/hkdf.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/cryptography.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## HKDF-SHA256 {#api-1cd7cf67b36f64c23e4a}

源码：`src/stdlib/cryptography/hkdf.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/hkdf.el#L1)

提供 RFC 5869 的 HKDF-SHA256 提取、扩展与便捷派生函数。

## hkdf_sha256 {#api-7c67285c72766cec637c}

源码：`src/stdlib/cryptography/hkdf.el:67` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/cryptography/hkdf.el#L67)

```el
export fn hkdf_sha256(ikm: Number[], salt: Number[] | void_t = void, info: Number[] | void_t = void, length: Number = 32): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

依次执行 HKDF-SHA256 的 Extract 与 Expand。

**参数**：ikm 输入密钥材料字节。

**参数**：salt 可选盐值；缺省时按 HKDF 使用零值盐。

**参数**：info 可选的上下文信息字节。

**参数**：length 输出密钥材料长度，范围为 0 到 8160 字节。

**返回值**：派生出的字节数组。

**失败与异常**：输出长度无效或超过上限时抛出 CryptoError。

### 示例：派生 32 字节密钥材料

```el
import { hkdf_sha256 } from "el:cryptography/"
let keyMaterial = hkdf_sha256(@[1, 2, 3])
```
