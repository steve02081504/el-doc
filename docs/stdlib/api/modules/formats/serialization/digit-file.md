# formats/serialization/digit-file.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## EOD 数位文件 {#api-5824d188d6bc30b942ee}

源码：`src/stdlib/formats/serialization/digit-file.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-file.el#L1)

为 EOD 对象图组织文件头、载荷和完整性校验。

## encodeEodDigitFile {#api-5f1e5511892051aae77e}

源码：`src/stdlib/formats/serialization/digit-file.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-file.el#L18)

写出带配置与校验的 EOD 数位文件。缺省使用目标数位基数和地址宽度。

```el-signature
export fn encodeEodDigitFile(value, profile: EodDigitProfile = targetEodDigitProfile(), schema: Number = eodFileSchema): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：编码文本对象

```el
import { encodeEodDigitFile } from "el:formats/serialization/"
let units = encodeEodDigitFile("EL")
```

## decodeEodDigitFile {#api-5e2fe75ef5463fe8c852}

源码：`src/stdlib/formats/serialization/digit-file.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-file.el#L36)

先验证文件配置、长度和校验，再按同一配置恢复 EOD 对象图。

```el-signature
export fn decodeEodDigitFile(units: Number[], profile: EodDigitProfile = targetEodDigitProfile(), limits: SerializationLimits = SerializationLimits())
```

### 示例：恢复文本对象

```el
import { encodeEodDigitFile, decodeEodDigitFile } from "el:formats/serialization/"
let value = decodeEodDigitFile(encodeEodDigitFile("EL"))
```
