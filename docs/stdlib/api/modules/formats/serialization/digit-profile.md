# formats/serialization/digit-profile.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## EOD 数位配置 {#api-daad3dcf236e6f2031df}

源码：`src/stdlib/formats/serialization/digit-profile.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-profile.el#L1)

指定 EOD 载荷的基数及地址宽度。

## EodDigitProfile {#api-99be3934839f1ead7921}

源码：`src/stdlib/formats/serialization/digit-profile.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-profile.el#L16)

指定 EOD 数位载荷的基数和每地址单元数位数。直接构造可在内存中使用合成目标。

```el-signature
export @assign(mode: "shared") class EodDigitProfile
```

### 示例：构造合成三进制配置

```el
import { EodDigitProfile } from "el:formats/serialization/"
let profile = EodDigitProfile(3, 5)
```

## targetEodDigitProfile {#api-c80af33e1eb6c69c7d01}

源码：`src/stdlib/formats/serialization/digit-profile.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/serialization/digit-profile.el#L44)

按目标地址宽度及选定基数创建 EOD 数位载荷配置。缺省使用目标基数。

```el-signature
export fn targetEodDigitProfile(radix: Number | nil_t = nil): EodDigitProfile
```

**返回类型**：[`EodDigitProfile`](digit-profile.md#api-99be3934839f1ead7921)

### 示例：使用目标地址宽度

```el
import { targetEodDigitProfile } from "el:formats/serialization/"
let profile = targetEodDigitProfile(2)
```
