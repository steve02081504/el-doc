# documents/package.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/documents.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## Office 文档包 {#api-e8e525f24ff71ac11a24}

源码：`src/stdlib/documents/package.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/package.el#L1)

读取、编辑和重新封装文档包部件。

## decodeOffice {#api-883cff65608e857e1b28}

源码：`src/stdlib/documents/package.el:130` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/package.el#L130)

读取使用目标或指定基数的 Office 包。

```el-signature
export fn decodeOffice(data: Number[], radix: Number | nil_t = nil): OfficePackage
```

**返回类型**：[`OfficePackage`](../../types.md#api-7fca6822013b6b181832)

### 示例：读取 EL 写出的办公室文档

```el
import { decodeOffice } from "el:documents/"
import { resolvePath } from "el:filesystem/"
let package = decodeOffice(resolvePath("notes.docx").readBytes())
```

## decodeStandardOffice {#api-ade927989703a058998d}

源码：`src/stdlib/documents/package.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/package.el#L142)

显式读取按固定 PK ZIP 协议编码的 OOXML 或 OpenDocument 包。

```el-signature
export fn decodeStandardOffice(data: Number[]): OfficePackage
```

**返回类型**：[`OfficePackage`](../../types.md#api-7fca6822013b6b181832)

### 示例：读取固定协议的文档包

```el
import { decodeStandardOffice } from "el:documents/"
import { resolvePath } from "el:filesystem/"
let package = decodeStandardOffice(resolvePath("notes.docx").readBytes())
```
