# database/storage/digit-framing.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/database.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数据库数位记录 {#api-8990031a090a7459c197}

源码：`src/stdlib/database/storage/digit-framing.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/storage/digit-framing.el#L1)

按存储配置组织整数字段、记录头与校验。

## targetStorageDigitProfile {#api-a0b3c9cadc98ac106c18}

源码：`src/stdlib/database/storage/digit-framing.el:162` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/storage/digit-framing.el#L162)

为持久存储选择目标支持的基数。缺省使用目标基数。

```el-signature
export fn targetStorageDigitProfile(radix: Number | nil_t = nil): StorageDigitProfile
```

**返回类型**：[`StorageDigitProfile`](../../../types.md#api-c9b2e83a2c343c580fe7)

### 示例：取得数据库的目标数位配置

```el
import { targetStorageDigitProfile } from "el:database/storage/index.el"
let profile = targetStorageDigitProfile()
```
