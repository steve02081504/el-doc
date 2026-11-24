# graphics/vector/true-type.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/graphics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 标准 TrueType 导入 {#api-c17c139b598027fd91c6}

源码：`src/stdlib/graphics/vector/true-type.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/true-type.el#L1)

读取 TrueType 字体的 Unicode 字形轮廓和水平度量。

## TrueTypeFace {#api-66d13e32cb7f458d1867}

源码：`src/stdlib/graphics/vector/true-type.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/true-type.el#L68)

从固定 TrueType 文件读取一个字面。输入缓冲区的所有权转交给字体对象。

```el-signature
export @assign(mode: "shared") class TrueTypeFace
```

### 示例：打开标准字体

```el
import { TrueTypeFace } from "el:graphics/vector/true-type.el"
import { readFileBuffer } from "el:filesystem/"
scope let face = TrueTypeFace(readFileBuffer("system.ttf"))
let glyph = face.glyph(65)
```
