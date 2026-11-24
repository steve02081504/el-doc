# archives/tar.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/archives.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## TAR 归档 {#api-d460c3c003f6c27e3a37}

源码：`src/stdlib/archives/tar.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/tar.el#L1)

按目标或调用方指定的基数存储归档条目。

## encodeTar {#api-d6a98609628a951ff853}

源码：`src/stdlib/archives/tar.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/tar.el#L13)

编码不压缩的目标数位归档，缺省采用目标基数；options.radix 可指定较小基数。

```el-signature
export fn encodeTar(entries: ArchiveEntry[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：编码空归档

```el
import { encodeTar } from "el:archives/"
let data = encodeTar(@[])
```

## decodeTar {#api-216ea1210e062a2582f2}

源码：`src/stdlib/archives/tar.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/tar.el#L24)

解码与所选基数及地址单元宽度匹配的原生 TAR 归档。

```el-signature
export fn decodeTar(data: Number[], options: ArchiveOptions = ArchiveOptions()): ArchiveEntry[]
```

**返回类型**：[`ArchiveEntry`](../../types.md#api-566266bfda7d84271278)[]

### 示例：读回空归档

```el
import { encodeTar, decodeTar } from "el:archives/"
let entries = decodeTar(encodeTar(@[]))
```
