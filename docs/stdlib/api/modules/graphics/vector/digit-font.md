# graphics/vector/digit-font.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/graphics.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数位字体轮廓文件 {#api-7308156c1e51ead2de7c}

源码：`src/stdlib/graphics/vector/digit-font.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/digit-font.el#L1)

保存字形映射、轮廓和水平度量。系统 TrueType 字体由显式导入接口读取。

## DigitFontFace {#api-d9a1fa94abcf1ae4087e}

源码：`src/stdlib/graphics/vector/digit-font.el:32` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/digit-font.el#L32)

按 Unicode 标量顺序保存字形及水平步进；查找缺失字形返回 nil。

```el-signature
export @assign(mode: "shared") class DigitFontFace
```

### 示例：建立字体轮廓集合

```el
import { DigitFontFace } from "el:graphics/vector/digit-font.el"
let face = DigitFontFace(2048)
```

## importTrueTypeGlyphs {#api-31d352a61e5dea29b735}

源码：`src/stdlib/graphics/vector/digit-font.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/digit-font.el#L66)

显式从固定 TrueType 格式导入指定字符的轮廓。codes 按 Unicode 标量升序排列。

```el-signature
export fn importTrueTypeGlyphs(face: TrueTypeFace, codes: Number[]): DigitFontFace
```

**返回类型**：[`DigitFontFace`](digit-font.md#api-d9a1fa94abcf1ae4087e)

### 示例：导入两个字符

```el
import { importTrueTypeGlyphs } from "el:graphics/vector/digit-font.el"
import { TrueTypeFace } from "el:graphics/vector/true-type.el"
import { readFileBuffer } from "el:filesystem/"
scope let face = TrueTypeFace(readFileBuffer("system.ttf"))
let glyphs = importTrueTypeGlyphs(face, @[65, 66])
```

## DigitFontFormat {#api-ce8530d88bb1d311b969}

源码：`src/stdlib/graphics/vector/digit-font.el:94` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/graphics/vector/digit-font.el#L94)

用目标或指定的较小基数保存字体轮廓。可通过 readFileAs 和 writeFileAs 读写。

```el-signature
export @assign(mode: "copy") class DigitFontFormat
```

### 示例：编码空字形表

```el
import { DigitFontFace, DigitFontFormat } from "el:graphics/vector/digit-font.el"
let units = DigitFontFormat().encode(DigitFontFace(2048))
```
