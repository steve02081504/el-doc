# filesystem/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文件系统引用与位置 {#api-e5202594b7cb01716dd4}

源码：`src/stdlib/filesystem/model.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/model.el#L1)

定义文件引用、已解析位置、提供者登记和文件系统错误。

## Path {#api-01450bc86834bd922aa5}

源码：`src/stdlib/filesystem/model.el:119` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/model.el#L119)

保存传给文件系统的引用文本。相对引用在解析时使用所选上下文。

```el-signature
export @assign(mode: "copy") class Path extends TextOperand
```

### 示例：保存相对文件引用

```el
import { Path } from "el:filesystem/"
let reference = Path("file:./settings.json")
console.stdout.writeLine(reference.text())
```
