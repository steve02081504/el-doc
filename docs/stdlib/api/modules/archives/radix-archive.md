# archives/radix-archive.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/archives.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 归档记录与游程压缩 {#api-c7ee314c056e6b0e7e55}

源码：`src/stdlib/archives/radix-archive.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/radix-archive.el#L1)

按可选基数读写归档条目和独立压缩流。

## compressDigits {#api-8a6f985fe2ea53bec761}

源码：`src/stdlib/archives/radix-archive.el:263` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/radix-archive.el#L263)

使用与数位归档共用的自适应游程编码压缩地址单元数组。

```el-signature
export fn compressDigits(data: Number[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：压缩重复单元

```el
import { compressDigits } from "el:archives/"
let units = compressDigits(@[5, 5, 5, 5, 5])
```

## decompressDigits {#api-4afa577110bd475339d9}

源码：`src/stdlib/archives/radix-archive.el:282` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/radix-archive.el#L282)

按选定数位基数恢复地址单元数组，展开前检查 options.limits 的输出额度。

```el-signature
export fn decompressDigits(data: Number[], options: ArchiveOptions = ArchiveOptions()): Number[]
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：恢复压缩前的单元

```el
import { compressDigits, decompressDigits } from "el:archives/"
let original = decompressDigits(compressDigits(@[5, 5, 5, 5, 5]))
```
