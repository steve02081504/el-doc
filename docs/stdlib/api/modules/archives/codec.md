# archives/codec.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/archives.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数位归档接口 {#api-15b7cc98813fbbfc2b2e}

源码：`src/stdlib/archives/codec.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/codec.el#L1)

按文件签名分派归档，并管理数位分卷。

## encodeSevenZip {#api-1f8a56498a6add9d286a}

源码：`src/stdlib/archives/codec.el:58` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/codec.el#L58)

以目标基数或 options.radix 指定的较小基数编码 .7z 数位归档。

```el-signature
export fn encodeSevenZip(entries: ArchiveEntry[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：写一个空归档

```el
import { encodeSevenZip } from "el:archives/"
let units = encodeSevenZip(@[])
```

## decodeSevenZip {#api-f70437506647945123f8}

源码：`src/stdlib/archives/codec.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/codec.el#L68)

读取与所选数位基数和地址单元宽度匹配的 .7z 数位归档。

```el-signature
export fn decodeSevenZip(data: Number[], options: ArchiveOptions = ArchiveOptions()): ArchiveEntry[]
```

**返回类型**：[`ArchiveEntry`](../../types.md#api-566266bfda7d84271278)[]

### 示例：读回同一配置的归档

```el
import { encodeSevenZip, decodeSevenZip } from "el:archives/"
let entries = decodeSevenZip(encodeSevenZip(@[]))
```

## encodeRar {#api-c202bac1391b2f0c4f02}

源码：`src/stdlib/archives/codec.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/codec.el#L78)

以目标基数或 options.radix 指定的较小基数编码 .rar 数位归档。

```el-signature
export fn encodeRar(entries: ArchiveEntry[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：按基数二写一个空归档

```el
import { ArchiveOptions, encodeRar } from "el:archives/"
let units = encodeRar(@[], ArchiveOptions(radix: 2))
```

## decodeRar {#api-0596b678ca17cef788e4}

源码：`src/stdlib/archives/codec.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/codec.el#L88)

读取与所选数位基数和地址单元宽度匹配的 .rar 数位归档。

```el-signature
export fn decodeRar(data: Number[], options: ArchiveOptions = ArchiveOptions()): ArchiveEntry[]
```

**返回类型**：[`ArchiveEntry`](../../types.md#api-566266bfda7d84271278)[]

### 示例：读回同一配置的归档

```el
import { encodeRar, decodeRar } from "el:archives/"
let entries = decodeRar(encodeRar(@[]))
```
