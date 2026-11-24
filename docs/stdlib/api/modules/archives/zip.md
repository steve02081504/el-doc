# archives/zip.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/archives.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## ZIP 归档 {#api-94acf6e0b8de6bff2007}

源码：`src/stdlib/archives/zip.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/zip.el#L1)

使用同一套归档编码按编译目标基数或调用方选定的较小基数特化。

## encodeZip {#api-dacc7c8723f0a8d84745}

源码：`src/stdlib/archives/zip.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/zip.el#L17)

编码目标数位归档。缺省采用目标基数，options.radix 可指定从 2 到目标基数的整数。统一使用 .zip 扩展名。

```el-signature
export fn encodeZip(entries: ArchiveEntry[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：编码空归档

```el
import { encodeZip } from "el:archives/"
let data = encodeZip(@[])
```

## decodeZip {#api-e77ddc4b383a87b3f210}

源码：`src/stdlib/archives/zip.el:32` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/zip.el#L32)

按目标基数或 options.radix 指定的基数读取同一种归档表示。归档头记录基数与地址单元宽度。

```el-signature
export fn decodeZip(data: Number[], options: ArchiveOptions = ArchiveOptions()): ArchiveEntry[]
```

**返回类型**：[`ArchiveEntry`](../../types.md#api-566266bfda7d84271278)[]

### 示例：读回同一目标写出的归档

```el
import { encodeZip, decodeZip } from "el:archives/"
let entries = decodeZip(encodeZip(@[]))
```
